#!/usr/bin/env python3
"""y^2=x^3+7 的复数解曲面(黎曼曲面)，用 y 的相位(辐角)上色。
3 个空间轴 = (Re x, Im x, Re y)，颜色 = y 的相位 arg(y)。旋转展示。
(非 mod p，完整复数曲线)"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation, PillowWriter

X, Y = np.meshgrid(np.linspace(-3, 4.2, 200), np.linspace(-2.3, 2.3, 200))
xg = X + 1j*Y
y = np.sqrt(xg**3 + 7)
phase = (np.angle(y) % (2*np.pi))/(2*np.pi)   # 相位 -> [0,1]

fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection="3d")

surfs = []
for sign in (+1, -1):
    yy = sign*y
    ph = (np.angle(yy) % (2*np.pi))/(2*np.pi)
    surfs.append((np.real(yy), cm.hsv(ph)))

def update(frame):
    ax.clear()
    for Zreal, fc in surfs:
        ax.plot_surface(X, Y, Zreal, facecolors=fc, rstride=3, cstride=3,
                        linewidth=0, antialiased=True, alpha=0.95)
    # 红线：实曲线嵌在曲面上
    xr = np.linspace(-7**(1/3), 4.2, 400); yr = np.sqrt(xr**3+7)
    ax.plot(xr, np.zeros_like(xr),  yr, "k", lw=2)
    ax.plot(xr, np.zeros_like(xr), -yr, "k", lw=2)
    ax.set_title("complex curve y^2=x^3+7 (Riemann surface)\ncolor = phase of y;  black = real curve", fontsize=11)
    ax.set_xlabel("Re x"); ax.set_ylabel("Im x"); ax.set_zlabel("Re y")
    ax.view_init(elev=20, azim=frame); ax.set_box_aspect((1,1,0.8))
    return []

anim = FuncAnimation(fig, update, frames=np.arange(0, 360, 6), interval=80)
anim.save("ecc_phase.gif", writer=PillowWriter(fps=14))
print("saved ecc_phase.gif")

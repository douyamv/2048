#!/usr/bin/env python3
"""旋转动画：完整复数曲面 y^2=x^3+7（黎曼曲面），360°展示。
4维里的2维曲面，投影到3维(Re x, Im x, Re y)，颜色=Im y。红线=实曲线。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation, PillowWriter

fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection="3d")

# 复数曲面
X, Y = np.meshgrid(np.linspace(-3, 4.2, 180), np.linspace(-2.3, 2.3, 180))
xg = X + 1j*Y
s = xg**3 + 7
y = np.sqrt(s)
ImY = np.imag(y)
norm = plt.Normalize(ImY.min(), ImY.max())

for sign in (+1, -1):
    yy = sign*y
    ax.plot_surface(X, Y, np.real(yy), facecolors=cm.viridis(norm(np.imag(yy))),
                    rstride=3, cstride=3, linewidth=0, antialiased=True, alpha=0.92)

# 红色：实曲线
xr = np.linspace(-7**(1/3), 4.2, 600)
yr = np.sqrt(xr**3 + 7)
ax.plot(xr, np.zeros_like(xr),  yr, "crimson", lw=3, zorder=10)
ax.plot(xr, np.zeros_like(xr), -yr, "crimson", lw=3, zorder=10)

ax.set_xlabel("Re x"); ax.set_ylabel("Im x"); ax.set_zlabel("Re y")
ax.set_title("Full complex curve  y^2 = x^3 + 7\n(2D surface in 4D, projected; red = real curve)",
             fontsize=11)

def update(frame):
    ax.view_init(elev=20, azim=frame)
    return []

frames = np.arange(0, 360, 6)   # 60 帧
anim = FuncAnimation(fig, update, frames=frames, interval=80, blit=False)
anim.save("ecc_rotate.gif", writer=PillowWriter(fps=14))
print("saved ecc_rotate.gif")

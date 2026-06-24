#!/usr/bin/env python3
"""一个干净、清晰、慢慢转的甜甜圈：复数椭圆曲线 y^2=x^3+7 的真身形状。
红圈 = 实曲线(就是你最早看到的花瓶)。文件适中、慢速旋转。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

u = np.linspace(0, 2*np.pi, 140)
v = np.linspace(0, 2*np.pi, 140)
U, V = np.meshgrid(u, v)
R, r = 2.2, 0.9
X = (R + r*np.cos(V))*np.cos(U)
Y = (R + r*np.cos(V))*np.sin(U)
Z = r*np.sin(V)

# 红圈：实曲线 = 顶部一圈(清晰可见)
t = np.linspace(0, 2*np.pi, 400)
Xc = R*np.cos(t); Yc = R*np.sin(t); Zc = (r*1.04)*np.ones_like(t)

fig = plt.figure(figsize=(7.5, 7.5))
ax = fig.add_subplot(111, projection="3d")

def update(frame):
    ax.clear()
    ax.plot_surface(X, Y, Z, color="#E8B84B", alpha=0.95,
                    rstride=2, cstride=2, linewidth=0, antialiased=True, shade=True)
    ax.plot(Xc, Yc, Zc, color="crimson", lw=5, zorder=10)
    ax.set_title("complex curve  y^2 = x^3 + 7  =  a DONUT\n(red loop = the real curve)",
                 fontsize=15, pad=16)
    ax.set_box_aspect((1, 1, 0.5))
    ax.view_init(elev=34, azim=frame)
    ax.set_axis_off()
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(-1.6, 1.6)
    return []

# 慢速：每帧 6 度，60 帧绕一圈，fps=8 -> 一圈约 7.5 秒
frames = np.arange(0, 360, 6)
anim = FuncAnimation(fig, update, frames=frames, interval=125)
anim.save("ecc_donut_slow.gif", writer=PillowWriter(fps=8), dpi=80)
print("saved ecc_donut_slow.gif")

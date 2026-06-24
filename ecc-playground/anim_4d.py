#!/usr/bin/env python3
"""4维旋转动画：在 (Re y, Im y) 平面里转动，把隐藏的第4维显出来。
视角固定，变化的是“高度用 y 的哪个方向”——这是真正的4维旋转。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation, PillowWriter

X, Y = np.meshgrid(np.linspace(-3, 4.2, 150), np.linspace(-2.3, 2.3, 150))
xg = X + 1j*Y
y = np.sqrt(xg**3 + 7)
ReY, ImY = np.real(y), np.imag(y)

fig = plt.figure(figsize=(6.5, 6.5))
ax = fig.add_subplot(111, projection="3d")

def update(frame):
    ax.clear()
    th = np.deg2rad(frame)
    for sign in (+1, -1):
        h = sign*(np.cos(th)*ReY + np.sin(th)*ImY)     # 第4维方向的高度
        c = sign*(-np.sin(th)*ReY + np.cos(th)*ImY)    # 垂直分量 -> 颜色
        norm = plt.Normalize(c.min(), c.max())
        ax.plot_surface(X, Y, h, facecolors=cm.plasma(norm(c)),
                        rstride=3, cstride=3, linewidth=0, antialiased=True, alpha=0.92)
    ax.set_title(f"rotating in the 4th dimension (Re y <-> Im y)\nheight mixes Re y & Im y, angle={frame}deg",
                 fontsize=11)
    ax.set_xlabel("Re x"); ax.set_ylabel("Im x"); ax.set_zlabel("mixed y")
    ax.set_zlim(-6, 6); ax.view_init(elev=18, azim=-60)
    return []

frames = np.arange(0, 360, 8)   # 45 帧
anim = FuncAnimation(fig, update, frames=frames, interval=90, blit=False)
anim.save("ecc_4d.gif", writer=PillowWriter(fps=12))
print("saved ecc_4d.gif")

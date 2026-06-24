#!/usr/bin/env python3
"""复数椭圆曲线 E(C) 的真身 = 平坦环面，它天然住在 4 维(S^3)里。
这就是 Clifford 环面：在 4 维里旋转，投影到 3 维 -> 形态不断变化。
(非 mod p，纯复数曲面的几何本体)"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation, PillowWriter

u = np.linspace(0, 2*np.pi, 90)
v = np.linspace(0, 2*np.pi, 90)
U, V = np.meshgrid(u, v)
# 4 维单位 S^3 上的平坦环面（两个圆方向）
x1 = np.cos(U)/np.sqrt(2); x2 = np.sin(U)/np.sqrt(2)
x3 = np.cos(V)/np.sqrt(2); x4 = np.sin(V)/np.sqrt(2)
colors = cm.twilight((V % (2*np.pi))/(2*np.pi))

fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection="3d")

def update(frame):
    ax.clear()
    th = np.deg2rad(frame)
    # 4维旋转：在 (x1,x3) 平面转 + 在 (x2,x4) 平面转一点
    a = x1*np.cos(th) - x3*np.sin(th)
    c = x1*np.sin(th) + x3*np.cos(th)
    b = x2*np.cos(th*0.5) - x4*np.sin(th*0.5)
    d = x2*np.sin(th*0.5) + x4*np.cos(th*0.5)
    denom = 1.4 - d                       # 球极投影(从一个4维方向看)
    X, Y, Z = a/denom, b/denom, c/denom
    ax.plot_surface(X, Y, Z, facecolors=colors, rstride=2, cstride=2,
                    linewidth=0, antialiased=True, alpha=0.95)
    ax.set_title("the complex curve's TRUE shape:\na FLAT torus living in 4D (rotating in 4D)", fontsize=12)
    ax.set_xlim(-1.6,1.6); ax.set_ylim(-1.6,1.6); ax.set_zlim(-1.6,1.6)
    ax.set_box_aspect((1,1,1)); ax.view_init(elev=22, azim=40); ax.set_axis_off()
    return []

anim = FuncAnimation(fig, update, frames=np.arange(0, 360, 6), interval=80)
anim.save("ecc_torus4d.gif", writer=PillowWriter(fps=14))
print("saved ecc_torus4d.gif")

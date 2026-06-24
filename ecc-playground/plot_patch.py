#!/usr/bin/env python3
"""证明：甜甜圈上的一小块，看起来就是一张弯曲薄片。
所以“②像平面”和“③是甜甜圈”不矛盾——②是局部，③是全局。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(15, 6))
R, r = 2.0, 0.75

# 完整甜甜圈，高亮一小块
ax1 = fig.add_subplot(1, 2, 1, projection="3d")
u = np.linspace(0, 2*np.pi, 140); v = np.linspace(0, 2*np.pi, 140)
U, V = np.meshgrid(u, v)
X = (R + r*np.cos(V))*np.cos(U); Y = (R + r*np.cos(V))*np.sin(U); Z = r*np.sin(V)
ax1.plot_surface(X, Y, Z, color="wheat", alpha=0.30, rstride=2, cstride=2,
                 linewidth=0.1, edgecolor="goldenrod")
# 高亮的一小块 (u,v 取小范围)
us = np.linspace(0.6, 1.9, 40); vs = np.linspace(-0.9, 1.4, 40)
Us, Vs = np.meshgrid(us, vs)
Xs = (R + r*np.cos(Vs))*np.cos(Us); Ys = (R + r*np.cos(Vs))*np.sin(Us); Zs = r*np.sin(Vs)
ax1.plot_surface(Xs, Ys, Zs, color="crimson", alpha=0.95, rstride=1, cstride=1, linewidth=0)
ax1.set_title("(A) the whole donut\n(red = one small patch)", fontsize=13)
ax1.set_box_aspect((1, 1, 0.45)); ax1.view_init(elev=40, azim=-55); ax1.set_axis_off()

# 把那一小块单独拿出来 —— 看起来就是一张弯曲薄片（像图②）
ax2 = fig.add_subplot(1, 2, 2, projection="3d")
ax2.plot_surface(Xs, Ys, Zs, cmap="viridis", rstride=1, cstride=1,
                 linewidth=0, antialiased=True)
ax2.set_title("(B) that same patch, alone\n= a curved sheet — looks just like figure (2)!", fontsize=13)
ax2.view_init(elev=25, azim=-70); ax2.set_axis_off()

plt.suptitle("A piece of a donut looks like a flat-ish sheet  =>  (2) and (3) are the SAME object",
             fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig("ecc_patch.png", dpi=110, bbox_inches="tight")
print("saved ecc_patch.png")

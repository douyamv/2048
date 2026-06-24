#!/usr/bin/env python3
"""把 y^2 = x^3 + 7 的“完整复数曲线”画出来。
复数 x、复数 y 各占 2 维 -> 曲线是 4 维里的 2 维曲面。
用三种投影看它的“完整形状”。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm

fig = plt.figure(figsize=(20, 6.5))

# ---------- 图1：实数切片（你之前看到的“花瓶”，只是完整曲线的一个剖面）----------
ax1 = fig.add_subplot(1, 3, 1)
xr = np.linspace(-7**(1/3), 4.2, 2000)
yr = np.sqrt(xr**3 + 7)
ax1.plot(xr, yr, "crimson", lw=2.5)
ax1.plot(xr, -yr, "crimson", lw=2.5)
ax1.axhline(0, color="gray", lw=0.5); ax1.axvline(0, color="gray", lw=0.5)
ax1.set_title("(1) the REAL slice  (Im x = Im y = 0)\n— the 'vase' you saw is just this cut", fontsize=12)
ax1.set_xlabel("x"); ax1.set_ylabel("y"); ax1.grid(alpha=0.3)
ax1.set_aspect("equal", "box")

# ---------- 图2：完整复数解曲面（黎曼曲面）----------
# x 在复平面取网格，y = ±sqrt(x^3+7)。3D 轴: (Re x, Im x, Re y)，颜色 = Im y
ax2 = fig.add_subplot(1, 3, 2, projection="3d")
X, Y = np.meshgrid(np.linspace(-3, 4.2, 220), np.linspace(-2.3, 2.3, 220))
x = X + 1j*Y
s = x**3 + 7
y = np.sqrt(s)                      # 一支
ImY = np.imag(y)
norm = plt.Normalize(ImY.min(), ImY.max())
for sign in (+1, -1):               # 两支 ±y 一起画 = 完整曲面
    yy = sign*y
    ax2.plot_surface(X, Y, np.real(yy), facecolors=cm.viridis(norm(np.imag(yy))),
                     rstride=3, cstride=3, linewidth=0, antialiased=True, alpha=0.9)
# 红线：实曲线就嵌在这张曲面上（Im x=0 处那条缝）
m = (xr**3 + 7) >= 0
ax2.plot(xr, np.zeros_like(xr),  yr, "crimson", lw=3, zorder=10)
ax2.plot(xr, np.zeros_like(xr), -yr, "crimson", lw=3, zorder=10)
ax2.set_title("(2) the FULL complex curve (Riemann surface)\naxes: Re x, Im x, Re y;  color = Im y\nred = the real slice sitting inside it", fontsize=11)
ax2.set_xlabel("Re x"); ax2.set_ylabel("Im x"); ax2.set_zlabel("Re y")
ax2.view_init(elev=22, azim=-60)

# ---------- 图3：拓扑真身 —— 环面（甜甜圈）----------
# 在 ℂ 上 E 同胚于环面 ℂ/Λ；实曲线 = 环面上的一个圈
ax3 = fig.add_subplot(1, 3, 3, projection="3d")
u = np.linspace(0, 2*np.pi, 120)
v = np.linspace(0, 2*np.pi, 120)
U, V = np.meshgrid(u, v)
R, r = 2.0, 0.75
Xt = (R + r*np.cos(V))*np.cos(U)
Yt = (R + r*np.cos(V))*np.sin(U)
Zt = r*np.sin(V)
ax3.plot_surface(Xt, Yt, Zt, color="wheat", alpha=0.35, rstride=2, cstride=2,
                 linewidth=0.15, edgecolor="goldenrod", shade=True)
# 实曲线（D>0，单块）= 环面上的一个圈：贴在环面外赤道上（v=0，略抬到表面外侧）
t = np.linspace(0, 2*np.pi, 400)
rr = r*1.02
Xc = (R + rr*np.cos(0.0))*np.cos(t)
Yc = (R + rr*np.cos(0.0))*np.sin(t)
Zc = rr*np.sin(0.0)*np.ones_like(t)
ax3.plot(Xc, Yc, Zc, "crimson", lw=4, zorder=10, label="E(R): real curve = one loop")
# 另一个方向的圈（管子一圈）示意“两个周期 = 甜甜圈的两个圈”
Xm = (R + rr*np.cos(t))*np.cos(0.0)
Ym = (R + rr*np.cos(t))*np.sin(0.0)
Zm = rr*np.sin(t)
ax3.plot(Xm, Ym, Zm, "royalblue", lw=2.5, ls="--", zorder=10, label="the other period (tube loop)")
ax3.set_title("(3) topological truth: a TORUS (donut)\nE over C = C/lattice;  point addition = z1+z2 slide on it\nred loop = the real 'vase'", fontsize=11)
ax3.legend(loc="upper center", fontsize=8)
ax3.set_box_aspect((1, 1, 0.45)); ax3.view_init(elev=38, azim=-55)
ax3.set_axis_off()

plt.tight_layout()
plt.savefig("ecc_complex.png", dpi=105, bbox_inches="tight")
print("saved ecc_complex.png")

#!/usr/bin/env python3
"""复数世界里的椭圆曲线 = ℂ/格子。
左：一般格子 + 基本域(=甜甜圈) + n阶挠点排成规整网格。
右：secp256k1 的 j=0 六边形(Eisenstein)格子 —— 三重/六重对称的总根源。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import cmath

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

# ---- 左：一般格子 + 基本平行四边形(甜甜圈) + 挠点网格 ----
w1 = complex(1.0, 0.0)
w2 = complex(0.35, 0.95)
# 画格点
for a in range(-2, 4):
    for b in range(-2, 4):
        p = a*w1 + b*w2
        ax1.plot(p.real, p.imag, "ko", ms=3, alpha=0.5)
# 基本平行四边形
corners = [0, w1, w1+w2, w2, 0]
ax1.plot([c.real for c in corners], [c.imag for c in corners], "b-", lw=2)
ax1.fill([c.real for c in corners], [c.imag for c in corners], color="skyblue", alpha=0.3)
# n阶挠点网格 (n=5)
n = 5
for a in range(n):
    for b in range(n):
        p = (a*w1 + b*w2)/n
        ax1.plot(p.real, p.imag, "rs", ms=6)
ax1.set_title("E over C = C / lattice\nblue tile = the torus;  red grid = n-torsion (n=5) points", fontsize=12)
ax1.set_xlabel("Re"); ax1.set_ylabel("Im"); ax1.set_aspect("equal")
ax1.set_xlim(-1.2, 2.4); ax1.set_ylim(-1.2, 2.2); ax1.grid(alpha=0.2)
ax1.text(0.05, -1.0, "glue opposite edges -> donut\n(flat: like Pac-Man wraparound)", fontsize=9, color="navy")

# ---- 右：j=0 六边形(Eisenstein)格子 ----
om = cmath.exp(2j*cmath.pi/3)   # 立方根
e1 = complex(1.0, 0.0)
e2 = -om                         # 使格子为六边形
pts = []
for a in range(-3, 4):
    for b in range(-3, 4):
        p = a*e1 + b*e2
        pts.append(p)
        ax2.plot(p.real, p.imag, "o", color="darkgreen", ms=4)
# 高亮原点周围的6个最近邻 -> 六边形
origin_neighbors = sorted(pts, key=lambda z: abs(z))[1:7]
hexpts = sorted(origin_neighbors, key=lambda z: cmath.phase(z))
hx = [z.real for z in hexpts] + [hexpts[0].real]
hy = [z.imag for z in hexpts] + [hexpts[0].imag]
ax2.plot(hx, hy, "g-", lw=2)
ax2.fill(hx, hy, color="lightgreen", alpha=0.4)
ax2.plot(0, 0, "r*", ms=15)
ax2.set_title("secp256k1's lattice: j=0, HEXAGONAL (Eisenstein)\n6-fold symmetry => the 120deg / GLV symmetry", fontsize=12)
ax2.set_xlabel("Re"); ax2.set_ylabel("Im"); ax2.set_aspect("equal")
ax2.set_xlim(-3, 3); ax2.set_ylim(-3, 3); ax2.grid(alpha=0.2)

plt.suptitle("The complex elliptic curve is a flat torus C/lattice", fontsize=14, y=1.0)
plt.tight_layout()
plt.savefig("ecc_lattice.png", dpi=110, bbox_inches="tight")
print("saved ecc_lattice.png")

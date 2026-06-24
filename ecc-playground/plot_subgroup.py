#!/usr/bin/env python3
"""甜甜圈的完整结构是 2 维网格 (Z/n)^2；
密码用的 E(F_p)=Z/n 只是其中一条 1 维循环环线。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

n = 13
fig, ax = plt.subplots(figsize=(8.5, 8.5))

# 完整 n×n 挠点网格（甜甜圈的 2 维结构）
for a in range(n):
    for b in range(n):
        ax.plot(a, b, "o", color="lightgray", ms=10)

# 一条循环子群 Z/n：由 (1,5) 生成，走 n 步绕回原点
gx, gy = 1, 5
pts = [((k*gx) % n, (k*gy) % n) for k in range(n+1)]
xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
# 画点 + 标号（不连线，避免环绕跳线杂乱）
for k in range(n):
    ax.plot(xs[k], ys[k], "o", color="crimson", ms=15, zorder=5)
    ax.annotate(str(k), (xs[k], ys[k]), color="white", fontsize=9,
                ha="center", va="center", zorder=6)

ax.set_title(f"donut torsion = full {n}x{n} grid (Z/n)^2  [2D]\n"
             f"crypto group E(F_p) = ONE cyclic loop Z/n  [1D, red]\n"
             f"(the other direction lives in extension fields, unused)", fontsize=12)
ax.set_xlabel("cycle direction 1"); ax.set_ylabel("cycle direction 2")
ax.set_xticks(range(n)); ax.set_yticks(range(n))
ax.set_xlim(-0.7, n-0.3); ax.set_ylim(-0.7, n-0.3)
ax.set_aspect("equal"); ax.grid(alpha=0.25)
plt.tight_layout()
plt.savefig("ecc_subgroup.png", dpi=110, bbox_inches="tight")
print("saved ecc_subgroup.png")
print(f"红色循环子群(n={n}个点): {pts[:-1]}")

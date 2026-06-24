#!/usr/bin/env python3
"""展示复数曲线的对称：x 平面上的三重旋转(120°) + 三个根呈等边三角形。
这让我们只需画 1/3 扇形 × 1 层，其余靠对称补全。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import cmath

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

# ---- 左：|y| = |x^3+7|^(1/2) 在复 x 平面的热力图，看三重对称 ----
N = 600
g = np.linspace(-2.6, 2.6, N)
RX, IX = np.meshgrid(g, g)
x = RX + 1j*IX
absy = np.abs(x**3 + 7)**0.5
im = ax1.imshow(absy, extent=[-2.6,2.6,-2.6,2.6], origin="lower", cmap="magma")
plt.colorbar(im, ax=ax1, label="|y| = |x^3+7|^(1/2)", shrink=0.8)
# 三个根（分支点），120°等边三角形
roots = [ (7)**(1/3)*cmath.exp(1j*cmath.pi*(2*k+1)/3) for k in range(3) ]
for k,r in enumerate(roots):
    ax1.plot(r.real, r.imag, "co", ms=12, mec="white", mew=1.5)
    ax1.annotate(f"root{k+1}", (r.real, r.imag), color="cyan",
                 textcoords="offset points", xytext=(8,6), fontsize=11)
# 连成等边三角形
tri = roots + [roots[0]]
ax1.plot([z.real for z in tri], [z.imag for z in tri], "c--", lw=1.2, alpha=0.7)
# 120°旋转箭头
for ang in [0]:
    th = np.linspace(np.pi/2, np.pi/2+2*np.pi/3, 50)
    ax1.plot(2.3*np.cos(th), 2.3*np.sin(th), "w-", lw=1)
ax1.set_title("complex x-plane: 3-fold (120deg) symmetry\nthe 3 roots form an equilateral triangle", fontsize=12)
ax1.set_xlabel("Re x"); ax1.set_ylabel("Im x"); ax1.set_aspect("equal")

# ---- 右：把三重对称 + y镜像 总结成“基本域” ----
ax2.imshow(absy, extent=[-2.6,2.6,-2.6,2.6], origin="lower", cmap="magma", alpha=0.35)
# 高亮一个 120° 扇形（基本域）
th = np.linspace(np.pi/6, np.pi/6+2*np.pi/3, 100)
wedge_x = np.concatenate([[0], 2.6*np.cos(th), [0]])
wedge_y = np.concatenate([[0], 2.6*np.sin(th), [0]])
ax2.fill(wedge_x, wedge_y, color="lime", alpha=0.35, label="fundamental domain (1/3)")
for k,r in enumerate(roots):
    ax2.plot(r.real, r.imag, "co", ms=10, mec="white")
ax2.set_title("you only need 1/3 wedge x 1 sheet\nrotate x120deg + mirror y => the whole curve", fontsize=12)
ax2.set_xlabel("Re x"); ax2.set_ylabel("Im x"); ax2.set_aspect("equal")
ax2.legend(loc="upper right", fontsize=10)

plt.suptitle("Symmetries of  y^2 = x^3 + 7  let you omit 5/6 and regenerate by symmetry",
             fontsize=14, y=1.0)
plt.tight_layout()
plt.savefig("ecc_symmetry.png", dpi=110, bbox_inches="tight")
print("saved ecc_symmetry.png")
print("三个根(120°分布):")
for k,r in enumerate(roots):
    print(f"  root{k+1}: {r.real:+.3f}{r.imag:+.3f}i   角度 {np.degrees(cmath.phase(r)):.0f}deg")

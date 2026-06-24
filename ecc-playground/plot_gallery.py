#!/usr/bin/env python3
"""椭圆曲线画廊：y^2 = x^3 + a*x + b 的几种典型形状。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# 判别式相关量 D = 4a^3 + 27b^2
#   D > 0 : 一个实根 -> 单块
#   D < 0 : 三个实根 -> 两块（左边一个孤立椭圆环 + 右边开放臂）
#   D = 0 : 奇异曲线（尖点 cusp 或 结点 node），不能做密码
curves = [
    (0,  7,  "y^2 = x^3 + 7   (Ethereum)", "smooth, 1 piece"),
    (-1, 0,  "y^2 = x^3 - x",              "smooth, 2 pieces (oval+branch)"),
    (-2, 1,  "y^2 = x^3 - 2x + 1",         "smooth, 2 pieces"),
    (-3, 3,  "y^2 = x^3 - 3x + 3",         "smooth, 1 piece"),
    (0,  0,  "y^2 = x^3   (b=0)",          "SINGULAR: cusp (spike)"),
    (-3, 2,  "y^2 = x^3 - 3x + 2",         "SINGULAR: node (self-cross)"),
]

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
xx = np.linspace(-4, 5, 6000)

for ax, (a, b, title, sub) in zip(axes.flat, curves):
    rhs = xx**3 + a*xx + b
    m = rhs >= 0
    x_ok = xx[m]
    y_ok = np.sqrt(rhs[m])
    D = 4*a**3 + 27*b**2
    singular = (D == 0)
    col = "crimson" if singular else "royalblue"
    # 分段画，避免把两块之间的空隙连起来
    dx = np.diff(x_ok)
    breaks = np.where(dx > (xx[1]-xx[0])*1.5)[0]
    segs = np.split(np.arange(len(x_ok)), breaks+1)
    for s in segs:
        if len(s) > 1:
            ax.plot(x_ok[s],  y_ok[s], col, lw=2)
            ax.plot(x_ok[s], -y_ok[s], col, lw=2)
    ax.axhline(0, color="gray", lw=0.5); ax.axvline(0, color="gray", lw=0.5)
    ax.set_title(title, fontsize=12)
    ax.set_xlabel(sub, fontsize=10,
                  color=("crimson" if singular else "dimgray"))
    ax.set_xlim(-4, 5); ax.set_ylim(-9, 9)
    ax.set_aspect("equal", "box"); ax.grid(alpha=0.3)
    ax.text(-3.7, 7.3, f"4a^3+27b^2 = {D}", fontsize=9,
            color=("crimson" if singular else "green"))

plt.suptitle("Elliptic curve gallery:  y^2 = x^3 + a*x + b", fontsize=15, y=1.0)
plt.tight_layout()
plt.savefig("ecc_gallery.png", dpi=105, bbox_inches="tight")
print("saved ecc_gallery.png")

#!/usr/bin/env python3
"""画三张图：连续曲线、点加法几何、mod p 离散点云。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from break_toy_ecc import find_prime_order_curve

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# ---------- 图1：连续实数曲线 y^2 = x^3 + 7 ----------
ax = axes[0]
x = np.linspace(-2, 4, 1000)
rhs = x**3 + 7
mask = rhs >= 0
xv, yv = x[mask], np.sqrt(rhs[mask])
ax.plot(xv, yv, "b", lw=2)
ax.plot(xv, -yv, "b", lw=2)
ax.axhline(0, color="gray", lw=0.5)
ax.axvline(0, color="gray", lw=0.5)
ax.set_title("(1) continuous curve:  y^2 = x^3 + 7", fontsize=13)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.grid(alpha=0.3); ax.set_aspect("equal", "box")
ax.text(0.5, -8.5, "symmetric about x-axis", fontsize=9, color="gray")

# ---------- 图2：点加法几何（取交点再翻转）----------
ax = axes[1]
ax.plot(xv, yv, "b", lw=2); ax.plot(xv, -yv, "b", lw=2)
ax.axhline(0, color="gray", lw=0.5); ax.axvline(0, color="gray", lw=0.5)

# 取两个实数点 P, Q 做演示
def curve_y(xp):
    return np.sqrt(xp**3 + 7)
xP, xQ = -1.5, 0.5
P = (xP, curve_y(xP))
Q = (xQ, curve_y(xQ))
# 过 P、Q 的割线
s = (Q[1] - P[1]) / (Q[0] - P[0])
x3 = s**2 - P[0] - Q[0]
y3_line = s * (x3 - P[0]) + P[1]      # 第三交点（线上）
R = (x3, y3_line)
PQ = (x3, -y3_line)                    # 翻转后 = P+Q
# 画割线
lx = np.linspace(-2, 3.5, 100)
ax.plot(lx, s * (lx - P[0]) + P[1], "g--", lw=1.2, label="line through P, Q")
# 画翻转竖线
ax.plot([x3, x3], [y3_line, -y3_line], "r:", lw=1.2, label="reflect over x-axis")
for pt, name, col in [(P, "P", "black"), (Q, "Q", "black"),
                      (R, "R (3rd intersection)", "orange"), (PQ, "P+Q", "red")]:
    ax.plot(pt[0], pt[1], "o", color=col, ms=8)
    ax.annotate(name, pt, textcoords="offset points", xytext=(8, 6), fontsize=10)
ax.set_title("(2) addition:  line -> 3rd point R -> flip = P+Q", fontsize=13)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.legend(fontsize=8, loc="upper left"); ax.grid(alpha=0.3)
ax.set_xlim(-2.2, 3.8); ax.set_ylim(-11, 11)

# ---------- 图3：mod p 之后的离散点云 ----------
ax = axes[2]
curve, G, n = find_prime_order_curve(a=0, b=7)
p = curve.p
xs, ys = [], []
for X in range(p):
    rr = (X**3 + 7) % p
    if pow(rr, (p - 1) // 2, p) == 1 or rr == 0:
        from break_toy_ecc import modular_sqrt
        yy = modular_sqrt(rr, p)
        if yy is not None:
            xs += [X, X]; ys += [yy, (p - yy) % p]
ax.scatter(xs, ys, s=3, color="purple", alpha=0.6)
ax.set_title(f"(3) same curve mod p={p}:  {n} scattered points", fontsize=13)
ax.set_xlabel("x (mod p)"); ax.set_ylabel("y (mod p)")
ax.grid(alpha=0.3)
ax.text(p*0.05, p*0.92, "a smooth line --> a cloud of dots\n(no order, this is the 'scrambling')",
        fontsize=9, color="dimgray")

plt.tight_layout()
plt.savefig("ecc_curve.png", dpi=110, bbox_inches="tight")
print("saved ecc_curve.png")

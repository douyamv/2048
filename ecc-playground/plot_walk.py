#!/usr/bin/env python3
"""在 mod p 点云上，把 G, 2G, 3G, ... 按步数顺序连线，看“走步数”怎么乱跳。"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from break_toy_ecc import find_prime_order_curve, modular_sqrt

curve, G, n = find_prime_order_curve(a=0, b=7)
p = curve.p

# 全部点（点云，跟 G 无关）
xs, ys = [], []
for X in range(p):
    rr = (X**3 + 7) % p
    yy = modular_sqrt(rr, p)
    if yy is not None and (yy*yy) % p == rr:
        xs += [X, X]; ys += [yy, (p - yy) % p]

STEPS = 12
walk = []
P = None
for k in range(1, STEPS + 1):
    P = curve.add(P, G)
    fold = (P[0]**3 + 7) // p          # x^3+7 跳过了多少个 p 的倍数
    walk.append((k, P[0], P[1], fold))

fig, ax = plt.subplots(figsize=(9, 9))
ax.scatter(xs, ys, s=4, color="lightgray", alpha=0.7, label="all points (independent of G)")

wx = [w[1] for w in walk]
wy = [w[2] for w in walk]
# 连线（按步数顺序）
ax.plot(wx, wy, "-", color="crimson", lw=1.0, alpha=0.6)
for k, x, y, fold in walk:
    ax.plot(x, y, "o", color="crimson", ms=7)
    ax.annotate(f"{k}G\n(fold {fold})", (x, y), textcoords="offset points",
                xytext=(7, 5), fontsize=9, color="darkred", weight="bold")

ax.set_title(f"walk G -> 2G -> ... -> {STEPS}G  (fold = how many times x^3+7 wraps over p)\n"
             f"(curve y^2=x^3+7 mod {p}, G={G})", fontsize=11)
ax.set_xlabel("x (mod p)"); ax.set_ylabel("y (mod p)")
ax.legend(loc="upper right", fontsize=9)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("ecc_walk.png", dpi=110, bbox_inches="tight")
print("saved ecc_walk.png")
print("\n步数顺序的落点（含折叠次数 = (x^3+7)//p）：")
for k, x, y, fold in walk:
    print(f"  {k:2d}G = ({x:4d}, {y:4d})   x^3+7 折叠 {fold:>9} 次   (p^2={p*p})")

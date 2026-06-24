#!/usr/bin/env python3
"""坐标范围的真相：mod p 不是无限数轴的一小段，而是一个环(时钟)。
{0..p-1} 是整个数系，p 绕回 0，后面没有"更大的没用到的范围"。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5))

# 左：实数 —— 无限数轴
ax1.annotate("", xy=(11, 0), xytext=(-1, 0), arrowprops=dict(arrowstyle="<->", lw=2))
ax1.text(11.2, 0, "+inf", fontsize=12, va="center")
ax1.text(-1.8, 0, "-inf", fontsize=12, va="center")
for t in range(0, 11):
    ax1.plot(t, 0, "ko", ms=4)
ax1.set_title("real x:  an infinite line\n(x can grow without bound)", fontsize=13)
ax1.set_xlim(-3, 13); ax1.set_ylim(-2, 2); ax1.axis("off")

# 右：mod p —— 一个环(时钟)
p = 16  # 示意
th = np.linspace(0, 2*np.pi, p, endpoint=False)
cx, cy = np.cos(th), np.sin(th)
ax2.plot(np.append(cx, cx[0]), np.append(cy, cy[0]), "-", color="gray", lw=1.5)
for k in range(p):
    ax2.plot(cx[k], cy[k], "o", color="crimson", ms=11)
    ax2.annotate(str(k), (cx[k]*1.18, cy[k]*1.18), ha="center", va="center", fontsize=10)
# p 绕回 0 的箭头
ax2.annotate("x=p wraps to 0", (cx[0], cy[0]), textcoords="offset points",
             xytext=(40, 25), fontsize=12, color="darkred",
             arrowprops=dict(arrowstyle="->", color="darkred"))
ax2.set_title("mod p:  x lives on a CLOCK (wraps around)\n{0..p-1} is the WHOLE thing; nothing beyond", fontsize=13)
ax2.set_xlim(-1.6, 1.9); ax2.set_ylim(-1.5, 1.6); ax2.set_aspect("equal"); ax2.axis("off")
ax2.text(0, 0, f"p={p}\n(really 2^256)", ha="center", va="center", fontsize=11, color="gray")

plt.suptitle("{0,...,p-1} isn't a small slice of an infinite line -- it's the entire wrap-around number system",
             fontsize=13, y=1.0)
plt.tight_layout()
plt.savefig("ecc_clock.png", dpi=110, bbox_inches="tight")
print("saved ecc_clock.png")

#!/usr/bin/env python3
"""花瓶(开口) 如何 = 圈(闭合)：两条手臂在无穷远点碰头。
左：实曲线花瓶，上臂红、下臂蓝、鼻子绿。
右：同一条曲线闭合成圈 —— 上臂下臂在顶端∞点合并。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

# ---- 左：花瓶，手臂上色 ----
xr = np.linspace(-7**(1/3), 6.0, 1500)
yr = np.sqrt(xr**3 + 7)
ax1.plot(xr,  yr, color="crimson", lw=3)   # 上臂
ax1.plot(xr, -yr, color="royalblue", lw=3) # 下臂
ax1.plot(-7**(1/3), 0, "*", color="green", ms=22, zorder=5)  # 鼻子
ax1.annotate("nose\n(x=-cbrt7, y=0)", (-7**(1/3),0), color="green",
             textcoords="offset points", xytext=(12,-30), fontsize=11)
ax1.annotate("top arm -> +inf", (5.2, np.sqrt(5.2**3+7)), color="crimson",
             textcoords="offset points", xytext=(-130,-5), fontsize=11)
ax1.annotate("bottom arm -> -inf", (5.2,-np.sqrt(5.2**3+7)), color="royalblue",
             textcoords="offset points", xytext=(-150,5), fontsize=11)
ax1.axhline(0, color="gray", lw=0.5); ax1.axvline(0, color="gray", lw=0.5)
ax1.set_title("(1) the OPEN vase\ntwo arms shooting off to infinity", fontsize=13)
ax1.set_xlabel("x"); ax1.set_ylabel("y"); ax1.grid(alpha=0.3)
ax1.set_xlim(-3, 6.5); ax1.set_ylim(-16, 16)

# ---- 右：同一条曲线，闭合成圈 ----
th = np.linspace(-np.pi/2, 3*np.pi/2, 600)
cx, cy = np.cos(th), np.sin(th)
left = np.cos(th) <= 0    # 左半 = 上臂(红)
ax2.plot(cx[left],  cy[left],  color="crimson",  lw=4)
ax2.plot(cx[~left], cy[~left], color="royalblue", lw=4)
ax2.plot(0, -1, "*", color="green", ms=22, zorder=5)     # 鼻子(底部)
ax2.plot(0,  1, "o", color="black", ms=14, zorder=5)     # 无穷远点(顶部)
ax2.annotate("nose", (0,-1), color="green",
             textcoords="offset points", xytext=(10,-18), fontsize=12)
ax2.annotate("POINT AT INFINITY\n(both arms meet here!)", (0,1), color="black",
             textcoords="offset points", xytext=(15,5), fontsize=11)
ax2.annotate("top arm", (-1,0), color="crimson",
             textcoords="offset points", xytext=(-70,0), fontsize=11)
ax2.annotate("bottom arm", (1,0), color="royalblue",
             textcoords="offset points", xytext=(8,0), fontsize=11)
ax2.set_title("(2) add ONE point at infinity\n=> the vase closes into a LOOP (finite!)", fontsize=13)
ax2.set_aspect("equal"); ax2.axis("off")
ax2.set_xlim(-2.2, 2.6)

plt.suptitle("the open vase IS a circle, cut open at infinity and stretched flat",
             fontsize=14, y=1.0)
plt.tight_layout()
plt.savefig("ecc_close.png", dpi=110, bbox_inches="tight")
print("saved ecc_close.png")

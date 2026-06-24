#!/usr/bin/env python3
"""拉伸规则可视化：在甜甜圈上“均匀走”(等间隔的自然参数 z)，
落到 (x,y) 花瓶上 -> 靠近无穷远端被指数式拉开。
自然参数 z(x) = ∫ dx/y（椭圆积分）。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

x0 = -7**(1/3)                       # 鼻子
xs = np.linspace(x0 + 1e-6, 60, 400000)
ys = np.sqrt(xs**3 + 7)
# 自然参数 z(x) = 累积积分 ∫ dx/y
dz = np.gradient(xs) / ys
z = np.cumsum(dz)
z_total = z[-1]                      # 半周期（有限！）

# 在 z 上等间隔取点 -> 对应的 x
N = 22
z_uniform = np.linspace(0, z_total*0.999, N)
x_samp = np.interp(z_uniform, z, xs)
y_samp = np.sqrt(x_samp**3 + 7)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

# 左：甜甜圈自然坐标里，点是均匀的
ax1.plot(z_uniform, np.zeros_like(z_uniform), "-", color="lightgray", lw=2)
ax1.plot(z_uniform, np.zeros_like(z_uniform), "o", color="green", ms=9)
ax1.axvline(z_total, color="black", ls="--")
ax1.annotate("infinity point\n(z = half period)", (z_total, 0),
             textcoords="offset points", xytext=(-60, 30), fontsize=11)
ax1.annotate("nose\n(z=0)", (0,0), textcoords="offset points", xytext=(-10,30), fontsize=11, color="green")
ax1.set_title("(1) on the DONUT: walk in EQUAL steps\n(uniform natural coordinate z)", fontsize=12)
ax1.set_xlabel("z  (position on donut)"); ax1.set_yticks([])
ax1.set_ylim(-1, 1)

# 右：同样这些点落在花瓶上 -> 越靠近无穷越被拉开
xv = np.linspace(x0, 55, 2000); yv = np.sqrt(xv**3+7)
ax2.plot(xv,  yv, color="crimson", lw=2)
ax2.plot(xv, -yv, color="royalblue", lw=2)
ax2.plot(x_samp,  y_samp, "go", ms=9, zorder=5)
ax2.plot(x_samp, -y_samp, "go", ms=9, zorder=5)
ax2.plot(x0, 0, "g*", ms=20)
for i in range(N):
    ax2.plot([x_samp[i],x_samp[i]],[-y_samp[i],y_samp[i]], color="green", lw=0.4, alpha=0.4)
ax2.set_title("(2) same equal steps on the (x,y) VASE\n=> spread explodes toward infinity", fontsize=12)
ax2.set_xlabel("x"); ax2.set_ylabel("y"); ax2.grid(alpha=0.3)
ax2.set_xlim(-3, 55)
ax2.text(20, -200, "equal donut-steps  ->  huge x-jumps\nrule: x ~ 1/z^2 near infinity", fontsize=11, color="darkgreen")

plt.suptitle("the stretching rule: x = P(z), y = P'(z)  (Weierstrass function); P(z)~1/z^2 near infinity",
             fontsize=13, y=1.0)
plt.tight_layout()
plt.savefig("ecc_stretch.png", dpi=110, bbox_inches="tight")
print(f"saved ecc_stretch.png   (half period z_total ~ {z_total:.4f})")
print(f"等间隔 z 对应的 x: {np.round(x_samp[-6:],1)}  <- 末几步 x 暴涨")

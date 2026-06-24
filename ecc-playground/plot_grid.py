#!/usr/bin/env python3
"""4 个变量 (Re x, Im x, Re y, Im y) 的网格图(散点矩阵)。
4x4 格子，每格画两个变量的关系。完整表示这个 4 维曲面，不投影不旋转。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# 在复 x 平面取网格，算 y=±sqrt(x^3+7)
ReX = np.linspace(-3, 4, 160)
ImX = np.linspace(-2.5, 2.5, 160)
RX, IX = np.meshgrid(ReX, ImX)
x = (RX + 1j*IX).ravel()
y = np.sqrt(x**3 + 7)

# 两支 ±y 都收集，得到曲面上的点，每个点 4 个坐标
rex = np.concatenate([x.real,  x.real])
imx = np.concatenate([x.imag,  x.imag])
rey = np.concatenate([y.real, -y.real])
imy = np.concatenate([y.imag, -y.imag])
color = np.concatenate([x.imag, x.imag])   # 按 Im x 上色，便于看结构

vars_ = [rex, imx, rey, imy]
names = ["Re x", "Im x", "Re y", "Im y"]

fig, axes = plt.subplots(4, 4, figsize=(13, 13))
for i in range(4):
    for j in range(4):
        ax = axes[i][j]
        if i == j:
            ax.text(0.5, 0.5, names[i], ha="center", va="center",
                    fontsize=20, fontweight="bold", color="navy")
            ax.set_xticks([]); ax.set_yticks([])
        else:
            ax.scatter(vars_[j], vars_[i], s=0.5, c=color, cmap="coolwarm", alpha=0.5)
            ax.tick_params(labelsize=7)
        if i == 3:
            ax.set_xlabel(names[j], fontsize=11)
        if j == 0:
            ax.set_ylabel(names[i], fontsize=11)

plt.suptitle("the 4 variables of  y^2 = x^3 + 7  (complex), shown as a grid\n"
             "each cell = two of (Re x, Im x, Re y, Im y);  color = Im x",
             fontsize=14, y=0.995)
plt.tight_layout()
plt.savefig("ecc_grid.png", dpi=100, bbox_inches="tight")
print("saved ecc_grid.png")

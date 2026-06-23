#!/usr/bin/env python3
"""
玩具椭圆曲线密码学 (ECC) + 离散对数破解演示
=================================================

目的：直观感受「为什么小版本能破、大版本破不了」。

数学和真实的 secp256k1 完全一样：
    曲线方程   y^2 = x^3 + a*x + b   (mod p)
    私钥       一个整数 k
    公钥       点  Q = k * G   （G 是基点，k*G 表示把 G 自加 k 次）

「破解」= 已知公钥点 Q 和基点 G，反推出私钥 k。
这就是 椭圆曲线离散对数问题 (ECDLP)。

唯一的护城河是群的阶 n 有多大：
    - 暴力 / BSGS / Pollard's rho 的代价 ~ sqrt(n)
    - 小曲线 sqrt(n) 很小 -> 瞬间破
    - secp256k1 的 sqrt(n) ≈ 2^128 -> 宇宙寿命也破不了

运行：  python3 break_toy_ecc.py
"""

import random
import time
from math import isqrt


# ---------------------------------------------------------------------------
# 1. 椭圆曲线的基本运算（和 secp256k1 用的是同一套群运算，只是参数小）
# ---------------------------------------------------------------------------

class Curve:
    """椭圆曲线  y^2 = x^3 + a*x + b  (mod p)。无穷远点用 None 表示。"""

    def __init__(self, a, b, p):
        self.a, self.b, self.p = a, b, p

    def is_on_curve(self, P):
        if P is None:
            return True
        x, y = P
        return (y * y - (x * x * x + self.a * x + self.b)) % self.p == 0

    def add(self, P, Q):
        """椭圆曲线上的点加法（群运算）。"""
        if P is None:
            return Q
        if Q is None:
            return P
        x1, y1 = P
        x2, y2 = Q

        # P + (-P) = 无穷远点
        if x1 == x2 and (y1 + y2) % self.p == 0:
            return None

        if P == Q:
            # 切线斜率（倍点）
            s = (3 * x1 * x1 + self.a) * pow(2 * y1, -1, self.p) % self.p
        else:
            # 割线斜率
            s = (y2 - y1) * pow(x2 - x1, -1, self.p) % self.p

        x3 = (s * s - x1 - x2) % self.p
        y3 = (s * (x1 - x3) - y1) % self.p
        return (x3, y3)

    def mul(self, k, P):
        """标量乘 k*P，用 double-and-add，O(log k)。这一步正向很快、反推极难。"""
        result = None
        addend = P
        while k:
            if k & 1:
                result = self.add(result, addend)
            addend = self.add(addend, addend)
            k >>= 1
        return result

    def order_of(self, G):
        """暴力求基点 G 的阶（小曲线才可行，仅用于演示）。"""
        n = 1
        P = G
        while P is not None:
            P = self.add(P, G)
            n += 1
        return n


# ---------------------------------------------------------------------------
# 2. 破解算法一：Baby-step Giant-step  —— 时间和空间都是 O(sqrt(n))
# ---------------------------------------------------------------------------

def bsgs(curve, G, Q, n):
    """已知 Q = k*G，求 k。返回 k 或 None。"""
    m = isqrt(n) + 1

    # baby steps: 存表 { j*G : j }
    table = {}
    P = None
    for j in range(m):
        table[P] = j
        P = curve.add(P, G)

    # giant steps: Q - i*(m*G)
    mG = curve.mul(m, G)
    neg_mG = None if mG is None else (mG[0], (-mG[1]) % curve.p)
    gamma = Q
    for i in range(m):
        if gamma in table:
            return i * m + table[gamma]
        gamma = curve.add(gamma, neg_mG)
    return None


# ---------------------------------------------------------------------------
# 3. 破解算法二：Pollard's rho —— 时间 O(sqrt(n))，空间 O(1)（真实攻击用这个）
# ---------------------------------------------------------------------------

def pollard_rho(curve, G, Q, n):
    """已知 Q = k*G，求 k。基于生日悖论的随机游走，几乎不耗内存。"""

    def step(X, a, b):
        # 把当前点分到 3 个区，分别做不同的更新，制造伪随机游走
        x = 0 if X is None else X[0]
        region = x % 3
        if region == 0:
            return curve.add(X, Q), a, (b + 1) % n
        elif region == 1:
            return curve.add(X, X), (2 * a) % n, (2 * b) % n
        else:
            return curve.add(X, G), (a + 1) % n, b

    for _ in range(20):  # 偶尔会失败，多试几次
        a = random.randrange(n)
        b = random.randrange(n)
        X = curve.add(curve.mul(a, G), curve.mul(b, Q))
        Xa, Xb = a, b
        Y, Ya, Yb = X, Xa, Xb

        for _ in range(8 * isqrt(n) + 100):
            X, Xa, Xb = step(X, Xa, Xb)              # 慢指针走 1 步
            Y, Ya, Yb = step(*step(Y, Ya, Yb))       # 快指针走 2 步
            if X == Y:
                r = (Xb - Yb) % n
                if r == 0:
                    break  # 退化，换随机起点重来
                k = (Ya - Xa) * pow(r, -1, n) % n
                if curve.mul(k, G) == Q:
                    return k
                break
    return None


# ---------------------------------------------------------------------------
# 4. 演示
# ---------------------------------------------------------------------------

def modular_sqrt(a, p):
    """模平方根：求 r 使 r^2 ≡ a (mod p)，无解返回 None。Tonelli–Shanks。"""
    a %= p
    if a == 0:
        return 0
    if pow(a, (p - 1) // 2, p) != 1:  # 不是二次剩余
        return None
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    # Tonelli–Shanks (p % 4 == 1)
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1:
            t2 = (t2 * t2) % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c, t, r = i, (b * b) % p, (t * b * b) % p, (r * b) % p
    return r


def find_point(curve):
    """在曲线上找一个非无穷远的点作为基点。"""
    for x in range(1, curve.p):
        rhs = (x * x * x + curve.a * x + curve.b) % curve.p
        y = modular_sqrt(rhs, curve.p)
        if y is not None and (y * y) % curve.p == rhs:
            return (x, y)
    return None


def is_prime(n):
    if n < 2:
        return False
    for d in range(2, isqrt(n) + 1):
        if n % d == 0:
            return False
    return True


def find_prime_order_curve():
    """找一条玩具曲线，使其群阶为素数。素数阶下任意点都是生成元，
    Pollard's rho 求逆总是存在，演示最干净。"""
    for p in range(2003, 20000):
        if not is_prime(p):
            continue
        curve = Curve(a=2, b=2, p=p)
        # 4a^3 + 27b^2 != 0 才是合法曲线（无奇点）
        if (4 * curve.a ** 3 + 27 * curve.b ** 2) % p == 0:
            continue
        G = find_point(curve)
        if G is None:
            continue
        n = curve.order_of(G)
        if is_prime(n):
            return curve, G, n
    raise RuntimeError("没找到合适的曲线")


def banner(t):
    print("\n" + "=" * 64)
    print(t)
    print("=" * 64)


def demo_break_once():
    banner("演示 1：在一条玩具曲线上，从公钥反推私钥")

    # 自动找一条群阶为素数的小曲线 y^2 = x^3 + 2x + 2 (mod p)
    curve, G, n = find_prime_order_curve()
    assert curve.is_on_curve(G)

    print(f"曲线:  y^2 = x^3 + 2x + 2  (mod {curve.p})")
    print(f"基点 G = {G}")
    print(f"群的阶 n = {n}   ->   sqrt(n) ≈ {isqrt(n)}  (破解代价的量级)")

    # 偷偷选一个私钥，算出公钥，然后假装我们只知道公钥
    secret = random.randrange(2, n)
    Q = curve.mul(secret, G)
    print(f"\n[我们只被告知]  公钥 Q = {Q}")
    print(f"[真正的私钥]    k = {secret}   <- 假装不知道，现在去破它")

    t0 = time.time()
    found = bsgs(curve, G, Q, n)
    dt = (time.time() - t0) * 1000
    print(f"\nBaby-step Giant-step 破出来:  k = {found}")
    print(f"耗时: {dt:.2f} ms   ->   {'✅ 正确' if found == secret else '❌ 错误'}")

    t0 = time.time()
    found2 = pollard_rho(curve, G, Q, n)
    dt2 = (time.time() - t0) * 1000
    print(f"\nPollard's rho 破出来:        k = {found2}")
    print(f"耗时: {dt2:.2f} ms   ->   {'✅ 正确' if found2 == secret else '❌ 错误'}")


def demo_scaling():
    banner("演示 2：曲线越大，破解时间怎么爆炸 (~ sqrt(n))")

    # 一组阶逐渐变大的曲线，看 BSGS 的耗时随 sqrt(n) 增长
    curves = [
        Curve(a=2, b=3, p=97),
        Curve(a=2, b=3, p=2003),
        Curve(a=2, b=3, p=50021),
        Curve(a=2, b=3, p=1000003),
        Curve(a=2, b=3, p=15485863),
    ]

    print(f"{'素数域 p':>12} | {'群阶 n':>10} | {'sqrt(n)':>9} | {'BSGS 耗时':>12}")
    print("-" * 56)
    for curve in curves:
        # 找一个曲线上的点作为基点
        G = find_point(curve)
        if G is None:
            continue
        # Hasse 定理：群阶 n ≤ p + 1 + 2*sqrt(p)，用上界当搜索范围（不必精确求阶）
        n = curve.p + 1 + 2 * isqrt(curve.p)
        secret = random.randrange(2, curve.p)
        Q = curve.mul(secret, G)

        t0 = time.time()
        bsgs(curve, G, Q, n)
        dt = (time.time() - t0) * 1000
        print(f"{curve.p:>12} | {'≈'+str(n):>10} | {isqrt(n):>9} | {dt:>9.2f} ms")

    print("\n注意 sqrt(n) 这一列：它就是破解代价的量级。")
    print("secp256k1 的 sqrt(n) ≈ 2^128 ≈ 3.4 × 10^38，")
    print("把上表的耗时按这个比例外推 —— 远超宇宙寿命。这就是真实地址破不了的全部原因。")


if __name__ == "__main__":
    random.seed()
    demo_break_once()
    demo_scaling()

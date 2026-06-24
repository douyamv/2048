import cmath
from break_toy_ecc import find_prime_order_curve

# 发现一：x^3+7=0 的三个复数根
print('① x^3 + 7 = 0 的三个根（复数下恰好 3 个）：')
for kk in range(3):
    r = (7)**(1/3) * cmath.exp(1j*cmath.pi*(2*kk+1)/3)
    print(f'   根{kk+1} = {r.real:+.3f} {r.imag:+.3f}i')
print('   -> 实数图上只看到那个实根(-1.913)，另两个是共轭复数')
print()

curve, G, n = find_prime_order_curve(a=0, b=7)
p = curve.p
print(f'② 隐藏的复数对称(CM) -> 有限域上的 GLV 自同态  (p={p}, n={n})')

def cube_root_of_unity(m):
    for b in range(2, m):
        if pow(b, 3, m) == 1 and b != 1:
            return b
    return None

beta = cube_root_of_unity(p)   # mod p 的本原立方根
lam  = cube_root_of_unity(n)   # mod n 的本原立方根
print(f'   β = {beta}  (β^3 ≡ 1 mod p)')
print(f'   λ = {lam}  (λ^3 ≡ 1 mod n)')
print()

P = curve.mul(7, G)
phiP = ((beta * P[0]) % p, P[1])          # 自同态：只做一次乘法 β·x
print(f'   取 P = 7G = {P}')
print(f'   φ(P) = (β·x mod p, y) = {phiP}   <- 只做了 1 次乘法！')
print(f'   φ(P) 在曲线上吗? {curve.is_on_curve(phiP)}')

lamP  = curve.mul(lam, P)
lam2P = curve.mul((lam * lam) % n, P)
print(f'   λ·P  = {lamP}')
print(f'   λ²·P = {lam2P}')
print(f'   -> φ(P) 等于 λ·P 或 λ²·P 之一? {phiP in [lamP, lam2P]}')
print()
print('   含义：一次乘法 β·x，等价于把 P 乘上一个巨大的 λ。')
print('   这就是 secp256k1 的 GLV 加速 —— 直接来自复数立方根结构。')

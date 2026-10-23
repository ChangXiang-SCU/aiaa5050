"""④ 图灵测试设计：每个条件要跑多少场。

三方图灵测试里评委二选一，瞎猜是 50%。想检出"AI 被判成人的比例是 65%，
显著高于 50%"（单侧 alpha = 0.05，power = 0.8），需要多少场？

用法
    python power_n.py                  # 默认 p0=0.5, p1=0.65
    python power_n.py 0.5 0.6          # 改成检出 60%
"""
import sys
from math import ceil, comb, sqrt
from statistics import NormalDist


def n_normal(p0, p1, alpha=0.05, power=0.8):
    """正态近似公式。"""
    za, zb = NormalDist().inv_cdf(1 - alpha), NormalDist().inv_cdf(power)
    return ceil(((za * sqrt(p0 * (1 - p0)) + zb * sqrt(p1 * (1 - p1))) / (p1 - p0)) ** 2)


def tail(k, n, p):
    return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))


def n_exact(p0, p1, alpha=0.05, power=0.8, n_max=500):
    """精确二项检验：最小的 n，使检验的实际 power >= 目标。"""
    for n in range(5, n_max):
        k = next(k for k in range(n + 2) if k > n or tail(k, n, p0) <= alpha)
        if k <= n and tail(k, n, p1) >= power:
            return n, k
    return None, None


if __name__ == "__main__":
    p0 = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    p1 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.65
    n, k = n_exact(p0, p1)
    print(f"检出 {p1:.0%} vs {p0:.0%}（单侧 alpha=0.05，power=0.8）")
    print(f"正态近似：每个条件约 {n_normal(p0, p1)} 场")
    print(f"精确二项：每个条件 {n} 场，其中 >= {k} 场被判成人才算显著")

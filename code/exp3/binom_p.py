"""③ / ⑥A 没看见却知道：算"没看见"那些题的正确率和 p 值。

单侧二项检验：在纯瞎猜（四个方向，机会 25%）的前提下，答对 >= k 题的概率。

用法
    python binom_p.py 7 40          # 答对 7 题，共 40 题
    python binom_p.py 7 40 0.25     # 第三个参数是机会水平，默认 0.25
"""
import sys
from math import comb


def p_upper(k, n, p=0.25):
    """P(X >= k)，X ~ Binomial(n, p)。"""
    return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))


def threshold(n, p=0.25, alpha=0.05):
    """至少答对几题才能 p < alpha。"""
    for k in range(n + 1):
        if p_upper(k, n, p) < alpha:
            return k
    return None


if __name__ == "__main__":
    k, n = int(sys.argv[1]), int(sys.argv[2])
    p = float(sys.argv[3]) if len(sys.argv) > 3 else 0.25
    print(f"答对 {k}/{n} = {k / n:.1%}，机会水平 {p:.0%}")
    print(f"单侧 p = {p_upper(k, n, p):.3f}")
    print(f"{n} 题里至少答对 {threshold(n, p)} 题才 p < 0.05")

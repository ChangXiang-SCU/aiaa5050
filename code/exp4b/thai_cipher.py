"""④B 中文屋，你来当 · 自创玩法：把泰文规则书换成几何符号。

规则书里出现的每个泰文字符（字母、元音符、声调符）一一换成 U+25A0–U+25FF
区段的几何符号，空格、标点和换行不动。同一个字符永远换成同一个符号，所以
规则书照样能用，只是 AI 不能再"直接读泰文"了。

用法
    python thai_cipher.py rulebook.txt              # 默认随机种子 5050
    python thai_cipher.py rulebook.txt --seed 42
输出：编码后的规则书（屏幕上打印，同时存成 rulebook.enc.txt）+ 对照表（rulebook.key.txt）
两个输出文件都是 UTF-8，Windows 记事本能直接打开。

注意：这种逐字母替换挡不住 AI。我们试过，AI 第一句就从"第 1、4 位相同、
第 3、9 位相同"对上了 สวัสดีครับ，然后边聊边补全对照表。想真的挡住，
要换成现编的语言，或者整词随机换符号。
"""
import argparse
import os
import random
import sys

SYMBOLS = [chr(c) for c in range(0x25A0, 0x2600)]  # 96 个几何符号


def is_thai(ch):
    return 0x0E00 <= ord(ch) <= 0x0E7F  # 泰文区段


def build_key(text, seed=5050):
    chars = sorted({c for c in text if is_thai(c)})
    if len(chars) > len(SYMBOLS):
        raise SystemExit(f"泰文字符 {len(chars)} 个，超过符号数 {len(SYMBOLS)}")
    pool = SYMBOLS[:]
    random.Random(seed).shuffle(pool)
    return dict(zip(chars, pool))


def encode(text, key):
    return "".join(key.get(c, c) for c in text)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("rulebook")
    ap.add_argument("--seed", type=int, default=5050)
    a = ap.parse_args()
    with open(a.rulebook, encoding="utf-8") as f:
        text = f.read()
    key = build_key(text, a.seed)
    enc = encode(text, key)
    base = os.path.splitext(a.rulebook)[0]
    with open(base + ".enc.txt", "w", encoding="utf-8") as f:
        f.write(enc)
    out = base + ".key.txt"
    with open(out, "w", encoding="utf-8") as f:
        for th, sym in key.items():
            f.write(f"{th}\t{sym}\tU+{ord(th):04X}\n")
    # 中文 Windows 的控制台或重定向默认是 GBK，几何符号写不出来会报错，统一用 UTF-8
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(enc)
    print(f"\n# {len(key)} 个泰文字符，编码版写在 {base}.enc.txt，对照表写在 {out}")

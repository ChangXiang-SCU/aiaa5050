"""10/23 Living Structure · L-score：数线稿里的子结构（被线条围起来的封闭区域）。

原理和教程里的 Line Drawing Substructure Recognition 工具一样：把线条当墙，
对空白区域做连通区域标记，去掉外圈背景，剩下的每块就是一个子结构。
每张图会存一张 *_count.png 叠色图，方便肉眼核对。

用法
    pip install numpy scipy pillow
    python count.py level1.png level2.png level3.png ...
输出三种"补缝"设置下的个数（g0 不补缝，g1/g2 把线加粗 1/2 像素，防止断线漏数），
一般取 g1，再对着叠色图看一眼。

L-score：L = S × H。H 是层级数，S 是各层子结构数之和
（依据 Jiang & de Rijke 2023 里树的例子：1+2+8+24+96 = 134，H = 5，L = 670）。
"""
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as ndi


def count(path, thr=170, gap=1, min_frac=2e-5, save=True, crop=None):
    im = Image.open(path).convert("L")
    if crop:
        im = im.crop(crop)
    g = np.asarray(im)
    line = g < thr
    if gap > 0:
        line = ndi.binary_dilation(line, iterations=gap)
    free = ~line
    lab, n = ndi.label(free)  # 4 连通
    h, w = free.shape
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
    areas = ndi.sum(np.ones_like(lab), lab, index=np.arange(1, n + 1))
    min_area = max(12, min_frac * h * w)
    keep = [i + 1 for i, a in enumerate(areas) if a >= min_area and (i + 1) not in border]
    if save:
        rng = np.random.default_rng(0)
        col = np.zeros((n + 1, 3), np.uint8)
        col[keep] = rng.integers(60, 230, (len(keep), 3))
        rgb = col[lab]
        rgb[line] = 0
        rgb[(lab == 0) & ~line] = 255
        for b in border:
            if b:
                rgb[lab == b] = 255
        base, _ = os.path.splitext(path)
        Image.fromarray(rgb).save(base + "_count.png")
    return len(keep)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        r = {f"g{g}": count(p, gap=g, save=(g == 1)) for g in (0, 1, 2)}
        print(os.path.basename(p), r, flush=True)

"""10/23 Living Structure：从练习手册 PDF 里把一组对比图抠出来，左右各存一张。

用法
    pip install pymupdf numpy pillow
    python extract_pair.py "手册.pdf" 7          # 第 7 页（我们组是 Image Pair 7）
    python extract_pair.py "手册.pdf" 7 6        # 第 3 个参数：那一页的第几张嵌入图，默认取最大的
输出 pair_A.png、pair_B.png（放大 2 倍，方便描线）。
按"整块非白色的列"切左右两张，版式不一样的页可能要手动裁。
"""
import io
import sys

import fitz  # pymupdf
import numpy as np
from PIL import Image

pdf, page_no = sys.argv[1], int(sys.argv[2])
doc = fitz.open(pdf)
page = doc[page_no - 1]
imgs = page.get_images(full=True)
if len(sys.argv) > 3:
    xref = imgs[int(sys.argv[3])][0]
else:
    xref = max(imgs, key=lambda im: im[2] * im[3])[0]
img = Image.open(io.BytesIO(doc.extract_image(xref)["image"])).convert("RGB")

a = np.asarray(img).astype(int)
nonwhite = a.min(axis=2) < 235
active = nonwhite.mean(axis=0) > 0.5
spans, start = [], None
for x, v in enumerate(active):
    if v and start is None:
        start = x
    if not v and start is not None:
        spans.append((start, x))
        start = None
if start is not None:
    spans.append((start, len(active)))
spans = [s for s in spans if s[1] - s[0] > 200][:2]
if len(spans) < 2:
    sys.exit(f"没切出两张图（找到 {len(spans)} 段），请手动裁剪")

for (x0, x1), name in zip(spans, ["pair_A", "pair_B"]):
    ys = np.where(nonwhite[:, x0 + 20:x1 - 20].mean(axis=1) > 0.9)[0]
    crop = img.crop((x0 + 2, ys.min() + 2, x1 - 2, ys.max() - 1))
    crop.resize((crop.width * 2, crop.height * 2), Image.LANCZOS).save(name + ".png")
    print(name, crop.size)

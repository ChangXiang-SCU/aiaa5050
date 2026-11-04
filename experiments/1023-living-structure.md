# 10/23 机器没体验过美，也能认出美吗？ Living Structure + AI: Four Hands-On Exercises

10/23 · 江斌教授客座 · 3–5 人一组 · 材料：练习手册 PDF（Canvas Files）+ 线稿教程（都不放进仓库） · [网页版](https://changxiang-scu.github.io/aiaa5050/#ls)

## 目的

江斌教授的“活的结构”理论认为，美可以用结构来量：子结构越多、层次越深，越“有生命”。小组用四种方法给一对建筑打分，再讨论：机器没体验过美，能不能认出美。

## 要求

**要做什么**

每组拿到一对建筑照片，用四种方法比较哪个“更有生命、更完整”，组内每人负责一种：

- L-score：把建筑画成从简到繁的分级线稿，数每级的子结构（封闭区域），L = S × H。S 是各级子结构数之和，H 是级数；相邻两级的数目比要在 2 到 6 之间。
- B-score：Beautimeter，按 15 条性质打分。
- 3M VAS：视线热力图。账号用课上给的共享账号，这里不放。
- MOST：凭直觉选“哪个更像一个完整的自己”，再去问 AI。

**交什么**

- 各自方法的结果
- 组内讨论：机器没体验过美，能认出美吗
- 派人上台汇报

## 做法

我们组（第 7 组）的 L-score 部分：A 美国国家档案馆（新古典，Pope，1935） vs B 汉弗莱大楼（粗野主义，Breuer，1977）。

1. 用 `extract_pair.py` 从练习手册 PDF 里把这一组对比图抠出来。
2. 画线稿前先定死规则：只画照片里看得到的主立面；每级只加下一层确实看得到的构件；最后一级包含所有细节。两栋楼用同一套规则。
3. 每级线稿用 `count.py` 数子结构，对着叠色图核对。
4. 课上 GPT 出图连不上的话，教程允许手工画、手工改。

## 代码

需要 `pip install -r code/requirements.txt`（numpy、scipy、pillow、pymupdf）。

[`code/lscore/extract_pair.py`](../code/lscore/extract_pair.py)：

```bash
python code/lscore/extract_pair.py "手册.pdf" 7       # 第 7 页，输出 pair_A.png、pair_B.png
python code/lscore/extract_pair.py "手册.pdf" 7 6     # 第 3 个参数：那一页第几张嵌入图（从 0 数）
```

[`code/lscore/count.py`](../code/lscore/count.py)：

```bash
python code/lscore/count.py level1.png level2.png level3.png
```

每张图输出三种“补缝”设置下的个数（g0 不补缝，g1/g2 把线加粗 1/2 像素），一般取 g1；同时存一张 `*_count.png` 叠色图。

## 提示词

无。

## 结果

| | 各级子结构数 | S | H | L |
|---|---|---|---|---|
| A 档案馆 | 3 → 14 → 58 → 129 → 280 → 675 | 1159 | 6 | 6954 |
| B 汉弗莱 | 5 → 11 → 56 → 280 → 1016 | 1368 | 5 | 6840 |

几乎打平。B 的 S 有 89% 来自 180 个一模一样的窗洞；A 靠多一层细部，赢在 H。

口径一换排名就翻：去掉装饰，A 只剩 2420；S 只算最后一级，A 4050、B 5080。

## 反思

- L-score 数的是结构，哪些结构算数，是人先定好的。
- 子结构别手数，用 `count.py`，再对着叠色图看一眼。

未收录：另外三种方法的结果和组内讨论。

# AIAA 5050 Machine Consciousness · 课上实验整理

**网址：https://changxiang-scu.github.io/aiaa5050/**

每个实验要做什么、交什么、怎么做顺手，加上能直接用的代码和提示词。这学期每节课后更新。
个人整理，不是官方材料，要求以老师的 slide 和 Canvas 为准。

## 目录

每个实验一份文档，都按同一个结构写：**目的、要求、做法、代码、提示词、结果、反思**。做法、结果、反思是我自己的记录，仅供参考；标“未收录”的是还没整理进来的部分。

| 编号 | 实验 | 日期 | 形式 | 代码 / 提示词 |
|---|---|---|---|---|
| ① | [意识是什么？](experiments/01-what-is-consciousness.md) | 9/4 | 个人 · 先不用 AI | 无 |
| ② | [让 GWT 被看见](experiments/02-make-gwt-visible.md)（即 ⑥C） | 9/11 | 20 分钟 · 一张图 + 盲测 | `image-gen/gen_image.py`、`prompts/exp2_gwt_v2.txt`、`prompts/blind_test.txt` |
| ③ | [没看见，却知道](experiments/03-seeing-without-seeing.md)（即 ⑥A） | 9/18 | 网页 40 题 | `exp3/binom_p.py` |
| ④ | [设计你的图灵测试](experiments/04-turing-test-design.md) | 10/9 | 30 分钟 · Task 3 禁用 AI | `exp4/power_n.py` |
| ④B | [中文屋，你来当](experiments/04b-chinese-room.md) | 10/9 | 25 分钟 · 泰文规则书 | `exp4b/thai_cipher.py`、`exp4b/room_prompt.txt` |
| ⑥B | [找不同](experiments/06b-spot-the-change.md) | 模块 06 | 网页 10 轮 · 人 vs AI | 无 |
| ⑥D | [找错字](experiments/06d-proofreading-race.md) | 模块 06 | 网页 4 段 · 人 vs AI | 无 |
| ⑥G | [让另外五家理论被看见](experiments/06g-other-five-theories.md) | 模块 06 | 40 分钟 · 五张图 + 盲测 | `image-gen/gen_image.py`、`prompts/6g_*.txt`、`prompts/blind_test.txt` |
| 10/23 | [Living Structure + AI](experiments/1023-living-structure.md) | 10/23 | 江斌教授客座 · 小组 | `lscore/count.py`、`lscore/extract_pair.py` |

模块 06「人脑与理论」（10/10 补课起）把几个实验串在一起：① 实验与现象（⑥A 即 ③、⑥B）；② 四家理论 HOT、GWT、IIT、PP（⑥C 即 ②、⑥D）；③ 理论之争 COGITATE 2025；课上另加 ⑥G。

## 运行代码

**依赖**

- Python 3.8 或更新。
- `exp3/`、`exp4/`、`exp4b/`、`image-gen/` 只用标准库，装好 Python 就能跑。
- `lscore/` 要第三方库：`pip install -r code/requirements.txt`（numpy、scipy、pillow、pymupdf）。
- `image-gen/gen_image.py` 要自己的 OpenAI API key，放环境变量 `OPENAI_API_KEY`，别写进代码。可选 `OPENAI_BASE_URL` 换成兼容的接口地址。

**怎么跑**（都在仓库根目录）

| 脚本 | 命令 | 说明 |
|---|---|---|
| `exp3/binom_p.py` | `python code/exp3/binom_p.py 7 40` | 答对 7/40 的单侧 p 值，和至少要答对几题 |
| `exp4/power_n.py` | `python code/exp4/power_n.py 0.5 0.65` | 图灵测试每个条件要跑几场 |
| `exp4b/thai_cipher.py` | `python code/exp4b/thai_cipher.py rulebook.txt` | 泰文规则书换成几何符号，输出 `.enc.txt` 和 `.key.txt` |
| `image-gen/gen_image.py` | `python code/image-gen/gen_image.py code/prompts/6g_1_hot.txt A.png 1536x1024` | 提示词出图，单张 1 到 3 分钟 |
| `lscore/extract_pair.py` | `python code/lscore/extract_pair.py "手册.pdf" 7` | 从练习手册第 7 页抠出左右两张图 |
| `lscore/count.py` | `python code/lscore/count.py level1.png level2.png` | 数线稿子结构，出叠色图 |

**自检**：`python code/selftest.py` 用造出来的小数据把上面每个脚本跑一遍，不联网、不花钱（出图脚本用本机的假服务器测）。没装 `lscore/` 的依赖时，那两项会跳过。

## 文件

| 位置 | 内容 |
|---|---|
| `index.html` | 网页本身（由 `src/build.py` 生成，别直接改） |
| `src/index.tpl.html` | 网页的源文件，内容都在这里改 |
| `src/build.py` | 把源文件、代码、配图合成 `index.html` |
| `src/img/` | 配图（压缩到 1200 宽的 jpg） |
| `experiments/` | 每个实验一份文档；`_template.md` 是新实验的模板 |
| `code/exp3/` | ③ 没看见却知道：二项检验 p 值 |
| `code/exp4/` | ④ 图灵测试：样本量计算 |
| `code/exp4b/` | ④B 中文屋：泰文规则书换符号、屋中人提示词 |
| `code/image-gen/` | ② ⑥G 出图脚本 |
| `code/prompts/` | ② ⑥G 的出图提示词、盲测提问模板 |
| `code/lscore/` | 10/23 L-score：数子结构、从手册抠对比图 |
| `code/requirements.txt` | `lscore/` 的第三方依赖 |
| `code/selftest.py` | 所有脚本的离线自检 |

## 每节课后怎么更新

1. 在 `src/index.tpl.html` 里加一节新实验：照抄现有的一节（`<section class="exp" id="...">`），写清楚这个实验在干嘛、要做什么、交什么、坑；标题旁的 `chip code` 写出勤码；顶部「一览」加一张卡片，「出勤码」表加一行，导航加一个链接。
2. 复制 `experiments/_template.md` 写一份文档，再在上面「目录」表里加一行。
3. 有新代码或提示词：放进 `code/`，再在 `src/build.py` 的 `FILES` 里登记一行。新脚本最好在 `code/selftest.py` 里也加一项。
4. 有新配图：压到 1200 宽 jpg 放进 `src/img/`，在 `src/build.py` 的 `IMAGES` 里登记。
5. 在仓库根目录运行 `python src/build.py`。它会检查页内链接都能跳到、没有破折号，失败会直接报错。
6. 本地用浏览器打开 `index.html` 看一眼，然后 `git commit` + `git push`。GitHub Pages 一般 20 秒内更新。

## 不放的东西

学号、邮箱；课上给的共享账号密码；⑥B 这类实验的标准答案（提前知道就没法做）；写明禁止用 AI 的部分（如 ④ Task 3）；老师课件原件；任何 API key 或 token。

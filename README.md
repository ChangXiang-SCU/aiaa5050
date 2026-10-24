# AIAA 5050 Machine Consciousness · 课上实验整理

**网址：https://changxiang-scu.github.io/aiaa5050/**

每个实验要做什么、交什么、怎么做顺手，每节课的出勤码，加上能直接用的代码和提示词。这学期每节课后更新。
个人整理，不是官方材料，要求以老师的 slide 和 Canvas 为准。

## 文件

| 位置 | 内容 |
|---|---|
| `index.html` | 网页本身（由 `src/build.py` 生成，别直接改） |
| `src/index.tpl.html` | 网页的源文件，内容都在这里改 |
| `src/build.py` | 把源文件、代码、配图合成 `index.html` |
| `src/img/` | 配图（压缩到 1200 宽的 jpg） |
| `code/exp3/` | ③ 没看见却知道：二项检验 p 值 |
| `code/exp4/` | ④ 图灵测试：样本量计算 |
| `code/exp4b/` | ④B 中文屋：泰文规则书换符号、屋中人提示词 |
| `code/image-gen/` | ② ⑥G 出图脚本（key 放环境变量 `OPENAI_API_KEY`） |
| `code/prompts/` | ② ⑥G 的出图提示词、盲测提问模板 |
| `code/lscore/` | 10/23 L-score：数子结构、从手册抠对比图 |

## 每节课后怎么更新

1. 在 `src/index.tpl.html` 里加一节新实验：照抄现有的一节（`<section class="exp" id="...">`），写清楚这个实验在干嘛、要做什么、交什么、坑；标题旁的 `chip code` 写出勤码；顶部「一览」加一张卡片，「出勤码」表加一行，导航加一个链接。
2. 有新代码或提示词：放进 `code/`，再在 `src/build.py` 的 `FILES` 里登记一行。
3. 有新配图：压到 1200 宽 jpg 放进 `src/img/`，在 `src/build.py` 的 `IMAGES` 里登记。
4. 在仓库根目录运行 `python src/build.py`。它会检查页内链接都能跳到、没有破折号，失败会直接报错。
5. 本地用浏览器打开 `index.html` 看一眼，然后 `git commit` + `git push`。GitHub Pages 一般 20 秒内更新。

## 不放的东西

学号、邮箱；课上给的共享账号密码；⑥B 这类实验的标准答案（提前知道就没法做）；写明禁止用 AI 的部分（如 ④ Task 3）；老师课件原件；任何 API key 或 token。

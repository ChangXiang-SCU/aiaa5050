# ⑥G 让另外五家理论被看见 Make the Other Five Theories Visible

模块 06 · 40 分钟 · 个人 · 工具不限 · 材料：课上 slide · [网页版](https://changxiang-scu.github.io/aiaa5050/#e6g)

## 目的

接着 ②：把另外五个意识理论，高阶理论 HOT、注意图式 AST、整合信息 IIT、预测加工 PP、量子意识 Orch-OR，各画成一张图，打乱后让 AI 盲猜每张是哪个理论。

## 要求

**要做什么**

1. 对话弄懂 HOT、AST、IIT、PP、量子意识（Orch-OR）。
2. 每家一张图（或 10 秒以内的视频）。
3. AI 盲测：新开对话，五件打乱一起发，别写理论名。
4. 自创玩法。

好作品检验：HOT 谁在看着谁？AST 的简图在哪？IIT 为什么拆不开？PP 猜了什么？量子哪一刻坍缩？加分：自创隐喻。

**交什么**

- 作品
- 每张的标题 + 一句话
- 最终提示词 + 工具
- 盲测回答（猜对几张）
- 自创玩法
- 原始记录

另记 session code、模型名称版本；新对话前关记忆。

## 做法

- 统一画风：暖白底、深蓝线条、只用一个橙色强调。五张统一画风，盲测时 AI 只能看内容。
- 出图用 GPT Image（经 Figma 的 generate_image），五张都是第一版。
- 盲测：新开 Claude Opus 5.5 会话，文件名改成 A 到 E。
- 自创玩法：把 ② 的 GWT 图也放进去，六张打乱，再换模型。

## 代码

[`code/image-gen/gen_image.py`](../code/image-gen/gen_image.py) 可以直接用下面的提示词出图（这次实际是经 Figma 出的）：

```bash
python code/image-gen/gen_image.py code/prompts/6g_1_hot.txt A.png 1536x1024
```

## 提示词

| 理论 | 标题 | 提示词 |
|---|---|---|
| HOT | 《做对了，不等于看见了》 | [`6g_1_hot.txt`](../code/prompts/6g_1_hot.txt) |
| AST | 《脑子里的小地图》 | [`6g_2_ast.txt`](../code/prompts/6g_2_ast.txt) |
| IIT | 《拆不开的鲁班锁》 | [`6g_3_iit.txt`](../code/prompts/6g_3_iit.txt) |
| PP | 《黑暗里多出来的那一级台阶》 | [`6g_4_pp.txt`](../code/prompts/6g_4_pp.txt) |
| Orch-OR | 《没人看，它也会落下》 | [`6g_5_orchor.txt`](../code/prompts/6g_5_orchor.txt) |

盲测提问模板：[`blind_test.txt`](../code/prompts/blind_test.txt)

## 结果

| 理论 | 画面 | 图 |
|---|---|---|
| HOT | 两个一样的分拣机器人都把瓶子投对了，只有一个头上有个小人盯着它自己的胸口屏幕，举牌 “I AM SEEING A BOTTLE” | [6G_1_HOT.jpg](../src/img/6G_1_HOT.jpg) |
| AST | 真实的注意是一团乱线；头里的游戏小地图上只有一个干净的扇形 ME → 狗，旁边还有别人的 HER | [6G_2_AST.jpg](../src/img/6G_2_AST.jpg) |
| IIT | 灯泡板剪开：NOTHING LOST；鲁班锁剪开：EVERYTHING LOST | [6G_3_IIT.jpg](../src/img/6G_3_IIT.jpg) |
| PP | 手电只照脚下一级，其余台阶是脑子投出的虚线，多猜了一级，落脚处一个 “!” | [6G_4_PP.jpg](../src/img/6G_4_PP.jpg) |
| Orch-OR | 微管里的硬币处在叠加态，到 THRESHOLD 同时倒下；胶片代表离散的瞬间；空椅子代表没有观察者 | [6G_5_OrchOR.jpg](../src/img/6G_5_OrchOR.jpg) |

盲测（Claude Opus 5.5）：5 / 5。把握度 PP 90%、IIT 95%、Orch-OR 85%、HOT 80%、AST 70%。

自创玩法，六张打乱（加上 ② 的 GWT）：

- Opus 6/6，说最容易混的是 AST 和 HOT（都在画“系统给自己的内部状态再做一层表征”）。
- Haiku 5/6，把量子那张认成“阈值点火 / 离散帧”（把握 40%），说最容易混的是 GWT 和量子（都讲阈值）。

## 反思

- 两个模型混淆的方向不一样；THRESHOLD 这个线索太通用。
- 最难画的是 AST：要给一个看不见的东西画简图，而且一画“自我表征”就和 HOT 撞车。
- 五张统一画风，盲测时 AI 只能看内容，结果更有说服力。

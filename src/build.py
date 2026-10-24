"""生成网页：src/index.tpl.html + code/ + src/img/ -> 仓库根目录的 index.html（单文件，图片内嵌）。

用法（在仓库根目录）：python src/build.py
可选：UPDATED=2026-10-30 python src/build.py   指定页面上的"最后更新"日期，默认今天。
"""
import base64
import datetime
import html
import os
import re

D = os.path.dirname(os.path.abspath(__file__))      # src/
ROOT = os.path.dirname(D)                           # 仓库根目录
C = os.path.join(ROOT, "code")
I = os.path.join(D, "img")

FILES = [
    ("exp3/binom_p.py", "③", "算“没看见”那些题的正确率和 p 值，以及至少要答对几题。用法：python binom_p.py 7 40"),
    ("exp4/power_n.py", "④", "图灵测试每个条件要跑多少场（正态近似 + 精确二项）。"),
    ("exp4b/thai_cipher.py", "④B", "把泰文规则书里每个字符换成几何符号，输出编码版和对照表。"),
    ("exp4b/room_prompt.txt", "④B", "让 AI 当屋中人的提示词，把编码后的 6 条规则贴进去。"),
    ("image-gen/gen_image.py", "② ⑥G", "文字提示词出图（OpenAI Images API，只用标准库）。key 放环境变量 OPENAI_API_KEY。"),
    ("prompts/exp2_gwt_v2.txt", "②", "GWT 图《每轮只有一个发言人》的最终提示词。"),
    ("prompts/6g_1_hot.txt", "⑥G", "HOT《做对了，不等于看见了》"),
    ("prompts/6g_2_ast.txt", "⑥G", "AST《脑子里的小地图》"),
    ("prompts/6g_3_iit.txt", "⑥G", "IIT《拆不开的鲁班锁》"),
    ("prompts/6g_4_pp.txt", "⑥G", "PP《黑暗里多出来的那一级台阶》"),
    ("prompts/6g_5_orchor.txt", "⑥G", "Orch-OR《没人看，它也会落下》"),
    ("prompts/blind_test.txt", "② ⑥G", "AI 盲测的提问模板。"),
    ("lscore/count.py", "10/23", "数线稿里的子结构（封闭区域），出叠色图核对。"),
    ("lscore/extract_pair.py", "10/23", "从练习手册 PDF 里抠出一组对比图。"),
]

IMAGES = {
    "gwt": "gwt_v2.jpg",
    "6g": [("6G_1_HOT.jpg", "HOT《做对了，不等于看见了》"),
           ("6G_2_AST.jpg", "AST《脑子里的小地图》"),
           ("6G_3_IIT.jpg", "IIT《拆不开的鲁班锁》"),
           ("6G_4_PP.jpg", "PP《黑暗里多出来的那一级台阶》"),
           ("6G_5_OrchOR.jpg", "Orch-OR《没人看，它也会落下》")],
}


def slug(path):
    return "f-" + os.path.splitext(os.path.basename(path))[0]


def data_uri(name):
    p = os.path.join(I, name)
    if not os.path.exists(p):
        return None
    with open(p, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()


def file_card(path, tag, desc):
    with open(os.path.join(C, path), encoding="utf-8") as f:
        src = f.read().rstrip("\n")
    name = os.path.basename(path)
    sid = slug(path)
    n = src.count("\n") + 1
    return (f'<article class="file" id="{sid}"><div class="fh"><span class="fn">{name}</span>'
            f'<span class="for">{tag}</span><p class="desc">{html.escape(desc)}</p>'
            f'<div class="btns"><button type="button" data-copy="{sid}">复制</button>'
            f'<button type="button" data-dl="{sid}" data-name="{name}">下载</button></div></div>'
            f'<details><summary>看内容（{n} 行）</summary><pre><code>{html.escape(src)}</code></pre></details></article>')


def main():
    with open(os.path.join(D, "index.tpl.html"), encoding="utf-8") as f:
        t = f.read()
    t = t.replace("{{UPDATED}}", os.environ.get("UPDATED") or datetime.date.today().isoformat())
    t = t.replace("<!--FILES-->", "\n".join(file_card(*x) for x in FILES))

    def img(m):
        key, cap = m.group(1), m.group(2)
        uri = data_uri(IMAGES[key])
        if not uri:
            return ""
        return f'<figure><img src="{uri}" alt="{html.escape(cap)}" width="1200" height="800" decoding="async"><figcaption>{html.escape(cap)}</figcaption></figure>'
    t = re.sub(r"<!--IMG:(\w+)\|(.*?)-->", img, t)

    def gallery(m):
        items = []
        for name, cap in IMAGES[m.group(1)]:
            uri = data_uri(name)
            if uri:
                items.append(f'<figure><img src="{uri}" alt="{html.escape(cap)}" width="1200" height="800" decoding="async"><figcaption>{html.escape(cap)}</figcaption></figure>')
        return f'<div class="gallery">{"".join(items)}</div>' if items else ""
    t = re.sub(r"<!--GALLERY:(\w+)-->", gallery, t)

    # every in-page link must resolve
    ids = set(re.findall(r'id="([^"]+)"', t))
    bad = [h for h in re.findall(r'href="#([^"]+)"', t) if h not in ids]
    assert not bad, f"broken anchors: {bad}"
    assert "—" not in t, "em dash found"

    assert "{{" not in t, "unfilled placeholder"
    out = os.path.join(ROOT, "index.html")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(t)
    print("wrote", out, f"{os.path.getsize(out)/1024:.0f} KB")


if __name__ == "__main__":
    main()

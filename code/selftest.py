"""离线自检：把 code/ 下每个脚本用造出来的小数据跑一遍，不联网、不花钱。

用法（在仓库根目录）
    python code/selftest.py
lscore/ 两个脚本要 numpy scipy pillow pymupdf（pip install -r code/requirements.txt），
没装就跳过这两项。gen_image.py 用本机一个假的 API 服务器测，不会真的调 OpenAI。
"""
import base64
import http.server
import json
import os
import subprocess
import sys
import tempfile
import threading

C = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
results = []


def run(args, cwd, env=None, expect=0):
    e = dict(os.environ, PYTHONIOENCODING="utf-8")
    e.update(env or {})
    r = subprocess.run([PY, os.path.join(C, args[0])] + args[1:], cwd=cwd, env=e,
                       capture_output=True, text=True, encoding="utf-8")
    return r.returncode == expect, (r.stdout + r.stderr).strip()


def check(name, ok, detail=""):
    results.append((name, ok))
    print("通过" if ok else "失败", name)
    if not ok:
        print("    " + detail.replace("\n", "\n    "))


def main():
    with tempfile.TemporaryDirectory(prefix="aiaa5050-") as tmp:
        return checks(tmp)


def checks(tmp):
    ok, out = run(["exp3/binom_p.py", "7", "40"], tmp)
    check("exp3/binom_p.py：7/40 的 p = 0.904，至少 16 题", ok and "p = 0.904" in out and "16 题" in out, out)

    ok, out = run(["exp4/power_n.py"], tmp)
    check("exp4/power_n.py：65% vs 50% 每个条件约 70 场", ok and "67 场" in out and "69 场" in out, out)

    rb = os.path.join(tmp, "rulebook.txt")
    with open(rb, "w", encoding="utf-8") as f:
        f.write("1. 收到：สวัสดีครับ → 回：สวัสดีค่ะ\n")
    ok, out = run(["exp4b/thai_cipher.py", rb], tmp, {"PYTHONIOENCODING": "gbk"})
    enc = open(os.path.join(tmp, "rulebook.enc.txt"), encoding="utf-8").read() if ok else ""
    check("exp4b/thai_cipher.py：GBK 控制台下也能输出，泰文全部换掉",
          ok and enc and not any(0x0E00 <= ord(ch) <= 0x0E7F for ch in enc)
          and os.path.exists(os.path.join(tmp, "rulebook.key.txt")), out)

    png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")

    class H(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            body = json.dumps({"data": [{"b64_json": base64.b64encode(png).decode()}]}).encode()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    env = {"OPENAI_API_KEY": "selftest", "OPENAI_BASE_URL": f"http://127.0.0.1:{srv.server_port}/v1/",
           "NO_PROXY": "127.0.0.1", "no_proxy": "127.0.0.1"}
    ok, out = run(["image-gen/gen_image.py", os.path.join(C, "prompts", "6g_1_hot.txt"),
                   "out.png", "1536x1024"], tmp, env)
    got = open(os.path.join(tmp, "out.png"), "rb").read() if ok else b""
    check("image-gen/gen_image.py：请求和存图（假服务器）", ok and got == png, out)
    srv.shutdown()

    try:
        import numpy  # noqa: F401
        import scipy  # noqa: F401
        from PIL import Image, ImageDraw
        try:
            import pymupdf as fitz
        except ImportError:
            import fitz
    except ImportError as e:
        print("跳过 lscore/ 两项：", e, "（pip install -r code/requirements.txt）")
    else:
        im = Image.new("L", (600, 400), 255)
        d = ImageDraw.Draw(im)
        d.rectangle([50, 50, 550, 350], outline=0, width=3)
        for x in (217, 383):
            d.line([x, 50, x, 350], fill=0, width=3)
        d.line([50, 200, 550, 200], fill=0, width=3)
        im.save(os.path.join(tmp, "grid.png"))
        ok, out = run(["lscore/count.py", "grid.png"], tmp)
        check("lscore/count.py：2×3 格子数出 6 个子结构", ok and "'g1': 6" in out, out)

        pair = Image.new("RGB", (1400, 600), "white")
        d = ImageDraw.Draw(pair)
        d.rectangle([40, 60, 660, 540], fill=(120, 90, 60))
        d.rectangle([740, 60, 1360, 540], fill=(60, 90, 120))
        pair.save(os.path.join(tmp, "pair.png"))
        doc = fitz.open()
        doc.new_page().insert_image(fitz.Rect(20, 100, 580, 340), filename=os.path.join(tmp, "pair.png"))
        doc.save(os.path.join(tmp, "book.pdf"))
        ok, out = run(["lscore/extract_pair.py", "book.pdf", "1"], tmp)
        check("lscore/extract_pair.py：从 PDF 页里切出左右两张",
              ok and os.path.exists(os.path.join(tmp, "pair_A.png")) and os.path.exists(os.path.join(tmp, "pair_B.png")), out)

    bad = [n for n, ok in results if not ok]
    print(f"\n{len(results) - len(bad)}/{len(results)} 通过")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

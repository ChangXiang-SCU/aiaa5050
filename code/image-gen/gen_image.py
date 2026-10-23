"""② / ⑥G 出图：OpenAI Images API，文字提示词 -> 一张 PNG。只用 Python 标准库。

先设好 key：
    Windows PowerShell:  $env:OPENAI_API_KEY = "sk-..."
    macOS / Linux:       export OPENAI_API_KEY=sk-...
用法
    python gen_image.py prompt.txt out.png 1536x1024
    python gen_image.py prompt.txt out.png 1536x1024 gpt-image-1   # 第 4 个参数换模型（默认 gpt-image-2）
单张高质量图要 1–3 分钟，别急着关窗口。
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.request

API = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1") + "/images/generations"


def main():
    prompt_file, out, size = sys.argv[1], sys.argv[2], sys.argv[3]
    model = sys.argv[4] if len(sys.argv) > 4 else "gpt-image-2"
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        sys.exit("先设置环境变量 OPENAI_API_KEY")
    with open(prompt_file, encoding="utf-8") as f:
        prompt = f.read()
    payload = {"model": model, "prompt": prompt, "size": size, "quality": "high", "n": 1}
    req = urllib.request.Request(
        API, data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            d = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print("HTTPERR", e.code, e.read().decode("utf-8")[:900])
        return 1
    item = d["data"][0]
    raw = base64.b64decode(item["b64_json"]) if item.get("b64_json") else \
        urllib.request.urlopen(item["url"], timeout=300).read()
    with open(out, "wb") as f:
        f.write(raw)
    print("OK", out, len(raw))
    return 0


if __name__ == "__main__":
    sys.exit(main())

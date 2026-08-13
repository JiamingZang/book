import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

t = open("handbook/trading-handbook.html", encoding="utf-8").read()
# 找所有 img 的 alt
alts = re.findall(r'<img[^>]*alt="([^"]*)"[^>]*>', t)
caps = re.findall(r'<p class="figcap">([^<]+)</p>', t)
print("imgs:", len(alts), "caps:", len(caps))
no_cap = []
for a in alts:
    cap_txt = re.sub(r"<[^>]+>", "", a).strip()
    if not re.match(r"^图\s*\d+", cap_txt):
        no_cap.append(cap_txt[:60])
print("无图注的图:", no_cap if no_cap else "无")
# 校验一一对应
ids_img = set(re.findall(r'<img[^>]*alt="(图\s*\d+[-.]\d+R?)', t))
ids_cap = set(re.findall(r'<p class="figcap">(图\s*\d+[-.]\d+R?)', t))
print("img 图号:", len(ids_img), "cap 图号:", len(ids_cap))
print("img 有 cap 没有:", ids_img - ids_cap)
print("cap 有 img 没有:", ids_cap - ids_img)

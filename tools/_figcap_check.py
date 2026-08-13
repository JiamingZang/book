import sys
import pymupdf

sys.stdout.reconfigure(encoding="utf-8")

d = pymupdf.open("handbook/trading-handbook.pdf")
found = 0
for i, p in enumerate(d):
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            s = l["spans"][0]
            txt = s["text"].strip()
            if txt.startswith("图 2-1") or txt.startswith("图 2-2"):
                x0, x1 = l["bbox"][0], l["bbox"][2]
                w = p.rect.width
                off = (x0 + x1) / 2 - w / 2
                print(
                    "page %d: [%s] x0=%.0f x1=%.0f w=%.0f 居中偏差=%.0fpt font=%s size=%.1f"
                    % (i + 1, txt[:18], x0, x1, w, off, s["font"], s["size"])
                )
                found += 1
print("figcap lines found:", found)

import sys
import pymupdf

sys.stdout.reconfigure(encoding="utf-8")

d = pymupdf.open("handbook/trading-handbook.pdf")
for i, p in enumerate(d):
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if "自测" in s["text"] or "小结" in s["text"]:
                    print(
                        "page %d: [%s] color=#%06x size=%.1f font=%s"
                        % (i + 1, s["text"][:20], s["color"], s["size"], s["font"])
                    )

"""扫描 PDF 页面，检测 matplotlib 教学级真实图的特色颜色是否正常渲染"""
import pymupdf, sys
from PIL import Image
import io

PDF = r"c:\Users\18315\Desktop\新建文件夹\handbook\trading-handbook.pdf"
# matplotlib 手绘图特色色：(名称, 参考RGB, 容差)
COLORS = {
    "红涨": ((239, 83, 80), 25),
    "绿跌": ((38, 166, 154), 25),
    "蓝标注": ((21, 101, 192), 30),
    "橙通道": ((239, 108, 0), 30),
    "紫ATR": ((123, 31, 162), 35),
}
MIN_PIXELS = 300  # 每页每个颜色至少这么多像素才算"存在"

def count_color(img, ref, tol):
    n = 0
    px = img.load()
    w, h = img.size
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            r, g, b = px[x, y][:3]
            if abs(r-ref[0]) <= tol and abs(g-ref[1]) <= tol and abs(b-ref[2]) <= tol:
                n += 1
    return n * 4  # 每2px采样，乘4估算总量

doc = pymupdf.open(PDF)
print(f"总页数: {len(doc)}")
hits = []  # (page, {color: count})
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=60)  # 低分辨率快速扫描
    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    found = {}
    for name, (ref, tol) in COLORS.items():
        c = count_color(img, ref, tol)
        if c >= MIN_PIXELS:
            found[name] = c
    if found:
        hits.append((i + 1, found))

print(f"含 matplotlib 特色颜色的页面: {len(hits)}")
for p, found in hits:
    print(f"  第{p}页: {found}")
doc.close()

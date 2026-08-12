# -*- coding: utf-8 -*-
"""
trading-handbook.pdf → 章节 Markdown 提取脚本
- 按章节页码边界拆分
- find_tables 还原表格为 Markdown 表格
- 提取图片到 images/，并在原文位置插入引用
- 中文硬折行合并
"""
import os
import re
import pymupdf

PDF = "trading-handbook.pdf"
OUT = "handbook"
IMG_DIR = os.path.join(OUT, "images")

# 章节定义: (文件名, 标题, 起始页(1-based), 结束页(含))
CHAPTERS = [
    ("00_封面与前言", "交易手册：价格行为 · SMC · 仓位 · 心态 · Prop 考核", 1, 4),
    ("01_第1章_市场是怎么运作的", "第 1 章 市场是怎么运作的", 5, 12),
    ("02_第2章_读懂价格行为", "第 2 章 读懂价格行为", 13, 19),
    ("03_第3章_入场信号", "第 3 章 入场信号", 20, 26),
    ("04_第4章_交易系统", "第 4 章 交易系统：入场与出场", 27, 35),
    ("05_第5章_聪明钱概念SMC", "第 5 章 聪明钱概念（SMC）", 36, 43),
    ("06_第6章_仓位与风险", "第 6 章 仓位与风险", 44, 49),
    ("07_第7章_执行与心态", "第 7 章 执行与心态", 50, 54),
    ("08_第8章_工具与验证", "第 8 章 工具与验证", 55, 59),
    ("09_第9章_Prop考核实战", "第 9 章 Prop Firm 考核实战", 60, 63),
    ("10_第10章_期权", "第 10 章 期权：交易的另一个维度", 64, 69),
    ("11_附录_术语表与学习资源", "附录 术语表与学习资源", 70, 74),
]

# 每章图片的说明（用 (xref, 页码) 识别）
IMG_CAPTIONS = {
    ("111", 13): "图 2-1 一根 K 线的结构：实体与影线",
    ("117", 15): "图 2-2 趋势：HH/HL 与 LH/LL 的高低点排列",
    ("120", 16): "图 2-3 支撑与阻力：多次测试与角色互换",
    ("123", 17): "图 2-4 实战演练：锤子线跌破支撑后快速拉回（sweep 雏形）",
    ("133", 21): "图 3-1 假突破：冲破前高后收回，扫掉追突破者",
    ("123", 22): "图 3-2 Pin Bar：锤子线（长影线 + 小实体）",
    ("138", 23): "图 3-3 看涨吞没：大阳线包住前一根小阴线",
    ("139", 23): "图 3-4 内包线：波动收缩，等待突破方向",
    ("150", 28): "图 4-1 趋势回调交易：入场 / 止损 / 目标",
    ("187", 41): "图 5-1 Wyckoff 吸筹结构：PS→SC→AR→ST→Spring→SOS→LPS",
}

# 标题识别
RE_CH_TITLE = re.compile(r"^第\s*\d+\s*章")
RE_SEC_TITLE = re.compile(r"^\d+\.\d+")
RE_OTHER_TITLE = re.compile(r"^(本章小结|全书收尾|附录|前言|章节地图|怎么读|一个提醒|免责|本手册)")
RE_ITEM = re.compile(r"^(\s*[-*•]\s+|\s*\d+[.、]\s*)")


def heading_level(line):
    """判断标题级别，非标题返回 None"""
    s = line.strip()
    if RE_CH_TITLE.match(s) or s.startswith("附录"):
        return 1
    if RE_SEC_TITLE.match(s) or RE_OTHER_TITLE.match(s):
        return 2
    return None


def clean_cjk_spaces(s):
    """去掉中文字符之间的空格（PDF 折行/表格残留）"""
    return re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", s)


def clean_cell(c):
    """表格单元格清理：换行转空格、转义竖线、去中文字符间空格"""
    return clean_cjk_spaces((c or "").strip().replace("|", "\\|").replace("\n", " "))


def is_para_end(line):
    """行尾是否代表段落自然结束（可终止折行合并）——只检查最后字符"""
    s = line.rstrip()
    if not s:
        return True
    return s[-1] in "。！？；：）)””』』』…" or s.endswith("——")


def merge_lines(lines):
    """合并中文硬折行；识别标题转 markdown 层级；保留列表项/短行；空行=段落分隔"""
    merged = []
    buf = ""

    def flush():
        nonlocal buf
        if buf:
            merged.append(buf)
            buf = ""

    for ln in lines:
        raw = ln.strip()
        lvl = heading_level(raw)
        if lvl:
            flush()
            merged.append("#" * (lvl + 1) + " " + raw)
            continue
        s = clean_cjk_spaces(raw)
        if not s:
            flush()
            continue
        if RE_ITEM.match(s):
            flush()
            buf = s  # 列表项暂存，等续行或下一轮 flush
            continue
        if buf and not is_para_end(buf):
            buf += s
        else:
            flush()
            buf = s
    flush()
    return merged


def blocks_to_markdown(page, tables, img_files=None):
    """把页面的文本块+表格+图片按 y 排序转成 markdown 行序列
    img_files: xref -> 实际保存的文件名（同一 xref 复用页面指向首次出现页的文件）
    """
    img_files = img_files or {}
    out = []
    # 收集文本块（跳过表格区域），行级收集；按 y 间隔检测段落分隔
    tb_rects = [t.bbox for t in tables] if tables else []
    blocks = []
    prev_y1 = None
    for b in page.get_text("blocks"):
        x0, y0, x1, y1, text = b[0], b[1], b[2], b[3], b[4]
        if not text.strip():
            continue
        in_table = any(x0 >= r[0] - 2 and y0 >= r[1] - 2 and x1 <= r[2] + 2 and y1 <= r[3] + 2 for r in tb_rects)
        if in_table:
            continue
        if prev_y1 is not None and (y0 - prev_y1) > 20:
            blocks.append((y0, "line", ""))  # 段落分隔标记
        prev_y1 = y1
        for line in text.splitlines():
            if line.strip():
                blocks.append((y0, "line", line.strip()))
    # 收集图片
    for img in page.get_images(full=True):
        xref = img[0]
        rects = page.get_image_rects(xref)
        if not rects:
            continue
        bbox = rects[0]
        fname = img_files.get(xref, f"fig_p{page.number + 1}_x{xref}.png")
        cap = IMG_CAPTIONS.get((str(xref), page.number + 1), f"图（第 {page.number + 1} 页）")
        blocks.append((bbox.y0, "image", f"![{cap}](images/{fname})\n\n*{cap}*"))
    # 收集表格
    for t in (tables or []):
        rows = t.extract()
        if rows:
            rows = [r for r in rows if any((c or "").strip() for c in r)]
            if not rows:
                continue
            ncol = max(len(r) for r in rows)
            header = rows[0] + [""] * (ncol - len(rows[0]))
            body = [r + [""] * (ncol - len(r)) for r in rows[1:]]
            md = ["| " + " | ".join(clean_cell(c) for c in header) + " |"]
            md.append("| " + " | ".join(["---"] * ncol) + " |")
            for r in body:
                md.append("| " + " | ".join(clean_cell(c) for c in r) + " |")
            blocks.append((t.bbox[1], "table", "\n".join(md)))
    blocks.sort(key=lambda x: x[0])
    out = []
    pending = []
    for _, kind, payload in blocks:
        if kind == "line":
            pending.append(payload)
        else:
            if pending:
                out.extend(merge_lines(pending))
                pending = []
            out.append(payload)
    if pending:
        out.extend(merge_lines(pending))
    return out


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    doc = pymupdf.open(PDF)
    # 提取所有图片（按出现页保存，同一 xref 只保存一次）
    extracted = {}
    for pno in range(doc.page_count):
        page = doc[pno]
        for xref, *_ in page.get_images(full=True):
            if xref in extracted:
                continue
            pix = pymupdf.Pixmap(doc, xref)
            if pix.colorspace and pix.colorspace.n > 3:
                pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
            fname = f"fig_p{pno + 1}_x{xref}.png"
            pix.save(os.path.join(IMG_DIR, fname))
            extracted[xref] = fname

    # 按章节输出
    index_lines = ["# 交易手册（Markdown 版）", "",
                   "> 由 `trading-handbook.pdf` 自动提取：按章节拆分、表格还原、图片引用。",
                   "> 本手册为学习笔记性质，不构成投资建议。所有规则请在模拟账户验证 100+ 笔、确认期望值为正后再实战。",
                   ""]
    for fname, title, p_start, p_end in CHAPTERS:
        lines = [f"# {title}", ""]
        for pno in range(p_start - 1, p_end):
            page = doc[pno]
            tables = page.find_tables().tables if page.find_tables() else []
            lines.extend(blocks_to_markdown(page, tables, extracted))
            lines.append("")
        # 清理重复空行
        cleaned = []
        blank = 0
        for ln in lines:
            if not ln.strip():
                blank += 1
                if blank > 1:
                    continue
            else:
                blank = 0
            cleaned.append(ln)
        md_path = os.path.join(OUT, fname + ".md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(cleaned).strip() + "\n")
        index_lines.append(f"- [{title}]({fname}.md)")
        print(f"已生成 {md_path}")
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(index_lines) + "\n")
    print(f"已生成索引 README.md，图片 {len(extracted)} 张")


if __name__ == "__main__":
    main()

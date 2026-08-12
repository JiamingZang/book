# -*- coding: utf-8 -*-
"""
把 handbook/ 全部 md 合并为单文件 HTML（trading-handbook.html）
- 顺序：00 前言 -> 01-10 章 -> 11 附录
- 图片引用保持 images/xxx.png（HTML 输出到 handbook/ 下，相对路径有效）
- 内置 CSS：中文字体、表格、图片自适应、引用块样式

运行：python _build_html.py
"""
import sys
import re
import markdown

sys.stdout.reconfigure(encoding="utf-8")

FILES = [
    "00_封面与前言.md",
    "01_第1章_市场是怎么运作的.md",
    "02_第2章_读懂价格行为.md",
    "03_第3章_入场信号.md",
    "04_第4章_交易系统.md",
    "05_第5章_聪明钱概念SMC.md",
    "06_第6章_仓位与风险.md",
    "07_第7章_执行与心态.md",
    "08_第8章_工具与验证.md",
    "09_第9章_Prop考核实战.md",
    "10_第10章_期权.md",
    "11_附录_术语表与学习资源.md",
]

CSS = """
:root { --teal:#26a69a; --down:#ef5350; --dark:#263238; --gray:#90a4ae; }
* { box-sizing: border-box; }
body {
  font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", sans-serif;
  color: #333; line-height: 1.75; margin: 0 auto; max-width: 900px;
  padding: 24px 28px 80px;
}
h1 { color: var(--dark); border-bottom: 3px solid var(--teal); padding-bottom: 8px; margin-top: 56px; font-size: 1.7em; }
h2 { color: var(--teal); margin-top: 40px; font-size: 1.35em; border-left: 4px solid var(--teal); padding-left: 10px; }
h3 { color: var(--dark); margin-top: 28px; font-size: 1.15em; }
h4 { color: #455a64; }
table { border-collapse: collapse; margin: 14px 0 20px; width: 100%; font-size: 0.95em; }
th { background: #e0f2f1; color: #00695c; }
th, td { border: 1px solid #cfd8dc; padding: 6px 10px; text-align: left; vertical-align: top; }
tr:nth-child(even) td { background: #f8fafa; }
img { max-width: 100%; height: auto; display: block; margin: 12px auto; border: 1px solid #eceff1; border-radius: 4px; }
blockquote {
  border-left: 4px solid var(--teal); background: #f1f8f7; margin: 14px 0;
  padding: 10px 14px; color: #37474f;
}
code { background: #eceff1; padding: 2px 5px; border-radius: 3px; font-size: 0.9em; }
pre { background: #263238; color: #eceff1; padding: 14px; border-radius: 6px; overflow-x: auto; }
pre code { background: none; color: inherit; padding: 0; }
strong { color: var(--dark); }
hr { border: none; border-top: 1px dashed #cfd8dc; margin: 28px 0; }
"""


def main():
    parts = []
    for f in FILES:
        with open(f"handbook/{f}", encoding="utf-8") as fh:
            md = fh.read()
        # 每个文件按 h1 分段；h1 之前若有标题行（如 README 式引用）也保留
        html = markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists"])
        # 把图片路径解析为相对路径（md 已用 images/xxx.png，保持原样即可）
        parts.append(html)
    body = "\n<hr/>\n".join(parts)
    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>交易手册：价格行为 · SMC · 仓位 · 心态 · Prop 考核</title>
<style>{CSS}</style>
</head>
<body>
{body}
<p style="margin-top:60px;color:#90a4ae;font-size:0.85em;text-align:center;">
本手册为学习笔记性质，不构成投资建议。所有规则请在模拟账户验证 100+ 笔、确认期望值为正后再实战。
</p>
</body>
</html>
"""
    with open("handbook/trading-handbook.html", "w", encoding="utf-8") as fh:
        fh.write(doc)
    print(f"ok: handbook/trading-handbook.html ({len(doc)//1024} KB)")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
把 handbook/ 全部 md 合并为单文件 HTML（trading-handbook.html）
- 顺序：00 前言 -> 01-10 章 -> 11 附录
- 图片引用保持 images/xxx.png（HTML 输出到 handbook/ 下，相对路径有效）
- 内置 CSS：中文字体、表格、图片自适应、引用块样式
- v2 新增阅读体验：自动目录（右侧悬浮 TOC + 滚动高亮）、顶部阅读进度条、返回顶部按钮

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
html { scroll-behavior: smooth; }
body {
  font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", sans-serif;
  color: #333; line-height: 1.75; margin: 0 auto; max-width: 900px;
  padding: 24px 28px 80px;
}
h1 { color: var(--dark); border-bottom: 3px solid var(--teal); padding-bottom: 8px; margin-top: 56px; font-size: 1.7em; }
h2 { color: var(--teal); margin-top: 40px; font-size: 1.35em; border-left: 4px solid var(--teal); padding-left: 10px; }
h3 { color: var(--dark); margin-top: 28px; font-size: 1.15em; }
h4 { color: #455a64; }
h1, h2, h3 { scroll-margin-top: 14px; }
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
/* ---- v2 阅读体验：进度条 / TOC / 返回顶部 ---- */
#progress { position: fixed; top: 0; left: 0; height: 3px; width: 0%;
  background: linear-gradient(90deg, var(--teal), #4db6ac); z-index: 1000; }
#toc {
  position: fixed; right: 16px; top: 50%; transform: translateY(-50%);
  width: 230px; max-height: 78vh; overflow-y: auto;
  background: rgba(255,255,255,0.96); border: 1px solid #e0e0e0; border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08); padding: 10px 8px; font-size: 0.82em;
  line-height: 1.5; display: none;
}
#toc b { display: block; color: var(--dark); font-size: 0.95em; margin-bottom: 6px;
  border-bottom: 1px solid #eceff1; padding-bottom: 6px; }
#toc a { display: block; color: #546e7a; text-decoration: none; padding: 2px 6px;
  border-radius: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
#toc a:hover { background: #e0f2f1; color: var(--teal); }
#toc a.lv2 { padding-left: 16px; }
#toc a.lv3 { padding-left: 30px; font-size: 0.92em; color: #78909c; }
#toc a.active { background: var(--teal); color: #fff; }
#toc a.h1 { font-weight: bold; color: var(--dark); }
#toc .tocclose { display: none; }
@media (min-width: 1380px) { #toc { display: block; } }
/* ---- v3 移动端：抽屉式目录 + 悬浮按钮 ---- */
#tocbtn {
  position: fixed; right: 16px; bottom: 76px; z-index: 1001; display: none;
  background: var(--teal); color: #fff; border: none; border-radius: 20px;
  padding: 9px 16px; font-size: 13px; cursor: pointer;
  box-shadow: 0 2px 10px rgba(0,0,0,0.28); font-family: inherit;
}
#tocbtn:hover { background: #00897b; }
@media (max-width: 1379px) {
  #tocbtn { display: block; }
  #toc {
    display: block; position: fixed; left: 0; top: 0; bottom: 0;
    width: 78%; max-width: 320px; max-height: 100vh; border-radius: 0 10px 10px 0;
    transform: translateX(-105%); transition: transform 0.25s ease;
    z-index: 1002; box-shadow: 2px 0 14px rgba(0,0,0,0.18);
  }
  #toc.open { transform: translateX(0); }
  #toc .tocclose {
    display: block; float: right; background: none; border: none;
    color: var(--gray); font-size: 16px; cursor: pointer; padding: 0 4px;
  }
}
#backtop {
  position: fixed; right: 20px; bottom: 24px; width: 40px; height: 40px;
  border-radius: 50%; background: var(--teal); color: #fff; border: none;
  font-size: 18px; cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,0.25);
  display: none; z-index: 1000; line-height: 40px; text-align: center;
}
#backtop:hover { background: #00897b; }
/* ---- 打印版式：隐藏悬浮组件，章节分页，防图/表跨页 ---- */
@media print {
  #toc, #progress, #backtop, #tocbtn { display: none !important; }
  body { max-width: none; padding: 0 6px; }
  h1 { page-break-before: always; }
  h1:first-of-type { page-break-before: avoid; }
  h2, h3 { page-break-after: avoid; }
  img, table, pre, blockquote { page-break-inside: avoid; }
  a { color: inherit; text-decoration: none; }
}
"""

JS = """
<script>
(function () {
  // 阅读进度条
  var bar = document.getElementById('progress');
  function onScroll() {
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
    // 返回顶部按钮
    document.getElementById('backtop').style.display = h.scrollTop > 600 ? 'block' : 'none';
    // TOC 滚动高亮
    var links = document.querySelectorAll('#toc a');
    var cur = null;
    for (var i = 0; i < links.length; i++) {
      var el = document.getElementById(links[i].getAttribute('data-id'));
      if (el && el.getBoundingClientRect().top <= 120) cur = links[i];
    }
    for (var j = 0; j < links.length; j++) {
      links[j].classList.toggle('active', links[j] === cur);
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  document.getElementById('backtop').addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
  // TOC 折叠：点击 lv1 展开/收起其下小节（默认收起）
  document.querySelectorAll('#toc a.lv1').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var hid = a.getAttribute('data-id');
      var show = !a.classList.contains('open');
      document.querySelectorAll('#toc a[data-parent="' + hid + '"]').forEach(function (ch) {
        ch.style.display = show ? 'block' : 'none';
      });
      a.classList.toggle('open', show);
      e.preventDefault();
      if (show) document.getElementById(hid).scrollIntoView({ behavior: 'smooth' });
    });
  });
  // v3 移动端：悬浮按钮开合抽屉；点链接或关闭钮收起
  var tocbtn = document.getElementById('tocbtn');
  var toc = document.getElementById('toc');
  if (tocbtn && toc) {
    tocbtn.addEventListener('click', function () { toc.classList.toggle('open'); });
    toc.querySelectorAll('a, .tocclose').forEach(function (el) {
      el.addEventListener('click', function () { toc.classList.remove('open'); });
    });
  }
})();
</script>
"""


def main():
    parts = []
    toc_entries = []  # (level, title, id, parent_id)
    sec = 0
    for f in FILES:
        with open(f"handbook/{f}", encoding="utf-8") as fh:
            md = fh.read()
        html = markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists"])
        # 给 h1/h2/h3 加锚点 id，并收集目录条目
        hstack = [None, None, None]  # 各级最近 id

        def tag(m):
            nonlocal sec
            level = int(m.group(1))
            inner = m.group(2)
            title = re.sub(r"<[^>]+>", "", inner).strip()
            title = re.sub(r"\s+", " ", title)
            hid = "sec-%d" % sec
            sec += 1
            # 父级 = 上一级最近非空 id
            parent = None
            for lv in range(level - 1, 0, -1):
                if hstack[lv - 1]:
                    parent = hstack[lv - 1]
                    break
            hstack[level - 1] = hid
            for lv in range(level, 3):
                hstack[lv] = None
            toc_entries.append((level, title, hid, parent))
            return '<h%d id="%s">%s</h%d>' % (level, hid, inner, level)

        html = re.sub(r"<h([123])>(.*?)</h\1>", tag, html, flags=re.S)
        parts.append(html)

    # 生成 TOC HTML（h1 默认展开，h2/h3 挂在 h1 下并默认折叠）
    toc_html = ['<div id="toc"><b>目录<button class="tocclose" title="收起">×</button></b>']
    for level, title, hid, parent in toc_entries:
        if level == 1:
            cls = "lv1 h1"
            parent_attr = ""
        else:
            cls = "lv%d" % level
            parent_attr = ' data-parent="%s"' % parent if parent else ""
            disp = "" if parent else ""
        toc_html.append(
            '<a class="%s" href="#%s" data-id="%s"%s>%s</a>'
            % (cls, hid, hid, parent_attr, title)
        )
    toc_html.append("</div>")

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
<div id="progress"></div>
{"".join(toc_html)}
<button id="backtop" title="返回顶部">↑</button>
<button id="tocbtn">☰ 目录</button>
{body}
<p style="margin-top:60px;color:#90a4ae;font-size:0.85em;text-align:center;">
本手册为学习笔记性质，不构成投资建议。所有规则请在模拟账户验证 100+ 笔、确认期望值为正后再实战。
</p>
{JS}
</body>
</html>
"""
    with open("handbook/trading-handbook.html", "w", encoding="utf-8") as fh:
        fh.write(doc)
    print(f"ok: handbook/trading-handbook.html ({len(doc)//1024} KB, TOC {len(toc_entries)} 项)")


if __name__ == "__main__":
    main()

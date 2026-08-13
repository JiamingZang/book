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
/* ElegantBook 风格：深藏青主色（参考 ai-agent-book 排版），红涨绿跌不变 */
:root { --navy:#1e3a6b; --navy2:#2c4a7c; --down:#ef5350; --up:#26a69a; --dark:#263238; --gray:#90a4ae; --accentbg:#f2f5fa; }
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", sans-serif;
  color: #333; line-height: 1.75; margin: 0 auto; max-width: 900px;
  padding: 24px 28px 80px;
}
a { color: var(--navy); }
/* ---- 封面（打印时独占一页） ---- */
#cover {
  background: linear-gradient(160deg, #0f2440 0%, #1e3a6b 55%, #2c4a7c 100%);
  color: #fff; border-radius: 12px; padding: 70px 44px 56px; text-align: center;
  margin: 8px 0 36px;
}
#cover .kicker { font-size: 0.95em; letter-spacing: 6px; color: #9db4d9; margin-bottom: 18px; }
#cover h1 { color: #fff; border: none; padding: 0; margin: 0 0 14px; font-size: 2.6em; letter-spacing: 8px; background: none; box-shadow: none; }
#cover .sub { font-size: 1.15em; color: #c9d8f0; letter-spacing: 2px; }
#cover .rule { width: 64px; height: 3px; background: #4db6ac; border-radius: 2px; margin: 26px auto; }
#cover .desc { max-width: 560px; margin: 0 auto 30px; color: #b9c8e2; font-size: 0.95em; line-height: 1.9; }
#cover .meta { font-size: 0.82em; color: #7f95b8; letter-spacing: 1px; }
#cover .startbtn {
  display: inline-block; margin-top: 8px; padding: 12px 34px;
  background: #4db6ac; color: #0f2440; border-radius: 24px;
  font-size: 1.02em; font-weight: 700; letter-spacing: 3px; text-decoration: none;
  box-shadow: 0 4px 14px rgba(0,0,0,0.25); transition: transform 0.15s;
}
#cover .startbtn:hover { transform: translateY(-2px); background: #66c4bb; }
/* 自测答案折叠按钮 */
button.ansbtn {
  display: inline-block; margin: 6px 0 14px; padding: 6px 18px;
  background: var(--accentbg); color: var(--navy); border: 1px solid var(--navy);
  border-radius: 16px; font-size: 0.9em; cursor: pointer; font-family: inherit;
}
button.ansbtn:hover { background: var(--navy); color: #fff; }
/* ---- 标题 ---- */
h1 {
  color: #fff; background: linear-gradient(135deg, var(--navy) 0%, var(--navy2) 100%);
  padding: 16px 22px; border-radius: 8px; margin-top: 56px; font-size: 1.6em;
  border: none; box-shadow: 0 2px 10px rgba(30,58,107,0.25);
}
h1.booktitle { display: none; }
h2 { color: var(--navy); margin-top: 40px; font-size: 1.32em; border-left: 4px solid var(--navy); padding-left: 10px; }
h3 { color: var(--dark); margin-top: 28px; font-size: 1.15em; }
h4 { color: #455a64; }
h1, h2, h3 { scroll-margin-top: 14px; }
h3.quizhead {
  background: var(--navy); color: #fff; display: inline-block;
  padding: 7px 18px; border-radius: 6px; font-size: 1.1em; margin-top: 36px;
}
h3.sumhead {
  background: var(--accentbg); color: var(--navy); border-left: 4px solid var(--navy);
  padding: 8px 14px; border-radius: 0 6px 6px 0;
}
/* ---- 表格 ---- */
table { border-collapse: collapse; margin: 14px 0 20px; width: 100%; font-size: 0.95em; }
th { background: var(--navy); color: #fff; }
th, td { border: 1px solid #c9d4e4; padding: 6px 10px; text-align: left; vertical-align: top; }
tr:nth-child(even) td { background: #f7f9fc; }
/* ---- 图片与图注 ---- */
img { max-width: 100%; height: auto; display: block; margin: 12px auto; border: 1px solid #e3e9f2; border-radius: 4px; }
p.figcap { text-align: center; font-weight: 600; color: #455a64; font-size: 0.95em; margin: -4px 0 20px; }
/* ---- 引用块：深藏青左条（参考书 quote 样式） ---- */
blockquote {
  border-left: 3px solid var(--navy); background: var(--accentbg); margin: 14px 0;
  padding: 10px 14px; color: #37474f;
}
/* ---- 代码：浅灰底 + 深藏青左条（参考书 codebox） ---- */
code { background: #eef1f6; padding: 2px 5px; border-radius: 3px; font-size: 0.9em; color: #1e3a6b; }
pre {
  background: #f7f9fc; color: #263238; padding: 14px 16px; border-radius: 6px;
  overflow-x: auto; border: 1px solid #d8e0ec; border-left: 4px solid var(--navy);
}
pre code { background: none; color: inherit; padding: 0; }
strong { color: var(--dark); }
hr { border: none; border-top: 1px dashed #c9d4e4; margin: 28px 0; }
/* ---- v2 阅读体验：进度条 / TOC / 返回顶部 ---- */
#progress { position: fixed; top: 0; left: 0; height: 3px; width: 0%;
  background: linear-gradient(90deg, var(--navy), #4db6ac); z-index: 1000; }
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
#toc a:hover { background: var(--accentbg); color: var(--navy); }
#toc a.lv2 { padding-left: 16px; }
#toc a.lv3 { padding-left: 30px; font-size: 0.92em; color: #78909c; }
#toc a.active { background: var(--navy); color: #fff; }
#toc a.h1 { font-weight: bold; color: var(--dark); }
#toc .tocclose { display: none; }
@media (min-width: 1380px) { #toc { display: block; } }
/* ---- v3 移动端：抽屉式目录 + 悬浮按钮 ---- */
#tocbtn {
  position: fixed; right: 16px; bottom: 76px; z-index: 1001; display: none;
  background: var(--navy); color: #fff; border: none; border-radius: 20px;
  padding: 9px 16px; font-size: 13px; cursor: pointer;
  box-shadow: 0 2px 10px rgba(0,0,0,0.28); font-family: inherit;
}
#tocbtn:hover { background: var(--navy2); }
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
  border-radius: 50%; background: var(--navy); color: #fff; border: none;
  font-size: 18px; cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,0.25);
  display: none; z-index: 1000; line-height: 40px; text-align: center;
}
#backtop:hover { background: var(--navy2); }
/* ---- 打印版式：隐藏悬浮组件，封面/章节分页，防图/表跨页，段首缩进 ---- */
@media print {
  * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  @page :first { margin: 0; }
  #toc, #progress, #backtop, #tocbtn, button.ansbtn { display: none !important; }
  #cover .startbtn { display: none; }
  .ansbody { display: block !important; }
  body { max-width: none; padding: 0 6px; }
  #cover {
    border-radius: 0; margin: 0; padding: 90px 40px 40px; height: 88vh;
    page-break-after: always;
  }
  h1 { page-break-before: always; border-radius: 4px; }
  h1.booktitle { page-break-before: avoid; }
  #cover h1 { page-break-before: avoid; }
  h2, h3 { page-break-after: avoid; }
  img, table, pre, blockquote { page-break-inside: avoid; }
  a { color: inherit; text-decoration: none; }
  p { text-indent: 2em; }
  p.figcap, li p, td p, blockquote p { text-indent: 0; }
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
  // 图注：斜体且以“图 N-”/“表 N-”开头 → 父 <p> 加 figcap 类（居中加粗）
  document.querySelectorAll('p em').forEach(function (em) {
    if (/^(图|表)\\s*\\d/.test(em.textContent.trim())) {
      em.parentElement.classList.add('figcap');
    }
  });
  // 图注锚点：从图注文本解析“图 N-M(R)”→ id="fig-N-M(R)"
  var figids = {};
  document.querySelectorAll('p.figcap').forEach(function (p) {
    var m = /^(图)\\s*(\\d+-\\d+R?)/.exec(p.textContent.trim());
    if (m) {
      p.id = 'fig-' + m[2];
      figids[p.id] = true;
    }
  });
  // 正文“图 N-M”引用链接化：文本节点替换为 <a href="#fig-...">（仅当锚点存在）
  if (Object.keys(figids).length) {
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        var p = n.parentNode;
        if (p && p.classList && (p.classList.contains('figcap') || p.tagName === 'A')) {
          return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var tnodes = [];
    while (walker.nextNode()) tnodes.push(walker.currentNode);
    tnodes.forEach(function (n) {
      var t = n.nodeValue;
      var re = /(图)\\s*(\\d+-\\d+R?)/g;
      var out = [];
      var last = 0, m, changed = false;
      while ((m = re.exec(t)) !== null) {
        var key = 'fig-' + m[2];
        if (!figids[key]) continue;
        if (m.index > last) out.push(t.slice(last, m.index));
        var a = document.createElement('a');
        a.href = '#' + key;
        a.textContent = m[0];
        out.push(a);
        last = m.index + m[0].length;
        changed = true;
      }
      if (!changed) return;
      if (last < t.length) out.push(t.slice(last));
      var frag = document.createDocumentFragment();
      out.forEach(function (x) { frag.appendChild(typeof x === 'string' ? document.createTextNode(x) : x); });
      n.parentNode.replaceChild(frag, n);
    });
  }
  // 自测答案折叠：quizhead 后第一个含“答案”的段默认收起，按钮展开/收起
  document.querySelectorAll('h3.quizhead').forEach(function (q) {
    var el = q.nextElementSibling;
    while (el && el.tagName !== 'H3') {
      if (el.tagName === 'P' && el.querySelector('strong') &&
          el.querySelector('strong').textContent.indexOf('答案') !== -1) {
        el.classList.add('ansbody');
        el.style.display = 'none';
        var btn = document.createElement('button');
        btn.className = 'ansbtn';
        btn.textContent = '显示答案';
        el.parentNode.insertBefore(btn, el);
        btn.addEventListener('click', function () {
          var show = el.style.display === 'none';
          el.style.display = show ? 'block' : 'none';
          btn.textContent = show ? '收起答案' : '显示答案';
        });
        break;
      }
      el = el.nextElementSibling;
    }
  });
  // 封面“开始阅读”：滚动到隐藏书名 h1 之后的第一个标题
  var bt = document.querySelector('#cover .startbtn');
  if (bt) {
    bt.addEventListener('click', function (e) {
      e.preventDefault();
      var h = document.querySelector('h1.booktitle');
      var target = h ? h.nextElementSibling : null;
      while (target && target.tagName !== 'H1' && target.tagName !== 'H2' && target.tagName !== 'H3') {
        target = target.nextElementSibling;
      }
      if (target && target.id) document.getElementById(target.id).scrollIntoView({ behavior: 'smooth' });
    });
  }
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
    first_h1 = [False]  # 第一个 h1 隐藏（书名由封面块承担）
    for f in FILES:
        with open(f"handbook/{f}", encoding="utf-8") as fh:
            md = fh.read()
        html = markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists"])
        # 图注统一：alt 文本中的"图 N-M ..."提取为图片下方可见图注；
        # 若图片后紧跟重复的斜体图注（早期双写格式）则删除，避免显示两次。
        # 先闭合外层 p 再开新 p 包 img，兼容图片夹在段落中间的情况
        html = re.sub(
            r'<img alt="(图\s*\d+[-.]\d+R?[^"]*)" src="([^"]+)"\s*/?>',
            lambda m: '</p><p><img src="%s" alt="%s"></p><p class="figcap">%s</p>'
            % (m.group(2), m.group(1), m.group(1)),
            html,
        )
        html = re.sub(
            r'<p class="figcap">(图\s*\d+[-.]\d+R?[^<]*)</p>\s*<p><em>图\s*\d+[-.]\d+R?[^<]*</em></p>',
            r'<p class="figcap">\1</p>',
            html,
        )
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
            # 样式 class：第一个 h1 作封面书名（隐藏，锚点保留）/
            # 自测题标题 / 小结标题（ElegantBook 风格）
            cls = ""
            if level == 1 and not first_h1[0]:
                cls = ' class="booktitle"'
                first_h1[0] = True
            elif "自测" in title:
                cls = ' class="quizhead"'
            elif "小结" in title:
                cls = ' class="sumhead"'
            return '<h%d id="%s"%s>%s</h%d>' % (level, hid, cls, inner, level)

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
<div id="cover">
  <div class="kicker">交易 · 投资 · 通识</div>
  <h1>交易手册</h1>
  <div class="sub">价格行为 · SMC · 仓位 · 心态 · Prop 考核</div>
  <div class="rule"></div>
  <div class="desc">一套可验证、可重复、能控制风险的交易方法论。<br>
  市场基础 → 价格行为 → 信号 → 系统 → SMC → 仓位 → 心态 → 验证 → 应用</div>
  <a class="startbtn" href="#">开 始 阅 读</a>
  <div class="meta">学习笔记 · 非出版物 · 不构成投资建议</div>
</div>
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

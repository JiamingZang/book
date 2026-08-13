"""为 trading-handbook.pdf 添加书签目录（章节导航）"""
import pymupdf, re, os

MD_DIR = r"c:\Users\18315\Desktop\新建文件夹\handbook"
PDF = os.path.join(MD_DIR, "trading-handbook.pdf")

# 1. 从 md 提取标题
titles = []  # (level, title)
for fname in sorted(os.listdir(MD_DIR)):
    if not re.match(r"\d{2}_.+\.md$", fname):
        continue
    with open(os.path.join(MD_DIR, fname), encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"^(#{1,3}) (.+)$", line.rstrip())
            if not m:
                continue
            level = len(m.group(1))
            title = m.group(2)
            # 清理 markdown 内联标记
            title = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", title)
            title = title.replace("**", "").replace("*", "").replace("`", "")
            title = title.strip()
            if title:
                titles.append((level, title))

# 2. 统计重复标题（TOC 区会重复渲染，正文第 i 次出现 = 总匹配第 N+i 个）
from collections import Counter, defaultdict
cnt = Counter(t for _, t in titles)
seen = defaultdict(int)

# 3. 定位页面
doc = pymupdf.open(PDF)
pages = [p.get_text() for p in doc]
toc, missed = [], []
for level, title in titles:
    seen[title] += 1
    order = seen[title]
    found = None
    for cut in (22, 14, 8):
        q = title[:cut].strip()
        if len(q) < 2:
            continue
        matches = []
        if len(q) <= 6:  # 短标题用整行匹配，避免正文引用误匹配
            for i, txt in enumerate(pages):
                if any(line.strip() == q for line in txt.split("\n")):
                    matches.append(i + 1)
        else:
            matches = [i + 1 for i, txt in enumerate(pages) if q in txt]
        if matches:
            idx = cnt[title] + order - 1  # 跳过 TOC 区的 N 次重复
            found = matches[idx] if idx < len(matches) else matches[-1]
            break
    if found:
        toc.append((level, title[:60], found))
    else:
        missed.append((level, title))

# 4. 层级连续化（titles 顺序 = md 顺序 = 页面顺序，章标题重置 cur）
cur = 0
norm = []
for level, title, page in toc:
    if level == 1:
        cur = 1
    elif level > cur + 1:
        level = cur + 1
        cur = max(cur, level)
    else:
        cur = max(cur, level)
    norm.append((level, title, page))
print(f"toc 前5条: {norm[:5]}")
print(f"toc 层级分布: {sorted(set(l for l, _, _ in norm))}")
doc.set_toc(norm)
doc.save(PDF, incremental=True, encryption=pymupdf.PDF_ENCRYPT_KEEP)
doc.close()
print(f"总标题: {len(titles)}  书签写入: {len(toc)}  未定位: {len(missed)}")
for lv, t in missed[:20]:
    print(f"  未定位[{lv}] {t[:50]}")

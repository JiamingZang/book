# -*- coding: utf-8 -*-
"""图号重编号 v2：使每章合成图编号与正文出现顺序一致（修复后续批次插入导致的乱序）。
规则：
- 只重排合成图（无 R 后缀），按图片行出现顺序编号 1..N
- 真实数据图（X-YR）保持原编号不变，不参与编号分配
- 正文叙述引用同步替换；"图 X-YR" 整体不碰（负向断言）
只改 md 中的 "图 X-Y" 文本，图片文件名不变。"""
import re
import glob

FILES = sorted(glob.glob("handbook/0*.md") + glob.glob("handbook/10_*.md"))

# 阶段 1：收集全部图片行顺序（按行本身是否带 R 后缀判定真实图）
order = {}   # ch -> [(old, is_real), ...]
for f in FILES:
    t = open(f, encoding="utf-8").read()
    for m in re.finditer(r"^!\[图 (\d+)-(\d+)(R)?", t, re.M):
        ch, old = int(m.group(1)), int(m.group(2))
        is_real = bool(m.group(3))
        order.setdefault(ch, []).append((old, is_real))

# 阶段 2：合成图 old -> new 映射（按出现顺序 1..N，同号重复保留第一位置）
mapping = {}
for ch, olds in order.items():
    seen = []
    for old, is_real in olds:
        if is_real:
            continue
        if old in seen:
            continue
        seen.append(old)
        mapping[(ch, old)] = len(seen)

# 阶段 3：全局替换（负向断言排除 "图 X-YR"）
def repl(m):
    ch, old = int(m.group(1)), int(m.group(2))
    new = mapping.get((ch, old))
    return "图 %d-%d" % (ch, new) if new else m.group(0)

for f in FILES:
    t = open(f, encoding="utf-8").read()
    t2 = re.sub(r"图 (\d+)-(\d+)(?!R)", repl, t)
    if t2 != t:
        open(f, "w", encoding="utf-8", newline="\n").write(t2)
        print("更新", f)

# 阶段 4：报告每章变更
for ch, olds in sorted(order.items()):
    changed = []
    for old, is_real in olds:
        new = mapping.get((ch, old))
        if new and new != old and not is_real:
            changed.append((old, new))
    uniq = []
    for pair in changed:
        if pair not in uniq:
            uniq.append(pair)
    if uniq:
        print("第%d章: %s" % (ch, ", ".join("图%d-%d→图%d-%d" % (ch, o, ch, n) for o, n in uniq)))
    if ch in [c for c, _ in order.items() if any(r for _, r in order[c])]:
        reals = sorted(set(o for o, r in order[ch] if r))
        print("  真实图保持: %s" % ", ".join("图%d-%dR" % (ch, o) for o in reals))

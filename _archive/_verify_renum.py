# -*- coding: utf-8 -*-
"""验证重编号：对比 git HEAD 与工作区的每章图片行顺序，输出报告文件"""
import re
import glob
import subprocess

FILES = sorted(glob.glob("handbook/0*.md") + glob.glob("handbook/10_*.md"))
out = []

for f in FILES:
    name = f.split("\\")[-1]
    # git 版本（字节级，避免编码问题）
    p = subprocess.run(["git", "show", "HEAD:" + f.replace("\\", "/")],
                       capture_output=True)
    old_t = p.stdout.decode("utf-8", errors="replace")
    new_t = open(f, encoding="utf-8").read()

    def img_lines(t):
        return re.findall(r"^!\[图 (\d+-\d+R?)", t, re.M)

    old_imgs = img_lines(old_t)
    new_imgs = img_lines(new_t)
    out.append("=" * 60)
    out.append(name)
    out.append("旧顺序(HEAD): " + ", ".join(old_imgs))
    out.append("新顺序(工作区): " + ", ".join(new_imgs))
    # 检查新顺序异常：纯数字合成图应连续
    seq = []
    for s in new_imgs:
        if not s.endswith("R"):
            seq.append(int(s.split("-")[1]))
    if seq:
        dup = [n for n in set(seq) if seq.count(n) > 1]
        miss = [n for n in range(1, max(seq) + 1) if n not in seq]
        if dup or miss:
            out.append("  !!! 合成图异常 重复:%s 缺失:%s" % (dup, miss))
    # 检查叙述引用是否还有旧号（对比旧图号集合）
    old_nums = set()
    for m in re.finditer(r"图 (\d+)-(\d+)", old_t):
        if int(m.group(1)) == int(old_imgs[0].split("-")[0]) if old_imgs else False:
            old_nums.add(int(m.group(2)))
    new_nums = set()
    for m in re.finditer(r"图 (\d+)-(\d+)", new_t):
        if old_imgs and int(m.group(1)) == int(old_imgs[0].split("-")[0]):
            new_nums.add(int(m.group(2)))
    stale = [n for n in sorted(old_nums - new_nums) if n >= 1]
    if stale:
        out.append("  疑似残留旧引用(HEAD有而工作区无的纯数字): %s" % stale)

open("_verify_renum_out.txt", "w", encoding="utf-8").write("\n".join(out))
print("written")

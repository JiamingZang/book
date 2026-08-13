import glob
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

# 1) 每章图片引用数、斜体图注数、R图数
for f in sorted(glob.glob("handbook/*.md")):
    t = open(f, encoding="utf-8").read()
    imgs = re.findall(r"!\[([^\]]*)\]\(images/([^)]+)\)", t)
    ital = len(re.findall(r"^\*图 ", t, re.M))
    rfigs = [m[1] for m in imgs if "R" in m[1].split(".")[0][-3:] or "-R" in m[1]]
    print(
        "%-28s 图引用=%-3d 斜体图注=%-3d R图=%s"
        % (f.split("_")[-1][:16], len(imgs), ital, len(rfigs))
    )

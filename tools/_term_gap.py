# -*- coding: utf-8 -*-
"""正文高频英文术语 vs 术语表覆盖审计"""
import re, glob
from collections import Counter

STOP = set("""the of and to a in is for on with as by at from or an be this that are it not but was will you we your
have has been can all when which its more than into out over also if then so about like just what how may only same
there each after before most very other some these those should would could does do did done going want need know
make made get got use used using way still even because where while during between within without through under
against both each day week month year time market price action trade trading trader risk account order entry exit
stop loss target system setup signal bar chart trend range breakout pullback support resistance level high low open
close volume money make take give put back down up off one two three four five six seven eight nine ten their them
there's don't can't won't it's i'm you're that's this is are was were has have had been being""".split())

def main():
    body = ""
    for f in sorted(glob.glob("handbook/0*.md") + glob.glob("handbook/1*.md")):
        body += open(f, encoding="utf-8").read() + "\n"

    gloss = open("handbook/11_appendix_glossary.md", encoding="utf-8").read()

    # 正文中的英文单词/术语（含大小写、点号、连字符）
    words = re.findall(r"[A-Za-z][A-Za-z\-\.]{2,}", body)
    cnt = Counter(w for w in words if w.lower() not in STOP and not w.endswith("."))

    # 术语表覆盖：把术语表全部文本拆成词集合
    gloss_words = set(re.findall(r"[A-Za-z][A-Za-z\-\.]{2,}", gloss))

    out = ["== 高频英文术语未在术语表出现 =="]
    n = 0
    for w, c in cnt.most_common(400):
        if c < 6:
            break
        base = w.lower()
        if base in gloss_words or w in gloss_words or base.rstrip("s") in gloss_words:
            continue
        out.append(f"{w} ×{c}")
        n += 1
        if n >= 45:
            break
    print("\n".join(out))

if __name__ == "__main__":
    main()

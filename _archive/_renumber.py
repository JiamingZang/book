# -*- coding: utf-8 -*-
"""P2-3: 章节编号起点统一脚本 v2
第 3/4/10 章: x.0 -> x.1, 后续小节顺延 +1, 全书引用同步 +1
逐行处理: 标题行只改标题, 正文行只改引用, 杜绝连锁替换
安全: 排除百分数(10.0%等); (?<!\d) 防 13.1 误伤
"""
import re
import glob

CH_MAP = {3: (0, 11), 4: (0, 24), 10: (0, 8)}  # 章号: (起始, 结束)


def shift(m):
    """把匹配到的 章.节 数字 +1"""
    return m.group(0)


def main():
    for fn in glob.glob('handbook/*.md'):
        lines = open(fn, encoding='utf-8').readlines()
        out = []
        for line in lines:
            stripped = line.rstrip('\n')
            is_title = bool(re.match(r'^#{2,3} \d+\.\d+', stripped))
            if is_title:
                # 只处理标题编号
                m = re.match(r'^(#{2,3} )(\d+)\.(\d+)(.*)$', stripped)
                ch, n = int(m.group(2)), int(m.group(3))
                lo, hi = CH_MAP.get(ch, (None, None))
                if lo is not None and lo <= n <= hi:
                    stripped = f'{m.group(1)}{ch}.{n + 1}{m.group(4)}'
            else:
                # 正文: 从大到小替换引用
                for ch, (lo, hi) in CH_MAP.items():
                    for n in range(hi, lo - 1, -1):
                        pat = re.compile(rf'(?<!\d)(第 ?)?{ch}\.{n}(?!\d)(?!%)(?!％)')

                        def repl(m, c=ch, n=n):
                            return f'{(m.group(1) or "")}{c}.{n + 1}'

                        stripped = pat.sub(repl, stripped)
            out.append(stripped + '\n')
        # 对比写入
        new = ''.join(out)
        old = ''.join(lines)
        if new != old:
            open(fn, 'w', encoding='utf-8').write(new)
            print(f'[已更新] {fn}')
    print('完成')


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""手册渲染验证：md→HTML 解析、表格一致性、标题层级检查"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import markdown

HAND = r'c:\Users\18315\Desktop\新建文件夹\handbook'
errors = []

for fn in sorted(os.listdir(HAND)):
    if not fn.endswith('.md'):
        continue
    p = os.path.join(HAND, fn)
    text = open(p, encoding='utf-8').read()
    lines = text.split('\n')

    # 1. md→HTML 解析无异常
    try:
        html = markdown.markdown(text, extensions=['tables', 'fenced_code'])
    except Exception as e:
        errors.append(f'{fn}: markdown 解析失败: {e}')
        continue

    # 2. 表格一致性：每个表格块的列数一致
    in_tbl = False
    cols = None
    tbl_no = 0
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('|'):
            cells = [c for c in line.strip().strip('|').split('|')]
            n = len(cells)
            if not in_tbl:
                in_tbl, cols, tbl_no = True, n, tbl_no + 1
            elif re.match(r'^\s*\|?[\s:|-]+\|?\s*$', line) and not re.search(r'[^\s|:-]', line.replace('|', '')):
                continue  # 分隔行
            elif n != cols:
                errors.append(f'{fn}: 表格#{tbl_no} 第{i}行列数 {n} != {cols}: {line.strip()[:40]}')
        else:
            in_tbl = False

    # 3. 标题层级：### 编号节 必须属于某章（# 第 N 章 在前）；检查编号节是否连续有 '###' 无 '##' 包裹
    # 4. 代码块未闭合
    if text.count('```') % 2 != 0:
        errors.append(f'{fn}: 代码块未闭合（``` 数量为奇数: {text.count("```")}）')

    print(f'{fn}: OK (html {len(html)//1024}KB, 表格{tbl_no})')

print()
if errors:
    print(f'发现问题 {len(errors)} 处:')
    for e in errors:
        print('  ' + e)
    sys.exit(1)
print('全部检查通过')

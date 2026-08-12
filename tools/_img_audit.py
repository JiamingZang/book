# -*- coding: utf-8 -*-
"""图片引用完整性审计：md 中引用的 images/ 图片是否真实存在"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HAND = r'c:\Users\18315\Desktop\新建文件夹\handbook'
IMG = os.path.join(HAND, 'images')
if not os.path.isdir(IMG):
    print('images 目录不存在')
    sys.exit(1)

actual = {f for f in os.listdir(IMG) if f.lower().endswith('.png')}
pat = re.compile(r'!\[[^\]]*\]\((images/[^)]+)\)')

refs, missing = set(), []
for fn in sorted(os.listdir(HAND)):
    if not fn.endswith('.md'):
        continue
    p = os.path.join(HAND, fn)
    for i, line in enumerate(open(p, encoding='utf-8'), 1):
        for m in pat.finditer(line):
            rel = m.group(1).replace('\\', '/')
            name = os.path.basename(rel)
            refs.add(name)
            if name not in actual:
                missing.append((fn, i, name))

unused = actual - refs
print(f'引用图片数: {len(refs)}  实际文件数: {len(actual)}')
print(f'缺失(引用但无文件): {len(missing)}')
for fn, i, name in missing:
    print(f'  {fn}:{i} -> {name}')
print(f'未使用(有文件但无引用): {len(unused)}')
for name in sorted(unused):
    print(f'  {name}')

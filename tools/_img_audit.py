# -*- coding: utf-8 -*-
"""图片引用完整性审计：md 中引用的 images/ 图片是否真实存在
v51：兼容 Excalidraw 引用 `![[fig_x.excalidraw]]`——检查 .excalidraw 文件存在；
同名 .png（HTML/PDF 流水线用）视为被 .excalidraw 覆盖，不报未使用
"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HAND = r'c:\Users\18315\Desktop\新建文件夹\handbook'
IMG = os.path.join(HAND, 'images')
if not os.path.isdir(IMG):
    print('images 目录不存在')
    sys.exit(1)

actual = {f for f in os.listdir(IMG) if f.lower().endswith(('.png', '.excalidraw'))}
pat = re.compile(r'!\[[^\]]*\]\((images/[^)]+)\)|!\[\[(fig_[a-z0-9_]+)\.excalidraw\]\]')

refs, missing = set(), []
for fn in sorted(os.listdir(HAND)):
    if not fn.endswith('.md'):
        continue
    p = os.path.join(HAND, fn)
    for i, line in enumerate(open(p, encoding='utf-8'), 1):
        for m in pat.finditer(line):
            if m.group(1):
                name = os.path.basename(m.group(1).replace('\\', '/'))
            else:
                name = m.group(2) + '.excalidraw'
            refs.add(name)
            if name not in actual:
                missing.append((fn, i, name))

# 未使用：排除「同名 .excalidraw 被引用」的 png
used_ex = {n[:-11] for n in refs if n.endswith('.excalidraw')}
unused = {f for f in actual - refs
          if not (f.endswith('.png') and f[:-4] in used_ex)}

print(f'引用图片数: {len(refs)}  实际文件数: {len(actual)}')
print(f'缺失(引用但无文件): {len(missing)}')
for fn, i, name in missing:
    print(f'  {fn}:{i} -> {name}')
print(f'未使用(有文件但无引用): {len(unused)}')
for name in sorted(unused):
    print(f'  {name}')

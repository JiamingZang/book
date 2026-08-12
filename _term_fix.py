# -*- coding: utf-8 -*-
"""B1: 术语统一——替换裸用英文术语"""
import io
import sys
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. 04章 Barbwire 裸用 -> 铁丝网
fn = 'handbook/04_第4章_交易系统.md'
txt = open(fn, encoding='utf-8').read()
reps = [
    ('= Barbwire（不交易，等突破）', '= 铁丝网（不交易，等突破）'),
    ('**Barbwire 优先于 CV**', '**铁丝网优先于 CV**'),
    ('低密度区的 Barbwire 的处理', '低密度区的铁丝网的处理'),
    ('Barbwire 不用边界', '铁丝网不用边界'),
    ('25% Barbwire 不交易', '25% 铁丝网不交易'),
    ('| 铁丝网 | Barbwire |', '| 铁丝网（Barbwire） |'),
]
for a, b in reps:
    if a in txt:
        txt = txt.replace(a, b)
        print('OK:', a[:30])
    else:
        print('MISS:', a[:30])
open(fn, 'w', encoding='utf-8').write(txt)

# 2. 02章 spike 括注规范化
fn2 = 'handbook/02_第2章_读懂价格行为.md'
t2 = open(fn2, encoding='utf-8').read()
a = '这是"突破波动"（spike），市场所有权最有力的宣告'
b = '这是"突破波动"（尖峰，Spike），市场所有权最有力的宣告'
if a in t2:
    t2 = t2.replace(a, b)
    print('02章 spike 括注 OK')
else:
    print('02章 spike MISS')
open(fn2, 'w', encoding='utf-8').write(t2)

# 3. always-in 形式检查
print('--- always-in 形式 ---')
for fn in ['handbook/02_第2章_读懂价格行为.md', 'handbook/04_第4章_交易系统.md']:
    for i, l in enumerate(open(fn, encoding='utf-8').readlines(), 1):
        if re.search(r'[Aa]lways-?[Ii]n', l):
            print(f'{fn.split(chr(92))[-1]}:{i}: {l.strip()[:60]}')

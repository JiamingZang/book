# -*- coding: utf-8 -*-
"""B2: 来源标注统一为短标（方案A）
规则: 确定性模式自动替换, 复杂模式留待人工审查
短标对照: Ali=Ali闪卡, 突破=Ali突破白皮书, PA-N=PA_Agent文件N, 诊断=市场诊断框架
"""
import io
import sys
import re
import glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

REPLACEMENTS = [
    # ---- 纯来源标注 ----
    ('（Ali 闪卡第 2 部分）', '（Ali）'),
    ('（Ali 闪卡补充）', '（Ali 补充）'),
    ('（Ali 闪卡量化）', '（Ali）'),
    ('（Ali 闪卡）', '（Ali）'),
    ('（Ali 突破白皮书 Rev+FT）', '（突破 Rev+FT）'),
    ('（Ali 突破白皮书统计）', '（突破统计）'),
    ('（Ali 突破白皮书）', '（突破）'),
    ('（市场诊断框架）', '（诊断）'),
    ('（PA_Agent 文件 25）', '（PA-25）'),
    ('（PA_Agent 文件 23）', '（PA-23）'),
    ('（PA_Agent 文件 18）', '（PA-18）'),
    ('（PA_Agent 文件 19）', '（PA-19）'),
    ('（PA_Agent 文件 15）', '（PA-15）'),
    ('（PA_Agent 文件 14）', '（PA-14）'),
    ('（文件 14）', '（PA-14）'),
    ('（Brooks 规则库，PA_Agent 文件 18）', '（Brooks 规则库，PA-18）'),
    # ---- 混合: 术语 + 来源 ----
    ('（Give-up Bar，Ali 闪卡）', '（Give-up Bar，Ali）'),
    ('（Cup & Handle，Ali 闪卡）', '（Cup & Handle，Ali）'),
    ('（4 tick 窗口，Ali 闪卡）', '（4 tick 窗口，Ali）'),
    ('（Breakout Mode，Ali 闪卡）', '（Breakout Mode，Ali）'),
    ('（BOG，Ali 闪卡）', '（BOG，Ali）'),
    ('（COTC，Ali 闪卡）', '（COTC，Ali）'),
    ('（Urgency，Ali 闪卡）', '（Urgency，Ali）'),
    ('（Spike & Channel，Ali 闪卡）', '（Spike & Channel，Ali）'),
    ('（Spike & Climax，Ali 闪卡）', '（Spike & Climax，Ali）'),
    ('（基于百分比和回调势头，Ali 闪卡）', '（基于百分比和回调势头，Ali）'),
    ('（或小 FTW，Ali 闪卡）', '（或小 FTW，Ali）'),
    ('（Ali 闪卡，可交易的回调模板）', '（Ali：可交易的回调模板）'),
    ('（Ali 闪卡，H1/H2 反转 K 线）', '（Ali：H1/H2 反转 K 线）'),
    ('（Ali 闪卡，ES 日内常用）', '（Ali：ES 日内常用）'),
    ('（Ali 闪卡，时间管理）', '（Ali：时间管理）'),
    ('（Ali 闪卡，4 个特征）', '（Ali：4 个特征）'),
    ('（Ali 闪卡）**', '（Ali）**'),
]

total = 0
for fn in glob.glob('handbook/*.md'):
    txt = open(fn, encoding='utf-8').read()
    orig = txt
    for a, b in REPLACEMENTS:
        if a in txt:
            txt = txt.replace(a, b)
    if txt != orig:
        open(fn, 'w', encoding='utf-8').write(txt)
        total += 1
        print(f'[已更新] {fn}')
print(f'更新文件数: {total}')

# 剩余检查
print('--- 剩余 Ali 闪卡 ---')
for fn in glob.glob('handbook/*.md'):
    for i, l in enumerate(open(fn, encoding='utf-8').readlines(), 1):
        if 'Ali 闪卡' in l:
            print(f'  {fn.split(chr(92))[-1]}:{i}: {l.strip()[:80]}')

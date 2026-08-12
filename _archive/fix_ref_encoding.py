# -*- coding: utf-8 -*-
"""将 _ref_texts 中提取的文本转存为简单文件名（修复 PowerShell 管道编码问题）"""
import pathlib

d = pathlib.Path(r"c:\Users\18315\Desktop\新建文件夹\_ref_texts")
out = pathlib.Path(r"c:\Users\18315\Desktop\新建文件夹\_ref_clean")
out.mkdir(exist_ok=True)

mapping = {
    "micro_base": "高概率微通道交易系统基础，值得反复学习",
    "micro_core": "高概率微通道交易系统核心",
    "rose": "Rose的策略",
    "grandma": "GRANDMA策略-Rose",
    "top10": "阿布10种最佳价格行为交易模式",
    "breakout_wp": "突破白皮书研究",
    "breakout_next": "突破做单后续",
    "wyckoff2": "威科夫2_0",
    "pa_notes": "PA学习笔记",
    "howto_manual": "How to trade price a",
    "ross_hook": "洛氏霍克交易法",
    "leishen": "2025雷神导师计划",
}

for key, keyword in mapping.items():
    for f in d.iterdir():
        if keyword in f.name:
            data = f.read_bytes()
            # 尝试 utf-8，失败则尝试 gbk
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                text = data.decode("gbk", errors="replace")
            (out / (key + ".txt")).write_text(text, encoding="utf-8")
            print(key, "->", len(text), "chars")
            break
print("done")

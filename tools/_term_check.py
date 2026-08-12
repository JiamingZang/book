# -*- coding: utf-8 -*-
t = open("handbook/11_附录_术语表与学习资源.md", encoding="utf-8").read()
terms = ["点差", "滑点", "插针", "凯利", "复利", "破产概率", "Ask", "Bid",
         "挂单", "流动性", "Funded", "一致性", "过拟合", "夏普", "波动率",
         "配对交易", "协整", "Z-score", "ORB", "DOM", "Delta", "Gamma"]
out = ["== 术语表覆盖检查 =="]
for k in terms:
    out.append(f"{k}: {'有' if k in t else '缺'}")
print("\n".join(out))

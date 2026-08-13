# -*- coding: utf-8 -*-
"""检查新图：尺寸、颜色数量、非白色像素占比"""
from PIL import Image
import numpy as np

for name in ["fig_real_eth_2leg", "fig_real_btc_day", "fig_real_btc_range", "fig_real_btc_sweep"]:
    im = Image.open(f"handbook/images/{name}.png").convert("RGB")
    a = np.asarray(im)
    nonwhite = (a.sum(axis=2) < 720).mean()  # 非白像素比例
    uniq = len(np.unique(a.reshape(-1, 3), axis=0))
    print(f"{name}: {im.size} 非白占比={nonwhite:.3f} 颜色数={uniq}")

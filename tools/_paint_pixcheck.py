# -*- coding: utf-8 -*-
"""matplotlib 版真实图像素验证：检查每张图的关键颜色（标注框/线/通道）确实渲染"""
import os
from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(BASE, "handbook", "images")

# 颜色 -> (容差, 最低像素数)
COLORS = {
    "红涨#ef5350": ((239, 83, 80), 20, 3000),
    "绿跌#26a69a": ((38, 166, 154), 20, 3000),
    "蓝#1565c0": ((21, 101, 192), 25, 400),
    "橙#ef6c00": ((239, 108, 0), 25, 300),
    "紫#7b1fa2": ((123, 31, 162), 30, 400),
}

# 每张图必须包含的颜色（标注/线）
TARGETS = {
    "fig_real_eth_2leg.png": ["红涨#ef5350", "绿跌#26a69a", "蓝#1565c0", "橙#ef6c00"],
    "fig_real_btc_range.png": ["红涨#ef5350", "绿跌#26a69a", "蓝#1565c0", "橙#ef6c00"],
    "fig_real_btc_day.png": ["红涨#ef5350", "绿跌#26a69a", "蓝#1565c0", "橙#ef6c00"],
    "fig_real_btc_sweep.png": ["红涨#ef5350", "绿跌#26a69a", "蓝#1565c0", "橙#ef6c00", "紫#7b1fa2"],
    "fig_real_trailing_stop.png": ["红涨#ef5350", "绿跌#26a69a", "蓝#1565c0", "橙#ef6c00"],
    "fig_real_atr.png": ["红涨#ef5350", "绿跌#26a69a", "蓝#1565c0", "橙#ef6c00", "紫#7b1fa2"],
}

def count_color(im, rgb, tol):
    w, h = im.size
    px = im.load()
    n = 0
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            p = px[x, y]
            if abs(p[0] - rgb[0]) <= tol and abs(p[1] - rgb[1]) <= tol and abs(p[2] - rgb[2]) <= tol:
                n += 1
    return n * 4  # 每2px采样，乘4近似全量

def main():
    ok_all = True
    for fname, need in TARGETS.items():
        path = os.path.join(IMG, fname)
        im = Image.open(path).convert("RGB")
        w, h = im.size
        print("== %s  %dx%d" % (fname, w, h))
        for cname in need:
            rgb, tol, floor = COLORS[cname]
            n = count_color(im, rgb, tol)
            ok = n >= floor
            ok_all = ok_all and ok
            print("   %-14s %7d px  %s" % (cname, n, "OK" if ok else "FAIL<" + str(floor)))
    print("ALL PASS" if ok_all else "SOME FAIL")

if __name__ == "__main__":
    main()

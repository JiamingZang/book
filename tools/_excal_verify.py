# -*- coding: utf-8 -*-
"""精确验证 Excalidraw 重绘 PNG：每个盒子里的文本确实渲染了。

与 _excal_to_mpl.py 复用同一套布局变换（x0/y0/margin/axes limits/dpi），
用 ax.transData 把盒子的数据坐标转成像素坐标，再按该盒文本元素的
strokeColor（不是固定 #263238——阶段表头是彩色文本）统计区域内
接近该颜色的像素占比。占比过低 -> 空盒警告。

用法：
    python -X utf8 tools/_excal_verify.py [fig_name ...]   # 缺省全部 12 张
"""
import json
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]

IMG_DIR = "handbook/images"
EXCAL_SRC = "handbook/images/_excal_src"  # 源 .excalidraw 归档
TARGET_W_IN = 11.6
DPI = 160
ALL = [
    "fig_p2_checklist",
    "fig_p3_framework",
    "fig_p4_breakout_flow",
    "fig_p4_state_machine",
    "fig_p4_state_tree",
    "fig_p5_smc_flow",
    "fig_p7_three_stages",
    "fig_p7_flow",
    "fig_p8_verify_loop",
    "fig_p8_review_flow",
    "fig_p9_prop_flow",
    "fig_p10_strategy_tree",
]


def hex_rgb8(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def elem_bbox(els):
    xs, ys = [], []
    for e in els:
        t = e.get("type")
        x, y = e.get("x", 0.0), e.get("y", 0.0)
        if t == "rectangle":
            xs += [x, x + e.get("width", 0)]
            ys += [y, y + e.get("height", 0)]
        elif t == "text":
            xs += [x, x + e.get("width", 0)]
            ys += [y, y + e.get("height", 0)]
        elif t == "arrow":
            for p in e.get("points", []):
                xs.append(p[0])
                ys.append(p[1])
    return min(xs), min(ys), max(xs), max(ys)


def verify(name):
    with open(f"{EXCAL_SRC}/{name}.excalidraw", encoding="utf-8") as f:
        d = json.load(f)
    els = d["elements"]

    x0, y0, x1, y1 = elem_bbox(els)
    bw, bh = x1 - x0, y1 - y0
    margin = max(bw, bh) * 0.05
    W, H = bw + 2 * margin, bh + 2 * margin
    fig_w = TARGET_W_IN
    fig_h = H * (TARGET_W_IN / W)

    fig = plt.figure(figsize=(fig_w, fig_h), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x0 - margin, x1 + margin)
    ax.set_ylim(-(y1 + margin), -(y0 - margin))

    im = Image.open(f"{IMG_DIR}/{name}.png").convert("RGB")
    arr = np.asarray(im).astype(int)
    Hpx, Wpx = arr.shape[:2]

    boxes = {e["id"]: e for e in els if e.get("type") == "rectangle"}
    texts = [e for e in els if e.get("type") == "text" and (e.get("text") or "").strip()]

    n_box = 0
    n_empty = 0
    for bid, e in boxes.items():
        bx, by, bw2, bh2 = e.get("x", 0), e.get("y", 0), e.get("width", 0), e.get("height", 0)
        tcols = []
        for t in texts:
            if t.get("containerId") == bid:
                tcols.append(hex_rgb8(t.get("strokeColor", "#263238")))
        if not tcols:
            continue
        n_box += 1
        # 数据坐标 -> 像素坐标。axes 里 y 已翻转（Excalidraw 上缘小 y -> 数据大 y -> 屏上缘），
        # transData 返回的显示坐标 y 向上（左下原点），而 PNG 行向下增长，须再翻一次。
        (px0, dy0) = ax.transData.transform((bx, -by))
        (px1, dy1) = ax.transData.transform((bx + bw2, -(by + bh2)))
        xa, xb = int(min(px0, px1)), int(max(px0, px1))
        ya = int(Hpx - max(dy0, dy1))  # 顶边（显示 y 大）
        yb = int(Hpx - min(dy0, dy1))  # 底边
        xa, xb = max(0, xa), min(Wpx, xb)
        ya, yb = max(0, ya), min(Hpx, yb)
        if xb - xa < 4 or yb - ya < 4:
            print(f"  {bid}: region too small ({xa},{ya})-({xb},{yb})")
            n_empty += 1
            continue
        mask = np.zeros((yb - ya, xb - xa), dtype=bool)
        sub = arr[ya:yb, xa:xb]
        for c in tcols:
            mask |= (np.abs(sub - np.array(c)).sum(axis=2) < 60)
        frac = mask.mean()
        lbl = "OK" if frac > 0.001 else "EMPTY"
        if frac <= 0.001:
            n_empty += 1
        matched = [t for t in texts if t.get("containerId") == bid]
        ttxt = " / ".join(
            " ".join((t.get("text") or "").strip().split("\n")[:2]) for t in matched[:2]
        )
        print(f"  {bid} fill={e.get('backgroundColor')} col={[ '#%02x%02x%02x' % c for c in tcols ]} frac={frac:.4f} {lbl} | {ttxt[:26]}")
    print(f"{name}: boxes_with_text={n_box} empty={n_empty} img={Wpx}x{Hpx}")
    plt.close(fig)
    return n_empty


if __name__ == "__main__":
    names = sys.argv[1:] or ALL
    total = 0
    for n in names:
        total += verify(n)
    print("VERIFY DONE, total_empty =", total)

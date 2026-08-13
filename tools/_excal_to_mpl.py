# -*- coding: utf-8 -*-
"""把 Excalidraw JSON 流程图精确重排为 house style 的 matplotlib PNG。

背景：全库曾有 12 处 `![[fig_*.excalidraw]]` 嵌入（HTML/PDF 中渲染为手绘风格
导出图，且不在图号/图注体系内，属于"孤儿图"）。本脚本读取 .excalidraw 的
精确坐标/文本/箭头数据，用 matplotlib 画成与全库一致的干净风格，文件名不变，
供批次 66 把这些嵌入升级为标准图号图注图。

要点（踩过的坑）：
- 箭头 points 是**绝对坐标**（points[0]==元素 x,y），不能再加元素偏移；
- 文本行距/自动缩字全部用**数据单位**计算，避免英寸/数据单位混用；
- y 轴翻转：Excalidraw 原点在左上，matplotlib 在左下。

用法：
    python -X utf8 tools/_excal_to_mpl.py            # 全部 12 张
    python -X utf8 tools/_excal_to_mpl.py fig_p8_verify_loop   # 指定一张

输出：handbook/images/fig_*.png（覆盖同名 Excalidraw 导出图）
"""
import json
import math
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

IMG_DIR = "handbook/images"
EXCAL_SRC = "handbook/images/_excal_src"  # 源 .excalidraw 归档（批次 66 起迁入）
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


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4))


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
                xs.append(p[0])  # 绝对坐标
                ys.append(p[1])
    return min(xs), min(ys), max(xs), max(ys)


def convert(name):
    with open(f"{EXCAL_SRC}/{name}.excalidraw", encoding="utf-8") as f:
        d = json.load(f)
    els = d["elements"]

    x0, y0, x1, y1 = elem_bbox(els)
    bw, bh = x1 - x0, y1 - y0
    if bw <= 0 or bh <= 0:
        raise ValueError(f"{name}: empty bbox")

    margin = max(bw, bh) * 0.05
    W, H = bw + 2 * margin, bh + 2 * margin
    fig_w = TARGET_W_IN
    fig_h = H * (TARGET_W_IN / W)
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x0 - margin, x1 + margin)
    ax.set_ylim(-(y1 + margin), -(y0 - margin))
    ax.axis("off")
    renderer = fig.canvas.get_renderer()

    def yf(y):
        return -y

    # 单位换算：1 数据单位 = (TARGET_W_IN / W) 英寸；文本窗口宽度(px) -> 数据单位
    def px_to_units(px):
        return px / DPI / (TARGET_W_IN / W)

    # ---- 箭头（在矩形下层）----
    for e in els:
        if e.get("type") != "arrow":
            continue
        pts = e.get("points") or []
        if len(pts) < 2:
            continue
        xy = [(p[0], yf(p[1])) for p in pts]
        col = hex_rgb(e.get("strokeColor", "#263238"))
        lw = max(1.2, e.get("strokeWidth", 2) * 0.8)
        ax.plot([p[0] for p in xy], [p[1] for p in xy], color=col, lw=lw,
                solid_capstyle="round", zorder=1)

        def head(p_from, p_to, size):
            dx, dy = p_to[0] - p_from[0], p_to[1] - p_from[1]
            ang = math.atan2(dy, dx)
            tri = [
                p_to,
                (p_to[0] - size * math.cos(ang - 0.42), p_to[1] - size * math.sin(ang - 0.42)),
                (p_to[0] - size * math.cos(ang + 0.42), p_to[1] - size * math.sin(ang + 0.42)),
            ]
            ax.add_patch(Polygon(tri, closed=True, facecolor=col, edgecolor="none", zorder=2))

        hs = min(bw, bh) * 0.035
        if e.get("endArrowhead"):
            head(xy[-2], xy[-1], hs)
        if e.get("startArrowhead"):
            head(xy[1], xy[0], hs)

    # ---- 矩形 ----
    boxes = {}
    for e in els:
        if e.get("type") != "rectangle":
            continue
        boxes[e["id"]] = e
        x, y, w, h = e.get("x", 0), e.get("y", 0), e.get("width", 0), e.get("height", 0)
        fc = hex_rgb(e.get("backgroundColor", "#ffffff"))
        ec = hex_rgb(e.get("strokeColor", "#263238"))
        r = min(w, h) * 0.06
        ax.add_patch(FancyBboxPatch(
            (x, yf(y + h)), w, h,
            boxstyle=f"round,pad=0,rounding_size={r}",
            facecolor=fc, edgecolor=ec, lw=max(1.2, e.get("strokeWidth", 2) * 0.8),
            zorder=3,
        ))

    # ---- 文本 ----
    for e in els:
        if e.get("type") != "text":
            continue
        raw = e.get("originalText") or e.get("text", "")
        if not raw:
            continue
        lines = raw.split("\n")
        fs0 = e.get("fontSize", 19)
        col = hex_rgb(e.get("strokeColor", "#263238"))
        is_title = str(e.get("id", "")).startswith("title")
        line_h = e.get("lineHeight", 1.3) or 1.3
        cid = e.get("containerId")

        def pitch_units(fs_pt):
            # 行距（数据单位）：约等于 Excalidraw fontSize*lineHeight，随缩字线性缩放
            return fs_pt / 72 * 1.28 * (W / TARGET_W_IN)

        def measure(ln, fs):
            t = ax.text(0, 0, ln, fontsize=fs)
            w = px_to_units(t.get_window_extent(renderer=renderer).width)
            t.remove()
            return w

        if cid and cid in boxes:
            bx, by, bw2, bh2 = (boxes[cid].get(k) for k in ("x", "y", "width", "height"))
            fs_pt = fs0 * 0.72

            # 自动缩字：宽度（数据单位）与总行高都要放进盒子
            while fs_pt > 5.5:
                max_lw = max(measure(ln, fs_pt) for ln in lines)
                if max_lw <= bw2 * 0.94 and pitch_units(fs_pt) * len(lines) <= bh2 * 0.94:
                    break
                fs_pt -= 0.5
            cx = bx + bw2 / 2
            cy = yf(by + bh2 / 2)
            total_h = pitch_units(fs_pt) * (len(lines) - 1)
            for i, ln in enumerate(lines):
                ax.text(cx, cy + total_h / 2 - i * pitch_units(fs_pt), ln,
                        fontsize=fs_pt, color=col, ha="center", va="center", zorder=4)
        else:
            x, y = e.get("x", 0), e.get("y", 0)
            va_ax = {"top": "top", "middle": "center", "bottom": "bottom"}.get(
                e.get("verticalAlign", "top"), "top")
            ha_ax = e.get("textAlign", "left")
            fs_pt = fs0 * 0.72
            decl_w = e.get("width") or (x1 - x0) * 0.95  # 元素声明宽度；无则用图宽
            while fs_pt > 5.5:
                max_lw = max(measure(ln, fs_pt) for ln in lines)
                if max_lw <= decl_w * 0.98:
                    break
                fs_pt -= 0.5
            total_h = pitch_units(fs_pt) * (len(lines) - 1)
            for i, ln in enumerate(lines):
                ax.text(x, yf(y) - i * pitch_units(fs_pt), ln, fontsize=fs_pt, color=col,
                        ha=ha_ax, va=va_ax, linespacing=1.0,
                        fontweight="bold" if is_title else "normal", zorder=4)

    out = f"{IMG_DIR}/{name}.png"
    # 不用 bbox_inches='tight'：fig 尺寸已按内容 bbox+边距计算，tight 裁剪会改变
    # 像素映射、并把溢出文本的窗口范围算进画布导致宽高比失真
    fig.savefig(out, dpi=DPI, facecolor="white")
    plt.close(fig)
    print(f"OK {out}  {fig_w:.1f}x{fig_h:.1f} in (bbox {bw:.0f}x{bh:.0f} units)")


if __name__ == "__main__":
    names = sys.argv[1:] or ALL
    for n in names:
        convert(n)
    print("done")

# -*- coding: utf-8 -*-
"""Excalidraw PNG 错位诊断：测量每段文字的实际渲染 bbox，与容器矩形比较。
对每张流程图重新渲染（复用 _excalidraw_lib 的元素 → matplotlib），
保留 Text 对象后用 renderer.get_window_extent 测出真实像素位置，
再转回数据坐标，检查：文字中心 vs 容器中心偏差、文字是否溢出容器。
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

from _excalidraw_lib import ExcaliDoc, SCALE, PAD_X, PAD_TOP

import _excalidraw_gen as gen

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False


def diag_one(doc):
    """渲染 doc（不保存），返回 (issues, total)"""
    fig, ax = plt.subplots(figsize=doc.figsize)
    x0, x1 = doc.xlim
    y0, y1 = doc.ylim
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.axis("off")

    shapes = {}  # id -> (x0, y_bot, w, h) 数据坐标
    text_objs = []  # (el, Text, container_id or None)
    for el in doc.elements:
        if el["type"] in ("rectangle", "diamond", "ellipse"):
            px, py = el["x"], el["y"]
            xd0, yd_top = doc._inv(px, py)
            xd1, yd_bot = doc._inv(px + el["width"], py + el["height"])
            lw = el["strokeWidth"] * 0.8
            if el["type"] == "rectangle":
                ax.add_patch(FancyBboxPatch((xd0, yd_bot), xd1 - xd0, yd_top - yd_bot,
                                            boxstyle="round,pad=0.06",
                                            facecolor=el["backgroundColor"],
                                            edgecolor=el["strokeColor"], lw=lw, zorder=3))
            elif el["type"] == "diamond":
                cx, cy = (xd0 + xd1) / 2, (yd_top + yd_bot) / 2
                ax.add_patch(plt.Polygon([(cx, yd_top), (xd1, cy), (cx, yd_bot), (xd0, cy)],
                                         closed=True, facecolor=el["backgroundColor"],
                                         edgecolor=el["strokeColor"], lw=lw, zorder=3))
            else:
                cx, cy = (xd0 + xd1) / 2, (yd_top + yd_bot) / 2
                ax.add_patch(plt.Circle((cx, cy), min(xd1 - xd0, yd_top - yd_bot) / 2,
                                        facecolor=el["backgroundColor"],
                                        edgecolor=el["strokeColor"], lw=lw, zorder=3))
            shapes[el["id"]] = (xd0, yd_bot, xd1 - xd0, yd_top - yd_bot)
        elif el["type"] == "arrow":
            pts = el["points"]
            xs = [doc._inv(p[0], p[1])[0] for p in pts]
            ys = [doc._inv(p[0], p[1])[1] for p in pts]
            ls = "--" if el["strokeStyle"] == "dashed" else "-"
            if len(pts) == 2:
                ax.add_patch(FancyArrowPatch((xs[0], ys[0]), (xs[1], ys[1]),
                                             arrowstyle="-|>", mutation_scale=16,
                                             color=el["strokeColor"], lw=el["strokeWidth"],
                                             linestyle=ls, zorder=2))
            else:
                ax.plot(xs, ys, color=el["strokeColor"], lw=el["strokeWidth"],
                        linestyle=ls, zorder=2)
                ax.annotate("", xy=(xs[-1], ys[-1]), xytext=(xs[-2], ys[-2]),
                            arrowprops=dict(arrowstyle="-|>", color=el["strokeColor"],
                                            lw=el["strokeWidth"]), zorder=2)
        elif el["type"] == "line":
            pts = el["points"]
            xs = [doc._inv(p[0], p[1])[0] for p in pts]
            ys = [doc._inv(p[0], p[1])[1] for p in pts]
            ax.plot(xs, ys, color=el["strokeColor"], lw=el["strokeWidth"],
                    linestyle="--" if el["strokeStyle"] == "dashed" else "-", zorder=2)
        elif el["type"] == "text":
            if el["id"] == "title000":
                continue
            fs_pt = el["fontSize"] / 2.0
            tc = el["strokeColor"]
            if el.get("containerId") and el["containerId"] in shapes:
                xd0, yd_bot, wd, hd = shapes[el["containerId"]]
                cx, cy = xd0 + wd / 2, yd_bot + hd / 2
                lines = doc._wrap_text(el["text"], wd, fs_pt)
            else:
                px, py = el["x"], el["y"]
                w_px, h_px = el["width"], el["height"]
                xd0, yd_top = doc._inv(px, py)
                xd1, yd_bot = doc._inv(px + w_px, py + h_px)
                cx, cy = (xd0 + xd1) / 2, (yd_top + yd_bot) / 2
                lines = el["text"].split("\n")
            line_h = fs_pt * 1.53 / SCALE * 1.2
            total_h = line_h * (len(lines) - 1)
            start_y = cy + total_h / 2
            for i, ln in enumerate(lines):
                t = ax.text(cx, start_y - i * line_h, ln, fontsize=fs_pt, color=tc,
                            ha="center", va="center", zorder=5)
                text_objs.append((el, t, el.get("containerId") if el.get("containerId") in shapes else None))

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    trans = ax.transData.inverted()

    issues = []
    total = 0
    for el, t, cid in text_objs:
        total += 1
        bb = t.get_window_extent(renderer=renderer)
        (tx0, ty0), (tx1, ty1) = trans.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
        # 数据坐标（y 可能翻转，规范化）
        x_min, x_max = min(tx0, tx1), max(tx0, tx1)
        y_min, y_max = min(ty0, ty1), max(ty0, ty1)
        if cid:
            sx0, sy_bot, sw, sh = shapes[cid]
            scx, scy = sx0 + sw / 2, sy_bot + sh / 2
            tcx, tcy = (x_min + x_max) / 2, (y_min + y_max) / 2
            dx = abs(tcx - scx)
            dy = abs(tcy - scy)
            overflow = (x_min < sx0 - 0.02 or x_max > sx0 + sw + 0.02
                        or y_min < sy_bot - 0.02 or y_max > sy_bot + sh + 0.02)
            if dx > 0.06 or dy > 0.08 or overflow:
                issues.append(f"    [{el['id']}] 容器中心偏差 dx={dx:.2f} dy={dy:.2f} 溢出={overflow} "
                              f"框=({sx0:.1f},{sy_bot:.1f},{sw:.1f},{sh:.1f}) "
                              f"文字bbox=({x_min:.1f},{y_min:.1f},{x_max:.1f},{y_max:.1f}) "
                              f"文本: {el['text'][:18]!r}")
    plt.close(fig)
    return issues, total


def main():
    # (name, xlim, ylim, figsize)
    params = {
        "fig_p2_checklist": ((0, 10), (0, 10.8), (13.5, 5.8)),
        "fig_p3_framework": ((0, 12), (0, 6.6), (12.2, 6.2)),
        "fig_p4_breakout_flow": ((0, 10.5), (0, 10), (13.0, 7.2)),
        "fig_p4_state_machine": ((0, 13.2), (0, 6.6), (12.5, 6.2)),
        "fig_p4_state_tree": ((0, 18.6), (0, 9.5), (15.5, 8.2)),
        "fig_p5_smc_flow": ((0, 14), (0, 6.6), (14.5, 6.4)),
        "fig_p7_three_stages": ((0, 13.8), (0, 6.8), (13.5, 6.2)),
        "fig_p7_flow": ((0, 10), (0, 10), (13.0, 5.6)),
        "fig_p8_verify_loop": ((0, 13.4), (0, 7.4), (12.0, 6.4)),
        "fig_p8_review_flow": ((0, 14), (0, 6.4), (14.5, 6.2)),
        "fig_p9_prop_flow": ((0, 13.6), (0, 6.6), (12.5, 5.8)),
        "fig_p10_strategy_tree": ((0, 14), (0, 6.4), (14.5, 6.2)),
    }
    all_issues = 0
    for name, (xlim, ylim, figsize) in params.items():
        # 从磁盘读回 JSON 元素
        jp = os.path.join(gen.OUT, f"{name}.excalidraw")
        d = json.load(open(jp, encoding="utf-8"))
        doc = ExcaliDoc(name, xlim=xlim, ylim=ylim, figsize=figsize)
        doc.elements = d["elements"]
        issues, total = diag_one(doc)
        flag = "✓" if not issues else "✗"
        print(f"{flag} {doc.name}: 文本 {total} 段, 问题 {len(issues)}")
        for it in issues:
            print(it)
        all_issues += len(issues)
    print(f"\n总计问题 {all_issues}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Excalidraw 双输出库：同一份流程图数据 → .excalidraw（Obsidian 可编辑手绘风）+ PNG（HTML/PDF 用）

用法（在 tools/ 下）：
    from _excalidraw_lib import ExcaliDoc
    doc = ExcaliDoc("fig_x", xlim=(0,14), ylim=(0,7), title="...", figsize=(14, 6))
    doc.box(0.5, 5.0, 4.0, 1.2, "标题\\n正文", ec=TEAL, fs=11)   # 框内文本自动居中换行
    doc.arrow(4.5, 5.6, 6.0, 5.6, color=DARK)
    doc.text(7.0, 0.5, "自由注释", fs=10, color=GRAY)
    doc.export("handbook/images")   # 写 fig_x.excalidraw + fig_x.png

关键设计：
- 框内文本使用 Excalidraw 原生「容器文本」（text.containerId 绑定矩形 + 矩形 boundElements），
  Obsidian 打开时自动居中、按框宽换行，用户拖动矩形文本跟随；
- PNG 渲染时对容器文本按矩形宽度做 textwrap 换行再居中，与 .excalidraw 视觉一致；
- 自由文本（text()）按中文/ascii 宽度估算边界框，ha/va 控制对齐。
"""
import math
import os
import json
import textwrap
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

# ---------------- 配色（与 draw_handbook_figs.py 一致） ----------------
UP = "#26a69a"
DOWN = "#ef5350"
GRAY = "#90a4ae"
DARK = "#263238"
ORANGE = "#ef6c00"
TEAL = "#00897b"
NAVY = "#1e3a6b"
WHITE = "#ffffff"

# ---------------- Excalidraw 常量 ----------------
SCALE = 64.0        # matplotlib 坐标单位 → 像素
PAD_X = 60.0        # 左右像素边距
PAD_TOP = 90.0      # 顶部像素边距（标题区）
PAD_BOTTOM = 50.0   # 底部像素边距


def _stroke(ec):
    return ec if ec else "#1e1e1e"


def _fill_alpha(ec, fc=None):
    """背景色：fc 直接使用；否则线框色浅化（浅色块）"""
    def lighten(c, alpha):
        r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
        return "#%02x%02x%02x" % (int(r + (255 - r) * alpha),
                                  int(g + (255 - g) * alpha),
                                  int(b + (255 - b) * alpha))
    if fc:
        return fc
    return lighten(_stroke(ec), 0.78)


class ExcaliDoc:
    def __init__(self, name, xlim=(0, 14), ylim=(0, 7), title="", figsize=None):
        self.name = name
        self.xlim = xlim
        self.ylim = ylim
        self.title = title
        self.figsize = figsize
        self.elements = []
        self._id = 0

    # ---------------- 内部工具 ----------------
    def _nid(self):
        self._id += 1
        return "e%04d" % self._id

    def _px(self, x, y):
        """matplotlib 坐标 → excalidraw 像素（y 翻转）"""
        x0, x1 = self.xlim
        y0, y1 = self.ylim
        px = (x - x0) * SCALE + PAD_X
        py = (y1 - y) * SCALE + PAD_TOP
        return px, py

    def _inv(self, px, py):
        """像素 → 数据坐标"""
        x0 = self.xlim[0]
        y1 = self.ylim[1]
        return x0 + (px - PAD_X) / SCALE, y1 - (py - PAD_TOP) / SCALE

    def _est_text(self, text, fs_px):
        """估算文本像素宽高（中文≈fs，ascii≈fs*0.55，行高≈fs*1.35）"""
        lines = text.split("\n")
        wmax = 0.0
        for ln in lines:
            w = 0.0
            for ch in ln:
                w += fs_px * (0.55 if ord(ch) < 128 else 1.0)
            wmax = max(wmax, w)
        return wmax, len(lines) * fs_px * 1.35

    # ---------------- 元素 API ----------------
    def _shape(self, stype, x, y, w, h, text, ec, fs, fc, tc, rounded):
        """通用形状 + 容器文本（stype: rectangle/diamond/ellipse）"""
        px, py = self._px(x, y + h)          # 形状左上角（y 翻转后）
        pw, ph = w * SCALE, h * SCALE
        stroke = _stroke(ec)
        fill = _fill_alpha(ec, fc)
        sid = self._nid()
        bound = None
        if text:
            tid = self._nid()
            bound = [{"id": tid, "type": "text"}]
        self.elements.append({
            "id": sid, "type": stype,
            "x": px, "y": py, "width": pw, "height": ph, "angle": 0,
            "strokeColor": stroke, "backgroundColor": fill, "fillStyle": "hachure",
            "strokeWidth": 2, "strokeStyle": "solid", "roughness": 1, "opacity": 100,
            "groupIds": [], "frameId": None,
            "roundness": {"type": 3} if (stype == "rectangle" and rounded) else None,
            "seed": hash((sid, stype[0])) % 100000, "version": 1, "versionNonce": 1,
            "isDeleted": False, "boundElements": bound, "updated": 1,
            "link": None, "locked": False,
        })
        if text:
            self.elements.append({
                "id": tid, "type": "text",
                "x": px + 8, "y": py + 8, "width": max(10, pw - 16), "height": max(10, ph - 16),
                "angle": 0, "strokeColor": tc, "backgroundColor": "transparent",
                "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
                "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
                "roundness": None, "seed": hash((tid, "t")) % 100000, "version": 1,
                "versionNonce": 1, "isDeleted": False, "boundElements": None, "updated": 1,
                "link": None, "locked": False,
                "fontSize": fs * 1.9, "fontFamily": 1, "text": text,
                "textAlign": "center", "verticalAlign": "middle",
                "containerId": sid, "originalText": text, "lineHeight": 1.3,
                "baseline": fs * 1.9 * 0.9,
            })
        return sid

    def box(self, x, y, w, h, text, ec=GRAY, fs=10.5, fc=None, tc=DARK, rounded=True):
        return self._shape("rectangle", x, y, w, h, text, ec, fs, fc, tc, rounded)

    def diamond(self, x, y, w, h, text, ec=GRAY, fs=10.5, fc=None, tc=DARK):
        return self._shape("diamond", x, y, w, h, text, ec, fs, fc, tc, True)

    def ellipse(self, x, y, w, h, text, ec=GRAY, fs=10.5, fc=None, tc=DARK):
        return self._shape("ellipse", x, y, w, h, text, ec, fs, fc, tc, True)

    def text(self, x, y, text, fs=10.5, color=DARK, ha="center", va="center", maxw=None):
        """自由文本（ha/va 控制对齐；maxw 像素宽限制 → 自动换行）"""
        if maxw:
            fs_px = fs * 1.9
            lines = []
            for ln in text.split("\n"):
                cur = ""
                for ch in ln:
                    wch = fs_px * (0.55 if ord(ch) < 128 else 1.0)
                    if cur and self._est_text(cur, fs_px)[0] + wch > maxw:
                        lines.append(cur)
                        cur = ch
                    else:
                        cur += ch
                lines.append(cur)
            text = "\n".join(lines)
        w, h = self._est_text(text, fs * 1.9)
        px, py = self._px(x, y)
        if ha == "center":
            px -= w / 2
        elif ha == "right":
            px -= w
        if va == "bottom":
            py -= h
        elif va == "middle":
            py -= h / 2
        tid = self._nid()
        self.elements.append({
            "id": tid, "type": "text",
            "x": px, "y": py, "width": w, "height": h,
            "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
            "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
            "roundness": None, "seed": hash((tid, "tf")) % 100000, "version": 1,
            "versionNonce": 1, "isDeleted": False, "boundElements": None, "updated": 1,
            "link": None, "locked": False,
            "fontSize": fs * 1.9, "fontFamily": 1, "text": text,
            "textAlign": "center", "verticalAlign": "top",
            "containerId": None, "originalText": text, "lineHeight": 1.3,
            "baseline": fs * 1.9 * 0.9,
        })
        return tid

    def arrow(self, x1, y1, x2, y2, color=GRAY, dashed=False, rad=0.0, lw=2.0):
        p1 = self._px(x1, y1)
        p2 = self._px(x2, y2)
        if rad:
            mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
            dx, dy = p2[0] - p1[0], p2[1] - p1[1]
            length = math.hypot(dx, dy) or 1.0
            nx, ny = -dy / length, dx / length
            cx, cy = mx + nx * rad * length * 0.5, my + ny * rad * length * 0.5
            pts = []
            for t in np.linspace(0, 1, 24):
                pts.append([float((1 - t) ** 2 * p1[0] + 2 * (1 - t) * t * cx + t ** 2 * p2[0]),
                            float((1 - t) ** 2 * p1[1] + 2 * (1 - t) * t * cy + t ** 2 * p2[1])])
        else:
            pts = [[p1[0], p1[1]], [p2[0], p2[1]]]
        aid = self._nid()
        self.elements.append({
            "id": aid, "type": "arrow",
            "x": p1[0], "y": p1[1], "width": max(1.0, abs(p2[0] - p1[0])),
            "height": max(1.0, abs(p2[1] - p1[1])), "angle": 0,
            "strokeColor": color, "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": lw, "strokeStyle": "dashed" if dashed else "solid",
            "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
            "roundness": {"type": 2}, "seed": hash((aid, "a")) % 100000, "version": 1,
            "versionNonce": 1, "isDeleted": False, "boundElements": None, "updated": 1,
            "link": None, "locked": False,
            "points": pts, "lastCommittedPoint": None,
            "startBinding": None, "endBinding": None,
            "startArrowhead": None, "endArrowhead": "arrow",
        })
        return aid

    def line(self, x1, y1, x2, y2, color=GRAY, dashed=False, lw=1.5):
        p1 = self._px(x1, y1)
        p2 = self._px(x2, y2)
        lid = self._nid()
        self.elements.append({
            "id": lid, "type": "line",
            "x": p1[0], "y": p1[1], "width": max(1.0, abs(p2[0] - p1[0])),
            "height": max(1.0, abs(p2[1] - p1[1])), "angle": 0,
            "strokeColor": color, "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": lw, "strokeStyle": "dashed" if dashed else "solid",
            "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
            "roundness": {"type": 2}, "seed": hash((lid, "l")) % 100000, "version": 1,
            "versionNonce": 1, "isDeleted": False, "boundElements": None, "updated": 1,
            "link": None, "locked": False,
            "points": [[p1[0], p1[1]], [p2[0], p2[1]]],
        })
        return lid

    # ---------------- 输出 ----------------
    def export(self, out_dir):
        os.makedirs(out_dir, exist_ok=True)
        x0, x1 = self.xlim
        y0, y1 = self.ylim
        W = (x1 - x0) * SCALE + 2 * PAD_X
        H = (y1 - y0) * SCALE + PAD_TOP + PAD_BOTTOM
        if self.title:
            self.elements.append({
                "id": "title000", "type": "text",
                "x": PAD_X, "y": 14, "width": W - 2 * PAD_X, "height": 44,
                "angle": 0, "strokeColor": DARK, "backgroundColor": "transparent",
                "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
                "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
                "roundness": None, "seed": 99991, "version": 1,
                "versionNonce": 1, "isDeleted": False, "boundElements": None, "updated": 1,
                "link": None, "locked": False,
                "fontSize": 26, "fontFamily": 1, "text": self.title,
                "textAlign": "center", "verticalAlign": "top",
                "containerId": None, "originalText": self.title, "lineHeight": 1.3,
                "baseline": 23,
            })
        doc = {
            "type": "excalidraw",
            "version": 2,
            "source": "https://excalidraw.com",
            "elements": self.elements,
            "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff", "zoom": {"value": 1}},
            "files": {},
        }
        with open(os.path.join(out_dir, f"{self.name}.excalidraw"), "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False)
        # PNG
        if self.figsize:
            fig, ax = plt.subplots(figsize=self.figsize)
        else:
            fig, ax = plt.subplots(figsize=(max(8, (x1 - x0) * 1.05), max(4.4, (y1 - y0) * 0.95)))
        self._render_png(ax)
        if self.title:
            fig.suptitle(self.title, fontsize=12.5, color=DARK, y=0.985)
        fig.savefig(os.path.join(out_dir, f"{self.name}.png"), dpi=110,
                    bbox_inches="tight", facecolor="white")
        plt.close(fig)
        print(f"  ✓ {self.name}.excalidraw ({len(self.elements)} 元素) + {self.name}.png")

    # ---------------- PNG 渲染 ----------------
    def _render_png(self, ax):
        x0, x1 = self.xlim
        y0, y1 = self.ylim
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)
        ax.axis("off")
        # 形状（底层）
        shapes = {}
        for el in self.elements:
            if el["type"] in ("rectangle", "diamond", "ellipse"):
                px, py = el["x"], el["y"]
                xd0, yd_top = self._inv(px, py)
                xd1, yd_bot = self._inv(px + el["width"], py + el["height"])
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
        # 箭头 / 线
        for el in self.elements:
            if el["type"] == "arrow":
                pts = el["points"]
                xs = [self._inv(p[0], p[1])[0] for p in pts]
                ys = [self._inv(p[0], p[1])[1] for p in pts]
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
                xs = [self._inv(p[0], p[1])[0] for p in pts]
                ys = [self._inv(p[0], p[1])[1] for p in pts]
                ax.plot(xs, ys, color=el["strokeColor"], lw=el["strokeWidth"],
                        linestyle="--" if el["strokeStyle"] == "dashed" else "-", zorder=2)
        # 文本：容器文本按容器几何换行居中；自由文本按元素中心
        for el in self.elements:
            if el["type"] != "text" or el["id"] == "title000":
                continue
            fs_pt = el["fontSize"] / 2.0
            tc = el["strokeColor"]
            if el.get("containerId") and el["containerId"] in shapes:
                xd0, yd_bot, wd, hd = shapes[el["containerId"]]
                cx, cy = xd0 + wd / 2, yd_bot + hd / 2
                # 按容器宽度估算换行
                lines = self._wrap_text(el["text"], wd, fs_pt)
            else:
                px, py = el["x"], el["y"]
                w_px, h_px = el["width"], el["height"]
                xd0, yd_top = self._inv(px, py)
                xd1, yd_bot = self._inv(px + w_px, py + h_px)
                cx, cy = (xd0 + xd1) / 2, (yd_top + yd_bot) / 2
                lines = el["text"].split("\n")
            line_h = fs_pt * 1.53 / SCALE * 1.2   # matplotlib pt → 数据单位（行距）
            total_h = line_h * (len(lines) - 1)
            start_y = cy + total_h / 2
            for i, ln in enumerate(lines):
                ax.text(cx, start_y - i * line_h, ln, fontsize=fs_pt, color=tc,
                        ha="center", va="center", zorder=5)
            if el.get("containerId") and el["containerId"] in shapes:
                xd0, yd_bot, wd, hd = shapes[el["containerId"]]
                est_h = line_h * len(lines)
                if est_h > hd * 1.05:
                    print(f"    警告 {self.name}: 容器文本可能溢出 {el['containerId']} "
                          f"(估高 {est_h:.2f} > 框高 {hd:.2f}) 文本: {el['text'][:24]}…")

    def _wrap_text(self, text, wd, fs_pt):
        """按数据坐标宽度 wd 估算换行（中文≈fs，ascii≈fs*0.55，数据单位）"""
        if wd <= 0:
            return text.split("\n")
        ch_w = fs_pt * 1.53 / SCALE          # 中文宽（数据单位）
        out = []
        for ln in text.split("\n"):
            cur = ""
            for ch in ln:
                wch = ch_w * (0.55 if ord(ch) < 128 else 1.0)
                if cur and (self._est_text(cur, fs_pt)[0] * 1.53 / SCALE) + wch > wd:
                    out.append(cur)
                    cur = ch
                else:
                    cur += ch
            out.append(cur)
        return out


if __name__ == "__main__":
    doc = ExcaliDoc("_test_flow", xlim=(0, 10), ylim=(0, 6),
                    title="测试流程图", figsize=(10, 5))
    doc.box(0.5, 4.2, 3.0, 1.2, "开始\n第一步", ec=TEAL, fs=11)
    doc.box(6.0, 4.2, 3.0, 1.2, "结束\n完成", ec=ORANGE, fs=11)
    doc.arrow(3.5, 4.8, 6.0, 4.8, color=DARK)
    doc.text(0.5, 1.0, "注释", fs=10, color=GRAY)
    doc.export("handbook/images")
    print("自测完成")

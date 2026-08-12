# 交易手册仓库

价格行为 · SMC · 仓位 · 心态 · Prop 考核 —— 综合学习手册（Markdown 源 + 代码生成配图）。

## 目录结构

```
├── handbook/              # 手册本体（00 前言 ~ 11 附录，13 个 md + images/ + HTML + PDF）
│   ├── README.md          # 手册说明（阅读版/PDF 链接、配图统计、审计状态）
│   ├── trading-handbook.html  # 单文件阅读版（_build_html.py 生成）
│   ├── trading-handbook.pdf   # 打印版（Edge headless 导出）
│   └── images/            # 全部配图（代码生成）
├── tools/                 # 流水线脚本（绘图/构建/审计，README 见 tools/README.md）
├── _archive/              # 历史一次性脚本与输出（素材处理/OCR/PPT 提取等，仅供参考）
└── 素材目录               # _pa_agent_ref/ _ali_flashcards/ _breakout_research/ 等（git 忽略，不推送）
```

## 迭代流水线（每批优化）

1. 改内容（`handbook/*.md`）或加图（`tools/draw_handbook_figs.py`）
2. `python tools/draw_handbook_figs.py`（新增/修改图后）
3. `python tools/_build_html.py`（重建 HTML）
4. `python tools/_audit_all.py`（5 项审计全部通过）
5. 有图新增/重编号时：`python tools/_figorder_check.py` 确认图号顺序
6. 同步 `handbook/README.md`（配图数/审计状态）
7. PDF 重导（新增图后）：Edge headless 打印 `http://localhost:8899/trading-handbook.html`
8. git commit + push

## 图号规则

- 合成示意图按正文出现顺序编号 x-1..x-N；真实数据图带 R 后缀（如 10-3R）不参与编号。
- 图注标注"合成示意"/"真实数据"；真实图标注品种/日期/数据源。

## 审计状态

见 `handbook/README.md`（交叉引用悬空 0、图片引用完整、图号连续、渲染通过）。

# tools/ 脚本说明

所有命令**从仓库根目录运行**（脚本内路径为相对根目录的 `handbook/...`）。

## 流水线（每次迭代按序执行）

| 命令 | 作用 |
| --- | --- |
| `python tools/draw_handbook_figs.py` | 重绘全部合成示意图 → `handbook/images/`（新增/修改图后必须跑） |
| `python tools/_build_html.py` | 合并 handbook/ 全部 md → `handbook/trading-handbook.html`（单文件阅读版） |
| `python tools/_audit_all.py` | 统一跑 5 项审计并 UTF-8 汇总（见下），全部通过再推送 |

## 审计工具

| 脚本 | 检查内容 |
| --- | --- |
| `_xref_audit.py` | 交叉引用悬空（"第 x.y" 引用是否存在） |
| `_img_audit.py` | 图片引用与文件一一对应（缺失/未使用） |
| `_render_check.py` | 每章 md 能否正常渲染为 HTML |
| `_fignum_audit.py` | 各章图号连续无重复（R 真实图不参与） |
| `_html_check.py` | HTML 组件完整（TOC 锚点、抽屉、进度条） |
| `_figorder_check.py` | 各章图号是否按正文出现顺序递增（防乱序） |
| `_term_check.py` | 术语表关键词覆盖检查 |
| `_term_gap.py` | 正文高频英文术语 vs 术语表覆盖审计 |
| `_scan_ascii.py` | 代码块内 ASCII 图残留扫描（应全部替换为代码图） |

## 一次性工具

| 脚本 | 作用 |
| --- | --- |
| `_figrenum.py` | 图号按正文顺序重编号（占位符两步法，R 图不参与；修改前先跑 `_figorder_check.py`） |

## 真实数据图（独立数据源，需网络）

| 脚本 | 图 |
| --- | --- |
| `_real_figs.py` | 3.9/4.3/4.4/4.6 真实行情图（AkShare 上证指数/510300 ETF） |
| `_micro_fig.py` | 微通道真实图 |
| `_pair_fig.py` / `_pair_fig2.py` | 4.28 配对交易真实图（沪深 300/中证 500） |
| `_rv_fig.py` | 10.5 波动率均值回归真实图 |

> 历史一次性脚本与输出已归档至 `_archive/`（不参与手册构建）。

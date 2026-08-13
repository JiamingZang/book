# 交易手册（Markdown 版）

> **在线阅读版**：[trading-handbook.html](trading-handbook.html)（单文件合并版，浏览器直接打开，含封面、目录导航与移动端抽屉；由 `_build_html.py` 生成）
> **PDF 打印版**：[trading-handbook.pdf](trading-handbook.pdf)（347 页，159 图全嵌入，每章分页、全书书签 219 项、页脚页码；由 Edge headless 打印导出，内容与 md 同步）

> 基于 `trading-handbook.pdf` 拆分提取，并经逐章扩写优化：机制展开、算例补全、表格化、图片代码重绘。
> 配图全部由代码生成（135 张合成示意图 TradingView 风格 + 24 张真实行情图，脚本见 `draw_handbook_figs.py`、`_real_figs.py`、`_real_crypto_figs.py`、`_real_figs2.py`、`_real_figs3.py`、`_real_paint.py`、`_micro_fig.py`、`_pair_fig.py`、`_pair_fig2.py`、`_rv_fig.py`、`_batch45_figs.py`、`_batch45b_figs.py`、`_batch45c_figs.py`、`_batch46_figs.py`、`_batch47_figs.py`、`_batch48_figs.py`、`_batch67_figs.py`、`_batch67b_figs.py`、`_batch68a_figs.py`、`_batch68b_figs.py`、`_batch69a_figs.py`、`_batch69b_figs.py`、`_batch70a_figs.py`、`_batch70b_figs.py`、`_batch71a_figs.py`、`_batch71b_figs.py`、`_batch72a_figs.py`、`_batch73a_figs.py`、`_batch73b_figs.py`、`_batch74a_figs.py`、`_batch74b_figs.py`、`_batch75a_figs.py`、`_batch75b_figs.py`、`_batch76a_figs.py`、`_batch80a_figs.py`、`_fig_real_ch1_vol.py`、`_fig_real_ch8_backtest.py`、`_fig_real_ch9_eval.py`、`_fig_real_ch7_journal.py`、`_excal_to_mpl.py`），存放在 `images/`（其中 12 张流程图由 Excalidraw 源归档 `images/_excal_src/` 经 `_excal_to_mpl.py` 重绘为全库一致风格，并补上图号图注）。真实图（图号带 R 后缀，共 24 张）数据源为 AkShare 上证指数日线、510300 ETF 5 分钟线、沪深 300/中证 500 指数日线，以及 Binance BTCUSDT/ETHUSDT 5 分钟 K 线（`_fetch_binance.py` 拉取，数据在 `data/`，2026-06-29 ~ 08-13）。每张真实图均用 matplotlib 教学级渲染：红涨绿跌 K 线 + 箭头/文字框标注 + 支撑压力线/结构连线/EMA 均线/Volume Profile 等，图注标注品种/日期/数据源/涨跌幅；典型行情段由 `_find_segs.py` 系列脚本在真实数据中挖掘（spring、HH/HL 趋势、诱多下跌、巨量锤子线、扫 SSL 反转、Volume Profile、两段式移动、区间突破、sweep-CHoCH、均线趋势跟踪、波动率回归、配对价差、ATR 通道、移动止损、时段活跃度）。
> 已有机融合参考素材：洛氏霍克交易法（第 2/6/7 章）、威科夫 2.0（第 1/8 章）、雷神订单流（第 5 章）、南桥 5 分钟价格行为（第 3/4 章）、Al Brooks 十种最佳模式与缩写词典（第 3 章/附录）、阿布价格行为学（Brooks 课程中文翻译笔记，附录 C.3）、Ali 微通道与突破白皮书（第 3/4 章）、Tefi 交易本质课（太妃 PPT 系列 OCR）、学委知识库（宏观事件/概念卡片，第 1.8 节与术语表）；并补充基金/A 股/资产配置基础通识（第 1.16/1.17，编者）。
> 本手册为学习笔记性质，不构成投资建议。所有规则请在模拟账户验证 100+ 笔、确认期望值为正后再实战。

## 阅读结构

- **分层阅读**：前言含章节地图（【核心】/【进阶】/【查阅】三级）、三条阅读路径、全书概念地图、最小可用系统（一页跑起来）。
- **每章自测**：10 章章末均有「本章自测」，带答案解析，读完可自检。
- **第 4 章四篇**：篇一系统（4.1-4.11）+ 篇二出场（4.12-4.20）+ 篇三高级结构（4.21-4.25）+ 篇四补充系统（4.26-4.28：ORB/均线趋势跟踪/配对交易）+ 4.29 一个交易日走一遍（状态机串讲）。
- **进阶新增**：6.13 多策略资金分配（组合层风险预算）、8.12 订单流三件套（DOM/逐笔/Delta）、7.1 概率锚点速查表（★ 必记 3 个）。
- **审计状态**：章节编号全 10 章连续无重复（x.1 起）、图号连续无重复（含 R 真实图按正文顺序编号）、交叉引用悬空 0、图片引用 159/159 完整（无缺失无未用，图注全部可见且一一对应）、md 渲染验证全部通过。
- **排版风格**：参考《深入理解 AI Agent》（李博杰，ElegantBook 体系）——深藏青主题色 #1E3A6B、渐变封面页（打印独占一页）、章节横幅、自测题/小结标签、代码框左条、图注居中加粗、页脚页码、正文段首缩进 2em。

- [交易手册：价格行为 · SMC · 仓位 · 心态 · Prop 考核](00_cover_and_preface.md)
- [第 1 章 市场与工具全景](01_market_overview.md)
- [第 2 章 读懂价格行为](02_price_action.md)
- [第 3 章 入场信号](03_entry_signals.md)
- [第 4 章 交易系统：入场与出场](04_trading_system.md)
- [第 5 章 机构视角与流动性：SMC、Wyckoff、订单流的统一解读](05_smc.md)
- [第 6 章 仓位与风险](06_position_and_risk.md)
- [第 7 章 执行与心态](07_execution_and_mindset.md)
- [第 8 章 工具与验证](08_tools_and_validation.md)
- [第 9 章 Prop Firm 考核实战](09_prop_firm.md)
- [第 10 章 期权：交易的另一个维度](10_options.md)
- [附录 术语表与学习资源](11_appendix_glossary.md)

# 交易手册项目交接文档

> 给接手者的完整说明：项目现状、标准工作流、工具清单、关键规则、剩余待办。
> 最后更新：2026-08-13（批次 45c 完成后）

## 1. 项目速览

| 项 | 值 |
|---|---|
| 仓库 | `https://github.com/JiamingZang/book.git`（main 分支） |
| 工作目录 | `c:\Users\18315\Desktop\新建文件夹`（本地工作区，git 根目录） |
| 产物 | `handbook/` 下 13 个 md + `images/` 112 张图 + `trading-handbook.html`（单文件阅读版）+ `trading-handbook.pdf`（打印版） |
| 当前指标 | PDF 296 页、112 图全嵌入、书签 218 项、页脚页码；审计全绿（交叉引用悬空 0、图注 112/112 一一对应、图号连续无重复） |
| 内容 | 价格行为 · SMC · 仓位 · 心态 · Prop 考核 十 章 + 附录术语表；参考 ElegantBook 风格排版 |
| 持续指令 | 用户要求"每做完一批 git commit + push 一次"；优化方向"最好最易读最全面"，关注**真实数据图**与**缺图/缺图注**问题 |

## 2. 标准工作流（每次改完必走）

在 PowerShell（不支持 `&&`，用 `;`）中，工作目录 = 仓库根：

```powershell
cd "c:\Users\18315\Desktop\新建文件夹"

# ① 改 md 源文件（handbook/0X_第X章_*.md 或 images/ 新图）
# ② 重建单文件 HTML
python -X utf8 tools\_build_html.py

# ③ 全量审计（章节/xref/img/render/fignum/html 六项）
python -X utf8 tools\_audit_all.py

# ④ 图注一一对应审计（img 后 2 行内必须有 *图 X-X* 图注）
python -X utf8 tools\_capcheck_all.py

# ⑤ 图号序列审计（普通图按正文顺序连续；R 真实图独立序列）
python -X utf8 tools\_figseq_audit.py

# ⑥ 无图核心节扫描（找还缺图的【核心】小节）
python -X utf8 tools\_sec_nofig_scan.py

# ⑦ PDF 重导：Edge headless 打印（约 1-2 分钟，extension 报错是无害噪音）
powershell -ExecutionPolicy Bypass -File tools\_export_pdf.ps1
python -X utf8 tools\_pdf_outline.py   # 书签
python -X utf8 tools\_pdf_pagenum.py   # 页脚页码
python -X utf8 tools\_pdf_b45_check.py # 验证页数/图 xref/图注定位

# ⑧ 更新 handbook/README.md 的页数/图数/图注数
# ⑨ 提交推送
git add -A
git commit -m "批次XX: 改动摘要"
git push origin main
```

## 3. 工具清单（tools/）

### 画图（核心）
- `draw_handbook_figs.py` —— **画图风格基座**，导出 helper：`candle/hl_line/mark/annotate_mark/arrows/style_ax/savefig` 与配色 `UP=#26a69a(青涨)/DOWN=#ef5350(红跌)/DARK=#263238/GRAY=#90a4ae/ORANGE=#ff9800/TEAL`。新图脚本一律 `from draw_handbook_figs import ...` 复用；中文雅黑，双面板 figsize=(12, 5.9) dpi=160，输出到 `handbook/images/`。
- `_batch45_figs.py` / `_batch45b_figs.py` / `_batch45c_figs.py` —— 批次 45 系列画图脚本（可作新图的模板）
- `_real_figs.py` / `_real_figs2.py` / `_real_figs3.py` / `_real_crypto_figs.py` / `_real_paint.py` / `_micro_fig.py` / `_pair_fig.py` / `_pair_fig2.py` / `_rv_fig.py` —— 真实数据图脚本（fig_real_*.png）
- `_find_segs.py` / `_scan_segs*.py` / `_scan_days.py` / `_ema_scan.py` / `_analyze_*.py` —— 在真实数据中挖掘典型行情段（spring/诱多/锤子线/突破等）
- `_fetch_binance.py` —— 拉取 Binance BTCUSDT/ETHUSDT 5m 数据到 `data/`（CSV）

### 审计
- `_audit_all.py` —— 主审计入口（章节编号/交叉引用 xref/图片引用 img/渲染 render/图号 fignum/HTML）
- `_capcheck_all.py` —— **图注一一对应审计**（img 后 2 行内找 `*图 X-X*`，图号必须一致）
- `_figseq_audit.py` —— 图号序列审计
- `_sec_nofig_scan.py` —— 无图小节扫描（【核心】节补图的主要依据）
- `_figmap_dump.py <章节前缀>` —— 按行号 dump 某章全部图引用（重编号前必跑）
- `_fignum_audit.py` / `_figorder_check.py` / `_img_audit.py` / `_imgfmt_check.py` / `_img_diff_check.py` / `_check_figs.py` / `_cap_check.py` / `_cap_css_check.py` / `_dom_check*.py` / `_quiz_check.py` / `_term_check.py` / `_term_gap.py` / `_short_check.py` / `_readability_check.py` / `_scan_ascii.py` / `_xref_audit.py` / `_render_check.py` / `_nogap_scan.py` / `_fig_inventory.py` —— 单项审计工具
- `_figrenum.py` —— 图号重编号工具

### PDF
- `_export_pdf.ps1` —— Edge headless 打印 HTML→PDF（user-data-dir=edgepdf3）
- `_pdf_outline.py` —— 按 TOC 写书签（封面单独处理，1 条未定位属正常）
- `_pdf_pagenum.py` —— 页脚页码（跳过封面）
- `_pdf_*.py` 系列 —— PDF 验证（页数/图 xref/图注文本定位/像素采样）

### 构建
- `_build_html.py` —— md→单文件 HTML（提取 img alt 为居中加粗 figcap、删重复 em 图注、TOC 219、移动端抽屉）

## 4. 关键规则与坑（必读）

1. **R 图编号规则**：真实数据图（fig_real_*.png 共 19 张）图号带 R 后缀（2-1R、3-1R~3-3R、4-1R~4-9R、5-1R~5-3R、6-1R、10-3R），按正文出现顺序独立编号。**合成图绝对不能用 R**。新增真实图后：改图号 + 全章 R 序列顺延 + `_fignum_audit.py` 复核。
2. **图号顺延规则**：新图插入某节 → 图号按正文顺序定号，**其后所有普通图 +1 顺延**（img 行、figcap 行、正文引用"图 X-X"三处都要改）。第 2/3/4/6 章都执行过全量顺延，改前先 `_figmap_dump.py` 看全貌。
   - **陷阱**：正文里的日期如"3-13 起 7 天"（第 3 章 V 型反转案例）不是图号！正则必须带"图 "前缀，且排除 R 与数字后随（`图 3-(\d+)(?!R|\d)`）。日期"4-03/4-07"也不受影响。
   - **陷阱**：新插入的图号会被无差别顺延脚本误改——先插入并标号，再对"其后内容"做顺延，或顺延后手动把新图号改回。
3. **figcap 规则**：每张 img 后 2 行内必须有 `*图 X-X 描述*` 图注（HTML 构建时提取为可见图注；缺失 = 读者看不到图说明）。检查用 `_capcheck_all.py`。补图注 = img 后插 `*图 X-X <alt全文>*`。批量插入脚本会把已有图注的也插一遍造成重复——用 `_dedup_caps.py` 清理（保留最后一个）。img 后非空行的情况（如原图 4-13）需手工补。
4. **像素验证法**（模型不能直接看图）：pymupdf 打开 png，按步长采样统计主题色像素数验证内容存在（teal=#26a69a / orange=#ff9800 / down=#ef5350 / 蓝框 #1e3a6b 等）。
5. **PowerShell 陷阱**：内联 `python -c "..."` 里的引号会被吃掉——复杂逻辑一律写 .py 脚本执行；无 `&&`，用 `;`；`git push` 的 stderr 输出会让 exit code=1，但看输出里 `bfb3334..3eb6bbb main -> main` 即成功。
6. **grep 陷阱**：ripgrep 默认不支持 lookahead（`(?!R)` 返回 0 结果），用简单模式。
7. **git push 偶发故障**：GitHub 服务端 `Internal Server Error`（带 Request ID）——非本地问题，稍后重试即可（曾连续 5 次失败后自然恢复）。
8. **Edge 导出警告**：`managed_value_store_cache` / `fallback_task_provider` 报错是无害噪音，不影响 PDF。
9. **换行**：md 用 LF；git 会提示 LF→CRLF warning，无碍。
10. **自测答案引用**：改图号后自测答案里的"（图 X-X）"引用可能错位——用 `_quiz_check.py` + 人工核对答案与图内容对应关系（批次 45 靠顺延方案让答案自动对齐，是巧合也是教训：改图号时把自测答案一并检查）。

## 5. 剩余待办（按优先级）

### P0 补图（直接回应"好些地方没有"）
跑 `tools\_sec_nofig_scan.py` 找【核心】无图节，优先补：
- 第 4 章：4.9 海龟交易法则（仓位/退出规则示意图）、4.12 出场（期望值另一面）、4.18 一笔交易完整生命周期、4.19 完整案例（可做带时间轴的双面板）、4.1/4.2 系统六要素
- 第 6 章：6.3 连亏是必然（**已有概率图 6-4 破产，可补连亏路径示意**）、6.10 加仓、6.11 头寸心理
- 第 7 章：7.5 交易日志（日志字段模板图）、7.8 新手错误清单（思维导图式）
- 第 8 章：8.1~8.6 工具章六节全无图（图表/回测/日志/模拟/信息/防坑，可各补一张流程图）
- 第 9 章：9.2 平台选择、9.5 Funded 之后、9.6 出金合规、9.7 规则坑
- 第 10 章：10.1 期权直觉
- 第 1 章：1.2 品种对比、1.4 做多做空与合约规格、1.10 期货、1.13 加密货币

### P0 真实图扩充（直接回应"好些还不是真实的"）
当前真实图 19 张集中在 2/3/4/5/6/10 章；**第 1、7、8、9 章零真实图**。候选：
- 7.5 交易日志 → 真实账户净值/亏损曲线（可用合成但标注清楚，或从 prop 模拟数据画）
- 8.2 回测 → 真实数据回测权益曲线 + 回撤标注（data/ 有 BTC/ETH 5m CSV 可跑简单策略）
- 9 章 → 真实考核净值曲线（风险预算线 + 最大回撤线）
- 1.6/1.8 → 真实品种波动率对比（BTC vs ETH 5m 已有数据）
- 新真实图记得标 R 后缀并按 R 序列编号（见规则 1）

### P1 收尾与质量
- 批次 40 遗留：PDF 新风格视觉抽查（章横幅/图注/表格）——批次 39 后未人工抽查完
- 批次 33 遗留：跨章冗余审查——假突破家族（2.4/3.2/4.4）、概率表重复（突破失败率/反转概率）是否需融合
- `_quiz_check.py` 自测题全覆盖确认
- 学委知识库（batch36 已挖一轮）可再挖新概念补术语表

### P2 内容深化
- 10.5 波动率交易（IV/RV）细节补充
- 附录术语表持续同步新术语（ORB/DOM/Delta/配对交易/协整/Z-score/风险预算制已补）
- 每章"本章小结"可升级为速查卡

### 批次规划记录
- 批次 46+ 建议从 P0 补图开始，每批 3-5 张图 + 审计 + PDF + 推送；图多时拆两批（画图/审计推送）

## 6. 数据源与素材

- `data/btcusdt_5m.csv`、`data/ethusdt_5m.csv` —— Binance 5m K 线（2026-06-29 ~ 08-13，`_fetch_binance.py` 拉取）
- AkShare：上证指数 sh000001 日线、510300 ETF 5 分钟线、沪深 300/中证 500 日线（真实图脚本内联获取，需网络）
- 参考素材目录：`_ref_texts/`（OCR 文本）、`_ref_clean/`（清洗版）、`_pa_agent_ref/`（PA 策略文件 1-28）、`_ppt_text/`（太妃 PPT 系列）、`_ali_flashcards/`（Ali 卡片 1-802）、`_breakout_research/`（突破白皮书）、`英文著作 4本/`
- 手册内素材已融合：洛氏霍克（2/6/7 章）、威科夫 2.0（1/8 章）、雷神订单流（5 章）、南桥 5 分钟 PA（3/4 章）、Brooks 十种模式/缩写词典（3 章/附录）、阿布价格行为学（附录 C.3）、Ali 微通道/突破白皮书（3/4 章）、Tefi 课（太妃 PPT）、学委知识库（1.8/术语表）、基金/A 股/资产配置通识（1.16/1.17）

## 7. 最近提交记录（供参考）

- `3eb6bbb` 批次45b/45c：图2-3位置价值+图3-1判定框架+全库59处缺图注补齐+图号顺延(第2/3章)+PDF 296页112图
- `3eaf993` 批次45b：图2-3 位置决定价值（2.2核心节补图）+第2章图号顺延2-4~2-14
- `bfb3334` 批次45：补三张核心概念图（2-7趋势线/2-8缺口/4-7斐波那契）+真实图R标修正（4-8→4-5R、6-3→6-1R）+图号全量顺延
- 更早：批次39（ElegantBook 风格 CSS/封面/页码）、批次34-35（真实图 matplotlib 教学级重绘）、批次22（移动端抽屉目录）等

# Little Pig Stock

个人美股交易策略、分析和复盘仓库。

## 基本信息

- **持有人**：Kejing Yan
- **所在地**：Providence, RI（美东时间）
- **经纪商**：Robinhood（个人账户）+ IBKR（用户 5/14 提及,详情待补）
- **账户规模**：**$7,310.46**（Robinhood 真实账户总览,2026-05-29;持仓 $5,258.79 + 现金 $2,051.67,无加密）
- **历史净入金**：~$6,675（含 5/13 一笔 +$5,000;开户至今总盈利仅 ~+$635 / +9.5%）
- **风险偏好**：成长偏激进；账户层面回撤承受 ~-15-20%;单股 -25% 可接受;不能所有票一起 -25%
- **当前 YTD**：⚠️ **待核实**（旧记录称 +49%,但与完整交易历史对不上——真实账户回报约 +9.5%;+49% 可能指某早期阶段或单笔如 MU +39%,详见 `analysis/portfolio/2026-05-29_*.md` 第〇节）
- **当前持仓**（2026-05-29 实时）：CIEN 1 股（财报前已减 1 股）/ MU 1 股（另挂 $900 limit 加仓,建议撤）/ QCOM 3 股 / SPY ~1.375 股 / DTCR ~16.74 股 / **ASTS 5 股（5/29 再入 @$107.89）** / BB 30 股 + DJT 6/18 call + BB 6/12 call;NVDA/MRNA/BE/TSLA/BTC/GLD 等已全平

## 目录结构

```
.
├── README.md                                # 你在看的文件
├── strategy/                                # 策略框架
│   ├── framework_v0.8.md                    # 当前正式版框架（转录）
│   ├── framework_v0.8_original.pdf          # 原始 PDF
│   └── archive/
│       ├── CHANGELOG.md                     # 版本历史与变化
│       ├── framework_v0.6.md
│       └── framework_v0.6_original.pdf
├── analysis/                                # 所有分析,按用途分 3 个子目录
│   ├── INDEX.md                             # 索引（按日期 + 子目录速览）
│   ├── portfolio/                           # 持仓 / 操作复盘 / 客户画像 / 交易历史评分
│   │   ├── 2026-05-10_portfolio_review.md
│   │   ├── 2026-05-11_evening_decisions_review.md
│   │   ├── 2026-05-11_v0.8_framework_application.md
│   │   ├── 2026-05-11_deep_dive_asts_crwv_capital_deployment.md
│   │   ├── 2026-05-12_holdings_update_and_ops_review.md
│   │   └── 2026-05-14_trade_history_review_and_holdings_v3.md
│   ├── briefings/                           # 盘前简报 / 执行清单 / 情境手册
│   │   ├── 2026-05-11_pre_market_briefing.md
│   │   ├── 2026-05-11_execution_plan_and_asts_playbook.md
│   │   └── 2026-05-13_execution_checklist_and_optical_walkthrough.md
│   └── research/                            # 行业研究 / 标的 6 步评估 / 博主推文审查
│       ├── 2026-05-12_ai_datacenter_connectivity_bernstein.md
│       ├── 2026-05-14_4_sectors_deep_research.md
│       ├── 2026-05-14_4_sectors_deep_research.pdf
│       ├── 2026-05-14_baba_zhirun_thesis_review.md
│       └── 2026-05-14_nextronics_serenity_thesis_review.md
└── tools/                                   # 复用工具
    ├── tv_market_structure.pine             # TradingView 指标：顶底 + BOS/CHoCH + 回调参考区
    └── md_to_pdf.py                         # Markdown → PDF（中文 / xhtml2pdf + WenQuanYi）
```

## 策略框架（v0.8）

**散户事件驱动跟随策略 v0.8**（完成度 ~80%）

- 阶段 A：Pre-event Run-up ✅
- 阶段 B：PEAD ✅
- 阶段 C：Reverse PEAD ✅（v0.8 新增）
- 决策树 Stage A → B/C ✅
- L1/L2/L3 渐进激活 ✅

### 框架核心约束

| 约束 | 数值 |
|---|---|
| 单笔仓位上限 | 20% NAV |
| 同时持仓上限 | 2 个（A+B+C 任意组合） |
| 总账面事件暴露 | ≤ 40% NAV |
| 阶段 C L1 仓位 | 0%（仅识别） |
| Review 锁定 | 5 案例未审批不开新仓 |

### 框架边界

v0.8 是**纯事件驱动框架**，**不覆盖**：
- 核心 ETF 持仓（SPY/QQQ/SCHD）
- 单股长期持有（GOOG/ORCL/NVDA）
- 宏观对冲（GLD/BTC）
- 摩擦成本与税务

这些需要独立的"核心仓位管理规则"，目前未建立。

## 使用方法

### 每日工作流（建议）

1. 开盘前 30 分钟：查 `analysis/briefings/` 最新一份执行清单
2. 任何交易决策前：60 秒框架检查（阶段 A §5 / 阶段 C §8）+ 算这笔占 NAV 几 %
3. 看完任何研报 / 博主推文 / 新闻：**24h 内不准建仓**(冷静期)
4. 任何买卖完成后：3 行决策日志（为什么 / 反面理由 / 预期持有期）
5. 每周日：复盘本周交易，归档为 `analysis/portfolio/YYYY-MM-DD_*.md`
6. 每 5 个完整案例：触发 Review（命中率 + 偏差分析）

### 看到主题/标的想买的时候

1. 先看 `analysis/research/` 里是否已有评估
2. 没有的话,**自己**走 6 步清单(参考 `briefings/2026-05-13_..._optical_walkthrough.md` 第二部分,COHR 走过的实例)
3. 写出一行可证伪的 thesis（包含止损价位）
4. 算 sizing:≤ 8-10% NAV（单股）或 ≤ 5% NAV（赌场/期权）
5. 资金从砍现有相关仓位来,不净加风险敞口

### Claude Code 工作流（v0.8 PM 画像新增维度）

PM 已具备工具能力：**Python + yfinance + Claude Code**。
计划开发：
- 持仓监控脚本（每日浮盈、阶段 C Gate 自动检查）
- 决策日志模板自动化
- 5 案例 Review 自动统计

## 历史里程碑

- 2026-04-06：账户开户，首笔 SPY 买入
- 2026-04-30：MU 买入 @ $513（事后看是绝佳入场，5/13 卖在 $716 = +39% / +$79 单笔最大盈利）
- 2026-05-07：单日扫货 7 个标的（FOMO 高峰）
- 2026-05-08：v0.4 框架完成，阶段 A 全套规则
- 2026-05-10：v0.6 决策树完成；首次客户画像复盘
- 2026-05-10：v0.8 完整框架完成（主题 4），阶段 C 规则化
- 2026-05-11：v0.8 框架首次应用到实战决策（ASTS 财报应对,纪律性卖在 $82.85 锁 +25%）
- 2026-05-12：Bernstein AI 数据中心连接研报总结 + 持仓 v2 复盘 + 客户画像 v2 骨架
- 2026-05-13：de-scatter 执行清单 + COHR 6 步实例 + Pine 指标 v3(BOS/CHoCH + 参考区)
- 2026-05-14：核能/机器人/无人机/军工 4 板块深度研究 PDF + 持仓 v3 + 5/13 计划执行打分
- 2026-05-29：完整订单历史(4/6–5/28)轧差 → 持仓 v4 + 现金/NAV 全核算;发现账户口径问题(真实回报 ~+9.5% vs 旧称 +49%);两周高频翻仓纪律复盘;5/29 校准真实 NAV $7,310 + CIEN 减 1 股 + ASTS 再入复盘

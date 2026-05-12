# Little Pig Stock

个人美股交易策略、分析和复盘仓库。

## 基本信息

- **持有人**：PM
- **所在地**：美东时间
- **经纪商**：Robinhood（个人账户）
- **账户规模**：~$6,500-$8,500（持续加金中）
- **风险偏好**：成长偏激进，事件驱动 + 核心 ETF 混合
- **当前 YTD**：+49%（框架内提到）

## 目录结构

```
.
├── README.md                                # 你在看的文件
├── strategy/
│   ├── framework_v0.8.md                    # 当前正式版框架（转录）
│   ├── framework_v0.8_original.pdf          # 原始 PDF
│   └── archive/
│       ├── CHANGELOG.md                     # 版本历史与变化
│       ├── framework_v0.6.md                # 旧版本归档
│       └── framework_v0.6_original.pdf
├── analysis/
│   ├── INDEX.md                             # 分析索引（按时间倒序）
│   ├── 2026-05-13_execution_checklist_and_optical_walkthrough.md
│   ├── 2026-05-12_holdings_update_and_ops_review.md
│   ├── 2026-05-12_ai_datacenter_connectivity_bernstein.md
│   ├── 2026-05-11_execution_plan_and_asts_playbook.md
│   ├── 2026-05-11_v0.8_framework_application.md
│   ├── 2026-05-11_deep_dive_asts_crwv_capital_deployment.md
│   ├── 2026-05-11_evening_decisions_review.md
│   ├── 2026-05-11_pre_market_briefing.md
│   └── 2026-05-10_portfolio_review.md       # 起点：客户画像
└── tools/
    └── tv_market_structure.pine             # TradingView 指标：顶底 + BOS/CHoCH（看图辅助，非信号）
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

1. 开盘前 30 分钟：查 `analysis/INDEX.md` 最新一份简报
2. 任何交易决策前：60 秒框架检查（阶段 A §5 / 阶段 C §8）
3. 任何买卖完成后：3 行决策日志（为什么 / 反面理由 / 预期持有期）
4. 每周日：复盘本周交易，归档为 `analysis/YYYY-MM-DD_*.md`
5. 每 5 个完整案例：触发 Review（命中率 + 偏差分析）

### Claude Code 工作流（v0.8 PM 画像新增维度）

PM 已具备工具能力：**Python + yfinance + Claude Code**。
计划开发：
- 持仓监控脚本（每日浮盈、阶段 C Gate 自动检查）
- 决策日志模板自动化
- 5 案例 Review 自动统计

## 历史里程碑

- 2026-04-06：账户开户，首笔 SPY 买入
- 2026-04-30：MU 买入 @ $513（事后看是绝佳入场，YTD +47%）
- 2026-05-07：单日扫货 7 个标的（FOMO 高峰）
- 2026-05-08：v0.4 框架完成，阶段 A 全套规则
- 2026-05-10：v0.6 决策树完成；首次客户画像复盘
- 2026-05-10：v0.8 完整框架完成（主题 4），阶段 C 规则化
- 2026-05-11：v0.8 框架首次应用到实战决策（ASTS 财报应对）

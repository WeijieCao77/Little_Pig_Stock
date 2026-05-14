# 2026-05-11 执行计划 + ASTS 财报案例归档（v0.8 首个完整案例）

> 状态：周一开盘前的最终执行计划，所有决策已锁定
> 框架版本：v0.8（参考使用）
> 这是 v0.8 框架下**第一个会完整记录的案例**（虽然 ASTS/CRWV 入场早于 v0.8，属于"框架前持仓"）

---

## 一、周一（ET）执行清单

### 盘前/9:30 前
- [x] LITX 限价 buy 2 股 @ $47（已挂，9:30 后生效）

### 09:30:00 开盘（30 秒内完成）
- [ ] CRWV 市价卖 2 股（接受 -13.7% ≈ -$36）
- [ ] SCHD 市价卖 4.89 股全部（≈ +$150）
- [ ] MU 挂 trailing stop @ $700（锁 +36% 底；框架外自加机制）
- [ ] SNDK 挂 trailing stop @ $1,400（锁 +3.5% 底；缓冲设大因日内波动 ±5-8%）
- [ ] 取消 AAOI pending limit buy
- [ ] DRAM ETF 买入（建议 $200 不 $500：NAV 溢价 5.6% + 23 天连续流入 = 顶部信号）

### 09:30 后
- [ ] 不盯盘 LITX（限价单自动处理）
- [ ] AAOI/PFE/MRNA/QCOM 仅观察（MRNA 入场窗口 7/25-8/3）

### 15:30 ET — ASTS 决策点
看 ASTS 当前价：
- **≥ $80**（预热到位）→ 市价卖 4 股全部 → 锁 ≈ +$60 vs 当前 / +$95 vs 成本
- **< $80**（平稳或下跌）→ 市价卖 2 股 → 锁 ≈ +$17 vs 成本；留 2 股裸赌财报
  - ⚠️ **不挂 stop**（stop/trailing stop 盘后不触发，挂了白挂）
  - 接受 2 股下行 -40% = -$25 vs 成本（在可接受范围）

### 16:00 收盘 → 16-17:00 ASTS 财报盘后

### 周二 09:30 ET
- [ ] 看 ASTS 财报结果 → 按"四情境手册"（见下）操作
- [ ] 不抄底，先观察 24h
- [ ] LITX：如 $47 成交了 → 按计划周二卖；没成交 → 取消挂单

---

## 二、ASTS 财报四情境手册

**前提**：周一已卖 2-4 股，手上剩 0-2 股。

### 情境 1：大 Beat + BlueBird 解释充分 — 盘后 +20%+（概率 ~12%）

- 营收 beat $40M+、现金消耗低于预期、BlueBird-7 有补救方案
- ASTS 跳到 $90+
- **v0.8 路径**：Step 1 → 路径 1 → Step 2A（跳涨 ≥5%）→ Stage B 候选
- **操作**：
  - 周二开盘**不追**（框架："Stage B 接受错过完整第一波"）
  - 如果还持有 2 股 → 周二开盘市价卖，锁利润
  - 不重新建仓（Review 锁定 + L1 状态）
- **心理**：$35-$60 锁定利润是真实的，没有"少赚"

### 情境 2：温和 Beat / In-line — 盘后 ±5%（概率 ~30%）

- 营收 $36-40M、EPS 接近共识、BlueBird 提及但无明确补救
- ASTS 在 $71-78
- **v0.8 路径**：
  - 如反应 ±2% 内 + Volume 异常 ✅ → Step 2B 触发 → **Stage C L1 识别**
  - 如反应 -3% 到 -5% → Step 2B fail → 不做
- **操作**：
  - 持有的 2 股 → 周二开盘市价卖（平/微盈出）
  - 如 Stage C 触发 → 写完整 Stage C L1 日志（计入 5 案例毕业进度）
  - 不交易（L1 = 0% 仓位）

### 情境 3：温和 Miss / BlueBird 拖累 — 盘后 -5% 到 -15%（概率 ~35%）

- 营收 $35M、现金消耗加速、BlueBird 影响 2026 部署（少 5-7 颗）
- ASTS 跌到 $64-71
- **v0.8 路径**：Step 1 → 路径 3 边界；Step 2C 跳跌 5-15% + L1 → 识别但不做空
- **注意**：这不算"反应平淡"，所以**不是 Stage C 触发**（即时下跌 ≠ 延迟漂移）
- **操作**：
  - 持有的 2 股 → 周二开盘市价卖（止损 -$8 到 -$25 vs 成本）
  - **不抄底**（$66 卖出是因 EV 负，财报后不确定性更高）
  - 写日志记录现象

### 情境 4：大 Miss + BlueBird 灾难 — 盘后 -20%+（概率 ~23%）

- 营收 miss 显著、BlueBird 失败 + 后续延期 + 客户重谈、部署目标大幅下修
- ASTS 跳水到 $50-60
- **v0.8 路径**：Step 1 → 路径 3（暴雷）；Step 2C 跳跌 >5% + L1 → 仅识别避险
- **操作**：
  - 持有的 2 股 → 周二开盘市价卖（止损 -$25 到 -$50 vs 成本）
  - **绝不抄底**（结构性问题，卫星发射失败不是噪音）
  - 写 Stage C L1 识别日志 ⭐（这次识别 + 后续 24-36h 观察可计入 L1 → L2 毕业进度）
  - 一周后评估是否值得作为新的阶段 A 候选（下次催化剂 7-8 月卫星部署更新）

### 四情境统一原则
1. 不要因 ASTS 后续走势责怪自己 5/11 的决定（EV 看过程不看结果）
2. 不在周一盘后 / 周二 pre-market 下单（流动性差）
3. 任何情境先观察 24h（框架："Stage B 接受错过第一波"）
4. 每个情境都写日志（5 案例 Review 的第一个完整案例）
5. L1 = 0% 仓位，无例外

### ASTS 持仓机会成本表（你卖出后）

| 情境 | 概率 | 没卖的 4 股 P/L（vs 成本 $265）| 你锁定（卖 2-4 股）|
|---|---|---|---|
| 1. 大 Beat +20% | 12% | +$95 | +$17 ~ +$60 |
| 2. In-line ±5% | 30% | +$5 ~ +$15 | +$17 ~ +$60 |
| 3. 温和 Miss -10% | 35% | -$30 | +$17 ~ +$60 |
| 4. 大 Miss -20%+ | 23% | -$55 ~ -$85 | +$17 ~ +$60 |

**期望持仓 P/L ≈ -$8.85；锁定 +$17 到 +$60 → 比期望多赚 $26 到 $69**

---

## 三、LITX 迷你案例（框架外教学练习）

**注意**：这不属于事件驱动框架范畴（LITX 是 2x 杠杆 ETF，非"中大盘行业龙头"）。
记录在此作为"看到任何 2x/3x ETF 衍生品时的参考"。

### 标的
- LITX = Tradr 2X Long LITE Daily ETF（Lumentum 的 2x 每日杠杆）
- 催化剂：LITE 5/18 加入 Nasdaq-100，替代 CSGP（5/8 公告）
- 当前 ~$48.82（5/8 close），过去 1 周 -8.23%

### 为什么不买 LITX call（已否决）
- $60 Call 5/15：23.7% OTM + 4 天到期 + bid-ask 45%（$0.55/$1.00）+ 4 层杠杆衰减叠加
- 即使加入指数纳入催化剂，mid-price EV +$80，但 ask-price 后 EV 大幅缩水
- **更致命**：5/15 到期 < 5/18 生效日 → 错过最大单日 pop

### 实际方案：限价 buy 2 股 @ $47
- 9:30 后生效，-3.7% 折扣
- 成交概率 ~55%；不成交则保留现金
- 计划：周二卖出（1 天动量交易）
- **更优本应**：持有到 5/18 生效日卖（EV +$5-8 vs 1 天的 +$1），但用户选 1 天
- 风险对冲：如成交，挂 -10% stop @ $42.30（盘内有效）

### 教学要点
1. 2x/3x 杠杆 ETF 有 vol decay，期权再叠加 theta = 双重衰减
2. 杠杆 ETF 的期权 bid-ask 极宽（流动性差）
3. 指数纳入催化剂的最大涨幅在**生效日当天**，不是公告日
4. 散户陷阱：Robinhood 默认推最近到期（最便宜=最高 theta）
5. 想吃催化剂用现货或更长到期，别用最近到期的 OTM call

---

## 四、关键技术备忘：Robinhood Stop 订单的时段限制

| 订单类型 | 常规时段 9:30-16:00 | 盘前/盘后 | 24 小时市场 |
|---|---|---|---|
| Market | ✅ | ❌ | ❌ |
| Limit | ✅ | ✅（需开 extended hours）| ✅（部分股票）|
| **Stop loss / Trailing stop / Stop limit** | ✅ | **❌ 不触发** | **❌ 不触发** |

**含义**：
- 财报盘后公布（如 ASTS 5/11 4-5pm）→ stop 类订单**不会保护你**
- 跳空发生在盘后 → stop 在周二 9:30 开盘才激活 → 成交在**跳空后的开盘价**
- 唯一真正的财报跳空保护 = **在 4pm 常规收盘前主动卖出**
- 碎股（fractional shares）连 stop 都不能挂；整股能挂但时段限制照样适用

---

## 五、本次决策对 v0.8 框架的对照

| 决策 | v0.8 对照 | 结果 |
|---|---|---|
| 卖 SCHD | PM 画像不符（不要红利） | ✅ 符合 |
| 卖 CRWV | 错过阶段 A 窗口 | ✅ 止损合理 |
| ASTS ≥$80 全卖 / <$80 卖 2 留 2 | 兜底层 1（财报前清仓）的妥协版 | ⚠️ 部分违规（留 2 股赌财报），但下行可控 |
| MU/SNDK trailing stop | 框架外（非事件驱动持仓）| N/A |
| DRAM ETF | 框架外（板块配置）| N/A |
| LITX 现货 | 框架外（杠杆 ETF）| N/A |
| 不买 LITX/COIN/CONL call | "不投机"原则 | ✅ 符合 |
| 保留 DJT call | 历史违规，损失上限 $17 | ❌ 不符合，用户接受 |

**5 案例 Review 锁定状态**：技术上你有 ≥5 个事件驱动相关案例（CRWV/ASTS + 这次的决策），但都未按框架完整 Review。**严格执行 v0.8 = 完成首次 Review 后才能开真正的阶段 A/B/C 新仓**。本文档可作为 Review 起点。

---

## 六、数据来源

- ASTS 现价/财报：[Yahoo ASTS](https://finance.yahoo.com/quote/ASTS/), [TipRanks IV ±19.9%](https://www.tipranks.com/news/ast-spacemobile-asts-q1-earnings-on-deck-options-traders-brace-for-a-19-9-price-swing), [BlueBird-7 失败](https://www.foreignpolicyjournal.com/2026/05/06/ast-spacemobile-nasdaq-asts-stock-price-closes-at-68-43-as-bluebird-7-fallout-weighs-on-execution-narrative/)
- LITE 加入纳指 100：[Nasdaq 官方公告 5/18 生效](https://www.nasdaq.com/press-release/lumentum-holdings-inc-join-nasdaq-100-indexr-beginning-may-18-2026-2026-05-09)
- LITX = Tradr 2X Long LITE：[Tradr ETFs 官网](https://www.tradretfs.com/litx)
- CRWV 分析师 PT $85-$155：[The Street](https://www.thestreet.com/investing/stocks/wells-fargo-revamps-coreweave-stock-price-target-for-2026)
- DRAM ETF 顶部信号：[CNBC "hottest ETF since bitcoin-mania"](https://www.cnbc.com/2026/05/08/the-hottest-etf-since-bitcoin-mania-just-added-1-billion-in-a-day.html)
- 美伊战争 5/10-11：[CNN](https://www.cnn.com/2026/05/10/world/live-news/iran-war-news), 油价 [CNBC](https://www.cnbc.com/2026/05/07/oil-prices-today-trump-iran-strait-of-hormuz-us-crude-brent-.html)

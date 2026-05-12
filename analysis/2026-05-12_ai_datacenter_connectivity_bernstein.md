# 2026-05-12 Bernstein《Inside the War for AI Data Center Connectivity》总结 + 散户视角分析

> 来源：Bernstein 2026-05 白皮书《Artificial Intelligence: Inside the War for AI Data Center Connectivity》
> 性质：**结构性 / 主题研报**，不是事件驱动催化剂 → 不进 v0.8 框架，属于 Layer 1（标的池 / watch list）输入
> 重要说明：教育性梳理，不是投资建议。最终扣扳机的是你自己。

---

## 一、研报一句话

AI 数据中心的瓶颈正在从「算力」转向「连接」——数据在机柜内 / 机柜间 / 集群间怎么移动，
成了新的性能瓶颈和资本开支主战场。铜和光不是谁取代谁，而是**按距离 / 功耗 / 成本分工共存**。

两类连接：
- **Scale-up**：机柜内、近距离、高带宽（GPU↔GPU↔switch chip）→ 短期铜为主
- **Scale-out**：机柜间、集群间、网络交换（InfiniBand / Ethernet / 光模块 / 交换机）→ 光学（CPO）先从这里渗透

---

## 二、五个核心要点（压缩版）

### 1. CPO（co-packaged optics）：方向确定，放量不快

把 optical engine 挪到更靠近 switch chip / XPU 的地方 → 降损耗、降功耗、提带宽密度、提网络可靠性。

- NVIDIA 口径：CPO 交换机 vs 传统可插拔光模块——功耗效率 ×3.5、信号完整性 ×63、网络韧性 ×10、部署速度 ×1.3
- 传统 1.6Tbps 光模块 ≈ 30W，DSP 占一半以上
- Broadcom：CPO switch 每 bit optics cost 低 40%；Meta 测 Bailly CPO（51.2T）省 >500W
- Bernstein 测算：CPO 总成本至少比传统可插拔**高 ~10%**（BOM 可能降，但价值被上游半导体 / 交换机厂重新分配）；optical engine ≈ CPO BOM 的 45%

**节奏（关键）**：2026 H2 小批量出货（主要 scale-out，验证用）→ 真正大规模放量 **2028**；scale-up 里的 CPO 更晚（~2028 H2，高价值 XPU 不接受未验证的可靠性风险）。
慢的四个原因：服务性差（坏了可能换整台 switch / 返厂）、良率难、测试复杂、供应链集中（CSP 议价能力下降）。

### 2. TSMC COUPE：CPO 平台化的抓手

hybrid bonding 把 EIC + PIC 结合，上方精密附加 micro lens + FAU。研报认为 NVIDIA 和 Broadcom 都会转向 COUPE 路线。TSMC 直接 CPO/硅光收入贡献不大，但强化其 wafer / SoIC / CoWoS / 先进封装生态壁垒。
受益链条：optical engine、CW laser、FAU 光纤阵列、测试设备、先进封装平台、光学耦合 / 微光学零件。
点名方向：Chroma ATE、Lumentum、Coherent、TFC、Senko、FOCI、ficonTec。

### 3. 铜不会马上退出，CPC 延寿

铜：低功耗 / 低成本 / 高可靠，但带宽越高距离越短。224Gbps 下——passive DAC ≈ 2m、AEC ≈ 7m、>10m 光占优（rack-to-rack / intra-DC / DCI）。
**CPC（co-packaged copper）**：把高速铜缆连接器直接集成进 ASIC / switch package，绕开 PCB trace 损耗，让 448Gbps 级铜链路技术上仍可行 → 这是 Luxshare 的逻辑（GB300 铜连接新供应商，可能参与 Vera Rubin）。

### 4. PCB / HDI / ABF / 上游材料——2026 最确定的「价值量提升」

- 2025 全球 PCB ≈ 850 亿美元；HDI ≈ 160 亿（占 PCB ~18%）
- Blackwell rack：HDI+PCB 单 GPU 价值量 vs Hopper 约翻倍至 ~$300
- MLPCB 层数：主流 16+ 层 → Vera Rubin midplane 40+ 层 → Rubin Ultra backplane 可能 70+ 层
- CCL 占 PCB 成本 ~30%（其中铜箔 ~40% / 树脂 ~25% / 玻纤布 ~20%）
- 材料升级：Megtron 6 → M8 → 2026 评估 M8.5/M9；M9 可能用于 224Gbps AI server，成本可达 M6 的 5–10×

### 5. 卡点：T-glass / ABF film / HVLP 铜箔——供应偏紧支撑 2026 利润

- Ajinomoto 在 ABF film 市占率 ~95%（近垄断）；Functional Materials 利润率 ~54%，贡献近 1/3 业务利润；AI 在 ABF volume 占比 FY3/24 ~11% → FY3/27 ~23%
- Nittobo（T-glass 关键供应商）新增产能 2027 初才释放 → 2026 T-glass 仍偏紧
- 传导：Unimicron ABF substrate ASP 2026 每季度涨 5–7%，AI 占其收入 2026 ~50%

---

## 三、供应商地图 + Bernstein 评级（原文）

| 环节 | 公司 | 散户可买性（Robinhood） |
|---|---|---|
| CPO / 硅光平台 | **TSMC**、**NVIDIA**、**Broadcom** | TSM / NVDA / AVGO 均美股可买 ✅ |
| 光学组件 / 激光 | **Lumentum**、**Coherent** | LITE / COHR 美股可买 ✅ |
| 测试设备 | Chroma ATE | 台股 ❌（散户难买） |
| 铜连接 / CPC | Luxshare | A 股 002475.SZ ❌ |
| ABF substrate | Ibiden、Unimicron | 日股 / 台股 ❌ |
| HDI | Victory Giant、Unimicron | A 股 / 台股 ❌ |
| MLPCB | WUS、Victory Giant、Unimicron、TTM、ISU、Gold Circuit、Shengyi Electronics | 仅 TTM（TTMI）美股可买 ✅，其余 ❌ |
| CCL | Doosan、EMC、Shengyi Tech | 韩股 / 台股 / A 股 ❌ |
| ABF film | Ajinomoto | 日股 2802.T ❌ |
| T-glass | Nittobo | 日股 3110.T ❌ |

**Bernstein 覆盖评级 / 目标价**：
NVIDIA Outperform $300｜Broadcom Outperform $525｜TSMC Outperform $351 / NT$2,200｜Chroma ATE Outperform NT$1,660｜Luxshare Outperform CNY86｜Unimicron Outperform NT$610｜Ibiden Outperform JPY9,200｜Ajinomoto Market-Perform JPY5,100｜Largan Market-Perform NT$2,600

**投资节奏（研报口径）**：① 2026–2027 别幻想 CPO 全面替代——方向对，但要可靠性 / 成本 / 供应链成熟；② 眼前更确定的是 PCB/HDI/ABF/材料的价值量提升（Rubin / Rubin Ultra 拉动 midplane / backplane / substrate 面积和层数）；③ 长期壁垒在平台型 / 卡位型公司（TSMC COUPE/CoWoS、NVIDIA/Broadcom 交换芯片生态、Ajinomoto ABF film、Ibiden/Unimicron 高端 substrate、Luxshare 铜连接升级）。

**研报列的风险**：CPO 可靠性验证不及预期；CSP 继续偏好可插拔光模块、CPO 推迟；PCB/HDI/ABF 2026–27 扩产过快、2027 后毛利率回落；T-glass/ABF/铜箔涨价侵蚀下游利润；Rubin/Rubin Ultra 放量节奏变化；AI capex 放缓。

---

## 四、散户视角分析（这跟你的组合有什么关系）

### 1. 先泼一盆冷水：这是研报，不是催化剂

v0.8 框架是**纯事件驱动**（Stage A run-up / B PEAD / C reverse PEAD，全部围绕「合格催化剂」）。
一篇行业白皮书**不是催化剂**——它没有明确的事件日、没有 Beat/Miss、没有盘后跳涨。
所以：**不要因为读了这篇就去开仓任何「连接」标的**。它的正确归属是 Layer 1 的 watch list / 主题池输入，
以及未来「核心/卫星仓位管理规则」（README 明确说**还没建**）要考虑的产业背景。

按你自己的铁律第 1 条：「写不出『为什么买 / 哪止损 / 哪止盈』就不买」——「Bernstein 看好连接」**不构成**一句话理由。

### 2. 大部分受益标的你根本买不到

研报最硬的卡位股——Luxshare、Unimicron、Ibiden、Ajinomoto、Chroma ATE、Nittobo、WUS、Victory Giant——
全在 A 股 / 台股 / 日股 / 韩股，Robinhood 个人账户**够不着**。
能买的只有：**TSM、NVDA、AVGO、LITE、COHR、TTMI**，外加 ETF（QQQ / SOXX / GRID / DTCR）间接沾边。
对一个 $6.5–8.5K、单仓上限 10% 的账户，这意味着「连接主题」**最多就是 1–2 个卫星仓 + ETF**，不值得为它重构组合。

### 3. 跟你现有持仓的映射

| 你的持仓 | 与本研报的关系 | 含义 |
|---|---|---|
| **NVDA**（1 股，"加到 3 股 or 清掉"待决） | 研报的核心受益方之一（CPO 交换芯片生态、Rubin/Rubin Ultra 平台、COUPE） | **提供「加到 3 股变核心仓」一侧的论据**——但论据不等于扣扳机；仍受出口管制推文风险（见 5/10 复盘）。这篇可以作为「NVDA 二选一」决策时的一个加权项，不是单独理由 |
| **GRID**（智能电网 ETF） | 间接——AI 数据中心电力 / 基建需求 | 逻辑被研报侧面强化，但 GRID 是电力侧不是连接侧；5/10 复盘已定「持有不加，跌破 $180 减半」，研报**不改变**这个结论 |
| **DTCR**（数据中心 ETF） | 间接——数据中心 capex 主题 | 同上，与 GRID/QQQ 主题重叠；5/10 复盘已定「持有但不加，下次调仓可合并」，研报**不改变** |
| **ORCL**（AI/云） | 弱相关——CSP 侧需求方，不是连接供应链 | 无新增动作 |
| **MU / SNDK**（存储） | **不相关**——研报讲的是「连接」，不是 HBM/DRAM；别把这篇当成存储利好 | 仍按 5/10 复盘：二选一保留 MU，SNDK 减仓 |
| **QQQ**（纳指 100） | NVDA/AVGO/TSM 都在里面，是你**已经持有的、最稳的连接主题敞口** | 真想加连接主题，按框架优先级——先加 QQQ，而不是去追单一连接小盘股 |

### 4. 如果（仅仅是如果）你想加一点主题敞口——优先级

1. **加 QQQ**（核心仓还没到 15% 目标）——NVDA+AVGO+TSM 一揽子，零选股风险，符合 5/10 复盘方向
2. **NVDA 加到 3 股**——把现有 1 股「鸡肋仓」变成有意义的卫星仓；本研报是支持项之一；上限 10% NAV
3. 最多再考虑**一个**纯连接卫星仓（AVGO / TSM / LITE / COHR 里选一个，**只选一个**），仓位 ≤ 6–10% NAV，并且必须能写出独立的入场/止损逻辑——否则不开
4. **不碰** AAOI 这类光通信小盘股（5/10 复盘已经判过「没想清楚就别买」，这篇研报里 AAOI 根本没被点名）

### 5. 时间轴——别把 2028 的故事按 2026 的价格买

- **2026**：兑现的是 PCB/HDI/ABF/材料的价值量提升 + 铜连接（CPC）平台迁移红利——但这条线**几乎全是亚洲股**，散户够不着
- **2026–2028**：scale-up 仍以铜为主，CPO 小量验证
- **2028+**：CPO 大规模放量——这是「星辰大海」，但**离现金流还有 2 年**

研报自己都说 CPO 总成本比传统方案高 ~10%，放量靠可靠性/供应链成熟——所以市场上任何「CPO 概念暴涨」短期都更像情绪而非业绩。
按你 5/10 复盘的教训（5/7 单日扫货 7 只、FOMO 顶部建仓）：**主题研报最危险的用法，就是读完立刻冲概念股**。

### 6. 一句话结论

> 这篇研报对你的实际意义是：**给「NVDA 二选一」的「加仓」一侧加一票，给「QQQ 还要加」再加一个理由**——
> 仅此而已。不重构组合、不追连接概念小盘股、不把它当存储利好、不当它是事件催化剂。
> 真正的连接红利大头（Luxshare / Unimicron / Ibiden / Ajinomoto）你买不到，认了。

---

## 五、待办 / 跟踪触发条件

- [ ] 把 **AVGO / TSM / LITE / COHR** 加入 watch list（仅观察，不建仓）——若未来要开「连接卫星仓」，从这 4 个里选 1 个
- [ ] 「NVDA 二选一」决策时，把本研报列为「加仓侧」的一个加权项（不是决定项）
- [ ] 关注 NVIDIA / Broadcom 财报里关于 CPO 出货节奏、Rubin/Rubin Ultra 量产时间的口径变化（这才可能成为 v0.8 意义上的催化剂）
- [ ] 「核心/卫星仓位管理规则」建立时，把「AI 基建/连接」作为一个主题桶纳入，避免 GRID+DTCR+QQQ+NVDA 主题重叠失控

#!/usr/bin/env python3
"""
Little Pig Stock — 组合统计 + 图表生成器(DASHBOARD 的单一数据源)

用法:
    python3 tools/portfolio_stats.py

更新流程(每次拿到新交易记录时):
    1. 往下面 LEDGER 里按时间追加新成交(date, ticker, side B/S, qty, price)
    2. 更新 PRICES(当前持仓的最新价)和 ACCOUNT(账户总览快照)
    3. 运行本脚本 → 自动:
         - 重算 已实现/未实现/总盈亏、逐票盈亏、四桶占比
         - 重新生成 assets/pnl_curve.png 和 assets/pnl_by_ticker.png
         - 打印一段 Markdown,可直接粘进 DASHBOARD.md
依赖:matplotlib(pip install matplotlib)
"""
from collections import defaultdict
import datetime

# ── 1. 账户总览(从 Robinhood 账户页抄真实值)─────────────────────────
ACCOUNT = {
    "as_of": "2026-05-29",
    "nav": 7310.46,          # Total in Robinhood
    "cash": 2051.67,         # 现金(CIEN 减仓后约 2598,这里用快照值)
    "net_deposits": 6675.08, # 历史净入金(含 bonus)
}

# ── 2. 当前持仓最新价(用于未实现盈亏)──────────────────────────────
PRICES = {
    "MU": 923.52, "CIEN": 546.11, "QCOM": 248.82, "SPY": 754.65,
    "DTCR": 31.72, "ASTS": 130.79, "BB": 8.78,
}

# ── 3. 四桶目标(策略 v1.0)────────────────────────────────────────
BUCKETS_TARGET = {"现金": 1250, "核心": 1250, "卫星": 4160, "赌场": 650}

# ── 4. 完整成交台账(只放 FILLED 的股票/加密;期权单列见 OPTIONS)──────
LEDGER = [
 ("2026-04-06","SPY","B",0.303421,659.15),("2026-04-09","DTCR","B",5.738332,26.14),
 ("2026-04-10","SCHD","B",4.889178,30.68),("2026-04-14","CIBR","B",1.591723,62.83),
 ("2026-04-14","GRID","B",0.005516,181.27),("2026-04-16","SPY","B",0.071313,701.13),
 ("2026-04-16","CIBR","B",1.524855,65.58),("2026-04-16","QQQ","B",0.312827,639.33),
 ("2026-04-22","NFLX","B",1,93.12),("2026-04-22","PLD","B",1.23235,142.01),
 ("2026-04-22","GOOG","B",0.146732,333.94),("2026-04-23","CIBR","S",1,66.00),
 ("2026-04-27","CRWD","B",0.329745,454.90),("2026-04-27","PLD","S",1.23235,141.36),
 ("2026-04-28","NFLX","S",1,90.58),("2026-04-30","CIBR","S",2.116578,67.28),
 ("2026-04-30","MU","B",0.389552,513.41),("2026-04-30","NVDA","B",1,203.31),
 ("2026-04-30","CRWD","S",0.329745,438.69),("2026-05-06","CRWV","B",2,132.00),
 ("2026-05-07","BTC","B",0.00246281,81206.55),("2026-05-07","ASTS","B",4,66.23),
 ("2026-05-07","GLD","B",1,436.51),("2026-05-07","GRID","B",2,195.39),
 ("2026-05-07","GOOG","B",0.887423,394.40),("2026-05-07","SNDK","B",0.369773,1352.18),
 ("2026-05-07","SNDK","B",0.000724,1379.95),("2026-05-07","ORCL","B",3,194.52),
 ("2026-05-10","BTC","S",0.00246281,79893.99),("2026-05-10","MEM","B",10,55.15),
 ("2026-05-10","SCHD","S",4.889178,31.82),("2026-05-11","BTC","B",0.00614242,81398.61),
 ("2026-05-11","CIEN","B",2,580.00),("2026-05-11","ASTS","S",4,82.85),
 ("2026-05-11","CRWV","S",2,112.88),("2026-05-11","GLD","S",1,436.89),
 ("2026-05-12","BTC","S",0.00614242,79163.54),("2026-05-12","DTCR","B",11,30.60),
 ("2026-05-12","SPY","B",1,737.84),("2026-05-12","MEM","S",10,48.83),
 ("2026-05-12","ORCL","S",3,182.92),("2026-05-12","GOOG","S",1.034155,381.99),
 ("2026-05-12","CIEN","S",2,551.34),("2026-05-12","MU","S",0.389552,716.05),
 ("2026-05-12","SNDK","S",0.370497,1387.42),("2026-05-12","QQQ","S",0.312827,703.46),
 ("2026-05-12","MRNA","B",6,53.57),("2026-05-12","QCOM","B",3,212.19),
 ("2026-05-12","GRID","B",2,196.51),("2026-05-12","ASTS","B",2,73.22),
 ("2026-05-12","CIEN","B",1,577.38),("2026-05-12","MEM","B",10,51.98),
 ("2026-05-13","CIEN","S",1,546.00),("2026-05-13","ASTS","S",2,80.90),
 ("2026-05-13","GRID","S",4,187.76),("2026-05-14","MRNA","S",6,49.27),
 ("2026-05-15","MEM","B",3,51.17),("2026-05-19","BE","B",2,251.00),
 ("2026-05-19","MU","B",1,696.92),("2026-05-20","GRID","S",0.005516,188.16),
 ("2026-05-20","MEM","B",4,50.63),("2026-05-20","NVDA","B",1,224.00),
 ("2026-05-21","SATS","B",5,130.20),("2026-05-21","NVDA","B",2,219.00),
 ("2026-05-22","TSLA","B",1,427.23),("2026-05-22","BE","S",2,306.58),
 ("2026-05-22","SATS","S",5,120.90),("2026-05-26","BB","B",30,8.63),
 ("2026-05-26","MEM","S",17,59.59),("2026-05-26","MU","S",1,875.15),
 ("2026-05-27","MU","B",1,900.00),("2026-05-27","MU","S",1,900.00),
 ("2026-05-27","MU","B",1,909.78),("2026-05-27","CIEN","B",1,582.99),
 ("2026-05-28","TSLA","S",1,441.77),("2026-05-28","NVDA","S",4,213.35),
 ("2026-05-28","CIEN","B",1,571.31),("2026-05-29","ASTS","B",5,107.89),
 ("2026-05-29","CIEN","S",1,546.11),
]
# 数据缺口手工修正:LITE2X(首笔买入在 PDF 覆盖范围外,净额 -5.83);TSLA 赠股 +5.65
MANUAL_REALIZED = {"LITE2X": -5.83, "TSLA_bonus": 5.65}
OPTIONS_REALIZED = {"NVDA calls (5/15)": 157.0}   # 已平仓期权
OPTIONS_OPEN = {"DJT $15C 6/18": 17.0, "BB $9C 6/12": 62.0}  # 仍持有(按成本)

# 卫星桶主题归类(用于分散度展示)
THEME = {"MU":"AI硬件","CIEN":"AI光通信","QCOM":"半导体","ASTS":"太空",
         "SPY":"核心","DTCR":"AI数据中心","BB":"投机/软件"}


def fetch_live_prices():
    """本地有网时用 yfinance 拉实时价并更新 PRICES;无网/没装则保留手填值(优雅回退)。"""
    try:
        import yfinance as yf
    except ImportError:
        print("[价格] 未装 yfinance → 用手填 PRICES。本地启用实时价: pip install yfinance")
        return "fallback(no-lib)"
    ok = []
    for t in list(PRICES):
        try:
            info = yf.Ticker(t).fast_info
            px = info.get("last_price") or info.get("lastPrice")
            if px and float(px) > 0:
                PRICES[t] = round(float(px), 2); ok.append(t)
        except Exception:
            pass
    if ok:
        print(f"[价格] ✓ yfinance 实时价已更新: {', '.join(ok)}")
        return "live"
    print("[价格] yfinance 取价失败(可能本环境无外网)→ 用手填 PRICES")
    return "fallback(no-net)"


def compute():
    pos, cost, realized = defaultdict(float), defaultdict(float), defaultdict(float)
    by_date = defaultdict(float)
    for d, t, s, q, p in sorted(LEDGER, key=lambda x: x[0]):
        if s == "B":
            pos[t] += q; cost[t] += q * p
        else:
            avg = cost[t] / pos[t] if pos[t] > 1e-9 else p
            pnl = (p - avg) * q
            realized[t] += pnl; by_date[d] += pnl
            cost[t] -= avg * q; pos[t] -= q
            if pos[t] < 1e-9: pos[t] = 0; cost[t] = 0
    realized["LITE2X"] = MANUAL_REALIZED["LITE2X"]
    realized["TSLA"] += MANUAL_REALIZED["TSLA_bonus"]
    by_date["2026-05-06"] += MANUAL_REALIZED["TSLA_bonus"]
    by_date["2026-05-21"] += MANUAL_REALIZED["LITE2X"]
    unreal = {t: (PRICES[t] - cost[t] / pos[t]) * pos[t]
              for t in PRICES if pos.get(t, 0) > 1e-6}
    return pos, cost, realized, unreal, by_date


def make_charts(realized, unreal, by_date):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    # 累计已实现曲线
    cum, xs, ys = 0, [], []
    for d in sorted(by_date):
        cum += by_date[d]; xs.append(datetime.date.fromisoformat(d)); ys.append(cum)
    fig, ax = plt.subplots(figsize=(11, 5.2))
    ax.axhline(0, color="#888", lw=.8)
    ax.plot(xs, ys, marker="o", ms=4, lw=1.9, color="#d6541f")
    ax.fill_between(xs, ys, 0, where=[v >= 0 for v in ys], color="#2ca02c", alpha=.12, interpolate=True)
    ax.fill_between(xs, ys, 0, where=[v < 0 for v in ys], color="#d62728", alpha=.12, interpolate=True)
    ax.set_title(f"Cumulative REALIZED P&L (closed trades)  |  as of {ACCOUNT['as_of']}", fontsize=11)
    ax.set_ylabel("Cumulative realized P&L ($)"); ax.grid(alpha=.25)
    fig.autofmt_xdate(); fig.tight_layout(); fig.savefig("assets/pnl_curve.png", dpi=140); plt.close(fig)
    # 逐票总盈亏
    rows = []
    for t in set(list(realized) + list(unreal)):
        rows.append((t, realized.get(t, 0) + unreal.get(t, 0)))
    for k, v in OPTIONS_REALIZED.items():
        rows.append((k, v))
    rows.sort(key=lambda x: x[1])
    fig2, ax2 = plt.subplots(figsize=(11, 7))
    cols = ["#2ca02c" if v >= 0 else "#d62728" for _, v in rows]
    ax2.barh([r[0] for r in rows], [r[1] for r in rows], color=cols)
    for i, (_, v) in enumerate(rows):
        ax2.text(v + (3 if v >= 0 else -3), i, f"{v:+.0f}", va="center",
                 ha="left" if v >= 0 else "right", fontsize=7.5)
    ax2.axvline(0, color="#333", lw=.8)
    ax2.set_title(f"Per-ticker TOTAL P&L (realized + unrealized)  |  as of {ACCOUNT['as_of']}", fontsize=11)
    ax2.set_xlabel("Total P&L ($)"); ax2.grid(axis="x", alpha=.25)
    fig2.tight_layout(); fig2.savefig("assets/pnl_by_ticker.png", dpi=140); plt.close(fig2)


def main():
    price_mode = fetch_live_prices()   # 本地有网=实时价;否则回退手填
    pos, cost, realized, unreal, by_date = compute()
    TR = sum(realized.values()) + sum(OPTIONS_REALIZED.values())
    TU = sum(unreal.values())
    total = ACCOUNT["nav"] - ACCOUNT["net_deposits"]
    ret = total / ACCOUNT["net_deposits"] * 100
    wins = {t: v for t, v in realized.items() if v > 0}
    loss = {t: v for t, v in realized.items() if v < 0}
    try:
        make_charts(realized, unreal, by_date); chart_msg = "charts -> assets/*.png ✓"
    except ImportError:
        chart_msg = "matplotlib 未安装,跳过图表(pip install matplotlib)"

    print("="*60)
    print(f"账户快照 {ACCOUNT['as_of']}")
    print(f"  NAV ${ACCOUNT['nav']:.2f} | 现金 ${ACCOUNT['cash']:.2f} | 净入金 ${ACCOUNT['net_deposits']:.2f}")
    print(f"  总盈亏 ${total:+.2f} ({ret:+.1f}%)  [NAV - 入金,最硬的数]")
    print(f"  已实现 ${TR:+.2f} (股 ${TR-sum(OPTIONS_REALIZED.values()):+.2f} + 期权 ${sum(OPTIONS_REALIZED.values()):+.0f})")
    print(f"  未实现 ${TU:+.2f} (现价口径)")
    print(f"  胜率(已平仓票): {len(wins)}/{len(wins)+len(loss)} = {len(wins)/(len(wins)+len(loss))*100:.0f}%")
    print(f"  最大赢家: {max(realized,key=realized.get)} ${max(realized.values()):+.0f}  "
          f"最大输家: {min(realized,key=realized.get)} ${min(realized.values()):+.0f}")
    print("\n当前持仓:")
    for t in sorted(pos):
        if pos[t] > 1e-6:
            mv = PRICES.get(t, 0)*pos[t]
            print(f"  {t:6} {pos[t]:.4f} 股 @ avg ${cost[t]/pos[t]:.2f} | 现价 ${PRICES.get(t,0):.2f} "
                  f"| 市值 ${mv:.0f} | 未实现 ${unreal.get(t,0):+.0f} | {THEME.get(t,'?')}")
    print(f"\n价格模式: {price_mode}  |  {chart_msg}")
    print("="*60)


if __name__ == "__main__":
    main()

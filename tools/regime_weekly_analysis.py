#!/usr/bin/env python3
"""
Regime-aware + weekly-trend analysis for MU / XLE / BE / CIEN / MRNA.

Splits 2025-11 → 2026-05 into 4 event-driven regimes (PRE_SHOCK, SHOCK,
POST_CEASE, POST_CONS) instead of fixed 30/60/90-day windows, and prints
for each ticker per regime:
  - start close / end close / return
  - intra-regime max drawdown (peak-to-trough)
  - annualized realized vol

Plus, per ticker overall:
  - shock-low recovery (today / shock-low) and (today / pre-shock high)
  - 13-bin ASCII sparkline over the full 6 months
  - WEEKLY view: current up/down streak, change vs 4w / 12w / 26w ago,
    last 8 W-o-W % moves, and a simple "trending up vs still down" verdict

How to run LOCALLY (this script needs live Yahoo Finance access,
which the cloud sandbox blocks):

  pip install yfinance pandas numpy
  python3 regime_weekly_analysis.py

Then paste the entire printed output back to me in chat — I'll use it to
extend the 4-sector / catalyst report with the regime + weekly picture
for your actually-watched names.
"""
import sys
import numpy as np
import pandas as pd

try:
    import yfinance as yf
except ImportError:
    sys.exit("Missing yfinance.  Run:  pip install yfinance pandas numpy")

# ----------------- config -----------------
TICKERS = ["MU", "XLE", "BE", "CIEN", "MRNA"]
START   = "2025-11-01"
END     = "2026-05-15"   # exclusive

REGIMES = [
    ("PRE_SHOCK",  "2025-11-14", "2026-02-27"),
    ("SHOCK",      "2026-02-28", "2026-04-08"),
    ("POST_CEASE", "2026-04-09", "2026-04-30"),
    ("POST_CONS",  "2026-05-01", "2026-05-14"),
]

# ----------------- helpers -----------------
def sparkline(series, n_bins=13):
    """Compress series into n_bins points, render as 1-char-per-bin block bar."""
    if len(series) == 0:
        return "(no data)"
    blocks = "▁▂▃▄▅▆▇█"
    idx = np.linspace(0, len(series) - 1, n_bins, dtype=int)
    pts = series.iloc[idx].values
    lo, hi = float(pts.min()), float(pts.max())
    span = hi - lo if hi > lo else 1.0
    scaled = ((pts - lo) / span * (len(blocks) - 1)).astype(int)
    scaled = np.clip(scaled, 0, len(blocks) - 1)
    return "".join(blocks[s] for s in scaled)


def streak_and_direction(weekly_close):
    """Most-recent consecutive run of up/down weeks."""
    if len(weekly_close) < 2:
        return 0, "flat"
    diff = weekly_close.diff().dropna()
    last = diff.iloc[-1]
    direction = "up" if last > 0 else ("down" if last < 0 else "flat")
    n = 0
    for v in reversed(diff.values):
        if direction == "up" and v > 0:
            n += 1
        elif direction == "down" and v < 0:
            n += 1
        else:
            break
    return n, direction


def trend_verdict(weekly_close):
    """Simple verdict combining 4w / 12w slope + SMA position.
    Returns one of: UP / RECOVERING / SIDEWAYS / DOWN."""
    if len(weekly_close) < 12:
        return "INSUFFICIENT_DATA"
    last = float(weekly_close.iloc[-1])
    w4   = float(weekly_close.iloc[-4])
    w12  = float(weekly_close.iloc[-12])
    sma4 = float(weekly_close.tail(4).mean())
    sma12 = float(weekly_close.tail(12).mean())
    above_4 = last > sma4
    above_12 = last > sma12
    chg4  = last / w4  - 1
    chg12 = last / w12 - 1
    if chg4 > 0.02 and chg12 > 0.05 and above_4 and above_12:
        return "UP"
    if chg4 > 0.05 and chg12 < 0 and above_4 and not above_12:
        return "RECOVERING"
    if chg4 < -0.02 and chg12 < -0.05 and not above_4 and not above_12:
        return "DOWN"
    return "SIDEWAYS"


# ----------------- main -----------------
def main():
    df = yf.download(TICKERS, start=START, end=END,
                     progress=False, auto_adjust=False, group_by="ticker")

    for t in TICKERS:
        try:
            close = df[t]["Close"].dropna()
        except Exception:
            close = yf.download(t, start=START, end=END,
                                progress=False, auto_adjust=False)["Close"].dropna()
        if len(close) == 0:
            print(f"\n=== {t} ===\n  NO DATA")
            continue

        print(f"\n=== {t} ===")

        # ----- regime breakdown -----
        for name, s, e in REGIMES:
            seg = close.loc[s:e]
            if seg.empty:
                print(f"  {name:11s} {s}→{e}  NO DATA")
                continue
            ret = (seg.iloc[-1] / seg.iloc[0] - 1) * 100
            dd  = (seg / seg.cummax() - 1).min() * 100
            vol = seg.pct_change().std() * np.sqrt(252) * 100
            print(f"  {name:11s} {s}→{e}  "
                  f"ret={ret:+6.1f}%  intraDD={dd:+6.1f}%  "
                  f"vol_ann={vol:5.1f}%  "
                  f"px {float(seg.iloc[0]):7.2f} → {float(seg.iloc[-1]):7.2f}")

        # ----- shock-low recovery -----
        shock_seg = close.loc["2026-02-28":"2026-04-08"]
        if len(shock_seg) > 0:
            low = float(shock_seg.min())
            today = float(close.iloc[-1])
            pre = close.loc[:"2026-02-27"]
            pre_high = float(pre.max()) if len(pre) > 0 else float("nan")
            full_recovered = "✓" if today >= pre_high else " "
            print(f"  shock_low={low:.2f}  today={today:.2f}  "
                  f"recovery={today/low:.2f}x  "
                  f"vs_pre_shock_high={today/pre_high:.2f}x  "
                  f"[full_recovered={full_recovered}]")

        # ----- 6mo sparkline -----
        print(f"  sparkline (Nov→May, 13 bins):  {sparkline(close, 13)}")

        # ----- WEEKLY view -----
        weekly = close.resample("W-FRI").last().dropna()
        if len(weekly) < 4:
            print("  weekly: NOT ENOUGH WEEKLY DATA")
            continue
        wow = weekly.pct_change().dropna() * 100
        streak, direction = streak_and_direction(weekly)
        verdict = trend_verdict(weekly)
        last_close = float(weekly.iloc[-1])

        def chg_n(n):
            return last_close / float(weekly.iloc[-n]) * 100 - 100 if len(weekly) >= n else float("nan")

        print(f"  weekly:  trend_verdict = {verdict}  |  current streak = {streak}w {direction}")
        print(f"           Δ 4w = {chg_n(4):+6.1f}%   "
              f"Δ12w = {chg_n(12):+6.1f}%   "
              f"Δ26w = {chg_n(26):+6.1f}%")

        last_n = min(8, len(wow))
        last_dates = wow.tail(last_n).index.strftime("%m-%d")
        last_vals  = wow.tail(last_n).values
        print(f"  last {last_n} weekly W-o-W % (Fri close, oldest→newest):")
        print(f"    " + "  ".join(f"{d}:{v:+5.1f}" for d, v in zip(last_dates, last_vals)))

if __name__ == "__main__":
    main()

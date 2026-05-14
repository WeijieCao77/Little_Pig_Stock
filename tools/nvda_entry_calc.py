#!/usr/bin/env python3
"""
NVDA pre-earnings limit-buy calculator.

Pulls 30 trading days of NVDA daily OHLC, computes:
  - 22-day mean of daily LOWS (1 month)
  - 5-day mean of daily LOWS (1 week)
  - their stdevs
  - suggested limit-buy zones at mean / mean - 0.5 sigma / mean - 1 sigma
  - current discount/premium from each level
  - week-over-week trend verdict (UP/RECOVERING/SIDEWAYS/DOWN)

Run LOCALLY (cloud sandbox blocks Yahoo Finance):

  pip install yfinance pandas numpy
  python3 nvda_entry_calc.py

Paste the full stdout back to me.
"""
import sys
import numpy as np
import pandas as pd

try:
    import yfinance as yf
except ImportError:
    sys.exit("Install first:  pip install yfinance pandas numpy")

TICKER = "NVDA"
EARNINGS_DATE = "2026-05-20"   # Wed AMC

print(f"\n=== {TICKER}  pre-earnings entry calc  ===")
print(f"Earnings: {EARNINGS_DATE} AMC")
print()

# pull 60 calendar days to be safe (need ~30 trading days back from today)
df = yf.download(TICKER, period="60d", interval="1d",
                 progress=False, auto_adjust=False)
if df.empty:
    sys.exit(f"No data returned for {TICKER}")

# yfinance sometimes returns MultiIndex; flatten
if isinstance(df.columns, pd.MultiIndex):
    df.columns = [c[0] for c in df.columns]

df = df.tail(30).copy()  # last 30 trading days
print(f"Pulled {len(df)} trading days  ({df.index[0].date()} → {df.index[-1].date()})")

last_close = float(df["Close"].iloc[-1])
last_low   = float(df["Low"].iloc[-1])
last_high  = float(df["High"].iloc[-1])
print(f"Today: Close={last_close:.2f}  High={last_high:.2f}  Low={last_low:.2f}")

# ---------- daily lows ----------
lows = df["Low"]
lows_1m = lows.tail(22)
lows_1w = lows.tail(5)

m1m = float(lows_1m.mean())
s1m = float(lows_1m.std())
m1w = float(lows_1w.mean())
s1w = float(lows_1w.std())

print(f"\n--- daily LOWS ---")
print(f"  1M  (22d):  mean={m1m:7.2f}   std={s1m:5.2f}   min={float(lows_1m.min()):7.2f}   max={float(lows_1m.max()):7.2f}")
print(f"  1W  ( 5d):  mean={m1w:7.2f}   std={s1w:5.2f}   min={float(lows_1w.min()):7.2f}   max={float(lows_1w.max()):7.2f}")

# ---------- entry zones ----------
zones_1m = {
    "1M mean low":             m1m,
    "1M mean low - 0.5σ":      m1m - 0.5 * s1m,
    "1M mean low - 1.0σ":      m1m - 1.0 * s1m,
    "1M mean low - 1.5σ":      m1m - 1.5 * s1m,
}
zones_1w = {
    "1W mean low":             m1w,
    "1W mean low - 0.5σ":      m1w - 0.5 * s1w,
    "1W mean low - 1.0σ":      m1w - 1.0 * s1w,
}

print(f"\n--- 1M-derived buy zones ---")
for label, px in zones_1m.items():
    discount = (last_close / px - 1) * 100
    fill_hint = ("today's low ≤ this" if last_low <= px else "needs pullback")
    print(f"  {label:25s}  ${px:7.2f}   (today vs this: {discount:+5.1f}%, {fill_hint})")

print(f"\n--- 1W-derived buy zones ---")
for label, px in zones_1w.items():
    discount = (last_close / px - 1) * 100
    fill_hint = ("today's low ≤ this" if last_low <= px else "needs pullback")
    print(f"  {label:25s}  ${px:7.2f}   (today vs this: {discount:+5.1f}%, {fill_hint})")

# ---------- weekly trend ----------
weekly = df["Close"].resample("W-FRI").last().dropna()
def chg(n):
    return float(weekly.iloc[-1] / weekly.iloc[-n] - 1) * 100 if len(weekly) >= n else float("nan")

last4_changes = weekly.tail(4).pct_change().dropna() * 100
ups = sum(v > 0 for v in last4_changes.values)
downs = sum(v < 0 for v in last4_changes.values)

print(f"\n--- weekly trend ---")
print(f"  weeks pulled: {len(weekly)}")
print(f"  Δ vs 1w ago:  {chg(2):+5.1f}%   Δ4w:  {chg(5):+5.1f}%   Δ12w: {chg(12):+5.1f}%")
print(f"  last 4 W-o-W:  " + "  ".join(f"{v:+5.1f}%" for v in last4_changes.values))

# simple verdict
verdict = "SIDEWAYS"
if chg(2) > 1 and chg(5) > 3:
    verdict = "UP"
elif chg(2) > 3 and chg(5) < 0:
    verdict = "RECOVERING"
elif chg(2) < -1 and chg(5) < -3:
    verdict = "DOWN"
print(f"  trend verdict: {verdict}  (4w: {ups} up / {downs} down weeks)")

# ---------- recommended limit ----------
# heuristic: pick the most reasonable fill among the zones
# default = mean of 1M and 1W mean lows, rounded to nearest dollar
mid = (m1m + m1w) / 2
rec = round(mid)
rec_aggressive = round((m1w + (last_close - m1w) * 0.3))  # closer to current, easier fill
rec_patient    = round(m1m - 0.5 * s1m)
print(f"\n--- suggested limit buys ---")
print(f"  AGGRESSIVE (easy fill, low margin):   ${rec_aggressive}")
print(f"  BALANCED   (mean of 1M+1W avg lows):  ${rec}")
print(f"  PATIENT    (1M mean - 0.5σ):          ${rec_patient}")
print(f"\n  current price = ${last_close:.2f}, earnings 5/20 AMC")
print(f"  → if buying, place GTC limit; cancel by 5/19 close if not filled")
print(f"  → sell trigger: by 5/20 3:30pm ET regardless of price, OR exit on +5% from fill, whichever first")
print()

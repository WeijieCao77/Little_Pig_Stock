#!/usr/bin/env python3
"""
按需取实时报价 —— 网络放开(白名单 yahoo 域名)后即插即用。
用法:
    python3 tools/quote.py MU QCOM ASTS SPY
说明:
    - 默认走 yfinance(免费,约 15 分钟延迟)。
    - 本环境若被网络策略拦截,会明确提示"无外网",不会报错崩溃。
    - 想要真·实时,接 Finnhub/Alpha Vantage 等(需 API key),再扩展本脚本。
"""
import sys


def quotes(tickers):
    try:
        import yfinance as yf
    except ImportError:
        print("未装 yfinance → pip install yfinance"); return
    print(f"{'TICKER':8}{'PRICE':>10}{'CHG%':>9}{'TIME(UTC)':>22}")
    print("-" * 49)
    got = False
    for t in tickers:
        try:
            fi = yf.Ticker(t).fast_info
            px = fi.get("last_price"); prev = fi.get("previous_close")
            if px:
                chg = (px / prev - 1) * 100 if prev else float("nan")
                import datetime
                ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M")
                print(f"{t:8}{px:>10.2f}{chg:>8.2f}%{ts:>22}")
                got = True
            else:
                print(f"{t:8}{'(no data)':>10}")
        except Exception as e:
            print(f"{t:8}  取价失败: {type(e).__name__}(可能本环境无外网,见 tools/quote.py 顶部说明)")
    if not got:
        print("\n→ 没取到任何价。多半是这个环境网络被拦。"
              "\n  放开网络策略后(白名单 query1/2.finance.yahoo.com)即可用。")


if __name__ == "__main__":
    syms = [s.upper() for s in sys.argv[1:]] or ["MU", "QCOM", "ASTS", "CIEN", "SPY"]
    quotes(syms)

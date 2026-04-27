# main.py

import time
import traceback

from data.market_data_loader import MarketDataLoader
from market.market_universe import MarketUniverse
from scanner.scanner import Scanner
from strategy.strategy_engine import StrategyEngine
from probability.probability_engine import ProbabilityEngine


def run_engine():

    market_universe = MarketUniverse()
    data_loader = MarketDataLoader()

    strategy_engine = StrategyEngine()
    probability_engine = ProbabilityEngine()

    scanner = Scanner(strategy_engine, probability_engine)

    print("\n🚀 AstraQuant Engine Started...\n")

    TARGET_CYCLE_SECONDS = 60

    while True:

        try:
            start_time = time.time()

            symbols = market_universe.get_symbols()
            market_data = data_loader.load_market_data(symbols)

            scan_result = scanner.run_scan(market_data)

            opportunities = scan_result.get("opportunities", [])
            all_signals = scan_result.get("all_signals", [])
            metrics = scan_result.get("metrics", {})

            print("\n==============================")
            print(f"🕒 Cycle @ {time.strftime('%H:%M:%S')}")
            print("==============================")

            print(f"Total Opportunities: {len(opportunities)}")
            print(f"Strategy Signals: {metrics.get('strategy_count', 0)}")
            print(f"Probability Signals: {metrics.get('probability_count', 0)}")

            print("\n=== Market View ===")

            for s in all_signals:
                symbol = s.get("symbol", "N/A")
                prob = float(s.get("probability", 0))

                mom = s.get("momentum", "neutral")
                strength = float(s.get("strength", 0))
                history = s.get("history", [])

                trend = s.get("trend", "unknown")
                zone = s.get("zone", "unknown")
                breakout = s.get("breakout", False)
                setup = s.get("setup", "unknown")

                # 🔥 MTF
                mtf_alignment = s.get("mtf_alignment", "unknown")
                t1 = s.get("mtf_trend_1m", "unknown")
                t5 = s.get("mtf_trend_5m", "unknown")
                t15 = s.get("mtf_trend_15m", "unknown")

                # تنظيف
                prob_clean = round(prob, 3)
                strength_clean = round(strength, 2)
                history_clean = [round(x, 3) for x in history]

                # 🔥 Setup Label
                if setup == "real":
                    setup_label = "🔥 REAL"
                elif setup == "weak":
                    setup_label = "🟡 WEAK"
                elif setup == "fake":
                    setup_label = "❌ FAKE"
                else:
                    setup_label = "⚪ UNKNOWN"

                # 🔥 MTF Label
                if mtf_alignment == "strong":
                    mtf_label = "🔥 STRONG"
                elif mtf_alignment == "medium":
                    mtf_label = "🟡 MEDIUM"
                else:
                    mtf_label = "⚠️ WEAK"

                print(
                    f"{symbol} → {prob_clean} "
                    f"({mom}, str={strength_clean}) | {setup_label} | {mtf_label}"
                )

                print(
                    f"   ↳ trend: {trend} | zone: {zone} | breakout: {breakout}"
                )

                print(
                    f"   ↳ MTF: 1m={t1} | 5m={t5} | 15m={t15}"
                )

                print(f"   ↳ hist: {history_clean}")

            print("\n=== Opportunities ===")

            for op in opportunities[:10]:
                print({
                    "symbol": op.get("symbol", "N/A"),
                    "probability": round(float(op.get("probability_score", 0)), 3),
                    "momentum": op.get("momentum"),
                    "strength": round(float(op.get("strength", 0)), 2),
                    "setup": op.get("setup"),
                    "mtf_alignment": op.get("mtf_alignment")
                })

            elapsed = time.time() - start_time
            sleep_time = max(TARGET_CYCLE_SECONDS - elapsed, 5)

            print(f"\n⏳ Next cycle in {round(sleep_time,1)}s")
            print("==============================\n")

            time.sleep(sleep_time)

        except Exception:
            print("\n❌ ERROR DETECTED:")
            traceback.print_exc()
            print("\n🔁 Restarting cycle in 5 seconds...\n")
            time.sleep(5)


if __name__ == "__main__":
    run_engine()

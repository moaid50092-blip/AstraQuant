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

                # 🔥 Decision
                decision = s.get("decision", "N/A")
                direction = s.get("direction", "")
                score = s.get("score", 0)
                reasons = s.get("reasons", [])

                # 🔥 Confidence
                confidence = s.get("confidence_label", "")
                confidence_score = round(s.get("confidence_score", 0), 2)

                # 🔥 RANGE
                range_active = s.get("range_active", False)
                range_signal = s.get("range_signal", None)
                range_conf = round(s.get("range_confidence", 0), 2)

                # 🔥 EARLY
                entry_type = s.get("entry_type", "STANDARD")
                early_flag = "⚡ EARLY" if entry_type == "EARLY" else ""

                # تنظيف
                prob_clean = round(prob, 3)
                history_clean = [round(x, 3) for x in history]

                # 🔥 Strength Label (تحويل ذكي)
                if strength >= 0.75:
                    strength_label = "🔥 STRONG"
                elif strength >= 0.5:
                    strength_label = "🟡 BUILDING"
                else:
                    strength_label = "⚠️ WEAK"

                # 🔥 Direction Arrow
                if direction == "up":
                    arrow = "↑"
                elif direction == "down":
                    arrow = "↓"
                else:
                    arrow = "→"

                # 🔥 Decision Label
                if decision == "ENTER":
                    decision_label = f"🚀 ENTER {direction}"
                elif decision == "WATCH":
                    decision_label = "👀 WATCH"
                else:
                    decision_label = "❌ IGNORE"

                # 🔥 Confidence Label (منع التضارب)
                if confidence == "HIGH":
                    conf_label = f"🧠 HIGH ({confidence_score})"
                elif confidence == "MEDIUM":
                    conf_label = f"🟡 MED ({confidence_score})"
                else:
                    conf_label = f"⚠️ LOW ({confidence_score})"

                # 🔥 Range Label
                if range_active:
                    if range_signal:
                        range_label = f"📦 RANGE → {range_signal} ({range_conf})"
                    else:
                        range_label = "📦 RANGE"
                else:
                    range_label = ""

                # 🔥 HEADER الجديد
                print(
                    f"{symbol} → {prob_clean} {arrow} "
                    f"({strength_label}) {early_flag} | {decision_label} | {conf_label} {range_label}"
                )

                # 🔥 تفاصيل السوق
                print(f"   ↳ trend: {trend} | zone: {zone} | breakout: {breakout}")
                print(f"   ↳ MTF: 1m={t1} | 5m={t5} | 15m={t15}")
                print(f"   ↳ setup: {setup} | alignment: {mtf_alignment}")

                # 🔥 EARLY explanation
                if entry_type == "EARLY":
                    compression = s.get("compression", False)
                    acceleration = s.get("acceleration", False)
                    print(f"   ↳ ⚡ early: compression={compression}, acceleration={acceleration}")

                # 🔥 History
                print(f"   ↳ hist: {history_clean}")

                if reasons:
                    print(f"   ↳ reason: {', '.join(reasons[:3])}")

            print("\n=== Opportunities ===")

            for op in opportunities[:10]:
                print({
                    "symbol": op.get("symbol", "N/A"),
                    "probability": round(float(op.get("probability_score", 0)), 3),
                    "direction": op.get("direction"),
                    "score": op.get("score"),
                    "confidence": op.get("confidence")
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

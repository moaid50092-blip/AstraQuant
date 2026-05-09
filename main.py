import time
import traceback

from data.market_data_loader import MarketDataLoader
from market.market_universe import MarketUniverse

from scanner.scanner import Scanner

from strategy.strategy_engine import StrategyEngine
from probability.probability_engine import ProbabilityEngine

# =====================================================
# 🔥 TRADE LIFECYCLE
# =====================================================

from trade_lifecycle.trade_manager import (
    TradeManager
)

from trade_lifecycle.lifecycle_renderer import (
    render_lifecycle_events
)


# =====================================================
# 🔥 MARKET STATE ENGINE (Production Grade)
# =====================================================

def detect_market_state(all_signals):

    if not all_signals:
        return "UNKNOWN ❓ (no signals)"

    trends = [s.get("trend") for s in all_signals]
    breakouts = [s.get("breakout") for s in all_signals]

    strengths = [
        float(s.get("strength", 0))
        for s in all_signals
    ]

    probabilities = [
        float(s.get("probability", 0.5))
        for s in all_signals
    ]

    up = trends.count("up")
    down = trends.count("down")
    range_count = trends.count("range")

    breakout_count = sum(
        1 for b in breakouts if b
    )

    total = len(all_signals)

    avg_strength = sum(strengths) / total
    avg_prob = sum(probabilities) / total

    breakout_ratio = breakout_count / total
    range_ratio = range_count / total

    # =========================================
    # 🔥 TREND MARKET
    # =========================================

    if (
        breakout_ratio >= 0.4
        and avg_strength >= 0.58
        and avg_prob >= 0.55
    ):

        if up > down:
            return (
                "TREND 🚀 "
                "(bullish expansion)"
            )

        elif down > up:
            return (
                "TREND 🔻 "
                "(bearish expansion)"
            )

    # =========================================
    # 🔥 RANGE MARKET
    # =========================================

    if (
        range_ratio >= 0.6
        and breakout_ratio < 0.3
    ):

        return (
            "RANGE 📦 "
            "(sideways structure)"
        )

    # =========================================
    # 🔥 DEAD MARKET
    # =========================================

    if (
        avg_strength < 0.35
        and avg_prob < 0.52
    ):

        return (
            "DEAD 💤 "
            "(low momentum)"
        )

    return "MIXED ❓ (unclear structure)"


# =====================================================
# 🔥 SIGNAL DISPLAY
# =====================================================

def render_signal(signal):

    symbol = signal.get("symbol", "N/A")

    prob = round(
        float(signal.get("probability", 0)),
        3
    )

    strength = float(
        signal.get("strength", 0)
    )

    history = signal.get("history", [])

    trend = signal.get(
        "trend",
        "unknown"
    )

    zone = signal.get(
        "zone",
        "unknown"
    )

    breakout = signal.get(
        "breakout",
        False
    )

    setup = signal.get(
        "setup",
        "unknown"
    )

    decision = signal.get(
        "decision",
        "N/A"
    )

    direction = signal.get(
        "direction",
        ""
    )

    reasons = signal.get(
        "reasons",
        []
    )

    confidence = signal.get(
        "confidence_label",
        "LOW"
    )

    confidence_score = round(
        signal.get("confidence_score", 0),
        2
    )

    entry_type = signal.get(
        "entry_type",
        "STANDARD"
    )

    compression = signal.get(
        "compression",
        False
    )

    acceleration = signal.get(
        "acceleration",
        False
    )

    range_active = signal.get(
        "range_active",
        False
    )

    range_signal = signal.get(
        "range_signal",
        None
    )

    range_conf = round(
        signal.get("range_confidence", 0),
        2
    )

    mtf_alignment = signal.get(
        "mtf_alignment",
        "unknown"
    )

    t1 = signal.get(
        "mtf_trend_1m",
        "unknown"
    )

    t5 = signal.get(
        "mtf_trend_5m",
        "unknown"
    )

    t15 = signal.get(
        "mtf_trend_15m",
        "unknown"
    )

    # =========================================
    # 🔥 STRENGTH LABEL
    # =========================================

    if strength >= 0.75:

        strength_label = "🔥 STRONG"

    elif strength >= 0.5:

        strength_label = "🟡 BUILDING"

    else:

        strength_label = "⚠️ WEAK"

    # =========================================
    # 🔥 DIRECTION
    # =========================================

    if direction == "up":

        arrow = "↑"

    elif direction == "down":

        arrow = "↓"

    else:

        arrow = "→"

    # =========================================
    # 🔥 DECISION LABEL
    # =========================================

    if decision == "ENTER":

        if entry_type == "EARLY":

            decision_label = (
                f"⚡ EARLY ENTER "
                f"{direction}"
            )

        elif entry_type == "STRONG":

            decision_label = (
                f"🚀 ENTER STRONG "
                f"{direction}"
            )

        else:

            decision_label = (
                f"🚀 ENTER "
                f"{direction}"
            )

    elif decision == "WATCH":

        if entry_type == "EARLY":

            decision_label = (
                "⚡ WATCH "
                "(early forming)"
            )

        else:

            decision_label = "👀 WATCH"

    else:

        decision_label = "❌ IGNORE"

    # =========================================
    # 🔥 CONFIDENCE LABEL
    # =========================================

    if confidence == "HIGH":

        conf_label = (
            f"🧠 HIGH "
            f"({confidence_score})"
        )

    elif confidence == "MEDIUM":

        conf_label = (
            f"🟡 MED "
            f"({confidence_score})"
        )

    else:

        conf_label = (
            f"⚠️ LOW "
            f"({confidence_score})"
        )

    # =========================================
    # 🔥 RANGE LABEL
    # =========================================

    if range_active:

        if range_signal:

            range_label = (
                f"📦 RANGE → "
                f"{range_signal} "
                f"({range_conf})"
            )

        else:

            range_label = "📦 RANGE"

    else:

        range_label = ""

    # =========================================
    # 🔥 HEADER
    # =========================================

    print(
        f"{symbol} → {prob} {arrow} "
        f"({strength_label}) | "
        f"{decision_label} | "
        f"{conf_label} "
        f"{range_label}"
    )

    # =========================================
    # 🔥 DETAILS
    # =========================================

    print(
        f"   ↳ trend: {trend} | "
        f"zone: {zone} | "
        f"breakout: {breakout}"
    )

    print(
        f"   ↳ MTF: "
        f"1m={t1} | "
        f"5m={t5} | "
        f"15m={t15}"
    )

    print(
        f"   ↳ setup: {setup} | "
        f"alignment: {mtf_alignment}"
    )

    # =========================================
    # 🔥 EARLY DETAILS
    # =========================================

    if entry_type == "EARLY":

        print(
            f"   ↳ ⚡ early: "
            f"compression={compression}, "
            f"acceleration={acceleration}"
        )

    # =========================================
    # 🔥 HISTORY
    # =========================================

    history_clean = [
        round(float(x), 3)
        for x in history
    ]

    print(
        f"   ↳ hist: "
        f"{history_clean}"
    )

    # =========================================
    # 🔥 REASONS
    # =========================================

    if reasons:

        print(
            f"   ↳ reason: "
            f"{', '.join(reasons[:3])}"
        )


# =====================================================
# 🔥 ENGINE LOOP
# =====================================================

def run_engine():

    market_universe = MarketUniverse()

    data_loader = MarketDataLoader()

    strategy_engine = StrategyEngine()

    probability_engine = ProbabilityEngine()

    scanner = Scanner(
        strategy_engine,
        probability_engine
    )

    # =================================================
    # 🔥 TRADE MANAGER
    # =================================================

    trade_manager = TradeManager()

    print(
        "\n🚀 AstraQuant Engine Started...\n"
    )

    TARGET_CYCLE_SECONDS = 60

    while True:

        try:

            start_time = time.time()

            # =====================================
            # 🔥 LOAD DATA
            # =====================================

            symbols = (
                market_universe.get_symbols()
            )

            market_data = (
                data_loader.load_market_data(
                    symbols
                )
            )

            if not market_data:

                print(
                    "\n⚠️ No market data loaded.\n"
                )

                time.sleep(5)

                continue

            # =====================================
            # 🔥 SCAN
            # =====================================

            scan_result = scanner.run_scan(
                market_data
            )

            opportunities = scan_result.get(
                "opportunities",
                []
            )

            all_signals = scan_result.get(
                "all_signals",
                []
            )

            metrics = scan_result.get(
                "metrics",
                {}
            )

            # =====================================
            # 🔥 TRADE LIFECYCLE
            # =====================================

            lifecycle_events = (
                trade_manager.process_signals(
                    all_signals
                )
            )

            # =====================================
            # 🔥 MARKET STATE
            # =====================================

            market_state = (
                detect_market_state(
                    all_signals
                )
            )

            # =====================================
            # 🔥 HEADER
            # =====================================

            print(
                "\n=============================="
            )

            print(
                f"🕒 Cycle @ "
                f"{time.strftime('%H:%M:%S')}"
            )

            print(
                "=============================="
            )

            print(
                f"🌍 MARKET STATE: "
                f"{market_state}"
            )

            print(
                f"Total Opportunities: "
                f"{len(opportunities)}"
            )

            print(
                f"Strategy Signals: "
                f"{metrics.get('strategy_count', 0)}"
            )

            print(
                f"Probability Signals: "
                f"{metrics.get('probability_count', 0)}"
            )

            print("\n=== Market View ===")

            # =====================================
            # 🔥 SORT SIGNALS
            # =====================================

            sorted_signals = sorted(
                all_signals,
                key=lambda x: (
                    x.get("decision")
                    == "ENTER",

                    x.get(
                        "probability",
                        0
                    ),

                    x.get(
                        "strength",
                        0
                    )
                ),
                reverse=True
            )

            for signal in sorted_signals:

                render_signal(signal)

            # =====================================
            # 🔥 LIFECYCLE EVENTS
            # =====================================

            render_lifecycle_events(
                lifecycle_events
            )

            # =====================================
            # 🔥 OPPORTUNITIES
            # =====================================

            print("\n=== Opportunities ===")

            if not opportunities:

                print("No valid entries.")

            else:

                sorted_ops = sorted(
                    opportunities,
                    key=lambda x: (
                        x.get("score", 0),

                        x.get(
                            "probability_score",
                            0
                        )
                    ),
                    reverse=True
                )

                for op in sorted_ops[:10]:

                    print({

                        "symbol": op.get(
                            "symbol",
                            "N/A"
                        ),

                        "probability": round(
                            float(
                                op.get(
                                    "probability_score",
                                    0
                                )
                            ),
                            3
                        ),

                        "direction": op.get(
                            "direction"
                        ),

                        "score": op.get(
                            "score"
                        ),

                        "confidence": op.get(
                            "confidence"
                        ),

                        "entry_type": op.get(
                            "entry_type"
                        )
                    })

            # =====================================
            # 🔥 CLEANUP
            # =====================================

            trade_manager.cleanup_closed_trades()

            # =====================================
            # 🔥 SLEEP CONTROL
            # =====================================

            elapsed = (
                time.time()
                - start_time
            )

            sleep_time = max(
                TARGET_CYCLE_SECONDS
                - elapsed,
                5
            )

            print(
                f"\n⏳ Next cycle in "
                f"{round(sleep_time, 1)}s"
            )

            print(
                "==============================\n"
            )

            time.sleep(sleep_time)

        except KeyboardInterrupt:

            print(
                "\n🛑 AstraQuant stopped manually.\n"
            )

            break

        except Exception:

            print("\n❌ ERROR DETECTED:")

            traceback.print_exc()

            print(
                "\n🔁 Restarting cycle "
                "in 5 seconds...\n"
            )

            time.sleep(5)


# =====================================================
# 🔥 ENTRY
# =====================================================

if __name__ == "__main__":

    run_engine()

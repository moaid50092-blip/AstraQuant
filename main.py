# main.py

from data.market_data_loader import MarketDataLoader
from market.market_universe import MarketUniverse
from scanner.scanner import Scanner
from strategy.strategy_engine import StrategyEngine
from probability.probability_engine import ProbabilityEngine

# 🔥 NEW
from momentum.momentum_tracker import MomentumTracker


def main():

    # -------------------------------------------------
    # Initialize Components
    # -------------------------------------------------

    market_universe = MarketUniverse()
    data_loader = MarketDataLoader()

    strategy_engine = StrategyEngine()
    probability_engine = ProbabilityEngine()

    scanner = Scanner(strategy_engine, probability_engine)

    # 🔥 NEW (لازم يكون برا أي loop)
    momentum_tracker = MomentumTracker(window_size=4)

    # -------------------------------------------------
    # Load Market Data
    # -------------------------------------------------

    symbols = market_universe.get_symbols()
    market_data = data_loader.load_market_data(symbols)

    # -------------------------------------------------
    # Scanner
    # -------------------------------------------------

    scan_result = scanner.run_scan(market_data)

    opportunities = scan_result.get("opportunities", [])
    all_signals = scan_result.get("all_signals", [])
    metrics = scan_result.get("metrics", {})

    # -------------------------------------------------
    # Output
    # -------------------------------------------------

    print("\n=== Scanner Output ===")

    print(f"Total Opportunities: {len(opportunities)}")
    print(f"Strategy Signals: {metrics.get('strategy_count', 0)}")
    print(f"Probability Signals: {metrics.get('probability_count', 0)}")

    # ---------------------------------------------
    # 🔥 ALL SIGNALS (Market View + Momentum)
    # ---------------------------------------------
    print("\n=== All Signals (Market View) ===")

    for s in all_signals:
        symbol = s.get("symbol", "N/A")
        prob = float(s.get("probability", 0))

        # 🔥 تحديث المومنتوم
        momentum_tracker.update(symbol, prob)
        info = momentum_tracker.get_momentum_info(symbol)

        print(
            f"{symbol} → {round(prob, 3)} "
            f"({info['direction']}, strength={info['strength']}) "
            f"↳ history: {info['history']}"
        )

    # ---------------------------------------------
    # Opportunities (Filtered)
    # ---------------------------------------------
    print("\n=== High Probability Opportunities ===")

    for op in opportunities[:10]:
        print({
            "symbol": op.get("symbol", "N/A"),
            "probability": op.get("probability_score", "N/A")
        })

    print("\n========================\n")


if __name__ == "__main__":
    main()

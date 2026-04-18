# main.py

from data.market_data_loader import MarketDataLoader
from market.market_universe import MarketUniverse
from scanner.scanner import Scanner
from strategy.strategy_engine import StrategyEngine
from probability.probability_engine import ProbabilityEngine


def main():

    # -------------------------------------------------
    # Initialize Components
    # -------------------------------------------------

    market_universe = MarketUniverse()
    data_loader = MarketDataLoader()

    strategy_engine = StrategyEngine()
    probability_engine = ProbabilityEngine()

    scanner = Scanner(strategy_engine, probability_engine)

    # -------------------------------------------------
    # Load Market Data
    # -------------------------------------------------

    symbols = market_universe.get_symbols()
    market_data = data_loader.load_market_data(symbols)  # ✅ التعديل هون

    # -------------------------------------------------
    # Scanner Only
    # -------------------------------------------------

    scan_result = scanner.run_scan(market_data)

    opportunities = scan_result["opportunities"]
    metrics = scan_result["metrics"]

    # -------------------------------------------------
    # Output (Monitoring Only)
    # -------------------------------------------------

    print("\n=== Scanner Output ===")

    print(f"Total Opportunities: {len(opportunities)}")
    print(f"Strategy Signals: {metrics.get('strategy_count', 0)}")
    print(f"Probability Signals: {metrics.get('probability_count', 0)}")

    print("\nSample Opportunities:")

    for op in opportunities[:10]:  # فقط أول 10 للعرض
        print(op)

    print("========================\n")


if __name__ == "__main__":
    main()

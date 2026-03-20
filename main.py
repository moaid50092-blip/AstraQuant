# main.py

from data.market_data_loader import MarketDataLoader
from market.market_universe import MarketUniverse
from scanner.scanner import Scanner
from strategy.strategy_engine import StrategyEngine
from probability.probability_engine import ProbabilityEngine
from opportunity.opportunity_ranking_engine import OpportunityRankingEngine
from opportunity.opportunity_quality_engine import OpportunityQualityEngine
from portfolio.portfolio_manager import PortfolioManager
from portfolio.position_sizing_engine import PositionSizingEngine
from stability.signal_stability_engine import SignalStabilityEngine
from execution.execution_engine import ExecutionEngine
from learning.alpha_decay_engine import AlphaDecayEngine

from monitoring.instrumentation import Instrumentation


def main():

    # -------------------------------------------------
    # Initialize Components
    # -------------------------------------------------

    market_universe = MarketUniverse()
    data_loader = MarketDataLoader()

    strategy_engine = StrategyEngine()
    probability_engine = ProbabilityEngine()

    scanner = Scanner(strategy_engine, probability_engine)

    ranking_engine = OpportunityRankingEngine()
    quality_engine = OpportunityQualityEngine()

    portfolio_manager = PortfolioManager()
    position_sizing = PositionSizingEngine()
    stability_engine = SignalStabilityEngine()
    execution_engine = ExecutionEngine()

    learning_engine = AlphaDecayEngine()

    instrumentation = Instrumentation()

    # -------------------------------------------------
    # Load Market Data
    # -------------------------------------------------

    symbols = market_universe.get_symbols()
    market_data = data_loader.load(symbols)

    # -------------------------------------------------
    # Scanner (with metrics)
    # -------------------------------------------------

    scan_result = scanner.run_scan(market_data)

    opportunities = scan_result["opportunities"]
    metrics = scan_result["metrics"]

    # ---------------------------------------------
    # Instrumentation (Scanner Level)
    # ---------------------------------------------

    instrumentation.update("scanner", len(opportunities))
    instrumentation.update("strategy", metrics["strategy_count"])
    instrumentation.update("probability", metrics["probability_count"])

    # -------------------------------------------------
    # Ranking
    # -------------------------------------------------

    ranked_opportunities = ranking_engine.rank(opportunities)

    # -------------------------------------------------
    # Opportunity Quality
    # -------------------------------------------------

    quality_opportunities = quality_engine.evaluate(ranked_opportunities)

    # -------------------------------------------------
    # Portfolio Selection
    # -------------------------------------------------

    selected_trades = portfolio_manager.select(quality_opportunities)

    # -------------------------------------------------
    # Position Sizing
    # -------------------------------------------------

    sized_trades = position_sizing.apply(selected_trades)

    # -------------------------------------------------
    # Signal Stability
    # -------------------------------------------------

    stable_trades = []

    for trade in sized_trades:
        if stability_engine.evaluate(trade):
            stable_trades.append(trade)

    # -------------------------------------------------
    # Execution
    # -------------------------------------------------

    executed_trades = execution_engine.execute(stable_trades)

    # -------------------------------------------------
    # Temporary Trade Output (Monitoring Only)
    # -------------------------------------------------

    print("\n=== Executed Trades ===")
    for trade in executed_trades:
        print({
            "symbol": trade.get("symbol", "N/A"),
            "entry": trade.get("entry", "N/A"),
            "stop_loss": trade.get("stop_loss", "N/A"),
            "take_profit": trade.get("take_profit", "N/A"),
        })
    print("========================\n")

    instrumentation.update("execution", len(executed_trades))

    # -------------------------------------------------
    # Learning
    # -------------------------------------------------

    learning_engine.update(executed_trades)

    # -------------------------------------------------
    # Report
    # -------------------------------------------------

    instrumentation.report()


if __name__ == "__main__":
    main()

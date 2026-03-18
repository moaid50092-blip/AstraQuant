# main.py

"""
AstraQuant — Main Entry Point

This file initializes all core components and runs the system pipeline.

Pipeline:

Market Universe
→ Market Data
→ Scanner (Two-Stage)
→ Strategy Detection
→ Intelligence Engines
→ Probability Engine
→ Opportunity Ranking
→ Opportunity Quality
→ Portfolio Manager
→ Position Sizing
→ Signal Stability
→ Execution Engine
"""

from market.market_universe import MarketUniverse
from data.market_data import MarketData
from scanner.scanner import Scanner

from strategy.strategy_engine import StrategyEngine

from intelligence.mtf_engine import MTFEngine
from intelligence.liquidity_engine import LiquidityEngine
from intelligence.structure_engine import StructureEngine
from intelligence.session_engine import SessionEngine
from intelligence.cross_asset_engine import CrossAssetEngine

from probability.probability_engine import ProbabilityEngine

from ranking.opportunity_ranking_engine import OpportunityRankingEngine
from quality.opportunity_quality_engine import OpportunityQualityEngine

from portfolio.portfolio_manager import PortfolioManager
from portfolio.position_sizing_engine import PositionSizingEngine

from execution.signal_stability_engine import SignalStabilityEngine
from execution.execution_engine import ExecutionEngine

from utils.logger import Logger


class AstraQuant:

    def __init__(self):

        # Infrastructure
        self.logger = Logger()

        # Market Layer
        self.market_universe = MarketUniverse()
        self.market_data = MarketData()

        # Strategy
        self.strategy_engine = StrategyEngine()

        # Intelligence
        self.mtf_engine = MTFEngine()
        self.liquidity_engine = LiquidityEngine()
        self.structure_engine = StructureEngine()
        self.session_engine = SessionEngine()
        self.cross_asset_engine = CrossAssetEngine()

        # Probability
        self.probability_engine = ProbabilityEngine()

        # Scanner
        self.scanner = Scanner(
            strategy_engine=self.strategy_engine,
            probability_engine=self.probability_engine
        )

        # Ranking
        self.ranking_engine = OpportunityRankingEngine()

        # Opportunity Quality
        self.quality_engine = OpportunityQualityEngine()

        # Portfolio
        self.portfolio_manager = PortfolioManager()
        self.position_sizing = PositionSizingEngine()

        # Execution
        self.signal_stability = SignalStabilityEngine()
        self.execution_engine = ExecutionEngine()

    # -------------------------------------------------
    # Run One Cycle
    # -------------------------------------------------

    def run_cycle(self):

        # ---------------------------------------------
        # Market Universe
        # ---------------------------------------------
        symbols = self.market_universe.get_universe()

        # ---------------------------------------------
        # Market Data
        # ---------------------------------------------
        market_data = self.market_data.load_market_data(symbols)

        # ---------------------------------------------
        # Scanner
        # ---------------------------------------------
        opportunities = self.scanner.run_scan(market_data)

        if not opportunities:
            return

        # ---------------------------------------------
        # Opportunity Ranking
        # ---------------------------------------------
        ranked = self.ranking_engine.rank(opportunities)

        # ---------------------------------------------
        # Opportunity Quality
        # ---------------------------------------------
        market_quality = self.quality_engine.evaluate(ranked)

        # ---------------------------------------------
        # Portfolio Decision
        # ---------------------------------------------
        trades = self.portfolio_manager.select_trades(
            ranked,
            market_quality
        )

        # ---------------------------------------------
        # Position Sizing
        # ---------------------------------------------
        sized_trades = self.position_sizing.apply(trades)

        # ---------------------------------------------
        # Signal Stability
        # ---------------------------------------------
        confirmed_trades = self.signal_stability.confirm(sized_trades)

        # ---------------------------------------------
        # Execution
        # ---------------------------------------------
        self.execution_engine.execute(confirmed_trades)


# -------------------------------------------------
# System Loop
# -------------------------------------------------

def run():

    system = AstraQuant()

    while True:

        try:

            system.run_cycle()

        except Exception as e:

            system.logger.error(str(e))


if __name__ == "__main__":

    run()

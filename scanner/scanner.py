# scanner/scanner.py

"""
Main Market Scanner

Implements the Two-Stage Scanner architecture.

Stage 1 → Fast Scan
    Lightweight ranking of all assets

Stage 2 → Deep Analysis
    Strategy detection + Probability evaluation
    only for selected candidates
"""

from scanner.fast_scanner import FastScanner


class Scanner:

    def __init__(self, strategy_engine, probability_engine, candidate_count=10):

        self.strategy_engine = strategy_engine
        self.probability_engine = probability_engine

        # stage 1 scanner
        self.fast_scanner = FastScanner(candidate_count=candidate_count)

    # -------------------------------------------------
    # Run Full Scan
    # -------------------------------------------------

    def run_scan(self, market_data):

        """
        market_data format:

        {
            "BTC": dataframe,
            "ETH": dataframe,
            ...
        }
        """

        # ---------------------------------------------
        # Stage 1 — Fast Scan
        # ---------------------------------------------

        ranked_assets = self.fast_scanner.rank_assets(market_data)

        candidates = self.fast_scanner.select_candidates(ranked_assets)

        candidate_symbols = [c["symbol"] for c in candidates]

        # ---------------------------------------------
        # Stage 2 — Deep Analysis
        # ---------------------------------------------

        opportunities = []

        for symbol in candidate_symbols:

            df = market_data.get(symbol)

            if df is None:
                continue

            # -----------------------------------------
            # Strategy Detection
            # -----------------------------------------

            strategy_signal = self.strategy_engine.detect(symbol, df)

            if strategy_signal is None:
                continue

            # -----------------------------------------
            # Probability Evaluation
            # -----------------------------------------

            probability = self.probability_engine.evaluate(strategy_signal)

            opportunity = {
                "symbol": symbol,
                "signal": strategy_signal,
                "probability_score": probability
            }

            opportunities.append(opportunity)

        return opportunities

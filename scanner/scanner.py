# scanner/scanner.py

from scanner.fast_scanner import FastScanner


class Scanner:
    """
    Main Market Scanner

    Implements Two-Stage Scanning:

    Stage 1:
        Fast market scan for all assets

    Stage 2:
        Deep analysis only for selected candidates

    Now includes internal observability metrics:
        • strategy_count
        • probability_count
    """

    def __init__(self, strategy_engine, probability_engine, candidate_count=10):

        self.strategy_engine = strategy_engine
        self.probability_engine = probability_engine

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
        # Stage 1: Fast Scan
        # ---------------------------------------------
        ranked_assets = self.fast_scanner.rank_assets(market_data)

        candidates = self.fast_scanner.select_candidates(ranked_assets)

        candidate_symbols = [c["symbol"] for c in candidates]

        # ---------------------------------------------
        # Stage 2: Deep Analysis
        # ---------------------------------------------
        opportunities = []

        strategy_count = 0
        probability_count = 0

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

            strategy_count += 1

            # -----------------------------------------
            # Probability Evaluation
            # -----------------------------------------
            probability = self.probability_engine.evaluate(strategy_signal)

            # (no filtering — always passes)
            probability_count += 1

            opportunity = {
                "symbol": symbol,
                "signal": strategy_signal,
                "probability_score": probability
            }

            opportunities.append(opportunity)

        # ---------------------------------------------
        # Return with Metrics (Observability Only)
        # ---------------------------------------------
        return {
            "opportunities": opportunities,
            "metrics": {
                "strategy_count": strategy_count,
                "probability_count": probability_count
            }
        }

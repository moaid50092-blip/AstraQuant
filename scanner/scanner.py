from scanner.fast_scanner import FastScanner

# 🔥 Momentum
from momentum.momentum_tracker import MomentumTracker

# 🔥 Context
from context.context_analyzer import ContextAnalyzer


class Scanner:

    def __init__(self, strategy_engine, probability_engine, candidate_count=10):

        self.strategy_engine = strategy_engine
        self.probability_engine = probability_engine

        self.fast_scanner = FastScanner(candidate_count=candidate_count)

        # 🔥 minimum probability threshold
        self.min_probability = 0.52

        # 🔥 Momentum tracker (stateful)
        self.momentum_tracker = MomentumTracker(window_size=4)

        # 🔥 Context analyzer
        self.context_analyzer = ContextAnalyzer()

    # -------------------------------------------------
    # Run Full Scan
    # -------------------------------------------------

    def run_scan(self, market_data):

        ranked_assets = self.fast_scanner.rank_assets(market_data)
        candidates = self.fast_scanner.select_candidates(ranked_assets)

        candidate_symbols = [c["symbol"] for c in candidates]

        opportunities = []
        all_signals = []

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

            probability_count += 1

            # -----------------------------------------
            # 🔥 Momentum
            # -----------------------------------------
            self.momentum_tracker.update(symbol, probability)
            momentum_info = self.momentum_tracker.get_momentum_info(symbol)

            # -----------------------------------------
            # 🔥 Context
            # -----------------------------------------
            context = self.context_analyzer.analyze(df)

            # -----------------------------------------
            # 🔥 Real vs Fake Detector (Observation Mode)
            # -----------------------------------------
            setup_quality = "unclear"

            if (
                momentum_info["direction"] == "up"
                and momentum_info["strength"] >= 0.67
                and context["trend"] == "up"
                and context["zone"] != "resistance"
            ):
                setup_quality = "real"

            elif (
                momentum_info["direction"] == "up"
                and (
                    context["zone"] == "resistance"
                    or context["trend"] == "range"
                )
            ):
                setup_quality = "fake"

            # -----------------------------------------
            # Store ALL signals
            # -----------------------------------------
            all_signals.append({
                "symbol": symbol,
                "probability": float(probability),

                # Momentum
                "momentum": momentum_info["direction"],
                "strength": momentum_info["strength"],
                "history": momentum_info["history"],

                # Context
                "trend": context["trend"],
                "zone": context["zone"],
                "breakout": context["breakout"],

                # Setup quality
                "setup": setup_quality
            })

            # -----------------------------------------
            # Filter opportunities
            # -----------------------------------------
            if probability < self.min_probability:
                continue

            opportunity = {
                "symbol": symbol,
                "signal": strategy_signal,
                "probability_score": probability,

                # Momentum
                "momentum": momentum_info["direction"],
                "strength": momentum_info["strength"],

                # Context
                "trend": context["trend"],
                "zone": context["zone"],
                "breakout": context["breakout"],

                # Setup
                "setup": setup_quality
            }

            opportunities.append(opportunity)

        return {
            "opportunities": opportunities,
            "all_signals": all_signals,
            "metrics": {
                "strategy_count": strategy_count,
                "probability_count": probability_count
            }
        }

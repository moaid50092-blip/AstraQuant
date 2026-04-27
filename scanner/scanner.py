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

        self.min_probability = 0.52

        self.momentum_tracker = MomentumTracker(window_size=4)
        self.context_analyzer = ContextAnalyzer()

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

            # Strategy
            strategy_signal = self.strategy_engine.detect(symbol, df)
            if strategy_signal is None:
                continue

            strategy_count += 1

            # Probability
            probability = self.probability_engine.evaluate(strategy_signal)
            probability_count += 1

            # Momentum
            self.momentum_tracker.update(symbol, probability)
            momentum_info = self.momentum_tracker.get_momentum_info(symbol)

            # 🔥 Context (مهم جدًا — الآن مع المومنتوم)
            context = self.context_analyzer.analyze(
                df,
                momentum_info["direction"],
                momentum_info["strength"]
            )

            # -----------------------------------------
            # Store ALL signals
            # -----------------------------------------
            all_signals.append({
                "symbol": symbol,
                "probability": float(probability),

                "momentum": momentum_info["direction"],
                "strength": momentum_info["strength"],
                "history": momentum_info["history"],

                "trend": context["trend"],
                "zone": context["zone"],
                "breakout": context["breakout"],
                "setup": context["setup"]
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

                "momentum": momentum_info["direction"],
                "strength": momentum_info["strength"],

                "trend": context["trend"],
                "zone": context["zone"],
                "breakout": context["breakout"],
                "setup": context["setup"]
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

from scanner.fast_scanner import FastScanner

# 🔥 Momentum
from momentum.momentum_tracker import MomentumTracker

# 🔥 Context
from context.context_analyzer import ContextAnalyzer

# 🔥 MTF
from context.mtf_analyzer import MTFAnalyzer

# 🔥 Decision (SAFE IMPORT)
try:
    from decision.decision_engine_v2 import DecisionEngineV2
    USE_V2 = True
except ImportError:
    from decision.decision_engine import DecisionEngine
    USE_V2 = False


class Scanner:

    def __init__(self, strategy_engine, probability_engine, candidate_count=10):

        self.strategy_engine = strategy_engine
        self.probability_engine = probability_engine

        self.fast_scanner = FastScanner(candidate_count=candidate_count)

        self.min_probability = 0.52

        self.momentum_tracker = MomentumTracker(window_size=4)
        self.context_analyzer = ContextAnalyzer()
        self.mtf_analyzer = MTFAnalyzer()

        # 🔥 Decision Engine (smart init)
        if USE_V2:
            self.decision_engine = DecisionEngineV2()
        else:
            self.decision_engine = DecisionEngine()

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

            frames = market_data.get(symbol)
            if frames is None:
                continue

            df_1m = frames.get("1m")
            df_5m = frames.get("5m")
            df_15m = frames.get("15m")

            if df_1m is None:
                continue

            # Strategy
            strategy_signal = self.strategy_engine.detect(symbol, df_1m)
            if strategy_signal is None:
                continue

            strategy_count += 1

            # Probability
            probability = self.probability_engine.evaluate(strategy_signal)
            probability_count += 1

            # Momentum
            self.momentum_tracker.update(symbol, probability)
            momentum_info = self.momentum_tracker.get_momentum_info(symbol)

            # Context
            context = self.context_analyzer.analyze(
                df_1m,
                momentum_info["direction"],
                momentum_info["strength"]
            )

            # MTF
            mtf = self.mtf_analyzer.analyze(
                df_1m,
                df_5m,
                df_15m
            )

            # -----------------------------------------
            # Decision (V2 or fallback)
            # -----------------------------------------
            decision_input = {
                "probability": probability,
                "momentum": momentum_info["direction"],
                "strength": momentum_info["strength"],
                "trend": context["trend"],
                "zone": context["zone"],
                "breakout": context["breakout"],
                "setup": context["setup"],
                "mtf": {
                    "1m": mtf.get("trend_1m"),
                    "5m": mtf.get("trend_5m"),
                    "15m": mtf.get("trend_15m")
                }
            }

            decision = self.decision_engine.evaluate(decision_input)

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
                "setup": context["setup"],

                "mtf_alignment": mtf.get("alignment"),
                "mtf_trend_1m": mtf.get("trend_1m"),
                "mtf_trend_5m": mtf.get("trend_5m"),
                "mtf_trend_15m": mtf.get("trend_15m"),

                # Decision
                "decision": decision.get("decision"),
                "direction": decision.get("direction"),
                "score": decision.get("score"),
                "reasons": decision.get("reasons"),
            })

            # -----------------------------------------
            # Filter opportunities
            # -----------------------------------------
            if decision.get("decision") != "ENTER":
                continue

            opportunities.append({
                "symbol": symbol,
                "signal": strategy_signal,
                "probability_score": probability,

                "momentum": momentum_info["direction"],
                "strength": momentum_info["strength"],

                "trend": context["trend"],
                "zone": context["zone"],
                "breakout": context["breakout"],
                "setup": context["setup"],

                "mtf_alignment": mtf.get("alignment"),

                "direction": decision.get("direction"),
                "score": decision.get("score"),
            })

        return {
            "opportunities": opportunities,
            "all_signals": all_signals,
            "metrics": {
                "strategy_count": strategy_count,
                "probability_count": probability_count
            }
        }

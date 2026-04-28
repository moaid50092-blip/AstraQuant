from scanner.fast_scanner import FastScanner

# 🔥 Momentum
from momentum.momentum_tracker import MomentumTracker

# 🔥 Context (OLD)
from context.context_analyzer import ContextAnalyzer

# 🔥 Context V2 (NEW Overlay)
from context.context_analyzer_v2 import ContextAnalyzerV2

# 🔥 MTF
from context.mtf_analyzer import MTFAnalyzer

# 🔥 Decision
from decision.decision_engine import DecisionEngineV2


class Scanner:

    def __init__(self, strategy_engine, probability_engine, candidate_count=10):

        self.strategy_engine = strategy_engine
        self.probability_engine = probability_engine

        self.fast_scanner = FastScanner(candidate_count=candidate_count)

        self.min_probability = 0.52

        self.momentum_tracker = MomentumTracker(window_size=4)

        # OLD
        self.context_analyzer = ContextAnalyzer()

        # 🔥 NEW (Overlay فقط)
        self.context_v2 = ContextAnalyzerV2()

        self.mtf_analyzer = MTFAnalyzer()

        self.decision_engine = DecisionEngineV2()

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

            # -----------------------------------------
            # Strategy
            # -----------------------------------------
            strategy_signal = self.strategy_engine.detect(symbol, df_1m)
            if strategy_signal is None:
                continue

            strategy_count += 1

            # -----------------------------------------
            # Probability
            # -----------------------------------------
            probability = self.probability_engine.evaluate(strategy_signal)
            probability_count += 1

            # -----------------------------------------
            # Momentum
            # -----------------------------------------
            self.momentum_tracker.update(symbol, probability)
            momentum_info = self.momentum_tracker.get_momentum_info(symbol)

            # -----------------------------------------
            # Context (OLD)
            # -----------------------------------------
            context = self.context_analyzer.analyze(
                df_1m,
                momentum_info["direction"],
                momentum_info["strength"]
            )

            # -----------------------------------------
            # 🔥 Context V2 (Overlay)
            # -----------------------------------------
            context_v2 = self.context_v2.analyze(
                df_1m,
                momentum_info["direction"],
                momentum_info["strength"],
                context
            )

            # -----------------------------------------
            # MTF
            # -----------------------------------------
            mtf = self.mtf_analyzer.analyze(
                df_1m,
                df_5m,
                df_15m
            )

            # -----------------------------------------
            # Decision
            # -----------------------------------------
            decision = self.decision_engine.evaluate({
                "probability": probability,
                "momentum": momentum_info["direction"],
                "strength": momentum_info["strength"],
                "trend": context["trend"],
                "zone": context["zone"],
                "breakout": context["breakout"],
                "setup": context["setup"],
                "mtf": {
                    "1m": mtf["trend_1m"],
                    "5m": mtf["trend_5m"],
                    "15m": mtf["trend_15m"]
                }
            })

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

                "mtf_alignment": mtf["alignment"],
                "mtf_trend_1m": mtf["trend_1m"],
                "mtf_trend_5m": mtf["trend_5m"],
                "mtf_trend_15m": mtf["trend_15m"],

                # 🔥 Decision
                "decision": decision["decision"],
                "direction": decision["direction"],
                "score": decision["score"],
                "reasons": decision["reasons"],

                # 🔥 NEW (Overlay فقط)
                "confidence_score": context_v2["confidence_score"],
                "confidence_label": context_v2["confidence_label"]
            })

            # -----------------------------------------
            # Filter
            # -----------------------------------------
            if decision["decision"] != "ENTER":
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
                "setup": context["setup"],

                "mtf_alignment": mtf["alignment"],

                "direction": decision["direction"],
                "score": decision["score"],

                # 🔥 NEW
                "confidence": context_v2["confidence_label"]
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

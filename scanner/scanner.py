from scanner.fast_scanner import FastScanner

from momentum.momentum_tracker import MomentumTracker
from context.context_analyzer import ContextAnalyzer
from context.context_analyzer_v2 import ContextAnalyzerV2
from context.mtf_analyzer import MTFAnalyzer

from decision.decision_engine_v3 import DecisionEngineV3
from context.range_engine_v2 import RangeEngineV2


class Scanner:

    def __init__(self, strategy_engine, probability_engine, candidate_count=10):

        self.strategy_engine = strategy_engine
        self.probability_engine = probability_engine

        self.fast_scanner = FastScanner(candidate_count=candidate_count)

        self.momentum_tracker = MomentumTracker(window_size=4)

        self.context_analyzer = ContextAnalyzer()
        self.context_v2 = ContextAnalyzerV2()

        self.mtf_analyzer = MTFAnalyzer()

        self.decision_engine = DecisionEngineV3()

        self.range_engine = RangeEngineV2()

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
            # 🔥 Probability Engine (التعديل الأهم)
            # -----------------------------------------
            probability = self.probability_engine.evaluate(strategy_signal)
            probability_count += 1

            # -----------------------------------------
            # 🔥 HYBRID MOMENTUM
            # -----------------------------------------
            hybrid_strength = (
                0.6 * strategy_signal["strength"] +
                0.4 * abs(probability - 0.5) * 2
            )

            self.momentum_tracker.update(symbol, hybrid_strength)
            momentum_info = self.momentum_tracker.get_momentum_info(symbol)

            if strategy_signal["momentum"] != "neutral":
                momentum_info["direction"] = strategy_signal["momentum"]

            # -----------------------------------------
            # Context
            # -----------------------------------------
            context = self.context_analyzer.analyze(
                df_1m,
                momentum_info["direction"],
                momentum_info["strength"]
            )

            context_v2 = self.context_v2.analyze(
                df_1m,
                momentum_info["direction"],
                momentum_info["strength"],
                context
            )

            # -----------------------------------------
            # RANGE
            # -----------------------------------------
            range_info = self.range_engine.analyze(
                df_1m,
                momentum_info["direction"]
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
            # 🔥 Decision (مع تمرير EARLY)
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
                },

                # 🔥 RANGE
                "range_active": range_info["range_active"],
                "range_signal": range_info["signal"],
                "range_confidence": range_info["confidence"],
                "range_location": range_info["location"],

                # 🔥 CONTEXT
                "confidence": context_v2["confidence_label"],

                # 🔥 EARLY FIX (هذا كان ناقص عندك)
                "early_entry": strategy_signal.get("early_entry", False),
                "acceleration": strategy_signal.get("acceleration", False)
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

                "decision": decision["decision"],
                "direction": decision["direction"],
                "score": decision["score"],
                "reasons": decision.get("reasons", []),

                "confidence_score": context_v2["confidence_score"],
                "confidence_label": context_v2["confidence_label"],

                "range_active": range_info["range_active"],
                "range_signal": range_info["signal"],
                "range_confidence": range_info["confidence"],

                # 🔥 EARLY OUTPUT
                "entry_type": decision.get("entry_type", "STANDARD"),
                "compression": strategy_signal.get("compression", False),
                "acceleration": strategy_signal.get("acceleration", False)
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

                "confidence": context_v2["confidence_label"],

                "range_signal": range_info["signal"],

                "entry_type": decision.get("entry_type", "STANDARD")
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

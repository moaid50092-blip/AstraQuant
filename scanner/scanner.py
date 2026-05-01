from scanner.fast_scanner import FastScanner

from momentum.momentum_tracker import MomentumTracker
from context.context_analyzer import ContextAnalyzer
from context.context_analyzer_v2 import ContextAnalyzerV2
from context.mtf_analyzer import MTFAnalyzer

# 🔥 HYBRID
from decision.decision_engine_hybrid import DecisionEngineHybrid

# 🔥 RANGE
from context.range_engine_v2 import RangeEngineV2

# 🔥 EDGE TRACKER
from analytics.edge_tracker import EdgeTracker


class Scanner:

    def __init__(self, strategy_engine, probability_engine, candidate_count=10):

        self.strategy_engine = strategy_engine
        self.probability_engine = probability_engine

        self.fast_scanner = FastScanner(candidate_count=candidate_count)

        self.momentum_tracker = MomentumTracker(window_size=4)

        self.context_analyzer = ContextAnalyzer()
        self.context_v2 = ContextAnalyzerV2()

        self.mtf_analyzer = MTFAnalyzer()

        self.decision_engine = DecisionEngineHybrid()
        self.range_engine = RangeEngineV2()

        # 🔥 NEW
        self.edge_tracker = EdgeTracker()

    # -------------------------------------------------
    def run_scan(self, market_data):

        ranked_assets = self.fast_scanner.rank_assets(market_data)
        candidates = self.fast_scanner.select_candidates(ranked_assets)

        candidate_symbols = [c["symbol"] for c in candidates]

        opportunities = []
        all_signals = []

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

            # Probability
            base_probability = self.probability_engine.evaluate(strategy_signal)

            # Momentum
            self.momentum_tracker.update(symbol, base_probability)
            momentum_info = self.momentum_tracker.get_momentum_info(symbol)

            # Context
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

            # Range
            range_info = self.range_engine.analyze(
                df_1m,
                momentum_info["direction"]
            ) or {
                "range_active": False,
                "signal": None,
                "confidence": 0,
                "location": None
            }

            # MTF
            mtf = self.mtf_analyzer.analyze(df_1m, df_5m, df_15m)

            # 🔥 Dynamic Probability
            probability = base_probability

            if mtf["alignment"] == "strong":
                probability += 0.02

            if context["breakout"]:
                probability += 0.02

            if range_info["signal"]:
                probability += 0.015

            if context_v2["confidence_label"] == "HIGH":
                probability += 0.025

            probability = min(probability, 0.99)

            # Decision
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
                "range_active": range_info["range_active"],
                "range_signal": range_info["signal"],
                "range_confidence": range_info["confidence"],
                "range_location": range_info["location"],
                "confidence": context_v2["confidence_label"]
            })

            # Store signal
            signal_data = {
                "symbol": symbol,
                "score": decision["score"],
                "probability": probability,
                "confidence_label": context_v2["confidence_label"],
                "mode": decision["mode"],
                "direction": decision["direction"]
            }

            # 🔥 تسجيل الصفقة
            trade_id = None
            if decision["decision"] == "ENTER":
                trade_id = self.edge_tracker.log_trade(signal_data)

            all_signals.append({
                **signal_data,
                "decision": decision["decision"],
                "trade_id": trade_id
            })

            # Filter
            if decision["decision"] != "ENTER":
                continue

            opportunities.append({
                "symbol": symbol,
                "direction": decision["direction"],
                "score": decision["score"],
                "probability": probability,
                "trade_id": trade_id
            })

        return {
            "opportunities": opportunities,
            "all_signals": all_signals
        }

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
    # 🔥 CRO: CLASSIFICATION
    # -------------------------------------------------
    def _classify_trade(self, score, mtf_alignment, breakout):

        if score >= 8 and mtf_alignment == "strong" and breakout:
            return "A+"
        elif score >= 7:
            return "A"
        elif score >= 5.5:
            return "B"
        else:
            return "C"

    # -------------------------------------------------
    # 🔥 CRO: MODE
    # -------------------------------------------------
    def _detect_mode(self, trend, range_active, setup):

        if range_active:
            return "RANGE"
        if setup == "real" and trend in ["up", "down"]:
            return "TREND"
        return "TRANSITION"

    # -------------------------------------------------
    # 🔥 CRO: POSITION SIZE
    # -------------------------------------------------
    def _get_position_size(self, trade_class):

        return {
            "A+": 1.0,
            "A": 0.7,
            "B": 0.4,
            "C": 0.2
        }.get(trade_class, 0.2)

    # -------------------------------------------------
    # 🔥 CRO: TRADE PLAN
    # -------------------------------------------------
    def _build_trade_plan(self, df, direction, trade_class):

        last_price = float(df["close"].iloc[-1])

        # SL بسيط احترافي (مؤقت)
        if direction == "up":
            sl = last_price * 0.995
            tp1 = last_price * 1.01
            tp2 = last_price * 1.02
        else:
            sl = last_price * 1.005
            tp1 = last_price * 0.99
            tp2 = last_price * 0.98

        size = self._get_position_size(trade_class)

        return {
            "entry": round(last_price, 4),
            "sl": round(sl, 4),
            "tp1": round(tp1, 4),
            "tp2": round(tp2, 4),
            "size": size
        }

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
            strategy_signal = self.strategy_engine.detect(symbol, df_1m)
            if strategy_signal is None:
                continue

            strategy_count += 1

            probability = strategy_signal.get("base_score", 0.5)
            probability_count += 1

            hybrid_strength = (
                0.6 * strategy_signal["strength"] +
                0.4 * abs(probability - 0.5) * 2
            )

            self.momentum_tracker.update(symbol, hybrid_strength)
            momentum_info = self.momentum_tracker.get_momentum_info(symbol)

            if strategy_signal["momentum"] != "neutral":
                momentum_info["direction"] = strategy_signal["momentum"]

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
            range_info = self.range_engine.analyze(
                df_1m,
                momentum_info["direction"]
            )

            if range_info is None:
                range_info = {
                    "range_active": False,
                    "signal": None,
                    "confidence": 0,
                    "location": None
                }

            # -----------------------------------------
            mtf = self.mtf_analyzer.analyze(
                df_1m,
                df_5m,
                df_15m
            )

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
                "range_active": range_info["range_active"],
                "range_signal": range_info["signal"],
                "range_confidence": range_info["confidence"],
                "range_location": range_info["location"],
                "confidence": context_v2["confidence_label"]
            })

            # -----------------------------------------
            # 🔥 CRO LOGIC
            # -----------------------------------------
            trade_class = self._classify_trade(
                decision["score"],
                mtf["alignment"],
                context["breakout"]
            )

            trade_mode = self._detect_mode(
                context["trend"],
                range_info["range_active"],
                context["setup"]
            )

            trade_plan = {}

            if decision["decision"] == "ENTER":
                trade_plan = self._build_trade_plan(
                    df_1m,
                    decision["direction"],
                    trade_class
                )

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

                # 🔥 NEW
                "trade_class": trade_class,
                "trade_mode": trade_mode,
                "trade_plan": trade_plan
            })

            # -----------------------------------------
            if decision["decision"] != "ENTER":
                continue

            opportunity = {
                "symbol": symbol,
                "signal": strategy_signal,
                "probability_score": probability,

                "direction": decision["direction"],
                "score": decision["score"],
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

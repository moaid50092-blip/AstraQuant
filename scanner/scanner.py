from scanner.fast_scanner import FastScanner

from momentum.momentum_tracker import MomentumTracker

from context.context_analyzer import ContextAnalyzer
from context.context_analyzer_v2 import ContextAnalyzerV2
from context.mtf_analyzer import MTFAnalyzer

from decision.decision_engine_v3 import DecisionEngineV3
from context.range_engine_v2 import RangeEngineV2


class Scanner:

    def __init__(
        self,
        strategy_engine,
        probability_engine,
        candidate_count=10
    ):

        self.strategy_engine = strategy_engine
        self.probability_engine = probability_engine

        self.fast_scanner = FastScanner(
            candidate_count=candidate_count
        )

        # 🔥 رفع الثبات للذهب والأسواق السريعة
        self.momentum_tracker = MomentumTracker(
            window_size=6
        )

        self.context_analyzer = ContextAnalyzer()

        self.context_v2 = ContextAnalyzerV2()

        self.mtf_analyzer = MTFAnalyzer()

        self.decision_engine = DecisionEngineV3()

        self.range_engine = RangeEngineV2()

    # =================================================
    # 🔥 SAFE FRAME EXTRACTION
    # =================================================

    def _extract_frames(self, frames):

        if not frames:
            return None, None, None

        return (
            frames.get("1m"),
            frames.get("5m"),
            frames.get("15m")
        )

    # =================================================
    # 🔥 BUILD MTF PAYLOAD
    # =================================================

    def _build_mtf_payload(self, mtf):

        return {
            "1m": mtf["trend_1m"],
            "5m": mtf["trend_5m"],
            "15m": mtf["trend_15m"]
        }

    # =================================================
    # 🔥 SMART EARLY MERGE
    # =================================================

    def _merge_early_logic(
        self,
        strategy_signal,
        momentum_info,
        probability,
        context_v2
    ):

        strategy_early = strategy_signal.get(
            "early_entry",
            False
        )

        strategy_accel = strategy_signal.get(
            "acceleration",
            False
        )

        momentum_early = momentum_info.get(
            "early_entry",
            False
        )

        momentum_accel = momentum_info.get(
            "acceleration",
            False
        )

        confidence = context_v2.get(
            "confidence_label",
            "LOW"
        )

        strength = momentum_info.get(
            "strength",
            0
        )

        # =========================================
        # 🔥 PRIMARY MERGE
        # =========================================

        early_entry = (
            strategy_early or momentum_early
        )

        acceleration = (
            strategy_accel or momentum_accel
        )

        # =========================================
        # 🔥 NOISE FILTER
        # =========================================

        if early_entry:

            # EARLY ضعيف
            if (
                strength < 0.42
                and probability < 0.54
            ):
                early_entry = False

            # acceleration بدون ثقة
            if (
                acceleration
                and confidence == "LOW"
                and probability < 0.55
            ):
                acceleration = False

        return early_entry, acceleration

    # =================================================
    # 🔥 BUILD DECISION PAYLOAD
    # =================================================

    def _build_decision_payload(
        self,
        probability,
        momentum_info,
        context,
        mtf,
        range_info,
        context_v2,
        early_entry,
        acceleration
    ):

        return {
            "probability": probability,

            "momentum": momentum_info["direction"],
            "strength": momentum_info["strength"],

            "trend": context["trend"],
            "zone": context["zone"],
            "breakout": context["breakout"],
            "setup": context["setup"],

            "mtf": self._build_mtf_payload(mtf),

            # RANGE
            "range_active": range_info["range_active"],
            "range_signal": range_info["signal"],
            "range_confidence": range_info["confidence"],
            "range_location": range_info["location"],

            # CONTEXT
            "confidence": context_v2[
                "confidence_label"
            ],

            # EARLY
            "early_entry": early_entry,
            "acceleration": acceleration
        }

    # =================================================
    # 🔥 BUILD SIGNAL OBJECT
    # =================================================

    def _build_signal_output(
        self,
        symbol,
        probability,
        momentum_info,
        context,
        mtf,
        decision,
        context_v2,
        range_info,
        strategy_signal,
        acceleration
    ):

        return {
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

            "reasons": decision.get(
                "reasons",
                []
            ),

            "confidence_score": context_v2[
                "confidence_score"
            ],

            "confidence_label": context_v2[
                "confidence_label"
            ],

            # RANGE
            "range_active": range_info[
                "range_active"
            ],

            "range_signal": range_info[
                "signal"
            ],

            "range_confidence": range_info[
                "confidence"
            ],

            # ENTRY
            "entry_type": decision.get(
                "entry_type",
                "STANDARD"
            ),

            # EARLY
            "compression": strategy_signal.get(
                "compression",
                False
            ),

            "acceleration": acceleration
        }

    # =================================================
    # 🔥 BUILD OPPORTUNITY
    # =================================================

    def _build_opportunity(
        self,
        symbol,
        strategy_signal,
        probability,
        momentum_info,
        context,
        mtf,
        decision,
        context_v2,
        range_info
    ):

        return {
            "symbol": symbol,

            "signal": strategy_signal,

            "probability_score": probability,

            "momentum": momentum_info[
                "direction"
            ],

            "strength": momentum_info[
                "strength"
            ],

            "trend": context["trend"],
            "zone": context["zone"],
            "breakout": context["breakout"],
            "setup": context["setup"],

            "mtf_alignment": mtf["alignment"],

            "direction": decision["direction"],
            "score": decision["score"],

            "confidence": context_v2[
                "confidence_label"
            ],

            "range_signal": range_info[
                "signal"
            ],

            "entry_type": decision.get(
                "entry_type",
                "STANDARD"
            )
        }

    # =================================================
    # 🔥 MAIN SCAN LOOP
    # =================================================

    def run_scan(self, market_data):

        ranked_assets = self.fast_scanner.rank_assets(
            market_data
        )

        candidates = self.fast_scanner.select_candidates(
            ranked_assets
        )

        candidate_symbols = [
            c["symbol"]
            for c in candidates
        ]

        opportunities = []

        all_signals = []

        strategy_count = 0
        probability_count = 0

        # =============================================
        # 🔥 MAIN LOOP
        # =============================================

        for symbol in candidate_symbols:

            try:

                frames = market_data.get(symbol)

                df_1m, df_5m, df_15m = (
                    self._extract_frames(frames)
                )

                # -------------------------------------
                # SAFETY
                # -------------------------------------

                if (
                    df_1m is None
                    or len(df_1m) < 30
                ):
                    continue

                # -------------------------------------
                # STRATEGY
                # -------------------------------------

                strategy_signal = (
                    self.strategy_engine.detect(
                        symbol,
                        df_1m
                    )
                )

                if strategy_signal is None:
                    continue

                strategy_count += 1

                # -------------------------------------
                # PROBABILITY
                # -------------------------------------

                probability = (
                    self.probability_engine.evaluate(
                        strategy_signal
                    )
                )

                probability_count += 1

                # -------------------------------------
                # 🔥 HYBRID MOMENTUM
                # -------------------------------------

                hybrid_strength = (
                    0.6 *
                    strategy_signal["strength"]

                    +

                    0.4 *
                    abs(probability - 0.5) * 2
                )

                self.momentum_tracker.update(
                    symbol,
                    hybrid_strength
                )

                momentum_info = (
                    self.momentum_tracker
                    .get_momentum_info(symbol)
                )

                # =====================================
                # 🔥 DIRECTION OVERRIDE
                # =====================================

                if (
                    strategy_signal["momentum"]
                    != "neutral"
                ):

                    momentum_info["direction"] = (
                        strategy_signal["momentum"]
                    )

                # -------------------------------------
                # CONTEXT
                # -------------------------------------

                context = (
                    self.context_analyzer.analyze(
                        df_1m,
                        momentum_info["direction"],
                        momentum_info["strength"]
                    )
                )

                context_v2 = (
                    self.context_v2.analyze(
                        df_1m,
                        momentum_info["direction"],
                        momentum_info["strength"],
                        context
                    )
                )

                # -------------------------------------
                # RANGE
                # -------------------------------------

                range_info = (
                    self.range_engine.analyze(
                        df_1m,
                        momentum_info["direction"]
                    )
                )

                # -------------------------------------
                # MTF
                # -------------------------------------

                mtf = self.mtf_analyzer.analyze(
                    df_1m,
                    df_5m,
                    df_15m
                )

                # =====================================
                # 🔥 SMART EARLY SYSTEM
                # =====================================

                early_entry, acceleration = (
                    self._merge_early_logic(
                        strategy_signal,
                        momentum_info,
                        probability,
                        context_v2
                    )
                )

                # -------------------------------------
                # DECISION
                # -------------------------------------

                decision_payload = (
                    self._build_decision_payload(
                        probability,
                        momentum_info,
                        context,
                        mtf,
                        range_info,
                        context_v2,
                        early_entry,
                        acceleration
                    )
                )

                decision = (
                    self.decision_engine.evaluate(
                        decision_payload
                    )
                )

                # -------------------------------------
                # STORE SIGNAL
                # -------------------------------------

                signal_output = (
                    self._build_signal_output(
                        symbol,
                        probability,
                        momentum_info,
                        context,
                        mtf,
                        decision,
                        context_v2,
                        range_info,
                        strategy_signal,
                        acceleration
                    )
                )

                all_signals.append(signal_output)

                # -------------------------------------
                # FILTER ENTRIES
                # -------------------------------------

                if decision["decision"] != "ENTER":
                    continue

                opportunity = (
                    self._build_opportunity(
                        symbol,
                        strategy_signal,
                        probability,
                        momentum_info,
                        context,
                        mtf,
                        decision,
                        context_v2,
                        range_info
                    )
                )

                opportunities.append(opportunity)

            # =========================================
            # 🔥 ISOLATED FAIL PROTECTION
            # =========================================

            except Exception as e:

                print(
                    f"\n⚠️ Scanner Error "
                    f"[{symbol}] → {e}"
                )

                continue

        # =============================================
        # 🔥 SORT OUTPUTS
        # =============================================

        opportunities = sorted(
            opportunities,
            key=lambda x: (
                x.get("score", 0),
                x.get("probability_score", 0)
            ),
            reverse=True
        )

        all_signals = sorted(
            all_signals,
            key=lambda x: (
                x.get("decision") == "ENTER",
                x.get("probability", 0),
                x.get("strength", 0)
            ),
            reverse=True
        )

        return {
            "opportunities": opportunities,

            "all_signals": all_signals,

            "metrics": {
                "strategy_count": strategy_count,
                "probability_count": probability_count
            }
        }

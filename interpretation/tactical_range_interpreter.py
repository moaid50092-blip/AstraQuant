# interpretation/tactical_range_interpreter.py


class TacticalRangeInterpreter:

    """
    Passive tactical semantic interpreter.

    Responsibilities:
    - Translate raw range context
      into descriptive behavioral semantics
    - Improve operator readability
    - Remain fully isolated from:
        - execution authority
        - lifecycle logic
        - probability modification
        - signal filtering
        - behavioral mutation

    Important:
    - Descriptive only
    - Non-authoritative
    - Operator-facing only
    """

    # ==================================================
    # 🔥 INTERPRET
    # ==================================================

    def interpret(
        self,
        range_result,
        momentum_dir=None
    ):

        if not range_result:
            return {}

        if not range_result.get("range_active"):
            return {}

        semantics = {

            "rotation_stability":
                self._interpret_rotation_stability(
                    range_result
                ),

            "context_state":
                self._interpret_context_state(
                    range_result,
                    momentum_dir
                ),

            "structural_persistence":
                self._interpret_structural_persistence(
                    range_result
                ),

            "zone_interaction":
                self._interpret_zone_interaction(
                    range_result
                ),

            "rotational_behavior":
                self._interpret_rotational_behavior(
                    range_result
                )
        }

        return semantics

    # ==================================================
    # 🔥 ROTATION STABILITY
    # ==================================================

    def _interpret_rotation_stability(
        self,
        range_result
    ):

        confidence = range_result.get(
            "confidence",
            0
        )

        rejection = range_result.get(
            "rejection"
        )

        fake_breakout = range_result.get(
            "fake_breakout"
        )

        # ==========================================
        # 🔥 STABLE
        # ==========================================

        if (
            confidence >= 0.7
            and (
                rejection is not None
                or fake_breakout is not None
            )
        ):

            return "Stable"

        # ==========================================
        # 🔥 FRAGMENTED
        # ==========================================

        if confidence < 0.35:

            return "Fragmented"

        # ==========================================
        # 🔥 TRANSITIONAL
        # ==========================================

        return "Transitional"

    # ==================================================
    # 🔥 CONTEXT STATE
    # ==================================================

    def _interpret_context_state(
        self,
        range_result,
        momentum_dir
    ):

        signal = range_result.get(
            "signal"
        )

        if (
            signal is None
            or momentum_dir is None
        ):

            return "Mixed"

        aligned = (
            (signal == "BUY" and momentum_dir == "up")
            or
            (signal == "SELL" and momentum_dir == "down")
        )

        opposite = (
            (signal == "BUY" and momentum_dir == "down")
            or
            (signal == "SELL" and momentum_dir == "up")
        )

        if aligned:

            return "Aligned"

        if opposite:

            return "Counter-Rotational"

        return "Mixed"

    # ==================================================
    # 🔥 STRUCTURAL PERSISTENCE
    # ==================================================

    def _interpret_structural_persistence(
        self,
        range_result
    ):

        confidence = range_result.get(
            "confidence",
            0
        )

        if confidence >= 0.8:

            return "Sustained"

        if confidence <= 0.3:

            return "Fading"

        return "Responsive"

    # ==================================================
    # 🔥 ZONE INTERACTION
    # ==================================================

    def _interpret_zone_interaction(
        self,
        range_result
    ):

        location = range_result.get(
            "location"
        )

        rejection = range_result.get(
            "rejection"
        )

        fake_breakout = range_result.get(
            "fake_breakout"
        )

        if (
            location in ["top", "bottom"]
            and (
                rejection is not None
                or fake_breakout is not None
            )
        ):

            return "Responsive"

        if location == "middle":

            return "Neutral"

        return "Weak"

    # ==================================================
    # 🔥 ROTATIONAL BEHAVIOR
    # ==================================================

    def _interpret_rotational_behavior(
        self,
        range_result
    ):

        rejection = range_result.get(
            "rejection"
        )

        fake_breakout = range_result.get(
            "fake_breakout"
        )

        # ==========================================
        # 🔥 REACTIVE
        # ==========================================

        if fake_breakout is not None:

            return "Reactive"

        # ==========================================
        # 🔥 BALANCED
        # ==========================================

        if rejection is not None:

            return "Balanced"

        # ==========================================
        # 🔥 NOISY
        # ==========================================

        return "Noisy"

import numpy as np


class ProbabilityEngine:

    def __init__(self):
        pass

    # -------------------------------------------------
    def evaluate(self, signal):

        base = signal.get("base_score", 0.5)

        # =========================================
        # 🔥 HIERARCHICAL MODIFIERS
        # =========================================

        structure = signal.get("structure_score", 0.5)
        mtf = signal.get("mtf_score", 0.5)
        liquidity = signal.get("liquidity_score", 0.5)

        context = signal.get("context_score", 0.5)
        historical = signal.get("historical_score", 0.5)
        volatility = signal.get("volatility_score", 0.5)

        factor = signal.get("factor_score", 0.5)
        session = signal.get("session_score", 0.5)

        # =========================================
        # 🔥 WEIGHTED MARKET EDGE
        # =========================================

        weighted_edge = (

            structure * 0.25 +
            mtf * 0.20 +
            liquidity * 0.15 +

            factor * 0.12 +
            historical * 0.10 +

            volatility * 0.08 +
            context * 0.05 +
            session * 0.05
        )

        # =========================================
        # 🔥 BLEND WITH BASE SCORE
        # =========================================

        edge = (
            base * 0.55 +
            weighted_edge * 0.45
        )

        # =========================================
        # 🔥 AGREEMENT ENGINE
        # =========================================

        core = [
            structure,
            mtf,
            liquidity,
            factor
        ]

        aligned = sum(
            1 for x in core
            if abs(x - 0.5) > 0.08
        )

        if aligned >= 4:
            edge += 0.03

        elif aligned <= 1:
            edge -= 0.04

        # =========================================
        # 🔥 DISPERSION FILTER
        # =========================================

        variance = np.var(core)
        std = variance ** 0.5

        if std > 0.16:
            edge -= 0.05

        elif std < 0.05:
            edge += 0.03

        # =========================================
        # 🔥 VOLATILITY SANITY
        # =========================================

        if volatility > 0.9:
            edge -= 0.04

        elif volatility < 0.15:
            edge -= 0.03

        # =========================================
        # 🔥 EARLY INTELLIGENCE
        # =========================================

        early = signal.get("early_entry", False)
        acceleration = signal.get("acceleration", False)

        strength = signal.get("strength", 0)

        if (
            early
            and acceleration
            and structure > 0.55
            and mtf > 0.55
            and strength > 0.5
        ):
            edge += 0.035

        elif early and strength > 0.45:
            edge += 0.01

        # =========================================
        # 🔥 NON-LINEAR CURVE
        # =========================================

        if edge > 0.62:
            edge += (edge - 0.62) * 0.35

        elif edge < 0.38:
            edge -= (0.38 - edge) * 0.35

        # =========================================
        # 🔥 RANGE PENALTY
        # =========================================

        if (
            structure < 0.52
            and mtf < 0.52
            and liquidity < 0.55
        ):
            edge -= 0.04

        # =========================================
        # 🔥 FINAL NORMALIZATION
        # =========================================

        return self._normalize(edge)

    # -------------------------------------------------
    def _normalize(self, value):

        value = max(
            0.0,
            min(1.0, value)
        )

        return round(value, 3)

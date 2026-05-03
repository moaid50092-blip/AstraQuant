class ProbabilityEngine:

    def __init__(self):
        pass

    # -------------------------------------------------
    def evaluate(self, signal):

        base = signal.get("base_score", 0.5)

        modifiers = [
            signal.get("structure_score", 0.5),
            signal.get("liquidity_score", 0.5),
            signal.get("session_score", 0.5),
            signal.get("context_score", 0.5),
            signal.get("mtf_score", 0.5),
            signal.get("factor_score", 0.5),
            signal.get("historical_score", 0.5),
            signal.get("volatility_score", 0.5)
        ]

        # =========================================
        # 🔥 CRO CORE LOGIC (Dynamic Edge)
        # =========================================

        # deviation from neutral
        deviations = [(m - 0.5) for m in modifiers]

        avg_dev = sum(deviations) / len(deviations)

        # 🔥 Adaptive Multiplier (حسب قوة السوق)
        strength = abs(base - 0.5)

        if strength > 0.15:
            multiplier = 1.6   # سوق قوي
        elif strength > 0.08:
            multiplier = 1.4   # متوسط
        else:
            multiplier = 1.2   # سوق ضعيف

        edge = base + (avg_dev * multiplier)

        # =========================================
        # 🔥 NON-LINEAR PUSH (يعطي حركة حقيقية)
        # =========================================

        if edge > 0.55:
            edge += (edge - 0.55) * 0.6

        elif edge < 0.45:
            edge -= (0.45 - edge) * 0.6

        # =========================================
        # 🔥 EARLY INTELLIGENCE BOOST
        # =========================================

        if signal.get("early_entry"):
            edge += 0.03

        if signal.get("acceleration"):
            edge += 0.02

        # =========================================

        return self._normalize(edge)

    # -------------------------------------------------
    def _normalize(self, value):

        if value < 0:
            return 0

        if value > 1:
            return 1

        return round(value, 3)

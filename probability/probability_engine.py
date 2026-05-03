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
        # 🔥 CRO CORE LOGIC
        # =========================================

        # نحسب الانحراف عن 0.5
        deviations = [(m - 0.5) for m in modifiers]

        # متوسط التأثير
        avg_dev = sum(deviations) / len(deviations)

        # قوة التأثير (تضخيم ذكي)
        edge = base + (avg_dev * 1.8)

        # =========================================

        return self._normalize(edge)

    # -------------------------------------------------
    def _normalize(self, value):

        if value < 0:
            return 0

        if value > 1:
            return 1

        return round(value, 3)

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
        # 🔥 STEP 1: BASE EDGE
        # =========================================

        deviations = [(m - 0.5) for m in modifiers]
        avg_dev = sum(deviations) / len(deviations)

        strength = abs(base - 0.5)

        if strength > 0.15:
            multiplier = 1.7
        elif strength > 0.08:
            multiplier = 1.5
        else:
            multiplier = 1.25

        edge = base + (avg_dev * multiplier)

        # =========================================
        # 🔥 STEP 2: AGREEMENT BOOST
        # =========================================

        aligned = sum(1 for m in modifiers if abs(m - 0.5) > 0.08)

        if aligned >= 6:
            edge += 0.04
        elif aligned <= 2:
            edge -= 0.04

        # =========================================
        # 🔥 STEP 3: DISPERSION FILTER
        # =========================================

        mean = sum(modifiers) / len(modifiers)
        variance = sum((m - mean) ** 2 for m in modifiers) / len(modifiers)
        std = variance ** 0.5

        if std > 0.18:
            edge -= 0.05   # تضارب عالي = تقليل الثقة

        elif std < 0.08:
            edge += 0.05   # توافق عالي = تعزيز

        # =========================================
        # 🔥 STEP 4: NON-LINEAR EXPANSION
        # =========================================

        if edge > 0.56:
            edge += (edge - 0.56) * 0.8

        elif edge < 0.44:
            edge -= (0.44 - edge) * 0.8

        # =========================================
        # 🔥 STEP 5: EARLY INTELLIGENCE (SMART)
        # =========================================

        if signal.get("early_entry"):
            edge += 0.02

        if signal.get("acceleration"):
            edge += 0.025

        # إذا الاثنين موجودين
        if signal.get("early_entry") and signal.get("acceleration"):
            edge += 0.02

        # =========================================
        # 🔥 STEP 6: FINAL CLAMP
        # =========================================

        return self._normalize(edge)

    # -------------------------------------------------
    def _normalize(self, value):

        if value < 0:
            return 0

        if value > 1:
            return 1

        return round(value, 3)

class DecisionEngineV2:

    def evaluate(self, signal):

        reasons = []
        score = 0

        prob = signal.get("probability", 0)
        momentum = signal.get("momentum")
        strength = signal.get("strength", 0)

        trend = signal.get("trend")
        zone = signal.get("zone")
        breakout = signal.get("breakout")
        setup = signal.get("setup")

        mtf = signal.get("mtf", {})

        mtf_values = list(mtf.values()) if isinstance(mtf, dict) else []

        # =================================================
        # 🔥 1) GATE (فلتر صارم)
        # =================================================

        if setup == "fake":
            return self._ignore("FAKE SETUP")

        if trend == "range":
            return self._ignore("RANGE MARKET")

        if strength < 0.5:
            return self._ignore("WEAK MOMENTUM")

        # =================================================
        # 🔥 2) تحديد الاتجاه
        # =================================================

        if momentum == "up":
            direction = "LONG"
        elif momentum == "down":
            direction = "SHORT"
        else:
            return self._ignore("NO CLEAR DIRECTION")

        # =================================================
        # 🔥 3) Smart Scoring
        # =================================================

        # Setup
        if setup == "real":
            score += 2
            reasons.append("REAL SETUP")

        # Momentum Strength
        if strength >= 0.67:
            score += 2
            reasons.append("STRONG MOMENTUM")

        # Trend alignment
        if momentum == trend:
            score += 1
            reasons.append("TREND ALIGN")

        # MTF alignment (مرن)
        aligned = sum(1 for x in mtf_values if x == momentum)

        if aligned >= 2:
            score += 2
            reasons.append("MTF ALIGN")

        # Breakout (ذكي)
        if breakout:
            score += 2
            reasons.append("BREAKOUT")

        # Probability
        if prob >= 0.55:
            score += 1
            reasons.append("HIGH PROB")

        # =================================================
        # 🔥 4) Zone Risk (نقطة قوية جدًا)
        # =================================================

        if direction == "LONG" and zone == "high":
            score -= 2
            reasons.append("BAD ZONE (HIGH)")

        if direction == "SHORT" and zone == "low":
            score -= 2
            reasons.append("BAD ZONE (LOW)")

        # =================================================
        # 🔥 5) القرار النهائي
        # =================================================

        if score >= 7:
            decision = "ENTER"
        elif score >= 5:
            decision = "WATCH"
        else:
            decision = "IGNORE"

        return {
            "decision": decision,
            "direction": direction,
            "score": score,
            "reasons": reasons
        }

    # -----------------------------------------------------

    def _ignore(self, reason):
        return {
            "decision": "IGNORE",
            "direction": "NONE",
            "score": 0,
            "reasons": [reason]
        }

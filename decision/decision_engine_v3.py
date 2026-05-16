class DecisionEngineV3:

    def __init__(self):

        self.weights = {
            "trend": 2.5,
            "mtf": 2.0,
            "breakout": 3.0,
            "momentum": 2.0,
            "zone": 1.0,
            "range": 2.0,
            "setup": 2.0
        }

        self.trend_threshold = 6
        self.range_threshold = 4.8
        self.transition_threshold = 7

    # -------------------------------------------------
    # 🔥 GATEKEEPER
    # -------------------------------------------------
    def gate(self, data):

        if data.get("setup") == "fake":
            return "FAKE SETUP"

        strength = data.get("strength", 0)
        momentum = data.get("momentum")

        early = data.get("early_entry", False)

        mtf = data.get("mtf", {})

        mtf_1m = mtf.get("1m")
        mtf_5m = mtf.get("5m")
        mtf_15m = mtf.get("15m")

        breakout = data.get("breakout", False)

        zone = data.get("zone")

        trend = data.get("trend")

        acceleration = data.get(
            "acceleration",
            False
        )

        # =========================================
        # 🔥 PRESSURE DETECTION
        # =========================================

        mtf_down_pressure = (
            mtf_1m == "down"
            and mtf_5m == "down"
        )

        mtf_up_pressure = (
            mtf_1m == "up"
            and mtf_5m == "up"
        )

        # =========================================
        # 🔥 BUY FILTER
        # =========================================

        if momentum == "up":

            if strength < 0.45:
                return "WEAK MOMENTUM"

            # BUY ضد ضغط هابط
            if (
                mtf_down_pressure
                and not early
            ):
                return "MTF DOWN PRESSURE"

            # منع BUY إذا 15m عكس كامل
            if (
                mtf_15m == "down"
                and strength < 0.6
            ):
                return "HTF SELL PRESSURE"

            # 🔥 exhaustion suppression
            if (
                zone == "high"
                and not breakout
                and strength < 0.62
            ):
                return "BUY EXHAUSTION"

            # 🔥 weak transitional continuation
            if (
                trend != "up"
                and not breakout
                and strength < 0.58
            ):
                return "WEAK TRANSITION"

        # =========================================
        # 🔥 SELL FILTER
        # =========================================

        if momentum == "down":

            if strength < 0.40:
                return "WEAK MOMENTUM"

            if (
                not breakout
                and not early
                and strength < 0.55
            ):
                return "WEAK MOMENTUM"

            # SELL ضد ضغط صاعد
            if (
                mtf_up_pressure
                and not early
            ):
                return "MTF UP PRESSURE"

            # منع SELL إذا 15m صاعد بقوة
            if (
                mtf_15m == "up"
                and strength < 0.6
            ):
                return "HTF BUY PRESSURE"

            # 🔥 exhaustion suppression
            if (
                zone == "low"
                and not breakout
                and strength < 0.62
            ):
                return "SELL EXHAUSTION"

            # 🔥 weak transitional continuation
            if (
                trend != "down"
                and not breakout
                and strength < 0.58
            ):
                return "WEAK TRANSITION"

        # =========================================
        # 🔥 EARLY VALIDATION
        # =========================================

        if early:

            if not acceleration:
                return "WEAK EARLY"

            if strength < 0.5:
                return "WEAK EARLY"

            if (
                breakout is False
                and strength < 0.6
            ):
                return "UNCONFIRMED EARLY"

        # =========================================
        # 🔥 RANGE FILTER
        # =========================================

        if (
            data.get("trend") == "range"
            and not data.get("range_signal")
        ):
            return "EMPTY RANGE"

        return None

    # -------------------------------------------------
    # 🔥 MODE DETECTION
    # -------------------------------------------------
    def detect_mode(self, data):

        mtf = data.get("mtf", {})

        aligned_trend = (
            mtf.get("1m") ==
            mtf.get("5m") ==
            mtf.get("15m")
        )

        # 🔥 range فقط إذا السوق فعلاً غير متفق
        if (
            data.get("range_active")
            and not aligned_trend
        ):
            return "RANGE"

        # 🔥 trend فقط إذا في breakout حقيقي
        if (
            data.get("breakout")
            and aligned_trend
        ):
            return "TREND"

        return "TRANSITION"

    # -------------------------------------------------
    # 🔥 TREND SCORE
    # -------------------------------------------------
    def calculate_trend_score(self, data):

        score = 0

        if data["trend"] in ["up", "down"]:
            score += self.weights["trend"]

        mtf = data["mtf"]

        aligned = sum(
            1 for x in mtf.values()
            if x == data["momentum"]
        )

        if aligned >= 2:
            score += self.weights["mtf"]

        # breakout أهم عنصر
        if data["breakout"]:
            score += self.weights["breakout"]

        if data["strength"] >= 0.6:
            score += self.weights["momentum"]

        # zone confluence
        if data["zone"] in ["low", "high"]:
            score += self.weights["zone"]

        # setup quality
        if data["setup"] == "real":
            score += self.weights["setup"]

        # =========================================
        # 🔥 DIRECTIONAL CONFLUENCE
        # =========================================

        momentum = data.get("momentum")
        zone = data.get("zone")

        breakout = data.get("breakout")

        if (
            momentum == "up"
            and zone == "low"
        ):
            score += 0.5

        elif (
            momentum == "down"
            and zone == "high"
        ):
            score += 0.5

        # 🔥 breakout continuation boost
        if (
            breakout
            and aligned >= 3
            and data["strength"] >= 0.65
        ):
            score += 0.7

        # 🔥 exhaustion penalty
        if (
            momentum == "up"
            and zone == "high"
            and not breakout
        ):
            score -= 1.0

        elif (
            momentum == "down"
            and zone == "low"
            and not breakout
        ):
            score -= 1.0

        return score

    # -------------------------------------------------
    # 🔥 RANGE SCORE
    # -------------------------------------------------
    def calculate_range_score(self, data):

        signal = data.get("range_signal")
        conf = data.get("range_confidence", 0)

        if not signal:
            return 0, None

        score = self.weights["range"]

        # confidence scaling
        conf_score = min(1.0, conf / 2)

        score += conf_score * 1.5

        mtf = data.get("mtf", {})

        aligned = sum(
            1 for x in mtf.values()
            if x == data["momentum"]
        )

        # 🔥 confluence boost
        if aligned >= 2:
            score += 0.5

        # 🔥 noisy range suppression
        if aligned == 0:
            score -= 1.0

        # 🔥 weak rotational rejection
        if conf < 1.2:
            score -= 0.8

        # 🔥 zone logic
        if (
            signal == "BUY"
            and data["zone"] == "low"
        ):
            score += 0.8

        elif (
            signal == "SELL"
            and data["zone"] == "high"
        ):
            score += 0.8

        else:
            score -= 0.7

        # 🔥 breakout contamination
        if (
            data.get("breakout")
            and conf < 1.5
        ):
            score -= 0.8

        return score, signal

    # -------------------------------------------------
    # 🔥 INTELLIGENCE ADJUSTMENT
    # -------------------------------------------------
    def intelligence_adjustment(
        self,
        score,
        threshold,
        data
    ):

        prob = data.get("probability", 0)

        confidence = data.get(
            "confidence",
            "MEDIUM"
        )

        mode = self.detect_mode(data)

        # =========================================
        # 🔥 PROBABILITY
        # =========================================

        if prob > 0.65:
            score += 1.2

        elif prob > 0.6:
            score += 0.8

        elif prob > 0.55:
            score += 0.4

        elif prob < 0.46:
            threshold += 1.2

        elif prob < 0.49:
            threshold += 0.6

        # =========================================
        # 🔥 CONFIDENCE
        # =========================================

        if confidence == "HIGH":
            score += 0.7

        elif confidence == "LOW":
            threshold += 0.8

        # =========================================
        # 🔥 TRANSITIONAL HARDENING
        # =========================================

        if mode == "TRANSITION":

            mtf = data.get("mtf", {})

            aligned = sum(
                1 for x in mtf.values()
                if x == data.get("momentum")
            )

            breakout = data.get("breakout")

            strength = data.get("strength", 0)

            # 🔥 fragmented structure penalty
            if aligned <= 1:
                threshold += 1.0

            # 🔥 weak continuation suppression
            if strength < 0.58:
                threshold += 0.8

            # 🔥 low-quality expansion rejection
            if (
                not breakout
                and aligned < 2
            ):
                threshold += 0.7

        return score, threshold

    # -------------------------------------------------
    # 🔥 POSITION SIZE
    # -------------------------------------------------
    def position_size(self, score, prob):

        if prob > 0.65 and score >= 8:
            return 1.2

        if score >= 8:
            return 1.0

        elif score >= 6:
            return 0.7

        elif score >= 4.5:
            return 0.4

        return 0.0

    # -------------------------------------------------
    # 🔥 DIRECTION OVERLAY
    # -------------------------------------------------
    def apply_direction_overlay(
        self,
        data,
        direction
    ):

        trend = data.get("trend")
        zone = data.get("zone")

        mtf = data.get("mtf", {})

        # =========================================
        # 🔥 HTF OVERRIDE
        # =========================================

        if (
            mtf.get("5m") == "down"
            and mtf.get("15m") == "down"
        ):
            return "down"

        if (
            mtf.get("5m") == "up"
            and mtf.get("15m") == "up"
        ):
            return "up"

        # =========================================
        # 🔥 CONTEXT FALLBACK
        # =========================================

        if (
            trend == "down"
            and zone == "high"
        ):
            return "down"

        if (
            trend == "up"
            and zone == "low"
        ):
            return "up"

        return direction

    # -------------------------------------------------
    # 🔥 ENTRY CLASSIFICATION
    # -------------------------------------------------
    def classify_entry(
        self,
        data,
        score,
        threshold
    ):

        prob = data.get("probability", 0)

        confidence = data.get(
            "confidence",
            "MEDIUM"
        )

        early = data.get("early_entry", False)

        acceleration = data.get(
            "acceleration",
            False
        )

        strength = data.get("strength", 0)

        breakout = data.get("breakout")

        # =========================================
        # 🔥 EARLY
        # =========================================

        if (
            early
            and acceleration
            and breakout
            and strength > 0.55
            and prob > 0.58
        ):
            return "EARLY"

        # =========================================
        # 🔥 STRONG
        # =========================================

        if (
            prob > 0.6
            and confidence == "HIGH"
            and score >= threshold + 1
        ):
            return "STRONG"

        return "STANDARD"

    # -------------------------------------------------
    # 🔥 MAIN EVALUATION
    # -------------------------------------------------
    def evaluate(self, data):

        # =========================================
        # 🔥 GATE
        # =========================================

        gate_reason = self.gate(data)

        if gate_reason:

            return {
                "decision": "IGNORE",
                "direction": None,
                "score": 0,
                "mode": "BLOCKED",
                "size": 0,
                "reasons": [gate_reason],
                "entry_type": "STANDARD"
            }

        # =========================================
        # 🔥 MODE
        # =========================================

        mode = self.detect_mode(data)

        if mode == "TREND":

            score = self.calculate_trend_score(data)

            threshold = self.trend_threshold

            direction = data["momentum"]

        elif mode == "RANGE":

            score, direction = self.calculate_range_score(
                data
            )

            # 🔥 weak range rejection
            if data.get("range_confidence", 0) < 1.2:

                return {
                    "decision": "IGNORE",
                    "direction": None,
                    "score": round(score, 2),
                    "mode": mode,
                    "size": 0,
                    "reasons": ["weak range"],
                    "entry_type": "STANDARD"
                }

            threshold = self.range_threshold

        else:

            score = self.calculate_trend_score(data)

            threshold = self.transition_threshold

            direction = data["momentum"]

            # =====================================
            # 🔥 TRANSITIONAL FILTERING
            # =====================================

            mtf = data.get("mtf", {})

            aligned = sum(
                1 for x in mtf.values()
                if x == direction
            )

            if aligned <= 1:
                threshold += 1.0

            if (
                not data.get("breakout")
                and data.get("strength", 0) < 0.6
            ):
                threshold += 0.8

        # =========================================
        # 🔥 DIRECTION OVERLAY
        # =========================================

        direction = self.apply_direction_overlay(
            data,
            direction
        )

        # =========================================
        # 🔥 INTELLIGENCE
        # =========================================

        score, threshold = self.intelligence_adjustment(
            score,
            threshold,
            data
        )

        # =========================================
        # 🔥 EARLY FILTERING
        # =========================================

        early = data.get("early_entry", False)

        acceleration = data.get(
            "acceleration",
            False
        )

        strength = data.get("strength", 0)

        confidence = data.get(
            "confidence",
            "MEDIUM"
        )

        prob = data.get("probability", 0)

        breakout = data.get("breakout")

        # =========================================
        # 🔥 KILL WEAK EARLY
        # =========================================

        if (
            early
            and (
                strength < 0.5
                or prob < 0.55
                or not acceleration
            )
        ):
            early = False

        final_threshold = threshold

        # =========================================
        # 🔥 SMART EARLY THRESHOLD
        # =========================================

        if early:

            # 🔥 production-grade early
            if (
                acceleration
                and breakout
                and confidence == "HIGH"
                and prob > 0.6
                and strength > 0.58
            ):

                final_threshold -= 1.0

            elif (
                acceleration
                and confidence == "MEDIUM"
                and prob > 0.57
                and strength > 0.54
            ):

                final_threshold -= 0.3

            else:
                # early ضعيف = عقوبة
                final_threshold += 0.8

        # =========================================
        # 🔥 FINAL DIRECTIONAL VALIDATION
        # =========================================

        mtf = data.get("mtf", {})

        aligned = sum(
            1 for x in mtf.values()
            if x == direction
        )

        if (
            decision := (
                "ENTER"
                if score >= final_threshold
                else (
                    "WATCH"
                    if score >= final_threshold - 2
                    else "IGNORE"
                )
            )
        ) == "ENTER":

            # 🔥 weak directional confluence
            if aligned < 2:
                decision = "WATCH"

            # 🔥 exhaustion suppression
            if (
                direction == "up"
                and data.get("zone") == "high"
                and not breakout
            ):
                decision = "WATCH"

            elif (
                direction == "down"
                and data.get("zone") == "low"
                and not breakout
            ):
                decision = "WATCH"

            # 🔥 weak breakout continuation
            if (
                breakout
                and strength < 0.58
            ):
                decision = "WATCH"

        # =========================================
        # 🔥 ENTRY TYPE
        # =========================================

        entry_type = self.classify_entry(
            data,
            score,
            final_threshold
        )

        return {
            "decision": decision,
            "direction": direction,
            "score": round(score, 2),
            "mode": mode,
            "size": self.position_size(
                score,
                data.get("probability", 0)
            ),
            "reasons": [mode.lower()],
            "entry_type": entry_type
        }

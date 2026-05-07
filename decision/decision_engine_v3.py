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

        # =========================================
        # 🔥 SELL FILTER
        # =========================================

        if momentum == "down":

            if strength < 0.40:
                return "WEAK MOMENTUM"

            if (
                not data.get("breakout")
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

        # 🔥 zone logic
        if (
            signal == "BUY"
            and data["zone"] == "low"
        ):
            score += 0.5

        elif (
            signal == "SELL"
            and data["zone"] == "high"
        ):
            score += 0.5

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

        # =========================================
        # 🔥 EARLY
        # =========================================

        if (
            early
            and acceleration
            and strength > 0.45
            and prob > 0.54
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
            if data.get("range_confidence", 0) < 1:

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

        # =========================================
        # 🔥 KILL WEAK EARLY
        # =========================================

        if (
            early
            and (
                strength < 0.4
                or prob < 0.52
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
                and confidence == "HIGH"
                and prob > 0.58
            ):

                final_threshold -= 1.0

            elif (
                confidence == "MEDIUM"
                and prob > 0.55
            ):

                final_threshold -= 0.3

            else:
                # early ضعيف = عقوبة
                final_threshold += 0.5

        # =========================================
        # 🔥 FINAL DECISION
        # =========================================

        if score >= final_threshold:

            decision = "ENTER"

        elif score >= final_threshold - 2:

            decision = "WATCH"

        else:

            decision = "IGNORE"

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

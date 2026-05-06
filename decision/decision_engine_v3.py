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
    def gate(self, data):

        if data.get("setup") == "fake":
            return "FAKE SETUP"

        strength = data.get("strength", 0)
        momentum = data.get("momentum")
        early = data.get("early_entry", False)

        # BUY
        if momentum == "up" and strength < 0.45:
            return "WEAK MOMENTUM"

        # SELL (أذكى)
        if momentum == "down":
            if strength < 0.40:
                return "WEAK MOMENTUM"

            if not data.get("breakout") and not early and strength < 0.55:
                return "WEAK MOMENTUM"

        # RANGE
        if data.get("trend") == "range" and not data.get("range_signal"):
            return "EMPTY RANGE"

        return None

    # -------------------------------------------------
    def detect_mode(self, data):

        if data.get("range_active") and not data.get("breakout"):
            return "RANGE"

        if data.get("breakout") and data["mtf"]["1m"] == data["mtf"]["5m"] == data["mtf"]["15m"]:
            return "TREND"

        return "TRANSITION"

    # -------------------------------------------------
    def calculate_trend_score(self, data):

        score = 0

        if data["trend"] in ["up", "down"]:
            score += self.weights["trend"]

        mtf = data["mtf"]
        aligned = sum(1 for x in mtf.values() if x == data["momentum"])

        if aligned >= 2:
            score += self.weights["mtf"]

        if data["breakout"]:
            score += self.weights["breakout"]

        if data["strength"] >= 0.6:
            score += self.weights["momentum"]

        if data["zone"] in ["low", "high"]:
            score += self.weights["zone"]

        if data["setup"] == "real":
            score += self.weights["setup"]

        return score

    # -------------------------------------------------
    def calculate_range_score(self, data):

        signal = data.get("range_signal")
        conf = data.get("range_confidence", 0)

        if not signal:
            return 0, None

        conf_score = min(1.0, conf / 2)

        score = conf_score * 2
        score += self.weights["range"]

        if (signal == "BUY" and data["momentum"] == "up") or \
           (signal == "SELL" and data["momentum"] == "down"):
            score += 0.5

        return score, signal

    # -------------------------------------------------
    def intelligence_adjustment(self, score, threshold, data):

        prob = data.get("probability", 0)
        confidence = data.get("confidence", "MEDIUM")

        if prob > 0.6:
            score += 1.0
        elif prob > 0.55:
            score += 0.5
        elif prob < 0.48:
            threshold += 1.0

        if confidence == "HIGH":
            score += 0.7
        elif confidence == "LOW":
            threshold += 1.0

        return score, threshold

    # -------------------------------------------------
    def position_size(self, score, prob):

        if prob > 0.6 and score >= 8:
            return 1.2

        if score >= 8:
            return 1.0
        elif score >= 6:
            return 0.7
        elif score >= 4.5:
            return 0.4
        else:
            return 0.0

    # -------------------------------------------------
    def apply_direction_overlay(self, data, direction):

        trend = data.get("trend")
        zone = data.get("zone")

        if trend == "down" and zone == "high":
            return "down"

        if trend == "up" and zone == "low":
            return "up"

        return direction

    # -------------------------------------------------
    def classify_entry(self, data, score, threshold):

        prob = data.get("probability", 0)
        confidence = data.get("confidence", "MEDIUM")
        early = data.get("early_entry", False)
        acceleration = data.get("acceleration", False)
        strength = data.get("strength", 0)

        # ⚡ EARLY (محسّن)
        if early and (acceleration or strength > 0.6) and prob > 0.5:
            return "EARLY"

        # 🚀 STRONG
        if (
            prob > 0.58
            and confidence == "HIGH"
            and score >= threshold + 1
        ):
            return "STRONG"

        return "STANDARD"

    # -------------------------------------------------
    def evaluate(self, data):

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

        mode = self.detect_mode(data)

        if mode == "TREND":
            score = self.calculate_trend_score(data)
            threshold = self.trend_threshold
            direction = data["momentum"]

        elif mode == "RANGE":
            score, direction = self.calculate_range_score(data)

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

        direction = self.apply_direction_overlay(data, direction)

        score, threshold = self.intelligence_adjustment(score, threshold, data)

        # 🔥 EARLY LOGIC (محسّن)
        early = data.get("early_entry", False)
        acceleration = data.get("acceleration", False)
        strength = data.get("strength", 0)

        # فلتر EARLY الضعيف
        if early and strength < 0.35:
            early = False

        final_threshold = threshold

        if early:
            if acceleration:
                final_threshold -= 1.8
            else:
                final_threshold -= 1.0

        # 🎯 DECISION
        if score >= final_threshold:
            decision = "ENTER"
        elif score >= final_threshold - 2:
            decision = "WATCH"
        else:
            decision = "IGNORE"

        entry_type = self.classify_entry(data, score, final_threshold)

        return {
            "decision": decision,
            "direction": direction,
            "score": round(score, 2),
            "mode": mode,
            "size": self.position_size(score, data.get("probability", 0)),
            "reasons": [mode.lower()],
            "entry_type": entry_type
        }

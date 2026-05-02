class DecisionEngineV3:

    def __init__(self):

        # 🔥 Weights (نفسها)
        self.weights = {
            "trend": 2.5,
            "mtf": 2.0,
            "breakout": 3.0,
            "momentum": 2.0,
            "zone": 1.0,
            "range": 2.0,
            "setup": 2.0
        }

        # 🔥 Thresholds (CRO BALANCED)
        self.trend_threshold = 6
        self.range_threshold = 4.8
        self.transition_threshold = 6.3   # 🔥 كان 7 → صار أخف شوي

    # -------------------------------------------------
    # 🧠 Smart Gate
    # -------------------------------------------------
    def gate(self, data):

        if data.get("setup") == "fake":
            return "FAKE SETUP"

        if data.get("strength", 0) < 0.45:
            return "WEAK MOMENTUM"

        if data.get("trend") == "range" and not data.get("range_signal"):
            return "EMPTY RANGE"

        return None

    # -------------------------------------------------
    # 🧠 Detect Mode
    # -------------------------------------------------
    def detect_mode(self, data):

        if data.get("range_active") and not data.get("breakout"):
            return "RANGE"

        if data.get("breakout") and data["mtf"]["1m"] == data["mtf"]["5m"] == data["mtf"]["15m"]:
            return "TREND"

        return "TRANSITION"

    # -------------------------------------------------
    # 📊 Trend Score (🔥 فيه التعديل)
    # -------------------------------------------------
    def calculate_trend_score(self, data):

        score = 0

        if data["trend"] in ["up", "down"]:
            score += self.weights["trend"]

        mtf = data["mtf"]
        aligned = sum(1 for x in mtf.values() if x == data["momentum"])

        # 🔥 CRO FIX (أهم تعديل)
        if aligned == 3:
            score += self.weights["mtf"]
        elif aligned == 2:
            score += self.weights["mtf"] * 0.6   # 👈 دعم MEDIUM بدل صفر

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
    # 📦 Range Score
    # -------------------------------------------------
    def calculate_range_score(self, data):

        signal = data.get("range_signal")
        conf = data.get("range_confidence", 0)

        if not signal:
            return 0, None

        score = conf * 1.5
        score += self.weights["range"]

        if (signal == "BUY" and data["momentum"] == "up") or \
           (signal == "SELL" and data["momentum"] == "down"):
            score += 0.3

        return score, signal

    # -------------------------------------------------
    # 🧠 Intelligence Layer
    # -------------------------------------------------
    def intelligence_adjustment(self, score, threshold, data):

        prob = data.get("probability", 0)
        confidence = data.get("confidence", "MEDIUM")

        if prob > 0.6:
            score += 0.5
        elif prob < 0.5:
            threshold += 0.5

        if confidence == "HIGH":
            score += 0.5
        elif confidence == "LOW":
            threshold += 0.7

        return score, threshold

    # -------------------------------------------------
    # 🎯 Position Size
    # -------------------------------------------------
    def position_size(self, score):

        if score >= 8:
            return 1.0
        elif score >= 6:
            return 0.7
        elif score >= 4.5:
            return 0.4
        else:
            return 0.0

    # -------------------------------------------------
    # 🚀 MAIN
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
                "threshold": None,
                "raw_score": 0
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
                    "threshold": self.range_threshold,
                    "raw_score": round(score, 2)
                }

            threshold = self.range_threshold

        else:
            score = self.calculate_trend_score(data)
            threshold = self.transition_threshold
            direction = data["momentum"]

        score, threshold = self.intelligence_adjustment(score, threshold, data)

        raw_score = score

        if score >= threshold:
            decision = "ENTER"
        elif score >= threshold - 2:
            decision = "WATCH"
        else:
            decision = "IGNORE"

        return {
            "decision": decision,
            "direction": direction,
            "score": round(score, 2),
            "mode": mode,
            "size": self.position_size(score),
            "reasons": [mode.lower()],
            "threshold": round(threshold, 2),
            "raw_score": round(raw_score, 2)
        }

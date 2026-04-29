class DecisionEngineV3:

    def __init__(self):

        # 🔥 Thresholds
        self.trend_threshold = 6
        self.range_threshold = 1.2   # أخف لأن الرينج مختلف
        self.transition_threshold = 7

    # -------------------------------------------------
    # 🧠 Detect Market Mode
    # -------------------------------------------------
    def detect_mode(self, data):

        trend = data["trend"]
        breakout = data["breakout"]
        mtf = data["mtf"]

        if breakout and mtf["1m"] == mtf["5m"] == mtf["15m"]:
            return "TREND"

        if trend == "range" and not breakout:
            return "RANGE"

        return "TRANSITION"

    # -------------------------------------------------
    # 📊 TREND Logic (نفس القديم)
    # -------------------------------------------------
    def evaluate_trend(self, data):

        score = 0

        if data["trend"] in ["up", "down"]:
            score += 2.5

        mtf = data["mtf"]
        if mtf["1m"] == mtf["5m"] == mtf["15m"]:
            score += 2.0

        if data["breakout"]:
            score += 3.0

        if data["strength"] >= 0.6:
            score += 2.0

        if data["zone"] in ["low", "high"]:
            score += 1.0

        return score

    # -------------------------------------------------
    # 📦 RANGE Logic (الجديد 🔥)
    # -------------------------------------------------
    def evaluate_range(self, data):

        range_signal = data.get("range_signal")
        range_conf = data.get("range_confidence", 0)

        if range_signal is None:
            return 0, None

        score = range_conf

        # تعزيز بسيط مع المومنتوم
        if data["momentum"] == "up" and range_signal == "BUY":
            score += 0.3

        if data["momentum"] == "down" and range_signal == "SELL":
            score += 0.3

        direction = "BUY" if range_signal == "BUY" else "SELL"

        return score, direction

    # -------------------------------------------------
    # 🎯 Position Size
    # -------------------------------------------------
    def position_size(self, score):

        if score >= 8:
            return 1.0
        elif score >= 6:
            return 0.7
        elif score >= 4:
            return 0.4
        else:
            return 0.0

    # -------------------------------------------------
    # 🚀 Main Evaluation
    # -------------------------------------------------
    def evaluate(self, data):

        mode = self.detect_mode(data)

        # =============================
        # 🔥 TREND MODE
        # =============================
        if mode == "TREND":

            score = self.evaluate_trend(data)

            if score >= self.trend_threshold:
                decision = "ENTER"
            elif score >= self.trend_threshold - 2:
                decision = "WATCH"
            else:
                decision = "IGNORE"

            direction = data["momentum"]

        # =============================
        # 📦 RANGE MODE
        # =============================
        elif mode == "RANGE":

            score, direction = self.evaluate_range(data)

            if score >= self.range_threshold:
                decision = "ENTER"
            elif score >= self.range_threshold - 0.5:
                decision = "WATCH"
            else:
                decision = "IGNORE"

        # =============================
        # ⚠️ TRANSITION MODE
        # =============================
        else:

            score = self.evaluate_trend(data)

            if score >= self.transition_threshold:
                decision = "ENTER"
            else:
                decision = "IGNORE"

            direction = data["momentum"]

        size = self.position_size(score)

        return {
            "decision": decision,
            "direction": direction,
            "score": round(score, 2),
            "mode": mode,
            "size": size
        }

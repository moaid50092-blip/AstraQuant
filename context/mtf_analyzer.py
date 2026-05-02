# context/mtf_analyzer.py

class MTFAnalyzer:

    def __init__(self):
        pass

    def _get_trend(self, df):

        if df is None or len(df) < 5:
            return "unknown", 0.0

        closes = df["close"].values[-5:]

        up_moves = sum(1 for x, y in zip(closes, closes[1:]) if y > x)
        down_moves = sum(1 for x, y in zip(closes, closes[1:]) if y < x)

        total = len(closes) - 1
        if total == 0:
            return "range", 0.0

        up_ratio = up_moves / total
        down_ratio = down_moves / total

        strength = max(up_ratio, down_ratio)

        if up_ratio > 0.6:
            return "up", strength
        elif down_ratio > 0.6:
            return "down", strength
        else:
            return "range", strength

    # -------------------------------------------------
    def analyze(self, df_1m, df_5m, df_15m):

        t1, s1 = self._get_trend(df_1m)
        t5, s5 = self._get_trend(df_5m)
        t15, s15 = self._get_trend(df_15m)

        trends = [t1, t5, t15]

        # -----------------------------------------
        # Alignment Logic (احترافي)
        # -----------------------------------------

        same = len(set(trends)) == 1
        majority = max(set(trends), key=trends.count)

        # 🔥 alignment score (0 → 1)
        score = (
            (1 if t1 == majority else 0) * 0.4 +
            (1 if t5 == majority else 0) * 0.35 +
            (1 if t15 == majority else 0) * 0.25
        )

        # 🔥 label
        if same and majority != "range":
            alignment = "strong"
        elif score >= 0.6:
            alignment = "medium"
        else:
            alignment = "weak"

        # 🔥 bias
        if alignment != "weak" and majority in ["up", "down"]:
            bias = majority
        else:
            bias = "neutral"

        return {
            "trend_1m": t1,
            "trend_5m": t5,
            "trend_15m": t15,

            # 🔥 OLD (محافظة عليه)
            "alignment": alignment,

            # 🔥 NEW CRO
            "alignment_score": round(score, 2),
            "mtf_bias": bias,

            # 🔥 strengths (مهم لاحقًا)
            "strength_1m": round(s1, 2),
            "strength_5m": round(s5, 2),
            "strength_15m": round(s15, 2)
        }

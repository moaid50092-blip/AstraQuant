import numpy as np


class ContextAnalyzerV2:

    def __init__(self):
        self.w_short = 0.4
        self.w_mid = 0.35
        self.w_long = 0.25

    # -------------------------------------------------
    def _trend_score(self, closes, n):

        if len(closes) < n:
            return "range", 0.0

        seq = closes[-n:]
        diffs = np.diff(seq)

        total = len(diffs)
        if total == 0:
            return "range", 0.0

        up_moves = np.sum(diffs > 0)
        down_moves = np.sum(diffs < 0)

        up_ratio = up_moves / total
        down_ratio = down_moves / total

        strength = max(up_ratio, down_ratio)

        if up_ratio > 0.6:
            return "up", float(strength)
        elif down_ratio > 0.6:
            return "down", float(strength)
        else:
            return "range", float(strength)

    # -------------------------------------------------
    def _volatility(self, highs, lows):

        if len(highs) < 20:
            return float(np.mean(highs - lows))

        ranges = highs - lows
        return float(np.mean(ranges[-20:]))

    # -------------------------------------------------
    def analyze(self, df, momentum_dir, momentum_strength, base_context):

        closes = df["close"].values
        highs = df["high"].values
        lows = df["low"].values

        if momentum_dir not in ["up", "down"]:
            return {
                "confidence_score": 0.0,
                "confidence_label": "LOW",
                "reasons": ["NO MOMENTUM"]
            }

        # =========================
        # Trends
        # =========================
        short_trend, short_strength = self._trend_score(closes, 6)
        mid_trend, mid_strength = self._trend_score(closes, 20)
        long_trend, long_strength = self._trend_score(closes, 80)

        trends = [short_trend, mid_trend, long_trend]
        strengths = [short_strength, mid_strength, long_strength]
        weights = [self.w_short, self.w_mid, self.w_long]

        score = 0.0
        reasons = []

        align_count = 0

        for t, s, w, name in zip(trends, strengths, weights, ["SHORT", "MID", "LONG"]):

            if t == momentum_dir:
                score += w * s
                align_count += 1
                reasons.append(f"{name} ALIGN")
            else:
                score -= w * 0.6   # 🔥 عقوبة أقوى
                reasons.append(f"{name} MISALIGN")

        # =========================
        # 🔥 Global Alignment Boost
        # =========================
        if align_count == 3:
            score += 0.2
            reasons.append("FULL ALIGNMENT")
        elif align_count == 2:
            score += 0.1
            reasons.append("PARTIAL ALIGNMENT")
        else:
            score -= 0.15
            reasons.append("WEAK ALIGNMENT")

        # =========================
        # Momentum Boost
        # =========================
        if momentum_strength >= 0.65:
            score += 0.15
            reasons.append("STRONG MOMENTUM")

        # =========================
        # Zone Logic (مصَحّح)
        # =========================
        zone = base_context.get("zone")

        if momentum_dir == "up" and zone == "high":
            score -= 0.2
            reasons.append("BUY AT TOP")

        if momentum_dir == "down" and zone == "low":
            score -= 0.2
            reasons.append("SELL AT BOTTOM")

        # =========================
        # Breakout Intelligence
        # =========================
        if base_context.get("breakout"):

            recent_range = float(np.max(highs[-10:]) - np.min(lows[-10:]))
            avg_vol = float(np.mean(highs - lows))

            if recent_range > avg_vol:
                score += 0.2
                reasons.append("STRONG BREAKOUT")
            else:
                score += 0.08
                reasons.append("WEAK BREAKOUT")

        # =========================
        # Volatility Filter
        # =========================
        vol = self._volatility(highs, lows)
        avg_vol = float(np.mean(highs - lows))

        if vol < avg_vol * 0.7:
            score -= 0.12
            reasons.append("LOW VOLATILITY")

        # =========================
        # Normalize ذكي
        # =========================
        score = (score + 1) / 2   # تحويل من [-1,1] إلى [0,1]
        score = max(0.0, min(1.0, score))

        # =========================
        # Label محسّن
        # =========================
        if score >= 0.72:
            label = "HIGH"
        elif score >= 0.55:
            label = "MEDIUM"
        else:
            label = "LOW"

        return {
            "confidence_score": round(float(score), 3),
            "confidence_label": label,
            "reasons": reasons
        }

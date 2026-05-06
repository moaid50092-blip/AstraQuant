import numpy as np


class ContextAnalyzerV2:

    def __init__(self):
        # Weights
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

        # -----------------------------
        # Safety: No clear momentum
        # -----------------------------
        if momentum_dir not in ["up", "down"]:
            return {
                "confidence_score": 0.3,   # 🔥 بدل 0.0 (مهم)
                "confidence_label": "LOW",
                "short_trend": "range",
                "mid_trend": "range",
                "long_trend": "range",
                "reasons": ["NO MOMENTUM"]
            }

        # -----------------------------
        # Trend Layers
        # -----------------------------
        short_trend, short_strength = self._trend_score(closes, 6)
        mid_trend, mid_strength = self._trend_score(closes, 20)
        long_trend, long_strength = self._trend_score(closes, 80)

        # -----------------------------
        # Volatility
        # -----------------------------
        vol = self._volatility(highs, lows)
        avg_vol = float(np.mean(highs - lows))

        # -----------------------------
        # Alignment Score
        # -----------------------------
        score = 0.5   # 🔥 نبدأ من neutral بدل 0
        reasons = []

        def score_layer(trend, strength, weight, name):
            if trend == momentum_dir:
                return weight * strength, f"{name} ALIGN"
            else:
                return -weight * 0.35, f"{name} MISALIGN"  # 🔥 تخفيف العقوبة

        s, r = score_layer(short_trend, short_strength, self.w_short, "SHORT")
        score += s
        reasons.append(r)

        s, r = score_layer(mid_trend, mid_strength, self.w_mid, "MID")
        score += s
        reasons.append(r)

        s, r = score_layer(long_trend, long_strength, self.w_long, "LONG")
        score += s
        reasons.append(r)

        # -----------------------------
        # Momentum Boost
        # -----------------------------
        if momentum_strength >= 0.67:
            score += 0.12
            reasons.append("STRONG MOMENTUM")

        # -----------------------------
        # Zone Logic
        # -----------------------------
        zone = base_context.get("zone")

        if momentum_dir == "up" and zone == "high":
            score -= 0.1
            reasons.append("HIGH ZONE")

        if momentum_dir == "down" and zone == "low":
            score -= 0.1
            reasons.append("LOW ZONE")

        # -----------------------------
        # Breakout Intelligence
        # -----------------------------
        if base_context.get("breakout"):
            recent_range = float(np.max(highs[-10:]) - np.min(lows[-10:]))
            if recent_range > avg_vol:
                score += 0.12
                reasons.append("STRONG BREAKOUT")
            else:
                score += 0.05
                reasons.append("WEAK BREAKOUT")

        # -----------------------------
        # Volatility Filter
        # -----------------------------
        if vol < avg_vol * 0.7:
            score -= 0.08
            reasons.append("LOW VOLATILITY")

        # -----------------------------
        # Clamp (0 → 1)
        # -----------------------------
        score = max(0.0, min(1.0, score))

        # -----------------------------
        # Label
        # -----------------------------
        if score >= 0.7:
            label = "HIGH"
        elif score >= 0.52:
            label = "MEDIUM"
        else:
            label = "LOW"

        return {
            "confidence_score": float(round(score, 3)),
            "confidence_label": label,
            "short_trend": short_trend,
            "mid_trend": mid_trend,
            "long_trend": long_trend,
            "reasons": reasons
        }

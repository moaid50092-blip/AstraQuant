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
                "confidence_numeric": 0.0,
                "confidence_bias": "neutral",
                "alignment_score": 0.0,
                "short_trend": "range",
                "mid_trend": "range",
                "long_trend": "range",
                "reasons": ["NO MOMENTUM"]
            }

        short_trend, short_strength = self._trend_score(closes, 6)
        mid_trend, mid_strength = self._trend_score(closes, 20)
        long_trend, long_strength = self._trend_score(closes, 80)

        vol = self._volatility(highs, lows)
        avg_vol = float(np.mean(highs - lows))

        raw_score = 0.0
        reasons = []

        def score_layer(trend, strength, weight, name):
            if trend == momentum_dir:
                return weight * strength, f"{name} ALIGN"
            else:
                return -weight * 0.3, f"{name} MISALIGN"

        s, r = score_layer(short_trend, short_strength, self.w_short, "SHORT")
        raw_score += s
        reasons.append(r)

        s, r = score_layer(mid_trend, mid_strength, self.w_mid, "MID")
        raw_score += s
        reasons.append(r)

        s, r = score_layer(long_trend, long_strength, self.w_long, "LONG")
        raw_score += s
        reasons.append(r)

        if momentum_strength >= 0.67:
            raw_score += 0.15
            reasons.append("STRONG MOMENTUM")

        zone = base_context.get("zone")

        if momentum_dir == "up" and zone == "high":
            raw_score -= 0.2
            reasons.append("AT RESISTANCE")

        if momentum_dir == "down" and zone == "low":
            raw_score -= 0.2
            reasons.append("AT SUPPORT")

        if base_context.get("breakout"):
            recent_range = float(np.max(highs[-10:]) - np.min(lows[-10:]))
            if recent_range > avg_vol:
                raw_score += 0.15
                reasons.append("STRONG BREAKOUT")
            else:
                raw_score += 0.05
                reasons.append("WEAK BREAKOUT")

        if vol < avg_vol * 0.7:
            raw_score -= 0.1
            reasons.append("LOW VOLATILITY")

        # 🔥 normalization
        score = max(0.0, min(1.0, raw_score))

        # 🔥 label
        if score >= 0.75:
            label = "HIGH"
        elif score >= 0.55:
            label = "MEDIUM"
        else:
            label = "LOW"

        # 🔥 bias
        if score > 0.65:
            bias = momentum_dir
        else:
            bias = "neutral"

        return {
            "confidence_score": float(score),
            "confidence_label": label,

            # 🔥 NEW CRO
            "confidence_numeric": float(score),
            "confidence_bias": bias,
            "alignment_score": float(raw_score),

            "short_trend": short_trend,
            "mid_trend": mid_trend,
            "long_trend": long_trend,
            "reasons": reasons
        }

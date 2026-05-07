import numpy as np


class MTFAnalyzer:

    def __init__(self):
        pass

    # -------------------------------------------------
    # 🔥 Production-grade Trend Engine
    # -------------------------------------------------
    def _compute_trend(self, closes):

        closes = np.array(
            [c for c in closes if c == c],
            dtype=float
        )

        n = len(closes)

        # -----------------------------------------
        # 🔥 fallback
        # -----------------------------------------

        if n < 5:
            return "unknown", 0.0

        # -----------------------------------------
        # 🔥 low-data mode
        # -----------------------------------------

        if n < 20:

            diffs = np.diff(closes)

            up = np.sum(diffs > 0)
            down = np.sum(diffs < 0)

            total = up + down

            if total == 0:
                return "range", 0.0

            up_ratio = up / total
            down_ratio = down / total

            slope_strength = abs(
                (closes[-1] - closes[0]) / closes[0]
            )

            strength = min(
                1.0,
                slope_strength * 10
            )

            if up_ratio >= 0.62:
                return "up", float(strength)

            elif down_ratio >= 0.62:
                return "down", float(strength)

            return "range", float(strength)

        # -----------------------------------------
        # 🔥 multi-window pressure
        # -----------------------------------------

        short = closes[-5:]
        mid = closes[-10:]
        long = closes[-20:]

        def slope(arr):

            if arr[0] == 0:
                return 0

            return (arr[-1] - arr[0]) / arr[0]

        s_slope = slope(short)
        m_slope = slope(mid)
        l_slope = slope(long)

        avg_slope = (
            s_slope * 0.5 +
            m_slope * 0.3 +
            l_slope * 0.2
        )

        # -----------------------------------------
        # 🔥 directional consistency
        # -----------------------------------------

        diffs = np.diff(closes[-10:])

        if len(diffs) == 0:
            return "range", 0.0

        up_ratio = np.sum(diffs > 0) / len(diffs)
        down_ratio = np.sum(diffs < 0) / len(diffs)

        # -----------------------------------------
        # 🔥 adaptive thresholds
        # -----------------------------------------

        slope_strength = abs(avg_slope)

        if slope_strength < 0.0008:
            consistency_threshold = 0.68

        elif slope_strength < 0.0015:
            consistency_threshold = 0.60

        else:
            consistency_threshold = 0.55

        # -----------------------------------------
        # 🔥 final strength
        # -----------------------------------------

        strength = min(
            1.0,
            slope_strength * 14
        )

        # -----------------------------------------
        # 🔥 final decision
        # -----------------------------------------

        if (
            avg_slope > 0
            and up_ratio >= consistency_threshold
        ):
            return "up", float(strength)

        elif (
            avg_slope < 0
            and down_ratio >= consistency_threshold
        ):
            return "down", float(strength)

        return "range", float(strength)

    # -------------------------------------------------
    def analyze(self, df_1m, df_5m, df_15m):

        def process(df):

            if df is None or len(df) < 3:
                return "unknown", 0.0

            closes = df["close"].values

            return self._compute_trend(closes)

        trend_1m, str_1m = process(df_1m)
        trend_5m, str_5m = process(df_5m)
        trend_15m, str_15m = process(df_15m)

        # -----------------------------------------
        # 🔥 hierarchy
        # -----------------------------------------

        trends = {
            "1m": trend_1m,
            "5m": trend_5m,
            "15m": trend_15m
        }

        strengths = {
            "1m": str_1m,
            "5m": str_5m,
            "15m": str_15m
        }

        # -----------------------------------------
        # 🔥 HTF authority
        # -----------------------------------------

        htf_bias = trend_15m

        if htf_bias == "range":
            dominant_bias = trend_5m
        else:
            dominant_bias = htf_bias

        # -----------------------------------------
        # 🔥 alignment engine
        # -----------------------------------------

        aligned_count = sum(
            1 for t in trends.values()
            if t == dominant_bias
        )

        weighted_strength = (
            str_1m * 0.15 +
            str_5m * 0.35 +
            str_15m * 0.50
        )

        # -----------------------------------------
        # 🔥 alignment classification
        # -----------------------------------------

        if (
            dominant_bias != "range"
            and aligned_count == 3
            and weighted_strength > 0.55
        ):
            alignment = "strong"

        elif (
            dominant_bias != "range"
            and aligned_count >= 2
            and weighted_strength > 0.38
        ):
            alignment = "medium"

        else:
            alignment = "weak"

        # -----------------------------------------
        # 🔥 directional pressure
        # -----------------------------------------

        directional_pressure = "neutral"

        if trend_5m == trend_15m:

            if trend_15m == "up":
                directional_pressure = "bullish"

            elif trend_15m == "down":
                directional_pressure = "bearish"

        # -----------------------------------------
        avg_strength = (
            str_1m +
            str_5m +
            str_15m
        ) / 3

        return {
            "trend_1m": trend_1m,
            "trend_5m": trend_5m,
            "trend_15m": trend_15m,

            "strength_1m": round(str_1m, 2),
            "strength_5m": round(str_5m, 2),
            "strength_15m": round(str_15m, 2),

            "alignment": alignment,
            "avg_strength": round(avg_strength, 2),

            # 🔥 NEW
            "dominant_bias": dominant_bias,
            "directional_pressure": directional_pressure
        }

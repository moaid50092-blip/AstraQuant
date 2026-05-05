import numpy as np


class MTFAnalyzer:

    def __init__(self):
        pass

    # -------------------------------------------------
    def _compute_trend(self, closes):

        if len(closes) < 20:
            return "unknown", 0.0

        # 🔥 Multi-window trend
        short = closes[-5:]
        mid = closes[-10:]
        long = closes[-20:]

        def slope(arr):
            return (arr[-1] - arr[0]) / arr[0] if arr[0] != 0 else 0

        s_slope = slope(short)
        m_slope = slope(mid)
        l_slope = slope(long)

        # 🔥 Average slope
        avg_slope = (s_slope * 0.5 + m_slope * 0.3 + l_slope * 0.2)

        strength = min(1.0, abs(avg_slope) * 10)

        # 🔥 Noise filter
        diffs = np.diff(closes[-10:])
        consistency = np.sum(diffs > 0) / len(diffs) if avg_slope > 0 else np.sum(diffs < 0) / len(diffs)

        if avg_slope > 0.001 and consistency > 0.6:
            return "up", float(strength)

        elif avg_slope < -0.001 and consistency > 0.6:
            return "down", float(strength)

        else:
            return "range", float(strength)

    # -------------------------------------------------
    def analyze(self, df_1m, df_5m, df_15m):

        def process(df):
            if df is None or len(df) < 20:
                return "unknown", 0.0

            closes = df["close"].values
            return self._compute_trend(closes)

        trend_1m, str_1m = process(df_1m)
        trend_5m, str_5m = process(df_5m)
        trend_15m, str_15m = process(df_15m)

        trends = [trend_1m, trend_5m, trend_15m]
        strengths = [str_1m, str_5m, str_15m]

        # -----------------------------------------
        # 🔥 Smart Alignment
        # -----------------------------------------

        same = len(set(trends)) == 1 and trends[0] != "range"

        aligned_count = sum(1 for t in trends if t == trend_1m and t != "range")

        avg_strength = sum(strengths) / 3

        if same and avg_strength > 0.6:
            alignment = "strong"

        elif aligned_count >= 2 and avg_strength > 0.4:
            alignment = "medium"

        else:
            alignment = "weak"

        return {
            "trend_1m": trend_1m,
            "trend_5m": trend_5m,
            "trend_15m": trend_15m,

            "strength_1m": round(str_1m, 2),
            "strength_5m": round(str_5m, 2),
            "strength_15m": round(str_15m, 2),

            "alignment": alignment,
            "avg_strength": round(avg_strength, 2)
        }

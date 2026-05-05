import numpy as np


class MTFAnalyzer:

    def __init__(self):
        pass

    # -------------------------------------------------
    # 🔥 Robust Trend Engine (CRO-grade)
    # -------------------------------------------------
    def _compute_trend(self, closes):

        # 🔥 تنظيف NaN
        closes = np.array([c for c in closes if c == c], dtype=float)

        n = len(closes)

        # -----------------------------------------
        # 🔥 Fallback إذا البيانات قليلة (ما بنرجع unknown بسهولة)
        # -----------------------------------------
        if n < 5:
            return "unknown", 0.0

        if n < 20:
            # Dominance logic (بدل ما نكون blind)
            diffs = np.diff(closes)
            up = np.sum(diffs > 0)
            down = np.sum(diffs < 0)

            total = up + down
            if total == 0:
                return "range", 0.0

            up_ratio = up / total
            down_ratio = down / total

            strength = min(1.0, abs((closes[-1] - closes[0]) / closes[0]) * 8)

            if up_ratio >= 0.65:
                return "up", float(strength)
            elif down_ratio >= 0.65:
                return "down", float(strength)
            else:
                return "range", float(strength)

        # -----------------------------------------
        # 🔥 Multi-window (dynamic & stable)
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

        # 🔥 Weighted slope (أكثر استقرار)
        avg_slope = (s_slope * 0.5 + m_slope * 0.3 + l_slope * 0.2)

        # 🔥 Strength (scaled)
        strength = min(1.0, abs(avg_slope) * 12)

        # -----------------------------------------
        # 🔥 Consistency (Noise filter)
        # -----------------------------------------
        diffs = np.diff(closes[-10:])
        if len(diffs) == 0:
            return "range", float(strength)

        if avg_slope > 0:
            consistency = np.sum(diffs > 0) / len(diffs)
        else:
            consistency = np.sum(diffs < 0) / len(diffs)

        # -----------------------------------------
        # 🔥 Decision Logic (محسّن)
        # -----------------------------------------
        if avg_slope > 0.0008 and consistency > 0.55:
            return "up", float(strength)

        elif avg_slope < -0.0008 and consistency > 0.55:
            return "down", float(strength)

        else:
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

        trends = [trend_1m, trend_5m, trend_15m]
        strengths = [str_1m, str_5m, str_15m]

        # -----------------------------------------
        # 🔥 CRO Alignment Logic (أذكى من قبل)
        # -----------------------------------------

        # تجاهل unknown
        valid_trends = [t for t in trends if t != "unknown"]

        # إذا الكل unknown → ضعيف
        if len(valid_trends) == 0:
            alignment = "weak"
        else:
            # الأغلبية
            dominant = max(set(valid_trends), key=valid_trends.count)

            aligned_count = sum(1 for t in valid_trends if t == dominant)

            # 🔥 Weighted strength (15m أهم)
            weighted_strength = (
                str_1m * 0.2 +
                str_5m * 0.3 +
                str_15m * 0.5
            )

            if aligned_count == 3 and weighted_strength > 0.6:
                alignment = "strong"

            elif aligned_count >= 2 and weighted_strength > 0.4:
                alignment = "medium"

            else:
                alignment = "weak"

        avg_strength = sum(strengths) / 3

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

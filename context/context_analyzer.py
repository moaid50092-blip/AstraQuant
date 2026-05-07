import numpy as np


class ContextAnalyzer:

    def __init__(self, lookback=30):
        self.lookback = lookback

    # -------------------------------------------------
    def analyze(self, df, momentum=None, strength=0.0):

        if df is None or len(df) < 10:
            return self._empty()

        closes = df["close"].values
        highs = df["high"].values
        lows = df["low"].values

        current_price = closes[-1]

        # =========================================
        # 🔥 TREND ENGINE (Production Grade)
        # =========================================

        def slope(arr):

            if arr[0] == 0:
                return 0

            return (arr[-1] - arr[0]) / arr[0]

        short = closes[-5:]
        mid = closes[-10:]
        long = closes[-20:] if len(closes) >= 20 else closes

        s = slope(short)
        m = slope(mid)
        l = slope(long)

        # weighted directional pressure
        avg_slope = (
            s * 0.5 +
            m * 0.3 +
            l * 0.2
        )

        # -----------------------------------------
        # 🔥 consistency
        # -----------------------------------------

        diffs = np.diff(closes[-10:])

        if len(diffs) == 0:
            return self._empty()

        up_ratio = np.sum(diffs > 0) / len(diffs)
        down_ratio = np.sum(diffs < 0) / len(diffs)

        directional_bias = max(up_ratio, down_ratio)

        # -----------------------------------------
        # 🔥 dynamic thresholds
        # -----------------------------------------

        slope_strength = abs(avg_slope)

        # السوق الهادئ
        if slope_strength < 0.0008:
            threshold = 0.65

        # سوق طبيعي
        elif slope_strength < 0.002:
            threshold = 0.58

        # سوق واضح
        else:
            threshold = 0.54

        # -----------------------------------------
        # 🔥 final trend decision
        # -----------------------------------------

        if avg_slope > 0 and up_ratio >= threshold:
            trend = "up"

        elif avg_slope < 0 and down_ratio >= threshold:
            trend = "down"

        else:
            trend = "range"

        # =========================================
        # 🔥 ZONE ENGINE
        # =========================================

        lookback = min(self.lookback, len(df))

        recent_high = np.max(highs[-lookback:])
        recent_low = np.min(lows[-lookback:])

        range_size = recent_high - recent_low

        if range_size == 0:
            range_size = 1

        position = (
            (current_price - recent_low)
            / range_size
        )

        if position <= 0.25:
            zone = "low"

        elif position >= 0.75:
            zone = "high"

        else:
            zone = "middle"

        # =========================================
        # 🔥 BREAKOUT ENGINE (Improved)
        # =========================================

        prev_high = np.max(highs[-lookback:-1])
        prev_low = np.min(lows[-lookback:-1])

        breakout_buffer = range_size * 0.01

        breakout_up = (
            current_price >
            (prev_high + breakout_buffer)
        )

        breakout_down = (
            current_price <
            (prev_low - breakout_buffer)
        )

        breakout_strength = abs(
            closes[-1] - closes[-2]
        ) / closes[-2]

        breakout = False

        if breakout_up and breakout_strength > 0.0015:
            breakout = True

        elif breakout_down and breakout_strength > 0.0015:
            breakout = True

        # =========================================
        # 🔥 SETUP ENGINE (Context-aware)
        # =========================================

        setup = "unknown"

        if momentum:

            # BUY
            if momentum == "up":

                if (
                    breakout_up
                    and strength >= 0.55
                    and trend != "down"
                ):
                    setup = "real"

                elif (
                    strength >= 0.45
                    and trend != "down"
                ):
                    setup = "weak"

                else:
                    setup = "fake"

            # SELL
            elif momentum == "down":

                if (
                    breakout_down
                    and strength >= 0.55
                    and trend != "up"
                ):
                    setup = "real"

                elif (
                    strength >= 0.45
                    and trend != "up"
                ):
                    setup = "weak"

                else:
                    setup = "fake"

        # =========================================

        return {
            "trend": trend,
            "zone": zone,
            "breakout": breakout,
            "setup": setup
        }

    # -------------------------------------------------
    def _empty(self):

        return {
            "trend": "unknown",
            "zone": "unknown",
            "breakout": False,
            "setup": "unknown"
        }

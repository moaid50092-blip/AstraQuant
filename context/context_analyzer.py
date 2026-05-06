import numpy as np


class ContextAnalyzer:

    def __init__(self, lookback=30):
        self.lookback = lookback

    def analyze(self, df, momentum=None, strength=0.0):

        if df is None or len(df) < 10:
            return self._empty()

        closes = df["close"].values
        highs = df["high"].values
        lows = df["low"].values

        current_price = closes[-1]

        # =========================================
        # 🔥 TREND (Dominance Logic)
        # =========================================

        def slope(arr):
            return (arr[-1] - arr[0]) / arr[0] if arr[0] != 0 else 0

        short = closes[-5:]
        mid = closes[-10:]
        long = closes[-20:] if len(closes) >= 20 else closes

        s = slope(short)
        m = slope(mid)
        l = slope(long)

        avg_slope = (s * 0.5 + m * 0.3 + l * 0.2)

        diffs = np.diff(closes[-10:])
        up_ratio = np.sum(diffs > 0) / len(diffs)
        down_ratio = np.sum(diffs < 0) / len(diffs)

        if avg_slope > 0.001 and up_ratio > 0.6:
            trend = "up"
        elif avg_slope < -0.001 and down_ratio > 0.6:
            trend = "down"
        else:
            trend = "range"

        # =========================================
        # 🔥 ZONE (ديناميكي)
        # =========================================

        lookback = min(self.lookback, len(df))
        recent_high = np.max(highs[-lookback:])
        recent_low = np.min(lows[-lookback:])

        range_size = recent_high - recent_low if recent_high != recent_low else 1
        position = (current_price - recent_low) / range_size

        if position <= 0.25:
            zone = "low"
        elif position >= 0.75:
            zone = "high"
        else:
            zone = "middle"

        # =========================================
        # 🔥 BREAKOUT (حقيقي)
        # =========================================

        prev_high = np.max(highs[-lookback:-1])
        prev_low = np.min(lows[-lookback:-1])

        breakout_up = current_price > prev_high
        breakout_down = current_price < prev_low

        breakout_strength = abs(closes[-1] - closes[-2]) / closes[-2] if len(closes) > 1 else 0

        breakout = False
        if breakout_up and breakout_strength > 0.002:
            breakout = True
        elif breakout_down and breakout_strength > 0.002:
            breakout = True

        # =========================================
        # 🔥 SETUP (ذكي + مرن)
        # =========================================

        setup = "unknown"

        if momentum:

            # BUY
            if momentum == "up":
                if breakout_up and strength >= 0.55:
                    setup = "real"
                elif strength >= 0.45:
                    setup = "weak"
                else:
                    setup = "fake"

            # SELL
            elif momentum == "down":
                if breakout_down and strength >= 0.55:
                    setup = "real"
                elif strength >= 0.45:
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

    def _empty(self):
        return {
            "trend": "unknown",
            "zone": "unknown",
            "breakout": False,
            "setup": "unknown"
        }

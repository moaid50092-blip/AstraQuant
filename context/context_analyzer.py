# context/context_analyzer.py

import numpy as np


class ContextAnalyzer:

    def __init__(self, lookback=20):
        self.lookback = lookback

    def analyze(self, df):

        if df is None or len(df) < self.lookback:
            return {
                "trend": "unknown",
                "zone": "unknown",
                "breakout": False
            }

        highs = df["high"].values[-self.lookback:]
        lows = df["low"].values[-self.lookback:]
        closes = df["close"].values

        current_price = closes[-1]

        # -----------------------------
        # 1) Trend
        # -----------------------------
        recent_closes = closes[-5:]

        if all(x < y for x, y in zip(recent_closes, recent_closes[1:])):
            trend = "up"
        elif all(x > y for x, y in zip(recent_closes, recent_closes[1:])):
            trend = "down"
        else:
            trend = "range"

        # -----------------------------
        # 2) Zones
        # -----------------------------
        highest = np.max(highs)
        lowest = np.min(lows)

        range_size = highest - lowest if highest != lowest else 1

        # نسبة موقع السعر داخل الرينج
        position = (current_price - lowest) / range_size

        if position <= 0.3:
            zone = "support"
        elif position >= 0.7:
            zone = "resistance"
        else:
            zone = "middle"

        # -----------------------------
        # 3) Breakout
        # -----------------------------
        prev_high = np.max(highs[:-1])
        prev_low = np.min(lows[:-1])

        breakout = False

        if current_price > prev_high:
            breakout = True
        elif current_price < prev_low:
            breakout = True

        return {
            "trend": trend,
            "zone": zone,
            "breakout": breakout
        }

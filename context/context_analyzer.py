# context/context_analyzer.py

import numpy as np


class ContextAnalyzer:

    def __init__(self, lookback=20):
        self.lookback = lookback

    def analyze(self, df, momentum=None, strength=0.0):

        if df is None or len(df) < self.lookback:
            return self._empty()

        highs = df["high"].values[-self.lookback:]
        lows = df["low"].values[-self.lookback:]
        closes = df["close"].values

        current_price = closes[-1]

        # -----------------------------
        # 1) Trend (محسن)
        # -----------------------------
        recent_closes = closes[-5:]

        if all(x < y for x, y in zip(recent_closes, recent_closes[1:])):
            trend = "up"
        elif all(x > y for x, y in zip(recent_closes, recent_closes[1:])):
            trend = "down"
        else:
            trend = "range"

        # -----------------------------
        # 2) Zone
        # -----------------------------
        highest = np.max(highs)
        lowest = np.min(lows)

        range_size = highest - lowest if highest != lowest else 1
        position = (current_price - lowest) / range_size

        if position <= 0.3:
            zone = "low"
        elif position >= 0.7:
            zone = "high"
        else:
            zone = "middle"

        # -----------------------------
        # 3) Breakout (محسن)
        # -----------------------------
        prev_high = np.max(highs[:-1])
        prev_low = np.min(lows[:-1])

        breakout_up = current_price > prev_high
        breakout_down = current_price < prev_low

        breakout = breakout_up or breakout_down

        # -----------------------------
        # 4) Setup Classification 🔥
        # -----------------------------
        setup = "unknown"

        if momentum is None:
            setup = "unknown"

        else:
            if momentum == "up":
                if strength >= 0.6 and breakout_up:
                    setup = "real"
                elif strength >= 0.4:
                    setup = "weak"
                else:
                    setup = "fake"

            elif momentum == "down":
                if strength >= 0.6 and breakout_down:
                    setup = "real"
                elif strength >= 0.4:
                    setup = "weak"
                else:
                    setup = "fake"

            else:
                setup = "fake"

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

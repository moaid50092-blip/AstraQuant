import numpy as np


class RangeEngineV2:

    def __init__(self, window=50, tolerance=0.15, min_range_ratio=0.002):
        self.window = window
        self.tolerance = tolerance
        self.min_range_ratio = min_range_ratio

    # -----------------------------------------
    def detect_range(self, df):

        if len(df) < self.window:
            return None

        recent = df.iloc[-self.window:]

        high = recent["high"].max()
        low = recent["low"].min()

        range_size = high - low
        avg_price = recent["close"].mean()

        if avg_price == 0:
            return None

        range_ratio = range_size / avg_price

        if range_ratio < self.min_range_ratio:
            return None

        return {
            "high": high,
            "low": low,
            "size": range_size,
            "ratio": range_ratio  # 🔥 NEW
        }

    # -----------------------------------------
    def detect_location(self, price, range_data):

        high = range_data["high"]
        low = range_data["low"]
        size = range_data["size"]

        if price >= high - size * self.tolerance:
            return "top"

        if price <= low + size * self.tolerance:
            return "bottom"

        return "middle"

    # -----------------------------------------
    def detect_rejection(self, df):

        if len(df) < 2:
            return None

        last = df.iloc[-1]

        open_ = last["open"]
        close = last["close"]
        high = last["high"]
        low = last["low"]

        body = abs(close - open_)

        upper_wick = high - max(open_, close)
        lower_wick = min(open_, close) - low

        if upper_wick > body * 1.5:
            return "bearish"

        if lower_wick > body * 1.5:
            return "bullish"

        return None

    # -----------------------------------------
    def detect_fake_breakout(self, df, range_data):

        if len(df) < 2:
            return None

        last = df.iloc[-1]

        if last["high"] > range_data["high"] and last["close"] < range_data["high"]:
            return "fake_up"

        if last["low"] < range_data["low"] and last["close"] > range_data["low"]:
            return "fake_down"

        return None

    # -----------------------------------------
    def analyze(self, df, momentum_dir=None):

        result = {
            "range_active": False,
            "signal": None,
            "confidence": 0,
            "location": None,
            "rejection": None,
            "fake_breakout": None,
            "range_high": None,
            "range_low": None,

            # 🔥 NEW
            "range_strength": 0,
            "range_score": 0,
            "range_bias": "neutral",
            "tradable": False
        }

        range_data = self.detect_range(df)

        if range_data is None:
            return result

        result["range_active"] = True

        price = df["close"].iloc[-1]

        location = self.detect_location(price, range_data)
        rejection = self.detect_rejection(df)
        fake_break = self.detect_fake_breakout(df, range_data)

        result["location"] = location
        result["rejection"] = rejection
        result["fake_breakout"] = fake_break
        result["range_high"] = range_data["high"]
        result["range_low"] = range_data["low"]

        signal = None
        confidence = 0

        # -----------------------------------------
        # Entry Logic
        # -----------------------------------------

        if location == "bottom" and (rejection == "bullish" or fake_break == "fake_down"):
            signal = "BUY"
            confidence += 1

        elif location == "top" and (rejection == "bearish" or fake_break == "fake_up"):
            signal = "SELL"
            confidence += 1

        # -----------------------------------------
        # Momentum Confluence
        # -----------------------------------------
        if momentum_dir:
            if (signal == "BUY" and momentum_dir == "up") or \
               (signal == "SELL" and momentum_dir == "down"):
                confidence += 0.5

        # -----------------------------------------
        # 🔥 Range Strength
        # -----------------------------------------
        strength = min(range_data["ratio"] * 100, 1.0)

        # -----------------------------------------
        # 🔥 Range Score
        # -----------------------------------------
        range_score = confidence * 0.7 + strength * 0.3

        # -----------------------------------------
        # 🔥 Bias
        # -----------------------------------------
        if signal == "BUY":
            bias = "up"
        elif signal == "SELL":
            bias = "down"
        else:
            bias = "neutral"

        # -----------------------------------------
        # 🔥 Tradability
        # -----------------------------------------
        tradable = True if range_score >= 0.8 else False

        # -----------------------------------------
        # Save
        # -----------------------------------------
        result["signal"] = signal
        result["confidence"] = round(confidence, 2)

        result["range_strength"] = round(strength, 2)
        result["range_score"] = round(range_score, 2)
        result["range_bias"] = bias
        result["tradable"] = tradable

        return result

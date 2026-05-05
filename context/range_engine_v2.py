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

        # 🔥 قوة الرينج (كل ما كان أوضح = أفضل)
        compression = (recent["high"] - recent["low"]).std()
        strength = min(1.0, (range_ratio / self.min_range_ratio) * 0.5)

        return {
            "high": high,
            "low": low,
            "size": range_size,
            "strength": strength
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
            return None, 0

        last = df.iloc[-1]

        open_ = last["open"]
        close = last["close"]
        high = last["high"]
        low = last["low"]

        body = abs(close - open_)

        upper_wick = high - max(open_, close)
        lower_wick = min(open_, close) - low

        # 🔥 قوة الرفض
        if upper_wick > body * 1.5:
            strength = min(1.0, upper_wick / (body + 1e-6))
            return "bearish", strength

        if lower_wick > body * 1.5:
            strength = min(1.0, lower_wick / (body + 1e-6))
            return "bullish", strength

        return None, 0

    # -----------------------------------------
    def detect_fake_breakout(self, df, range_data):

        if len(df) < 2:
            return None, 0

        last = df.iloc[-1]

        high = range_data["high"]
        low = range_data["low"]

        # 🔥 fake breakout strength
        if last["high"] > high and last["close"] < high:
            strength = (last["high"] - high) / high
            return "fake_up", min(1.0, strength * 10)

        if last["low"] < low and last["close"] > low:
            strength = (low - last["low"]) / low
            return "fake_down", min(1.0, strength * 10)

        return None, 0

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
            "range_low": None
        }

        range_data = self.detect_range(df)

        if range_data is None:
            return result

        result["range_active"] = True

        price = df["close"].iloc[-1]

        location = self.detect_location(price, range_data)
        rejection, rej_strength = self.detect_rejection(df)
        fake_break, fake_strength = self.detect_fake_breakout(df, range_data)

        result["location"] = location
        result["rejection"] = rejection
        result["fake_breakout"] = fake_break
        result["range_high"] = range_data["high"]
        result["range_low"] = range_data["low"]

        signal = None
        confidence = 0

        # -----------------------------------------
        # 🎯 Entry Logic (Weighted)
        # -----------------------------------------

        # BUY
        if location == "bottom":
            if rejection == "bullish":
                signal = "BUY"
                confidence += 0.8 + rej_strength

            if fake_break == "fake_down":
                signal = "BUY"
                confidence += 0.8 + fake_strength

        # SELL
        elif location == "top":
            if rejection == "bearish":
                signal = "SELL"
                confidence += 0.8 + rej_strength

            if fake_break == "fake_up":
                signal = "SELL"
                confidence += 0.8 + fake_strength

        # -----------------------------------------
        # 🔥 Momentum Confluence
        # -----------------------------------------
        if momentum_dir and signal:
            if (signal == "BUY" and momentum_dir == "up") or \
               (signal == "SELL" and momentum_dir == "down"):
                confidence += 0.5

        # -----------------------------------------
        # 🔥 Range Strength Boost
        # -----------------------------------------
        confidence *= range_data["strength"]

        # -----------------------------------------
        # 🔥 Normalize
        # -----------------------------------------
        confidence = min(2.5, confidence)
        confidence = round(confidence, 2)

        result["signal"] = signal
        result["confidence"] = confidence

        return result

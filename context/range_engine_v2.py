import numpy as np


class RangeEngineV2:

    def __init__(self, window=50, tolerance=0.15, min_range_ratio=0.002):
        self.window = window
        self.tolerance = tolerance
        self.min_range_ratio = min_range_ratio

    # -----------------------------------------
    # 1️⃣ Detect Range
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

        # 🔥 فلترة الرينج الضعيف
        if range_ratio < self.min_range_ratio:
            return None

        return {
            "high": high,
            "low": low,
            "size": range_size
        }

    # -----------------------------------------
    # 2️⃣ Location
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
    # 3️⃣ Rejection (Wick Logic)
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
    # 4️⃣ Fake Breakout
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
    # 5️⃣ Main Analyze (نسخة احترافية)
    # -----------------------------------------
    def analyze(self, df, momentum_dir=None):

        # -----------------------------------------
        # Default Output (مهم جدًا)
        # -----------------------------------------
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

        # -----------------------------------------
        # Detect Range
        # -----------------------------------------
        range_data = self.detect_range(df)

        if range_data is None:
            return result

        result["range_active"] = True

        price = df["close"].iloc[-1]

        # -----------------------------------------
        # Context
        # -----------------------------------------
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
        # 🎯 Entry Logic
        # -----------------------------------------

        # BUY
        if location == "bottom" and (rejection == "bullish" or fake_break == "fake_down"):
            signal = "BUY"
            confidence += 1

        # SELL
        elif location == "top" and (rejection == "bearish" or fake_break == "fake_up"):
            signal = "SELL"
            confidence += 1

        # -----------------------------------------
        # 🔥 Momentum Confluence
        # -----------------------------------------
        if momentum_dir:
            if (signal == "BUY" and momentum_dir == "up") or \
               (signal == "SELL" and momentum_dir == "down"):
                confidence += 0.5

        # -----------------------------------------
        # Save
        # -----------------------------------------
        result["signal"] = signal
        result["confidence"] = round(confidence, 2)

        return result

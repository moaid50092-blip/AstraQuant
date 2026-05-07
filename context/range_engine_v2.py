import numpy as np


class RangeEngineV2:

    def __init__(
        self,
        window=50,
        tolerance=0.12,
        min_range_ratio=0.003
    ):

        self.window = window
        self.tolerance = tolerance

        # 🔥 رفع الحد الأدنى
        # لمنع micro-ranges الوهمية
        self.min_range_ratio = min_range_ratio

    # -------------------------------------------------
    # 🔥 RANGE DETECTION
    # -------------------------------------------------
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

        # =========================================
        # 🔥 FILTER 1:
        # منع الرينجات الصغيرة جدًا
        # =========================================

        if range_ratio < self.min_range_ratio:
            return None

        # =========================================
        # 🔥 FILTER 2:
        # range cleanliness
        # =========================================

        candle_ranges = recent["high"] - recent["low"]

        avg_candle = candle_ranges.mean()

        if avg_candle == 0:
            return None

        # إذا الرينج كله عبارة عن شموع فوضوية
        noisiness = candle_ranges.std() / avg_candle

        if noisiness > 1.2:
            return None

        # =========================================
        # 🔥 RANGE STRENGTH
        # =========================================

        compression = candle_ranges.std()

        compression_factor = 1 / (1 + compression)

        strength = (
            min(1.0, range_ratio / (self.min_range_ratio * 2))
            * compression_factor
        )

        strength = max(0.2, min(1.0, strength))

        return {
            "high": high,
            "low": low,
            "size": range_size,
            "strength": round(float(strength), 3)
        }

    # -------------------------------------------------
    # 🔥 LOCATION
    # -------------------------------------------------
    def detect_location(self, price, range_data):

        high = range_data["high"]
        low = range_data["low"]
        size = range_data["size"]

        if size <= 0:
            return "middle"

        position = (price - low) / size

        # 🔥 أكثر دقة
        if position >= (1 - self.tolerance):
            return "top"

        if position <= self.tolerance:
            return "bottom"

        return "middle"

    # -------------------------------------------------
    # 🔥 REJECTION DETECTION
    # -------------------------------------------------
    def detect_rejection(self, df):

        if len(df) < 2:
            return None, 0

        last = df.iloc[-1]

        open_ = last["open"]
        close = last["close"]
        high = last["high"]
        low = last["low"]

        body = abs(close - open_)

        # 🔥 حماية
        if body == 0:
            body = 1e-6

        upper_wick = high - max(open_, close)
        lower_wick = min(open_, close) - low

        candle_size = high - low

        if candle_size <= 0:
            return None, 0

        # =========================================
        # 🔥 BEARISH REJECTION
        # =========================================

        if (
            upper_wick > body * 1.8
            and upper_wick > candle_size * 0.35
        ):

            strength = upper_wick / candle_size

            return "bearish", round(min(1.0, strength), 3)

        # =========================================
        # 🔥 BULLISH REJECTION
        # =========================================

        if (
            lower_wick > body * 1.8
            and lower_wick > candle_size * 0.35
        ):

            strength = lower_wick / candle_size

            return "bullish", round(min(1.0, strength), 3)

        return None, 0

    # -------------------------------------------------
    # 🔥 FAKE BREAKOUT
    # -------------------------------------------------
    def detect_fake_breakout(self, df, range_data):

        if len(df) < 2:
            return None, 0

        last = df.iloc[-1]

        high = range_data["high"]
        low = range_data["low"]

        candle_size = last["high"] - last["low"]

        if candle_size <= 0:
            return None, 0

        # =========================================
        # 🔥 FAKE UP BREAKOUT
        # =========================================

        if (
            last["high"] > high
            and last["close"] < high
        ):

            penetration = last["high"] - high

            # 🔥 penetration حقيقي
            if penetration > candle_size * 0.15:

                strength = penetration / candle_size

                return "fake_up", round(min(1.0, strength), 3)

        # =========================================
        # 🔥 FAKE DOWN BREAKOUT
        # =========================================

        if (
            last["low"] < low
            and last["close"] > low
        ):

            penetration = low - last["low"]

            if penetration > candle_size * 0.15:

                strength = penetration / candle_size

                return "fake_down", round(min(1.0, strength), 3)

        return None, 0

    # -------------------------------------------------
    # 🔥 MAIN ANALYZE
    # -------------------------------------------------
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

        # =========================================
        # 🔥 RANGE
        # =========================================

        range_data = self.detect_range(df)

        if range_data is None:
            return result

        result["range_active"] = True

        price = df["close"].iloc[-1]

        location = self.detect_location(price, range_data)

        rejection, rej_strength = self.detect_rejection(df)

        fake_break, fake_strength = self.detect_fake_breakout(
            df,
            range_data
        )

        result["location"] = location
        result["rejection"] = rejection
        result["fake_breakout"] = fake_break

        result["range_high"] = range_data["high"]
        result["range_low"] = range_data["low"]

        signal = None
        confidence = 0.0

        # =========================================
        # 🔥 BUY LOGIC
        # =========================================

        if location == "bottom":

            if rejection == "bullish":

                signal = "BUY"

                confidence += 0.55 + (rej_strength * 0.4)

            if fake_break == "fake_down":

                signal = "BUY"

                confidence += 0.6 + (fake_strength * 0.5)

        # =========================================
        # 🔥 SELL LOGIC
        # =========================================

        elif location == "top":

            if rejection == "bearish":

                signal = "SELL"

                confidence += 0.55 + (rej_strength * 0.4)

            if fake_break == "fake_up":

                signal = "SELL"

                confidence += 0.6 + (fake_strength * 0.5)

        # =========================================
        # 🔥 MOMENTUM CONFLUENCE
        # =========================================

        if signal and momentum_dir:

            aligned = (
                (signal == "BUY" and momentum_dir == "up")
                or
                (signal == "SELL" and momentum_dir == "down")
            )

            opposite = (
                (signal == "BUY" and momentum_dir == "down")
                or
                (signal == "SELL" and momentum_dir == "up")
            )

            if aligned:
                confidence += 0.18

            elif opposite:
                confidence -= 0.15

        # =========================================
        # 🔥 RANGE STRENGTH
        # =========================================

        confidence *= range_data["strength"]

        # =========================================
        # 🔥 CLEAN FILTER
        # =========================================

        # إذا ما في rejection أو fake breakout حقيقي
        if (
            rejection is None
            and fake_break is None
        ):

            confidence *= 0.5

        # =========================================
        # 🔥 NORMALIZE
        # =========================================

        confidence = max(0.0, min(2.0, confidence))

        confidence = round(float(confidence), 2)

        # =========================================
        # 🔥 FINAL STORE
        # =========================================

        result["signal"] = signal
        result["confidence"] = confidence

        return result

from intelligence.historical_context_engine import HistoricalContextEngine
from intelligence.volatility_context_engine import VolatilityContextEngine


class StrategyEngine:

    def __init__(self):
        self.historical_engine = HistoricalContextEngine()
        self.volatility_engine = VolatilityContextEngine()

    # -------------------------------------------------
    def detect(self, symbol, df):

        if df is None or len(df) < 15:
            return None

        trend_strength = self._compute_trend_strength(df)
        volatility = self._compute_volatility(df)
        momentum = self._compute_momentum(df)

        # 🔥 EARLY
        early, compression, acceleration = self._detect_early_expansion(df, momentum)

        # -------------------------------------------------
        # 🔥 STRUCTURE (تحويل من float → logic)
        # -------------------------------------------------
        if trend_strength > 0.6:
            structure_score = 0.7
        elif trend_strength < 0.4:
            structure_score = 0.3
        else:
            structure_score = 0.5

        # -------------------------------------------------
        # 🔥 LIQUIDITY (مرتبط بالضغط)
        # -------------------------------------------------
        if compression:
            liquidity_score = 0.65
        else:
            liquidity_score = 0.45

        # -------------------------------------------------
        # 🔥 SESSION (مؤقت حيادي)
        # -------------------------------------------------
        session_score = 0.5

        # -------------------------------------------------
        # 🔥 CONTEXT (يعكس structure)
        # -------------------------------------------------
        context_score = structure_score

        # -------------------------------------------------
        # 🔥 FACTOR (مرتبط بالمومنتوم)
        # -------------------------------------------------
        if momentum > 0.55:
            factor_score = 0.65
        elif momentum < 0.45:
            factor_score = 0.35
        else:
            factor_score = 0.5

        base_score = momentum

        # -------------------------------------------------
        # 🔥 Pattern Boost
        # -------------------------------------------------
        pattern_boost = self._detect_liquidity_compression_breakout(df)
        base_score = min(1.0, base_score + pattern_boost)

        # -------------------------------------------------
        # 🔥 Consistency Adjustment
        # -------------------------------------------------
        scores = [structure_score, liquidity_score, factor_score]

        mean_score = sum(scores) / len(scores)
        variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)
        std = variance ** 0.5

        consistency = max(0.0, min(1.0, 1 - std))
        adjustment = (consistency - 0.5) * 0.1

        base_score = base_score * (1 + adjustment)
        base_score = max(0.0, min(1.0, base_score))

        # -------------------------------------------------
        # 🔥 VOLATILITY (تحويل لطبقات)
        # -------------------------------------------------
        raw_vol_score = self.volatility_engine.evaluate(df)

        if raw_vol_score > 0.6:
            volatility_score = 0.7
        elif raw_vol_score < 0.3:
            volatility_score = 0.3
        else:
            volatility_score = 0.5

        # -------------------------------------------------
        # 🔥 HISTORICAL
        # -------------------------------------------------
        market_features = {
            "trend_strength": trend_strength,
            "volatility": volatility,
            "momentum": momentum,
            "liquidity_state": liquidity_score,
            "session_context": session_score
        }

        historical_score = self.historical_engine.evaluate(market_features)

        # -------------------------------------------------
        # 🔥 DIRECTION
        # -------------------------------------------------
        if momentum > 0.52:
            direction = "up"
        elif momentum < 0.48:
            direction = "down"
        else:
            direction = "neutral"

        # -------------------------------------------------
        # 🔥 FINAL SIGNAL
        # -------------------------------------------------
        signal = {
            "symbol": symbol,
            "base_score": base_score,

            "momentum": direction,
            "strength": abs(momentum - 0.5) * 2,

            # EARLY
            "early_entry": early,
            "compression": compression,
            "acceleration": acceleration,

            # SCORES
            "structure_score": structure_score,
            "liquidity_score": liquidity_score,
            "session_score": session_score,
            "context_score": context_score,
            "mtf_score": 0.5,  # نفعله لاحقًا
            "factor_score": factor_score,
            "historical_score": historical_score,
            "volatility_score": volatility_score
        }

        return signal

    # -------------------------------------------------
    # 🔥 EARLY ENGINE
    # -------------------------------------------------
    def _detect_early_expansion(self, df, momentum):

        if len(df) < 20:
            return False, False, False

        highs = df["high"]
        lows = df["low"]
        closes = df["close"]

        recent_range = highs.iloc[-10:].max() - lows.iloc[-10:].min()
        prev_range = highs.iloc[-20:-10].max() - lows.iloc[-20:-10].min()

        compression = prev_range > 0 and (recent_range / prev_range) < 0.85

        breakout_up = closes.iloc[-1] > highs.iloc[-5:-1].max()
        breakout_down = closes.iloc[-1] < lows.iloc[-5:-1].min()

        breakout = breakout_up or breakout_down

        prev_momentum = (closes.iloc[-2] - closes.iloc[-11]) / closes.iloc[-11]
        prev_momentum = max(0.0, min(1.0, 0.5 + prev_momentum))

        acceleration = momentum > prev_momentum

        momentum_strength = abs(momentum - 0.5)

        early = (
            (compression and breakout) or
            (breakout and acceleration)
        ) and momentum_strength > 0.06

        return early, compression, acceleration

    # -------------------------------------------------
    def _detect_liquidity_compression_breakout(self, df):

        highs = df["high"]
        lows = df["low"]
        closes = df["close"]

        if len(df) < 20:
            return 0.0

        prev_high = highs.iloc[-10:-5].max()
        prev_low = lows.iloc[-10:-5].min()

        last_high = highs.iloc[-6]
        last_low = lows.iloc[-6]

        sweep_up = last_high > prev_high
        sweep_down = last_low < prev_low

        if not (sweep_up or sweep_down):
            return 0.0

        compression_range = highs.iloc[-5:].max() - lows.iloc[-5:].min()
        prior_range = highs.iloc[-15:-5].max() - lows.iloc[-15:-5].min()

        if prior_range == 0:
            return 0.0

        compression_ratio = compression_range / prior_range

        if compression_ratio > 0.5:
            return 0.0

        breakout_up = closes.iloc[-1] > highs.iloc[-5:-1].max()
        breakout_down = closes.iloc[-1] < lows.iloc[-5:-1].min()

        if breakout_up or breakout_down:
            return 0.15

        return 0.0

    # -------------------------------------------------
    def _compute_trend_strength(self, df):

        closes = df["close"]

        if len(closes) < 20:
            return 0.5

        trend = (closes.iloc[-1] - closes.iloc[-20]) / closes.iloc[-20]

        return max(0.0, min(1.0, 0.5 + trend))

    # -------------------------------------------------
    def _compute_volatility(self, df):

        returns = df["close"].pct_change().dropna()

        if len(returns) < 20:
            return 0.5

        vol = returns[-20:].std()

        return max(0.0, min(1.0, vol * 10))

    # -------------------------------------------------
    def _compute_momentum(self, df):

        closes = df["close"]

        if len(closes) < 10:
            return 0.5

        momentum = (closes.iloc[-1] - closes.iloc[-10]) / closes.iloc[-10]

        return max(0.0, min(1.0, 0.5 + momentum))

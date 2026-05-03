# strategy/strategy_engine.py

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
        # 🔥 STRUCTURE (مفعل)
        # -------------------------------------------------
        if trend_strength > 0.6:
            structure_score = 0.7
        elif trend_strength < 0.4:
            structure_score = 0.3
        else:
            structure_score = 0.5

        # -------------------------------------------------
        # 🔥 LIQUIDITY (ذكي بسيط)
        # -------------------------------------------------
        if compression:
            liquidity_score = 0.65
        else:
            liquidity_score = 0.45

        # -------------------------------------------------
        # 🔥 SESSION (مبدئي)
        # -------------------------------------------------
        session_score = 0.5  # نتركه حيادي حالياً

        # -------------------------------------------------
        # 🔥 CONTEXT (مرتبط بالترند)
        # -------------------------------------------------
        context_score = structure_score

        # -------------------------------------------------
        # 🔥 FACTOR (مرتبط بالـ momentum)
        # -------------------------------------------------
        if momentum > 0.55:
            factor_score = 0.65
        elif momentum < 0.45:
            factor_score = 0.35
        else:
            factor_score = 0.5

        base_score = momentum

        # -------------------------------------------------
        pattern_boost = self._detect_liquidity_compression_breakout(df)
        base_score = min(1.0, base_score + pattern_boost)

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
        # 🔥 VOLATILITY (مفعل)
        # -------------------------------------------------
        raw_vol_score = self.volatility_engine.evaluate(df)

        if raw_vol_score > 0.6:
            volatility_score = 0.7
        elif raw_vol_score < 0.3:
            volatility_score = 0.3
        else:
            volatility_score = 0.5

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
        if momentum > 0.52:
            direction = "up"
        elif momentum < 0.48:
            direction = "down"
        else:
            direction = "neutral"

        # -------------------------------------------------
        signal = {
            "symbol": symbol,
            "base_score": base_score,

            "momentum": direction,
            "strength": abs(momentum - 0.5) * 2,

            # 🔥 EARLY
            "early_entry": early,
            "compression": compression,
            "acceleration": acceleration,

            # 🔥 SCORES
            "structure_score": structure_score,
            "liquidity_score": liquidity_score,
            "session_score": session_score,
            "context_score": context_score,
            "mtf_score": 0.5,  # نفعله لاحقاً
            "factor_score": factor_score,
            "historical_score": historical_score,
            "volatility_score": volatility_score
        }

        return signal

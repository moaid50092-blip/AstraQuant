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

        # 🔥 EARLY (محسن CRO)
        early, compression, acceleration = self._detect_early_expansion(df, momentum)

        # baseline
        structure_score = trend_strength
        liquidity_score = 0.5
        session_score = 0.5
        context_score = 0.5
        mtf_score = 0.5
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
        volatility_score = self.volatility_engine.evaluate(df)

        market_features = {
            "trend_strength": trend_strength,
            "volatility": volatility,
            "momentum": momentum,
            "liquidity_state": liquidity_score,
            "session_context": session_score
        }

        historical_score = self.historical_engine.evaluate(market_features)

        # -------------------------------------------------
        # Direction (ثابت - لا نلمسه هون)
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

            # 🔥 CRO Layer
            "early_entry": early,
            "compression": compression,
            "acceleration": acceleration,

            "structure_score": structure_score,
            "liquidity_score": liquidity_score,
            "session_score": session_score,
            "context_score": context_score,
            "mtf_score": mtf_score,
            "factor_score": factor_score,
            "historical_score": historical_score,
            "volatility_score": volatility_score
        }

        return signal

    # -------------------------------------------------
    # 🔥 EARLY ENGINE (نسخة CRO محسنة)
    # -------------------------------------------------
    def _detect_early_expansion(self, df, momentum):

        if len(df) < 20:
            return False, False, False

        highs = df["high"]
        lows = df["low"]
        closes = df["close"]

        # -------------------------
        # Compression (خففنا الشرط)
        # -------------------------
        recent_range = highs.iloc[-10:].max() - lows.iloc[-10:].min()
        prev_range = highs.iloc[-20:-10].max() - lows.iloc[-20:-10].min()

        compression = prev_range > 0 and (recent_range / prev_range) < 0.85

        # -------------------------
        # Breakout
        # -------------------------
        breakout_up = closes.iloc[-1] > highs.iloc[-5:-1].max()
        breakout_down = closes.iloc[-1] < lows.iloc[-5:-1].min()

        breakout = breakout_up or breakout_down

        # -------------------------
        # Acceleration
        # -------------------------
        prev_momentum = (closes.iloc[-2] - closes.iloc[-11]) / closes.iloc[-11]
        prev_momentum = max(0.0, min(1.0, 0.5 + prev_momentum))

        acceleration = momentum > prev_momentum

        # -------------------------
        # Strength
        # -------------------------
        momentum_strength = abs(momentum - 0.5)

        # 🔥 CRO LOGIC (ذكي وموزون)
        early = (
            (compression and breakout) or
            (breakout and acceleration)
        ) and momentum_strength > 0.06

        return early, compression, acceleration

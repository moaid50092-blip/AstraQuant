# strategy/strategy_engine.py

from intelligence.historical_context_engine import HistoricalContextEngine
from intelligence.volatility_context_engine import VolatilityContextEngine


class StrategyEngine:

    def __init__(self):

        self.historical_engine = HistoricalContextEngine()
        self.volatility_engine = VolatilityContextEngine()

    # -------------------------------------------------
    # 🧠 Main Signal Detection
    # -------------------------------------------------
    def detect(self, symbol, df):

        if df is None or len(df) < 15:
            return None

        # -----------------------------------------
        # Core Features
        # -----------------------------------------
        trend_strength = self._compute_trend_strength(df)
        volatility = self._compute_volatility(df)
        momentum = self._compute_momentum(df)

        # -----------------------------------------
        # Base Layers
        # -----------------------------------------
        structure_score = trend_strength
        liquidity_score = 0.5
        session_score = 0.5
        context_score = 0.5
        mtf_score = 0.5
        factor_score = 0.5

        # -----------------------------------------
        # 🔥 Probability Layer
        # -----------------------------------------
        base_score = momentum

        # -----------------------------------------
        # 🔥 Strength Layer (منفصل بالكامل)
        # -----------------------------------------
        raw_strength = abs(momentum - 0.5) * 2

        # -----------------------------------------
        # 🔥 Pattern Boost (Breakout Intelligence)
        # -----------------------------------------
        pattern_boost = self._detect_liquidity_compression_breakout(df)
        base_score = min(1.0, base_score + pattern_boost)

        # -----------------------------------------
        # 🔥 Consistency Adjustment
        # -----------------------------------------
        scores = [structure_score, liquidity_score, factor_score]

        mean_score = sum(scores) / len(scores)
        variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)
        std = variance ** 0.5

        consistency = max(0.0, min(1.0, 1 - std))
        adjustment = (consistency - 0.5) * 0.1

        base_score = base_score * (1 + adjustment)
        base_score = max(0.0, min(1.0, base_score))

        # -----------------------------------------
        # 🔥 Context Engines
        # -----------------------------------------
        volatility_score = self.volatility_engine.evaluate(df)

        market_features = {
            "trend_strength": trend_strength,
            "volatility": volatility,
            "momentum": momentum,
            "liquidity_state": liquidity_score,
            "session_context": session_score
        }

        historical_score = self.historical_engine.evaluate(market_features)

        # -----------------------------------------
        # 🔥 Direction (محسن + Transition-ready)
        # -----------------------------------------
        if momentum > 0.53:
            direction = "up"
        elif momentum < 0.47:
            direction = "down"
        else:
            direction = "neutral"  # 🔥 مهم للـ Transition

        # -----------------------------------------
        # 🔥 Build Signal
        # -----------------------------------------
        signal = {
            "symbol": symbol,

            # 🧠 Probability
            "base_score": base_score,

            # 🎯 Direction
            "momentum": direction,

            # 💪 Strength
            "strength": raw_strength,

            # 🔍 Raw (للتحليل لاحقًا)
            "raw_momentum": momentum,

            # 🔧 Scores (مفيدة للتطوير لاحقًا)
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
    # 🔥 Liquidity Compression Breakout
    # -------------------------------------------------
    def _detect_liquidity_compression_breakout(self, df):

        if len(df) < 20:
            return 0.0

        highs = df["high"]
        lows = df["low"]
        closes = df["close"]

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
    # 📊 Trend Strength
    # -------------------------------------------------
    def _compute_trend_strength(self, df):

        closes = df["close"]

        if len(closes) < 20:
            return 0.5

        trend = (closes.iloc[-1] - closes.iloc[-20]) / closes.iloc[-20]

        return max(0.0, min(1.0, 0.5 + trend))

    # -------------------------------------------------
    # 📊 Volatility
    # -------------------------------------------------
    def _compute_volatility(self, df):

        returns = df["close"].pct_change().dropna()

        if len(returns) < 20:
            return 0.5

        vol = returns[-20:].std()

        return max(0.0, min(1.0, vol * 10))

    # -------------------------------------------------
    # 📊 Momentum
    # -------------------------------------------------
    def _compute_momentum(self, df):

        closes = df["close"]

        if len(closes) < 10:
            return 0.5

        momentum = (closes.iloc[-1] - closes.iloc[-10]) / closes.iloc[-10]

        return max(0.0, min(1.0, 0.5 + momentum))

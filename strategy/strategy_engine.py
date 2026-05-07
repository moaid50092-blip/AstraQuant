# strategy/strategy_engine.py

from intelligence.historical_context_engine import HistoricalContextEngine
from intelligence.volatility_context_engine import VolatilityContextEngine

import numpy as np
import datetime


class StrategyEngine:

    def __init__(self):

        self.historical_engine = HistoricalContextEngine()
        self.volatility_engine = VolatilityContextEngine()

    # -------------------------------------------------
    def detect(self, symbol, df):

        if df is None or len(df) < 40:
            return None

        # =========================================
        # 🔥 CORE MARKET INTELLIGENCE
        # =========================================

        trend_strength = self._compute_trend_strength(df)
        momentum_score = self._compute_momentum(df)
        volatility = self._compute_volatility(df)

        # =========================================
        # 🔥 STRUCTURE
        # =========================================

        liquidity_score = self._compute_liquidity_score(df)

        mtf_score = self._compute_mtf_score(df)

        session_score = self._compute_session_score()

        context_score = self._compute_context_score(
            volatility
        )

        factor_score = self._compute_factor_score(
            trend_strength,
            momentum_score
        )

        structure_score = (
            trend_strength * 0.6 +
            mtf_score * 0.4
        )

        # =========================================
        # 🔥 EARLY ENGINE
        # =========================================

        early, compression, acceleration = \
            self._detect_early_expansion(
                df,
                momentum_score,
                volatility
            )

        # =========================================
        # 🔥 BASE SCORE (rebalanced)
        # =========================================

        base_score = (

            structure_score * 0.35 +
            momentum_score * 0.25 +
            liquidity_score * 0.15 +
            mtf_score * 0.10 +
            factor_score * 0.10 +
            context_score * 0.05
        )

        # =========================================
        # 🔥 VOLATILITY FILTER
        # =========================================

        if 0.35 <= volatility <= 0.75:
            base_score += 0.03

        elif volatility > 0.90:
            base_score -= 0.04

        # =========================================
        # 🔥 PATTERN ENGINE
        # =========================================

        pattern_boost = \
            self._detect_liquidity_compression_breakout(df)

        base_score += pattern_boost

        # =========================================
        # 🔥 EARLY BOOST (smart)
        # =========================================

        if (
            early
            and acceleration
            and structure_score > 0.55
        ):
            base_score += 0.04

        elif early:
            base_score += 0.01

        # =========================================
        # 🔥 CONSISTENCY ENGINE
        # =========================================

        scores = [
            structure_score,
            liquidity_score,
            factor_score,
            context_score
        ]

        mean_score = sum(scores) / len(scores)

        variance = sum(
            (s - mean_score) ** 2
            for s in scores
        ) / len(scores)

        std = variance ** 0.5

        consistency = max(
            0.0,
            min(1.0, 1 - std)
        )

        adjustment = (
            (consistency - 0.5) * 0.12
        )

        base_score *= (1 + adjustment)

        # =========================================
        # 🔥 CLAMP
        # =========================================

        base_score = max(
            0.0,
            min(1.0, base_score)
        )

        # =========================================
        # 🔥 EXTERNAL ENGINES
        # =========================================

        volatility_score = \
            self.volatility_engine.evaluate(df)

        market_features = {

            "trend_strength": trend_strength,
            "volatility": volatility,
            "momentum": momentum_score,
            "liquidity_state": liquidity_score,
            "session_context": session_score
        }

        historical_score = \
            self.historical_engine.evaluate(
                market_features
            )

        # =========================================
        # 🔥 DIRECTION ENGINE (stable)
        # =========================================

        if momentum_score >= 0.56:
            direction = "up"

        elif momentum_score <= 0.44:
            direction = "down"

        else:
            direction = "neutral"

        # =========================================
        # 🔥 SIGNAL OUTPUT
        # =========================================

        signal = {

            "symbol": symbol,

            "base_score": round(base_score, 3),

            "momentum": direction,

            "strength": round(
                abs(momentum_score - 0.5) * 2,
                3
            ),

            # EARLY
            "early_entry": early,
            "compression": compression,
            "acceleration": acceleration,

            # SCORES
            "structure_score": round(structure_score, 3),
            "liquidity_score": round(liquidity_score, 3),
            "session_score": round(session_score, 3),
            "context_score": round(context_score, 3),
            "mtf_score": round(mtf_score, 3),
            "factor_score": round(factor_score, 3),
            "historical_score": round(historical_score, 3),
            "volatility_score": round(volatility_score, 3)
        }

        return signal

    # -------------------------------------------------
    def _compute_mtf_score(self, df):

        closes = df["close"]

        short = (
            closes.iloc[-1] -
            closes.iloc[-5]
        ) / closes.iloc[-5]

        mid = (
            closes.iloc[-1] -
            closes.iloc[-15]
        ) / closes.iloc[-15]

        long = (
            closes.iloc[-1] -
            closes.iloc[-30]
        ) / closes.iloc[-30]

        weighted = (
            short * 0.2 +
            mid * 0.3 +
            long * 0.5
        )

        return max(
            0.0,
            min(1.0, 0.5 + weighted * 4)
        )

    # -------------------------------------------------
    def _compute_liquidity_score(self, df):

        highs = df["high"]
        lows = df["low"]
        closes = df["close"]

        prev_high = highs.iloc[-15:-5].max()
        prev_low = lows.iloc[-15:-5].min()

        last_close = closes.iloc[-1]

        breakout_up = last_close > prev_high
        breakout_down = last_close < prev_low

        compression = (
            highs.iloc[-5:].max() -
            lows.iloc[-5:].min()
        )

        prior = (
            highs.iloc[-15:-5].max() -
            lows.iloc[-15:-5].min()
        )

        if prior == 0:
            return 0.5

        compression_ratio = compression / prior

        score = 0.5

        if breakout_up or breakout_down:
            score += 0.1

        if compression_ratio < 0.6:
            score += 0.1

        return max(
            0.0,
            min(1.0, score)
        )

    # -------------------------------------------------
    def _compute_session_score(self):

        hour = datetime.datetime.utcnow().hour

        # London + NY overlap
        if 12 <= hour <= 16:
            return 0.75

        # London
        elif 7 <= hour <= 11:
            return 0.65

        # Asia
        elif 0 <= hour <= 5:
            return 0.45

        return 0.50

    # -------------------------------------------------
    def _compute_context_score(self, volatility):

        if volatility > 0.8:
            return 0.35

        elif volatility < 0.25:
            return 0.40

        return 0.65

    # -------------------------------------------------
    def _compute_factor_score(
        self,
        trend_strength,
        momentum
    ):

        weighted = (
            trend_strength * 0.65 +
            momentum * 0.35
        )

        return max(
            0.0,
            min(1.0, weighted)
        )

    # -------------------------------------------------
    def _detect_early_expansion(
        self,
        df,
        momentum,
        volatility
    ):

        highs = df["high"]
        lows = df["low"]
        closes = df["close"]

        recent_range = (
            highs.iloc[-8:].max() -
            lows.iloc[-8:].min()
        )

        prev_range = (
            highs.iloc[-20:-8].max() -
            lows.iloc[-20:-8].min()
        )

        if prev_range == 0:
            return False, False, False

        compression = (
            recent_range / prev_range
        ) < 0.75

        breakout_up = (
            closes.iloc[-1] >
            highs.iloc[-5:-1].max()
        )

        breakout_down = (
            closes.iloc[-1] <
            lows.iloc[-5:-1].min()
        )

        breakout = (
            breakout_up or breakout_down
        )

        prev_momentum = (
            closes.iloc[-3] -
            closes.iloc[-12]
        ) / closes.iloc[-12]

        prev_momentum = max(
            0.0,
            min(1.0, 0.5 + prev_momentum)
        )

        acceleration = (
            abs(momentum - 0.5) >
            abs(prev_momentum - 0.5)
        )

        momentum_strength = abs(momentum - 0.5)

        early = (

            compression
            and breakout
            and acceleration
            and momentum_strength > 0.06
            and volatility > 0.3
        )

        return early, compression, acceleration

    # -------------------------------------------------
    def _detect_liquidity_compression_breakout(self, df):

        highs = df["high"]
        lows = df["low"]
        closes = df["close"]

        compression = (
            highs.iloc[-5:].max() -
            lows.iloc[-5:].min()
        )

        prior = (
            highs.iloc[-15:-5].max() -
            lows.iloc[-15:-5].min()
        )

        if prior == 0:
            return 0.0

        compression_ratio = compression / prior

        breakout = (

            closes.iloc[-1] >
            highs.iloc[-5:-1].max()

            or

            closes.iloc[-1] <
            lows.iloc[-5:-1].min()
        )

        if (
            compression_ratio < 0.5
            and breakout
        ):
            return 0.12

        return 0.0

    # -------------------------------------------------
    def _compute_trend_strength(self, df):

        closes = df["close"]

        short = (
            closes.iloc[-1] -
            closes.iloc[-10]
        ) / closes.iloc[-10]

        long = (
            closes.iloc[-1] -
            closes.iloc[-30]
        ) / closes.iloc[-30]

        weighted = (
            short * 0.4 +
            long * 0.6
        )

        return max(
            0.0,
            min(1.0, 0.5 + weighted * 5)
        )

    # -------------------------------------------------
    def _compute_volatility(self, df):

        returns = (
            df["close"]
            .pct_change()
            .dropna()
        )

        vol = returns[-20:].std()

        adaptive = vol * np.sqrt(20)

        return max(
            0.0,
            min(1.0, adaptive * 8)
        )

    # -------------------------------------------------
    def _compute_momentum(self, df):

        closes = df["close"]

        short = (
            closes.iloc[-1] -
            closes.iloc[-5]
        ) / closes.iloc[-5]

        medium = (
            closes.iloc[-1] -
            closes.iloc[-10]
        ) / closes.iloc[-10]

        long = (
            closes.iloc[-1] -
            closes.iloc[-20]
        ) / closes.iloc[-20]

        weighted = (
            short * 0.5 +
            medium * 0.3 +
            long * 0.2
        )

        return max(
            0.0,
            min(1.0, 0.5 + weighted * 6)
        )

# intelligence/volatility_context_engine.py

"""
Volatility Context Engine

This module detects volatility contraction and expansion readiness.

Markets often transition from low volatility (compression)
to high volatility (expansion). Detecting compression phases
can significantly improve breakout and momentum signals.

This engine does NOT produce trade signals.
It only produces a contextual volatility_score modifier.

Output range:
0.0 – 1.0
0.5 = neutral volatility context
"""

import numpy as np


class VolatilityContextEngine:

    def __init__(self):

        # minimum number of candles required
        self.min_period = 30

    # -------------------------------------------------
    # Public Interface
    # -------------------------------------------------

    def evaluate(self, df):

        """
        Evaluate volatility context from OHLCV dataframe.
        """

        if df is None or len(df) < self.min_period:
            return 0.5

        atr_compression = self._atr_compression(df)
        range_compression = self._range_compression(df)
        volatility_decline = self._volatility_decline(df)

        # combine the compression signals
        compression_score = (
            atr_compression * 0.4 +
            range_compression * 0.3 +
            volatility_decline * 0.3
        )

        # convert compression to expansion readiness
        volatility_score = 0.5 + (compression_score - 0.5) * 0.5

        return float(np.clip(volatility_score, 0.0, 1.0))

    # -------------------------------------------------
    # ATR Compression
    # -------------------------------------------------

    def _atr_compression(self, df):

        high = df["high"]
        low = df["low"]
        close = df["close"]

        tr = np.maximum(high - low,
                        np.maximum(abs(high - close.shift(1)),
                                   abs(low - close.shift(1))))

        atr = tr.rolling(14).mean()

        if atr.isna().all():
            return 0.5

        recent_atr = atr.iloc[-5:].mean()
        long_atr = atr.iloc[-20:].mean()

        if long_atr == 0:
            return 0.5

        compression = 1 - (recent_atr / long_atr)

        return float(np.clip(compression, 0.0, 1.0))

    # -------------------------------------------------
    # Candle Range Compression
    # -------------------------------------------------

    def _range_compression(self, df):

        candle_range = df["high"] - df["low"]

        short_range = candle_range.iloc[-5:].mean()
        long_range = candle_range.iloc[-20:].mean()

        if long_range == 0:
            return 0.5

        compression = 1 - (short_range / long_range)

        return float(np.clip(compression, 0.0, 1.0))

    # -------------------------------------------------
    # Volatility Decline
    # -------------------------------------------------

    def _volatility_decline(self, df):

        returns = df["close"].pct_change().dropna()

        if len(returns) < 20:
            return 0.5

        short_vol = returns.iloc[-5:].std()
        long_vol = returns.iloc[-20:].std()

        if long_vol == 0:
            return 0.5

        decline = 1 - (short_vol / long_vol)

        return float(np.clip(decline, 0.0, 1.0))

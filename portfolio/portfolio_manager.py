# portfolio/portfolio_manager.py

"""
Portfolio Manager

Responsible for:
• Position sizing
• Portfolio exposure control
• Correlation-aware exposure scaling

This module does NOT reject trades.
Instead it adjusts position sizes to reduce hidden
portfolio exposure when multiple assets are highly correlated.

This preserves AstraQuant's probabilistic architecture.
"""

import numpy as np


class PortfolioManager:

    def __init__(
        self,
        base_position_size=1.0,
        max_portfolio_exposure=5.0,
        correlation_threshold=0.75,
        correlation_lookback=50
    ):

        self.base_position_size = base_position_size
        self.max_portfolio_exposure = max_portfolio_exposure
        self.correlation_threshold = correlation_threshold
        self.correlation_lookback = correlation_lookback

        self.open_positions = {}

    # -------------------------------------------------
    # Allocate Positions
    # -------------------------------------------------

    def allocate_positions(self, opportunities, market_data):

        """
        opportunities format:

        [
            {
                "symbol": "BTC",
                "probability_score": 0.82
            }
        ]

        market_data format:

        {
            "BTC": dataframe,
            "ETH": dataframe
        }
        """

        trades = []

        for opportunity in opportunities:

            symbol = opportunity["symbol"]
            probability = opportunity.get("probability_score", 0)

            size = self._compute_position_size(probability)

            correlation_scale = self._compute_correlation_scale(
                symbol,
                market_data
            )

            final_size = size * correlation_scale

            if self._portfolio_exposure() + final_size > self.max_portfolio_exposure:
                final_size = max(
                    0,
                    self.max_portfolio_exposure - self._portfolio_exposure()
                )

            trade = {
                "symbol": symbol,
                "probability_score": probability,
                "position_size": final_size
            }

            if final_size > 0:
                trades.append(trade)
                self.open_positions[symbol] = final_size

        return trades

    # -------------------------------------------------
    # Position Size
    # -------------------------------------------------

    def _compute_position_size(self, probability):

        return self.base_position_size * probability

    # -------------------------------------------------
    # Correlation Scaling
    # -------------------------------------------------

    def _compute_correlation_scale(self, symbol, market_data):

        if symbol not in market_data:
            return 1.0

        if not self.open_positions:
            return 1.0

        df_target = market_data[symbol]

        closes_target = df_target["close"].pct_change().dropna()

        correlations = []

        for open_symbol in self.open_positions:

            if open_symbol not in market_data:
                continue

            df_open = market_data[open_symbol]

            closes_open = df_open["close"].pct_change().dropna()

            common_length = min(
                len(closes_target),
                len(closes_open),
                self.correlation_lookback
            )

            if common_length < 10:
                continue

            r1 = closes_target[-common_length:]
            r2 = closes_open[-common_length:]

            corr = np.corrcoef(r1, r2)[0, 1]

            correlations.append(abs(corr))

        if not correlations:
            return 1.0

        avg_corr = np.mean(correlations)

        if avg_corr < self.correlation_threshold:
            return 1.0

        scale = 1 - (avg_corr - self.correlation_threshold)

        scale = max(0.3, scale)

        return scale

    # -------------------------------------------------
    # Portfolio Exposure
    # -------------------------------------------------

    def _portfolio_exposure(self):

        return sum(self.open_positions.values())

    # -------------------------------------------------
    # Close Position
    # -------------------------------------------------

    def close_position(self, symbol):

        if symbol in self.open_positions:
            del self.open_positions[symbol]

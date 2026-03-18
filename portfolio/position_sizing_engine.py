# portfolio/position_sizing_engine.py

"""
Position Sizing Engine

Responsible for determining the final size of each trade.

Sizing is based on:
- probability_score (signal strength)
- optional size_modifier from correlation control
- base risk configuration

This engine converts opportunities into executable trade objects.
"""

import numpy as np


class PositionSizingEngine:

    def __init__(self, base_risk=1.0, max_size=1.0):

        # base position size multiplier
        self.base_risk = base_risk

        # absolute cap for position size
        self.max_size = max_size

    # -------------------------------------------------
    # Apply Position Sizing
    # -------------------------------------------------

    def apply(self, trades):

        """
        trades format:

        [
            {
                "symbol": "BTC",
                "probability_score": 0.82,
                "size_modifier": 0.6
            }
        ]
        """

        sized_trades = []

        for trade in trades:

            probability = trade.get("probability_score", 0.5)

            modifier = trade.get("size_modifier", 1.0)

            # convert probability to position size
            size = self._probability_to_size(probability)

            # apply correlation modifier
            size *= modifier

            # enforce max size
            size = min(size, self.max_size)

            trade["position_size"] = float(size)

            sized_trades.append(trade)

        return sized_trades

    # -------------------------------------------------
    # Probability → Size Mapping
    # -------------------------------------------------

    def _probability_to_size(self, probability):

        """
        Converts probability score into position size.

        Higher probability → larger position
        """

        probability = np.clip(probability, 0, 1)

        size = self.base_risk * probability

        return size

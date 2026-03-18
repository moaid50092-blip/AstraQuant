# portfolio/correlation_engine.py

"""
Portfolio Correlation Engine

Controls portfolio exposure when multiple trades are
likely driven by the same market movement.

Example:
BTC, ETH, and SOL often move together. Opening full-size
positions in all three may unintentionally concentrate risk.

Instead of removing trades completely, this engine reduces
position size proportionally when correlation is detected.

This preserves opportunity while controlling portfolio risk.
"""


class CorrelationEngine:

    def __init__(self):

        # assets considered part of the same crypto beta group
        self.crypto_beta_group = {
            "BTC", "ETH", "SOL", "BNB", "AVAX", "LINK", "ADA", "MATIC"
        }

        # reduction factor when correlation cluster detected
        self.correlation_reduction_factor = 0.6

    # -------------------------------------------------
    # Adjust Trades Based on Correlation
    # -------------------------------------------------

    def adjust(self, trades):

        """
        trades format:

        [
            {
                "symbol": "BTC",
                "signal": {...},
                "probability_score": 0.82
            }
        ]
        """

        if not trades:
            return []

        beta_trades = []
        non_beta_trades = []

        for trade in trades:

            symbol = trade["symbol"]

            if symbol in self.crypto_beta_group:
                beta_trades.append(trade)
            else:
                non_beta_trades.append(trade)

        # If more than one beta asset appears,
        # reduce position sizes to control correlated exposure
        if len(beta_trades) > 1:

            for trade in beta_trades:
                trade["size_modifier"] = self.correlation_reduction_factor

        else:

            for trade in beta_trades:
                trade["size_modifier"] = 1.0

        for trade in non_beta_trades:
            trade["size_modifier"] = 1.0

        return beta_trades + non_beta_trades

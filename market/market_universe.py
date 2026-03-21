# market/market_universe.py

"""
Market Universe

Responsible for building the list of assets that the
system will analyze during each cycle.

This implementation uses a dynamic market universe model.
The universe can later be connected to exchange data
(top volume assets, top liquidity pairs, etc.).

For the reference implementation we provide
a static high-liquidity crypto universe.
"""


class MarketUniverse:

    def __init__(self):

        # reference high-liquidity assets
        self.base_universe = [
            "BTC",
            "ETH",
            "SOL",
            "LINK"
        ]

    # -------------------------------------------------
    # Get Universe
    # -------------------------------------------------

    def get_universe(self):
        """
        Returns the current list of assets
        the system will analyze.
        """

        return list(self.base_universe)

    # -------------------------------------------------
    # Alias Method (Compatibility)
    # -------------------------------------------------

    def get_symbols(self):
        return self.get_universe()

    # -------------------------------------------------
    # Update Universe (future extension)
    # -------------------------------------------------

    def update_universe(self, new_assets):
        """
        Allows updating the universe dynamically.

        In future versions this can be driven by:
        - exchange volume rankings
        - liquidity filters
        - volatility filters
        """

        if not new_assets:
            return

        self.base_universe = list(new_assets)

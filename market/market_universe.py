class MarketUniverse:

    def __init__(self):

        # ✅ Binance trading pairs (IMPORTANT)
        self.base_universe = [
            "BTCUSDT",
            "ETHUSDT",
            "SOLUSDT",
            "XAUUSDT"
        ]

    # -------------------------------------------------
    def get_universe(self):
        return list(self.base_universe)

    # -------------------------------------------------
    def get_symbols(self):
        return self.get_universe()

    # -------------------------------------------------
    def update_universe(self, new_assets):

        if not new_assets:
            return

        self.base_universe = list(new_assets)

# data/market_data.py

"""
Market Data Loader

Responsible for retrieving market OHLCV data
for all assets in the current Market Universe.

In the reference implementation this module
generates synthetic OHLCV data so the system
can run without exchange connectivity.

Later it can be replaced with a real exchange
data connector (Binance / CCXT / Websocket etc.)
without affecting the rest of the architecture.
"""

import pandas as pd
import numpy as np
import time


class MarketDataLoader:

    def __init__(self):

        # length of synthetic dataset
        self.default_length = 200

    # -------------------------------------------------
    # Public Interface
    # -------------------------------------------------

    def load_market_data(self, symbols):

        """
        Returns market data dictionary:

        {
            "BTC": dataframe,
            "ETH": dataframe,
            ...
        }
        """

        market_data = {}

        for symbol in symbols:

            df = self._generate_fake_data(symbol)

            if df is not None:
                market_data[symbol] = df

        return market_data

    # -------------------------------------------------
    # Synthetic Data Generator
    # -------------------------------------------------

    def _generate_fake_data(self, symbol):

        """
        Generates synthetic OHLCV data.

        This keeps the architecture functional
        even without real exchange APIs.
        """

        length = self.default_length

        base_price = np.random.uniform(50, 500)

        prices = base_price + np.cumsum(
            np.random.normal(0, 1, length)
        )

        highs = prices + np.random.uniform(0, 2, length)
        lows = prices - np.random.uniform(0, 2, length)

        opens = prices + np.random.normal(0, 0.5, length)
        closes = prices

        volumes = np.random.uniform(1000, 10000, length)

        timestamps = pd.date_range(
            end=pd.Timestamp.now(),
            periods=length,
            freq="1min"
        )

        df = pd.DataFrame({
            "timestamp": timestamps,
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "volume": volumes
        })

        df.set_index("timestamp", inplace=True)

        return df

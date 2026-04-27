# data/market_data_loader.py

import pandas as pd
import numpy as np


class MarketDataLoader:

    def __init__(self):
        self.default_length = 200

    # -------------------------------------------------
    # Public Interface
    # -------------------------------------------------

    def load_market_data(self, symbols):

        market_data = {}

        for symbol in symbols:

            df_1m = self._generate_fake_data(symbol)

            if df_1m is None:
                continue

            # 🔥 إنشاء فريمات أعلى من نفس البيانات
            df_5m = self._resample(df_1m, "5min")
            df_15m = self._resample(df_1m, "15min")

            market_data[symbol] = {
                "1m": df_1m,
                "5m": df_5m,
                "15m": df_15m
            }

        return market_data

    # -------------------------------------------------
    # Synthetic Data
    # -------------------------------------------------

    def _generate_fake_data(self, symbol):

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
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "volume": volumes
        }, index=timestamps)

        return df

    # -------------------------------------------------
    # 🔥 Resampling (الذكاء الحقيقي هنا)
    # -------------------------------------------------

    def _resample(self, df, timeframe):

        return df.resample(timeframe).agg({
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum"
        }).dropna()

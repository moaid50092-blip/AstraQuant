# data/market_data_loader.py

import pandas as pd
import numpy as np
from binance.client import Client


class MarketDataLoader:

    def __init__(self):

        # 🔐 حط مفاتيحك هون (لا تشاركهم مع أحد)
        API_KEY = "GUZ3rnXueopAr6FKtrAs0Xv2U1euDZ9OHhMwUMwdPvbih2aCczPdw98WoUkQznGc"
        API_SECRET = "Z5Ll72YpykgRITrhVjm4CTtMVaCgvLPRZLP2RiBNedBFVEMV5SiB3Td62YyvGmF8"

        self.client = Client(API_KEY, API_SECRET)

        self.default_length = 200

    # -------------------------------------------------
    # Public Interface
    # -------------------------------------------------

    def load_market_data(self, symbols):

        market_data = {}

        for symbol in symbols:

            try:
                df_1m = self._get_binance_data(symbol, "1m", 200)

                if df_1m is None or df_1m.empty:
                    raise Exception("No data")

            except Exception:
                # 🔥 fallback (في حال فشل الاتصال)
                df_1m = self._generate_fake_data(symbol)

            df_5m = self._resample(df_1m, "5min")
            df_15m = self._resample(df_1m, "15min")

            market_data[symbol] = {
                "1m": df_1m,
                "5m": df_5m,
                "15m": df_15m
            }

        return market_data

    # -------------------------------------------------
    # 🔥 Binance Data
    # -------------------------------------------------

    def _get_binance_data(self, symbol, interval, limit=200):

        try:
            klines = self.client.get_klines(
                symbol=symbol,
                interval=interval,
                limit=limit
            )

            df = pd.DataFrame(klines, columns=[
                "timestamp", "open", "high", "low", "close", "volume",
                "close_time", "qav", "num_trades",
                "taker_base_vol", "taker_quote_vol", "ignore"
            ])

            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

            df = df[["timestamp", "open", "high", "low", "close", "volume"]]

            df.set_index("timestamp", inplace=True)

            df = df.astype(float)

            return df

        except Exception:
            return None

    # -------------------------------------------------
    # Synthetic Data (fallback)
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
    # Resampling
    # -------------------------------------------------

    def _resample(self, df, timeframe):

        return df.resample(timeframe).agg({
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum"
        }).dropna()

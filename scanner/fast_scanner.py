import numpy as np


class FastScanner:

    def __init__(self, candidate_count=10):
        self.candidate_count = candidate_count

    # -------------------------------------------------
    def compute_fast_score(self, df):

        if df is None or len(df) < 30:
            return 0.0

        closes = df["close"]
        volumes = df["volume"]

        # ---------------------------------------------
        # Momentum (signed)
        # ---------------------------------------------

        momentum = (
            closes.iloc[-1] - closes.iloc[-10]
        ) / max(closes.iloc[-10], 1e-9)

        momentum_score = np.clip(momentum * 5, -1, 1)

        # ---------------------------------------------
        # Volatility
        # ---------------------------------------------

        returns = closes.pct_change().dropna()
        volatility = np.std(returns[-20:]) if len(returns) >= 20 else 0
        volatility_score = np.clip(volatility * 10, 0, 1)

        # ---------------------------------------------
        # Volume
        # ---------------------------------------------

        avg_volume = volumes.iloc[-20:].mean()
        volume_activity = volumes.iloc[-1] / max(avg_volume, 1e-9)
        volume_score = np.clip(volume_activity / 2, 0, 1)

        # ---------------------------------------------
        # 🔥 DIRECTION-AWARE SCORE
        # ---------------------------------------------

        directional_strength = abs(momentum_score)

        fast_score = (
            directional_strength * 0.4
            + volatility_score * 0.3
            + volume_score * 0.3
        )

        return float(np.clip(fast_score, 0, 1))

    # -------------------------------------------------
    def rank_assets(self, market_data):

        scores = []

        for symbol, df in market_data.items():

            score = self.compute_fast_score(df)

            scores.append({
                "symbol": symbol,
                "fast_score": score
            })

        scores.sort(key=lambda x: x["fast_score"], reverse=True)

        return scores

    # -------------------------------------------------
    def select_candidates(self, ranked_assets):

        return ranked_assets[: self.candidate_count]

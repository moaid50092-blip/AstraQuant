# scanner/fast_scanner.py

"""
Fast Market Scanner

This module performs a lightweight scan across all assets
in the Market Universe to identify the most promising
candidates for deeper analysis.

It is the first stage of the Two-Stage Scanner Architecture.

Stage 1 → Fast Scan (momentum, volatility, volume)
Stage 2 → Deep Analysis (strategy + probability)

This module does NOT produce trading signals.
It only ranks assets based on activity and potential.
"""

import numpy as np


class FastScanner:

    def __init__(self, candidate_count=10):

        # number of assets to pass to deep analysis
        self.candidate_count = candidate_count

    # -------------------------------------------------
    # Compute Fast Score
    # -------------------------------------------------

    def compute_fast_score(self, df):

        """
        Computes a lightweight score using:
        - short momentum
        - recent volatility
        - volume activity
        """

        if df is None or len(df) < 30:
            return 0.0

        closes = df["close"]
        volumes = df["volume"]

        # ---------------------------------------------
        # Momentum
        # ---------------------------------------------

        momentum = (
            closes.iloc[-1] - closes.iloc[-10]
        ) / max(closes.iloc[-10], 1e-9)

        # ---------------------------------------------
        # Volatility
        # ---------------------------------------------

        returns = closes.pct_change().dropna()

        volatility = np.std(returns[-20:]) if len(returns) >= 20 else 0

        # ---------------------------------------------
        # Volume Activity
        # ---------------------------------------------

        avg_volume = volumes.iloc[-20:].mean()

        volume_activity = volumes.iloc[-1] / max(avg_volume, 1e-9)

        # ---------------------------------------------
        # Normalize Components
        # ---------------------------------------------

        momentum_score = np.clip(momentum * 5, -1, 1)

        volatility_score = np.clip(volatility * 10, 0, 1)

        volume_score = np.clip(volume_activity / 2, 0, 1)

        # ---------------------------------------------
        # Weighted Fast Score
        # ---------------------------------------------

        fast_score = (
            momentum_score * 0.4
            + volatility_score * 0.3
            + volume_score * 0.3
        )

        return float(np.clip(fast_score, 0, 1))

    # -------------------------------------------------
    # Rank All Assets
    # -------------------------------------------------

    def rank_assets(self, market_data):

        """
        market_data format:

        {
            "BTC": dataframe,
            "ETH": dataframe,
            ...
        }
        """

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
    # Select Top Candidates
    # -------------------------------------------------

    def select_candidates(self, ranked_assets):

        """
        Selects top N assets for deep analysis.
        """

        return ranked_assets[: self.candidate_count]

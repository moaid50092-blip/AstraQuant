# quality/opportunity_quality_engine.py

"""
Opportunity Quality Engine

Evaluates the overall quality of opportunities
available in the market during the current cycle.

The goal is to measure:

- How strong the best opportunities are
- How concentrated strong signals are
- Whether the market environment is favorable

This engine does NOT block trades.
It only provides a market_opportunity_quality metric
that can later influence position sizing or
portfolio aggressiveness.
"""

import numpy as np


class OpportunityQualityEngine:

    def __init__(self):
        pass

    # -------------------------------------------------
    # Public Interface
    # -------------------------------------------------

    def evaluate(self, ranked_opportunities):

        """
        ranked_opportunities format:

        [
            {"symbol": "...", "probability_score": 0.82},
            {"symbol": "...", "probability_score": 0.75},
            ...
        ]
        """

        if not ranked_opportunities:
            return {
                "market_quality": 0.0,
                "top_score": 0.0,
                "average_score": 0.0
            }

        scores = [op["probability_score"] for op in ranked_opportunities]

        top_score = max(scores)
        average_score = float(np.mean(scores))

        # simple market opportunity model
        market_quality = (
            top_score * 0.6 +
            average_score * 0.4
        )

        return {
            "market_quality": float(np.clip(market_quality, 0, 1)),
            "top_score": float(top_score),
            "average_score": float(average_score)
        }

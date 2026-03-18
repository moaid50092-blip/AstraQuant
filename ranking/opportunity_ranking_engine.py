# ranking/opportunity_ranking_engine.py

"""
Opportunity Ranking Engine

Responsible for ranking trading opportunities
after probability evaluation.

The goal is to identify the strongest opportunities
across all analyzed assets before portfolio decisions.

Important:
This module does NOT filter trades aggressively.
It only ranks them based on probability score.
"""


class OpportunityRankingEngine:

    def __init__(self, max_opportunities=10):
        self.max_opportunities = max_opportunities

    # -------------------------------------------------
    # Rank Opportunities
    # -------------------------------------------------

    def rank(self, opportunities):

        """
        opportunities format:

        [
            {
                "symbol": "BTC",
                "signal": {...},
                "probability_score": 0.82
            },
            ...
        ]
        """

        if not opportunities:
            return []

        ranked = sorted(
            opportunities,
            key=lambda x: x["probability_score"],
            reverse=True
        )

        return ranked[: self.max_opportunities]

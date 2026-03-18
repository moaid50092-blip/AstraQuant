# probability/probability_engine.py

"""
Probability Engine

Hierarchical Edge Model combining base signal with contextual modifiers.

Context layers include:

• Structure
• Liquidity
• Session
• Context
• Multi-timeframe
• Factor dominance
• Historical context
• Volatility context
"""

class ProbabilityEngine:

    def __init__(self):
        pass

    # -------------------------------------------------
    # Evaluate Trade Probability
    # -------------------------------------------------

    def evaluate(self, signal):

        base_edge = signal.get("base_score", 0.5)

        structure_modifier = self._modifier(signal.get("structure_score", 0.5))
        liquidity_modifier = self._modifier(signal.get("liquidity_score", 0.5))
        session_modifier = self._modifier(signal.get("session_score", 0.5))
        context_modifier = self._modifier(signal.get("context_score", 0.5))
        mtf_modifier = self._modifier(signal.get("mtf_score", 0.5))
        factor_modifier = self._modifier(signal.get("factor_score", 0.5))
        historical_modifier = self._modifier(signal.get("historical_score", 0.5))
        volatility_modifier = self._modifier(signal.get("volatility_score", 0.5))

        edge = base_edge

        # Apply contextual modifiers
        edge *= structure_modifier
        edge *= liquidity_modifier
        edge *= session_modifier
        edge *= context_modifier
        edge *= mtf_modifier
        edge *= factor_modifier
        edge *= historical_modifier
        edge *= volatility_modifier

        return self._normalize(edge)

    # -------------------------------------------------
    # Score Modifier
    # -------------------------------------------------

    def _modifier(self, score):

        """
        Convert score into soft probability modifier.

        score = 0.5 → neutral
        """

        return 0.8 + (score * 0.4)

    # -------------------------------------------------
    # Normalize Probability
    # -------------------------------------------------

    def _normalize(self, value):

        if value < 0:
            return 0

        if value > 1:
            return 1

        return value

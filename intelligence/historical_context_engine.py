# intelligence/historical_context_engine.py

"""
Historical Market Context Engine

Provides lightweight historical context to the trading system.

The engine compares the current market state with previously
observed market states and produces a small probabilistic
modifier indicating whether similar conditions historically
favored continuation or reversal.

Design principles:

• No hard filters
• Neutral output if insufficient data
• Lightweight memory-based approach
• Compatible with scanner-based architectures

Output:

historical_score in range [0,1]
0.5 = neutral
"""


import numpy as np
from collections import deque


class HistoricalContextEngine:

    def __init__(self, memory_size=5000, similarity_threshold=0.85):

        # rolling memory of past market states
        self.memory = deque(maxlen=memory_size)

        # similarity threshold for matching historical states
        self.similarity_threshold = similarity_threshold

        # neutral score
        self.neutral_score = 0.5

    # -------------------------------------------------
    # Evaluate Historical Context
    # -------------------------------------------------

    def evaluate(self, market_features):

        """
        market_features example:

        {
            "trend_strength": float,
            "volatility": float,
            "momentum": float,
            "liquidity_state": float,
            "session_context": float
        }
        """

        current_state = self._build_state_vector(market_features)

        if len(self.memory) < 50:
            return self.neutral_score

        similar_states = self._find_similar_states(current_state)

        if len(similar_states) < 5:
            return self.neutral_score

        historical_bias = self._evaluate_outcomes(similar_states)

        return self._convert_to_score(historical_bias)

    # -------------------------------------------------
    # Store Market State
    # -------------------------------------------------

    def store_state(self, market_features, outcome):

        """
        outcome example:

        +1 → continuation
        -1 → reversal
        """

        state = self._build_state_vector(market_features)

        self.memory.append({
            "state": state,
            "outcome": outcome
        })

    # -------------------------------------------------
    # Build State Vector
    # -------------------------------------------------

    def _build_state_vector(self, features):

        return np.array([
            features.get("trend_strength", 0.5),
            features.get("volatility", 0.5),
            features.get("momentum", 0.5),
            features.get("liquidity_state", 0.5),
            features.get("session_context", 0.5)
        ])

    # -------------------------------------------------
    # Find Similar Historical States
    # -------------------------------------------------

    def _find_similar_states(self, current_state):

        matches = []

        for record in self.memory:

            past_state = record["state"]

            similarity = self._cosine_similarity(current_state, past_state)

            if similarity >= self.similarity_threshold:
                matches.append(record)

        return matches

    # -------------------------------------------------
    # Evaluate Historical Outcomes
    # -------------------------------------------------

    def _evaluate_outcomes(self, similar_states):

        outcomes = [record["outcome"] for record in similar_states]

        if len(outcomes) == 0:
            return 0

        return np.mean(outcomes)

    # -------------------------------------------------
    # Convert Bias to Probability Score
    # -------------------------------------------------

    def _convert_to_score(self, bias):

        """
        Converts outcome bias to soft probability modifier.

        bias range:
        -1 → reversal tendency
        +1 → continuation tendency
        """

        score = 0.5 + (bias * 0.1)

        return np.clip(score, 0.3, 0.7)

    # -------------------------------------------------
    # Cosine Similarity
    # -------------------------------------------------

    def _cosine_similarity(self, a, b):

        dot = np.dot(a, b)

        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        if norm_a == 0 or norm_b == 0:
            return 0

        return dot / (norm_a * norm_b)

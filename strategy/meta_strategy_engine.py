# strategy/meta_strategy_engine.py

"""
Meta Strategy Engine

Provides a strategy orchestration layer for AstraQuant.

Purpose:
Allow the system to support multiple strategies in the future
without changing the architecture.

Behavior:

• If only one strategy is present → pass-through (no modification)
• If multiple strategies exist → select the most appropriate strategy
  based on simple context signals.

The engine remains passive until more than one strategy is registered.

This preserves AstraQuant's modular architecture.
"""


class MetaStrategyEngine:

    def __init__(self):

        # registry of available strategies
        self.strategy_registry = {}

    # -------------------------------------------------
    # Register Strategy
    # -------------------------------------------------

    def register_strategy(self, name, strategy):

        """
        Register a strategy module.

        Example:
        register_strategy("breakout", breakout_strategy)
        """

        self.strategy_registry[name] = strategy

    # -------------------------------------------------
    # Strategy Selection
    # -------------------------------------------------

    def select_strategy(self, market_context=None):

        """
        Returns the strategy that should be used.
        """

        # pass-through if only one strategy exists
        if len(self.strategy_registry) <= 1:

            if not self.strategy_registry:
                return None

            return list(self.strategy_registry.values())[0]

        # -------------------------------------------------
        # Multi-strategy selection (simple placeholder logic)
        # -------------------------------------------------

        if market_context is None:
            return list(self.strategy_registry.values())[0]

        market_state = market_context.get("market_state", "neutral")

        # simple rule example
        if market_state == "trend" and "trend_strategy" in self.strategy_registry:
            return self.strategy_registry["trend_strategy"]

        if market_state == "range" and "mean_reversion_strategy" in self.strategy_registry:
            return self.strategy_registry["mean_reversion_strategy"]

        # fallback
        return list(self.strategy_registry.values())[0]

    # -------------------------------------------------
    # Status
    # -------------------------------------------------

    def status(self):

        return {
            "strategies_registered": list(self.strategy_registry.keys()),
            "multi_strategy_active": len(self.strategy_registry) > 1
        }

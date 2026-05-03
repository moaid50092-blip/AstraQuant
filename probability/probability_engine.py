# probability/probability_engine.py

class ProbabilityEngine:

    def __init__(self):
        # 🔥 weights خفيفة (ما تكسر النظام)
        self.weights = {
            "structure": 0.15,
            "liquidity": 0.10,
            "session": 0.05,
            "context": 0.10,
            "mtf": 0.15,
            "factor": 0.10,
            "historical": 0.10,
            "volatility": 0.10
        }

    # -------------------------------------------------
    def evaluate(self, signal):

        edge = signal.get("base_score", 0.5)

        # 🔥 additive بدل multiplicative
        edge += (signal.get("structure_score", 0.5) - 0.5) * self.weights["structure"]
        edge += (signal.get("liquidity_score", 0.5) - 0.5) * self.weights["liquidity"]
        edge += (signal.get("session_score", 0.5) - 0.5) * self.weights["session"]
        edge += (signal.get("context_score", 0.5) - 0.5) * self.weights["context"]
        edge += (signal.get("mtf_score", 0.5) - 0.5) * self.weights["mtf"]
        edge += (signal.get("factor_score", 0.5) - 0.5) * self.weights["factor"]
        edge += (signal.get("historical_score", 0.5) - 0.5) * self.weights["historical"]
        edge += (signal.get("volatility_score", 0.5) - 0.5) * self.weights["volatility"]

        # 🔥 Early boost (خفيف جدًا)
        if signal.get("early_entry"):
            edge += 0.05

        return self._normalize(edge)

    # -------------------------------------------------
    def _normalize(self, value):

        if value < 0:
            return 0
        if value > 1:
            return 1

        return round(value, 3)

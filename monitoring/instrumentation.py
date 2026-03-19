# monitoring/instrumentation.py

class Instrumentation:

    def __init__(self):
        self.reset()

    # -------------------------------------------------
    # Reset Metrics
    # -------------------------------------------------

    def reset(self):
        self.metrics = {
            "scanner": 0,
            "strategy": 0,
            "probability": 0,
            "execution": 0
        }

    # -------------------------------------------------
    # Update Stage Count
    # -------------------------------------------------

    def update(self, stage, count):

        if stage in self.metrics:
            self.metrics[stage] = count

    # -------------------------------------------------
    # Compute Ratios
    # -------------------------------------------------

    def compute_ratios(self):

        scanner = self.metrics["scanner"]
        strategy = self.metrics["strategy"]
        probability = self.metrics["probability"]
        execution = self.metrics["execution"]

        return {
            "scan_to_strategy": self._safe_div(strategy, scanner),
            "strategy_to_probability": self._safe_div(probability, strategy),
            "probability_to_execution": self._safe_div(execution, probability)
        }

    # -------------------------------------------------
    # Safe Division
    # -------------------------------------------------

    def _safe_div(self, a, b):
        if b == 0:
            return 0
        return round(a / b, 3)

    # -------------------------------------------------
    # Report Output
    # -------------------------------------------------

    def report(self):

        ratios = self.compute_ratios()

        print("\n=== AstraQuant Instrumentation ===")
        print(f"Scanner Signals: {self.metrics['scanner']}")
        print(f"Strategy Signals: {self.metrics['strategy']}")
        print(f"Probability Signals: {self.metrics['probability']}")
        print(f"Executed Trades: {self.metrics['execution']}")

        print("\n--- Conversion Rates ---")
        print(f"Scan → Strategy: {ratios['scan_to_strategy']}")
        print(f"Strategy → Probability: {ratios['strategy_to_probability']}")
        print(f"Probability → Execution: {ratios['probability_to_execution']}")
        print("=================================\n")

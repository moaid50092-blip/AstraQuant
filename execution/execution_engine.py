# execution/execution_engine.py

"""
Execution Engine

Responsible for executing confirmed trades.

In the reference architecture this engine performs
a simulated execution (paper execution) and logs
all trades. The module is intentionally isolated so
that it can later be connected to a real exchange
connector without modifying the rest of the system.

Responsibilities:

• Receive confirmed trades
• Simulate execution
• Log execution events
• Maintain simple execution history
"""

from utils.logger import Logger
import datetime


class ExecutionEngine:

    def __init__(self):

        self.logger = Logger()

        # in-memory execution history
        self.execution_history = []

    # -------------------------------------------------
    # Execute Trades
    # -------------------------------------------------

    def execute(self, trades):

        """
        trades format:

        [
            {
                "symbol": "BTC",
                "probability_score": 0.82,
                "position_size": 0.5
            }
        ]
        """

        if not trades:
            return

        for trade in trades:

            execution_report = self._execute_trade(trade)

            self.execution_history.append(execution_report)

            self.logger.info(
                f"Executed trade: {execution_report}"
            )

    # -------------------------------------------------
    # Simulated Execution
    # -------------------------------------------------

    def _execute_trade(self, trade):

        symbol = trade.get("symbol")

        probability = trade.get("probability_score", 0.0)

        position_size = trade.get("position_size", 0.0)

        timestamp = datetime.datetime.utcnow().isoformat()

        execution_report = {
            "symbol": symbol,
            "probability": probability,
            "position_size": position_size,
            "timestamp": timestamp,
            "status": "executed"
        }

        return execution_report

    # -------------------------------------------------
    # Get Execution History
    # -------------------------------------------------

    def get_history(self):

        return self.execution_history

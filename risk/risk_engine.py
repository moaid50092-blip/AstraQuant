# risk/risk_engine.py

"""
Risk Engine

Provides portfolio-level risk protection without
interfering with trading logic.

Responsibilities:

• Maximum drawdown protection
• Daily loss limits
• Portfolio exposure monitoring
• Risk budgeting

Important:
This engine does NOT reject trades using hard filters.
Instead it returns risk modifiers that can reduce
position sizes when risk levels increase.
"""

import datetime


class RiskEngine:

    def __init__(
        self,
        max_drawdown=0.20,
        daily_loss_limit=0.05,
        base_capital=100000
    ):

        self.max_drawdown = max_drawdown
        self.daily_loss_limit = daily_loss_limit

        self.base_capital = base_capital
        self.current_equity = base_capital

        self.peak_equity = base_capital

        self.daily_pnl = 0
        self.last_day = datetime.date.today()

    # -------------------------------------------------
    # Register Trade Result
    # -------------------------------------------------

    def register_trade(self, pnl):

        """
        pnl: profit or loss of the trade in capital units
        """

        today = datetime.date.today()

        if today != self.last_day:
            self.daily_pnl = 0
            self.last_day = today

        self.daily_pnl += pnl

        self.current_equity += pnl

        if self.current_equity > self.peak_equity:
            self.peak_equity = self.current_equity

    # -------------------------------------------------
    # Drawdown Calculation
    # -------------------------------------------------

    def drawdown(self):

        return (self.peak_equity - self.current_equity) / self.peak_equity

    # -------------------------------------------------
    # Daily Loss
    # -------------------------------------------------

    def daily_loss(self):

        return abs(self.daily_pnl) / self.base_capital

    # -------------------------------------------------
    # Risk Modifier
    # -------------------------------------------------

    def risk_modifier(self):

        """
        Returns a multiplier for position sizes.
        """

        modifier = 1.0

        # drawdown protection
        dd = self.drawdown()

        if dd > self.max_drawdown * 0.5:
            modifier *= 0.7

        if dd > self.max_drawdown * 0.8:
            modifier *= 0.5

        # daily loss protection
        daily = self.daily_loss()

        if daily > self.daily_loss_limit * 0.5:
            modifier *= 0.7

        if daily > self.daily_loss_limit:
            modifier *= 0.4

        return modifier

    # -------------------------------------------------
    # Status
    # -------------------------------------------------

    def status(self):

        return {

            "equity": self.current_equity,
            "peak_equity": self.peak_equity,
            "drawdown": self.drawdown(),
            "daily_loss": self.daily_loss(),
            "risk_modifier": self.risk_modifier()

      }

# trade_lifecycle/trade_manager.py

from trade_lifecycle.trade_object import (
    TradeObject
)

from trade_lifecycle.lifecycle_profiles import (
    get_lifecycle_profile
)


class TradeManager:

    """
    Passive lifecycle orchestration layer.

    Responsibilities:
    - Track active trades
    - Route lifecycle evaluation
    - Maintain trade continuity
    - Coordinate lifecycle progression

    Important:
    - This layer is NOT a behavioral interpreter
    - This layer is NOT a market intelligence engine
    - This layer should remain execution-oriented
    - Behavioral semantics must remain external
    """

    # ==================================================
    # 🔥 INIT
    # ==================================================

    def __init__(self):

        # symbol -> TradeObject
        self.active_trades = {}

    # ==================================================
    # 🔥 UPDATE CYCLE
    # ==================================================

    def process_signals(
        self,
        signals
    ):

        lifecycle_events = []

        processed_symbols = set()

        # ==============================================
        # 🔥 PROCESS CURRENT SIGNALS
        # ==============================================

        for signal in signals:

            symbol = signal.get("symbol")

            if not symbol:
                continue

            processed_symbols.add(symbol)

            decision = signal.get(
                "decision",
                "IGNORE"
            )

            # ==========================================
            # 🔥 CREATE TRADE
            # ==========================================

            if (
                decision == "ENTER"
                and symbol not in self.active_trades
            ):

                trade = TradeObject(signal)

                self.active_trades[symbol] = trade

                lifecycle_events.append({

                    "type":
                        "TRADE_CREATED",

                    "symbol":
                        symbol,

                    "trade_type":
                        trade.trade_type,

                    "direction":
                        trade.direction,

                    "entry_type":
                        trade.entry_type,

                    "probability":
                        round(
                            trade.current_probability,
                            3
                        )
                })

            # ==========================================
            # 🔥 UPDATE EXISTING
            # ==========================================

            if symbol in self.active_trades:

                trade = self.active_trades[symbol]

                self._update_trade(
                    trade,
                    signal,
                    lifecycle_events
                )

        # ==============================================
        # 🔥 HANDLE MISSING SYMBOLS
        # ==============================================

        self._handle_missing_symbols(
            processed_symbols,
            lifecycle_events
        )

        return lifecycle_events

    # ==================================================
    # 🔥 UPDATE TRADE
    # ==================================================

    def _update_trade(
        self,
        trade,
        signal,
        lifecycle_events
    ):

        previous_state = trade.state

        # ==============================================
        # 🔥 UPDATE INTERNAL STATE
        # ==============================================

        trade.update(signal)

        # ==============================================
        # 🔥 PROFILE
        # ==============================================

        profile = get_lifecycle_profile(
            trade.trade_type
        )

        # ==============================================
        # 🔥 EXIT WATCH
        # ==============================================

        self._handle_exit_watch(
            trade,
            profile,
            lifecycle_events
        )

        # ==============================================
        # 🔥 EXIT CONFIRMATION
        # ==============================================

        self._handle_exit_confirmation(
            trade,
            profile,
            lifecycle_events
        )

        # ==============================================
        # 🔥 RECOVERY
        # ==============================================

        self._handle_recovery_transition(
            trade,
            previous_state,
            lifecycle_events
        )

    # ==================================================
    # 🔥 EXIT WATCH
    # ==================================================

    def _handle_exit_watch(
        self,
        trade,
        profile,
        lifecycle_events
    ):

        """
        Runtime execution coordination only.

        Important:
        - NOT behavioral interpretation
        - NOT collapse detection
        - NOT entropy analysis
        - NOT continuity intelligence
        """

        should_watch = (
            profile.should_start_exit_watch(
                trade
            )
        )

        if not should_watch:
            return

        if trade.exit_pending:
            return

        trade.exit_pending = True

        lifecycle_events.append({

            "type":
                "EXIT_WATCH",

            "symbol":
                trade.symbol,

            "trade_type":
                trade.trade_type,

            "probability":
                round(
                    trade.current_probability,
                    3
                ),

            "continuity_pressure":
                round(
                    trade.deterioration_score,
                    3
                ),

            "weak_cycles":
                trade.consecutive_weak_cycles
        })

    # ==================================================
    # 🔥 EXIT CONFIRMATION
    # ==================================================

    def _handle_exit_confirmation(
        self,
        trade,
        profile,
        lifecycle_events
    ):

        """
        Execution lifecycle confirmation layer.

        Important:
        - Confirmation logic remains heuristic
        - Does NOT represent behavioral truth
        - Does NOT imply real structural collapse
        """

        should_exit = (
            profile.should_confirm_exit(
                trade
            )
        )

        if not should_exit:
            return

        if trade.exit_confirmed:
            return

        trade.exit_confirmed = True

        trade.state = "EXIT"

        lifecycle_events.append({

            "type":
                "EXIT_CONFIRMED",

            "symbol":
                trade.symbol,

            "trade_type":
                trade.trade_type,

            "direction":
                trade.direction,

            "held_cycles":
                trade.cycles_alive,

            "peak_probability":
                round(
                    trade.highest_probability,
                    3
                ),

            "final_probability":
                round(
                    trade.current_probability,
                    3
                ),

            "reason":
                trade.exit_reason
                or "lifecycle_exit"
        })

    # ==================================================
    # 🔥 RECOVERY TRANSITION
    # ==================================================

    def _handle_recovery_transition(
        self,
        trade,
        previous_state,
        lifecycle_events
    ):

        """
        Runtime lifecycle recovery tracking.

        Important:
        - Recovery here means:
          lifecycle stabilization only

        - NOT:
          market recovery truth
          structural restoration
          continuity certainty
        """

        if previous_state != "ACTIVE":
            return

        if not trade.exit_pending:
            return

        if trade.exit_confirmed:
            return

        if (
            trade.consecutive_recovery_cycles
            < 2
        ):

            return

        trade.exit_pending = False

        lifecycle_events.append({

            "type":
                "TRADE_RECOVERED",

            "symbol":
                trade.symbol,

            "trade_type":
                trade.trade_type,

            "probability":
                round(
                    trade.current_probability,
                    3
                )
        })

    # ==================================================
    # 🔥 MISSING SYMBOLS
    # ==================================================

    def _handle_missing_symbols(
        self,
        processed_symbols,
        lifecycle_events
    ):

        """
        Missing symbol handling.

        Important:
        Symbol disappearance currently represents:
        continuity visibility loss

        NOT:
        guaranteed collapse
        guaranteed entropy
        guaranteed invalidation
        """

        for (
            symbol,
            trade
        ) in list(
            self.active_trades.items()
        ):

            if symbol in processed_symbols:
                continue

            # ==========================================
            # 🔥 SOFT CONTINUITY PRESSURE
            # ==========================================

            """
            NOTE:
            This remains heuristic lifecycle pressure,
            NOT behavioral collapse detection.
            """

            trade.consecutive_weak_cycles += 1

            trade.deterioration_score += 0.01

            # ==========================================
            # 🔥 PROFILE CHECK
            # ==========================================

            profile = get_lifecycle_profile(
                trade.trade_type
            )

            should_exit = (
                profile.should_confirm_exit(
                    trade
                )
            )

            if not should_exit:
                continue

            trade.exit_confirmed = True

            trade.state = "EXIT"

            lifecycle_events.append({

                "type":
                    "EXIT_CONFIRMED",

                "symbol":
                    trade.symbol,

                "trade_type":
                    trade.trade_type,

                "direction":
                    trade.direction,

                "held_cycles":
                    trade.cycles_alive,

                "peak_probability":
                    round(
                        trade.highest_probability,
                        3
                    ),

                "final_probability":
                    round(
                        trade.current_probability,
                        3
                    ),

                "reason":
                    "signal_visibility_lost"
            })

    # ==================================================
    # 🔥 CLEANUP
    # ==================================================

    def cleanup_closed_trades(self):

        removable = []

        for (
            symbol,
            trade
        ) in self.active_trades.items():

            if trade.exit_confirmed:

                removable.append(symbol)

        for symbol in removable:

            del self.active_trades[symbol]

    # ==================================================
    # 🔥 EXPORT
    # ==================================================

    def export_active_trades(self):

        result = []

        for trade in (
            self.active_trades.values()
        ):

            result.append(
                trade.export_state()
            )

        return result

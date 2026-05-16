# trade_lifecycle/trade_manager.py

from trade_lifecycle.trade_object import (
    TradeObject
)

from trade_lifecycle.lifecycle_profiles import (
    get_lifecycle_profile
)


class TradeManager:

    """
    Passive execution lifecycle orchestration layer.

    Responsibilities:
    - Track active trades
    - Route lifecycle evaluation
    - Maintain lifecycle continuity
    - Coordinate execution state progression
    - Preserve runtime lifecycle integrity

    Important:
    - This layer is NOT a behavioral interpreter
    - This layer is NOT a market intelligence engine
    - This layer is NOT a semantic classifier
    - This layer is NOT a predictive continuity layer
    - Behavioral interpretation must remain external

    Architectural Boundary:
    This layer MUST remain:
    - execution-oriented
    - lifecycle-coordinated
    - runtime deterministic
    - observer-neutral

    This layer MUST NOT evolve into:
    - behavioral continuity engine
    - adaptive execution layer
    - semantic predictor
    - market intelligence component
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

        previous_exit_confirmed = (
            trade.exit_confirmed
        )

        # ==============================================
        # 🔥 UPDATE INTERNAL STATE
        # ==============================================

        trade.update(signal)

        # ==============================================
        # 🔥 PROFILE
        # ==============================================

        """
        Lifecycle profiles remain execution heuristics.

        Important:
        - NOT behavioral intelligence
        - NOT continuity truth
        - NOT market structure interpretation
        """

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
            lifecycle_events,
            previous_exit_confirmed
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

        This layer tracks execution-oriented
        lifecycle pressure heuristics only.
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

            # ==========================================
            # Heuristic runtime visibility only
            # NOT behavioral truth
            # ==========================================

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
        lifecycle_events,
        previous_exit_confirmed
    ):

        """
        Execution lifecycle confirmation layer.

        Important:
        - Confirmation logic remains heuristic
        - Does NOT represent behavioral truth
        - Does NOT imply structural collapse
        - Does NOT imply continuity invalidation

        This remains runtime execution coordination only.
        """

        if (
            trade.exit_confirmed
            and not previous_exit_confirmed
        ):

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

            return

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
        Runtime lifecycle stabilization tracking.

        Important:
        - Recovery here means:
          lifecycle stabilization only

        - NOT:
          market recovery truth
          structural restoration
          continuity certainty
          predictive stabilization
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
    # 🔥 LIFECYCLE VISIBILITY LOSS
    # ==================================================

    def _apply_visibility_loss_pressure(
        self,
        trade
    ):

        """
        Runtime continuity visibility degradation.

        Important:
        Missing visibility currently represents:
        temporary lifecycle visibility loss only.

        This does NOT imply:
        - structural invalidation
        - continuity collapse
        - entropy dominance
        - behavioral decay

        This method exists to preserve:
        - lifecycle ownership isolation
        - mutation boundaries
        - runtime determinism
        """

        trade.consecutive_weak_cycles += 1

        trade.deterioration_score += 0.01

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
        continuity visibility loss only.

        NOT:
        guaranteed collapse
        guaranteed entropy
        guaranteed invalidation
        guaranteed structural failure
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
            # 🔥 SOFT VISIBILITY PRESSURE
            # ==========================================

            self._apply_visibility_loss_pressure(
                trade
            )

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

            if trade.exit_confirmed:
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
    # 🔥 EXPORT HELPERS
    # ==================================================

    def _export_trade_state(
        self,
        trade
    ):

        """
        Export isolation boundary.

        Important:
        Exported lifecycle state must remain:
        - observer-safe
        - execution-isolated
        - non-authoritative
        - non-semantic

        Observer layers MUST NOT feed
        exported state back into lifecycle decisions.
        """

        return trade.export_state()

    # ==================================================
    # 🔥 EXPORT
    # ==================================================

    def export_active_trades(self):

        result = []

        for symbol in sorted(
            self.active_trades.keys()
        ):

            trade = self.active_trades[symbol]

            result.append(
                self._export_trade_state(
                    trade
                )
            )

        return result

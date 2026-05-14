# trade_lifecycle/trade_object.py

import time

from observability.trace_sink import (
    append_trace
)


class TradeObject:

    """
    Pure lifecycle state container.

    Responsibilities:
    - Track active trade continuity
    - Persist conviction state
    - Track deterioration progression
    - Handle lifecycle transitions
    - Remain fully isolated from:
        - scanner logic
        - market prediction
        - execution authority
        - portfolio awareness

    Important:
    - This object stores raw lifecycle continuity
    - NOT behavioral intelligence
    - NOT predictive semantics
    - NOT adaptive logic
    """

    # ==================================================
    # 🔥 INIT
    # ==================================================

    def __init__(self, signal):

        self.trade_id = (
            f"{signal.get('symbol', 'UNKNOWN')}_"
            f"{int(time.time())}"
        )

        self.symbol = signal.get("symbol")

        self.direction = signal.get("direction")

        self.entry_type = signal.get(
            "entry_type",
            "STANDARD"
        )

        self.trade_type = self._detect_trade_type(
            signal
        )

        # ==========================================
        # 🔥 INITIAL STATE
        # ==========================================

        self.state = "ACTIVE"

        self.created_at = time.time()

        self.last_update = time.time()

        self.cycles_alive = 0

        # ==========================================
        # 🔥 CONTINUATION MATURITY
        # ==========================================

        """
        NOTE:
        This remains for runtime compatibility only.

        It is currently a lifecycle heuristic,
        NOT a behavioral truth descriptor.
        """

        self.continuation_mature = False

        # ==========================================
        # 🔥 CONVICTION
        # ==========================================

        self.initial_probability = float(
            signal.get("probability", 0.5)
        )

        self.current_probability = (
            self.initial_probability
        )

        self.highest_probability = (
            self.initial_probability
        )

        self.lowest_probability = (
            self.initial_probability
        )

        # ==========================================
        # 🔥 DETERIORATION
        # ==========================================

        """
        NOTE:
        deterioration_score currently represents
        continuity pressure accumulation.

        It does NOT necessarily imply:
        collapse
        failure
        entropy takeover
        """

        self.deterioration_score = 0.0

        self.warning_count = 0

        self.recovery_count = 0

        self.consecutive_weak_cycles = 0

        self.consecutive_recovery_cycles = 0

        # ==========================================
        # 🔥 RAW CONTINUITY STREAM
        # ==========================================

        """
        Raw continuity preservation layer.

        Important:
        - sequence-first
        - non-semantic
        - non-predictive
        - no execution authority
        """

        self.continuity_sequence = []

        # ==========================================
        # 🔥 STRUCTURE
        # ==========================================

        self.last_trend = signal.get(
            "trend",
            "unknown"
        )

        self.last_setup = signal.get(
            "setup",
            "unknown"
        )

        self.last_confidence = signal.get(
            "confidence_label",
            "LOW"
        )

        self.last_reason = (
            signal.get("reasons", [])
        )

        # ==========================================
        # 🔥 EXIT STATE
        # ==========================================

        self.exit_pending = False

        self.exit_confirmed = False

        self.exit_reason = None

        self.exit_cycle = None

        # ==========================================
        # 🔥 SNAPSHOT
        # ==========================================

        self.history = []

        # ==========================================
        # 🔥 BEHAVIORAL OBSERVABILITY
        # ==========================================

        """
        Passive semantic trace storage.

        Important:
        - Read-only
        - No execution authority
        - No lifecycle mutation
        - No adaptive behavior
        """

        self.behavioral_trace = []

        self._store_snapshot(signal)

        self._store_behavioral_trace()

    # ==================================================
    # 🔥 TYPE DETECTION
    # ==================================================

    def _detect_trade_type(self, signal):

        if signal.get("range_active"):
            return "RANGE"

        return "TREND"

    # ==================================================
    # 🔥 SNAPSHOT STORAGE
    # ==================================================

    def _store_snapshot(self, signal):

        snapshot = {

            "timestamp":
                time.time(),

            "probability":
                round(
                    float(
                        signal.get(
                            "probability",
                            0
                        )
                    ),
                    3
                ),

            "strength":
                round(
                    float(
                        signal.get(
                            "strength",
                            0
                        )
                    ),
                    3
                ),

            "trend":
                signal.get(
                    "trend",
                    "unknown"
                ),

            "setup":
                signal.get(
                    "setup",
                    "unknown"
                ),

            "confidence":
                signal.get(
                    "confidence_label",
                    "LOW"
                ),

            "decision":
                signal.get(
                    "decision",
                    "IGNORE"
                )
        }

        self.history.append(snapshot)

        self.history = self.history[-25:]

    # ==================================================
    # 🔥 RAW CONTINUITY STORAGE
    # ==================================================

    def _store_continuity_transition(
        self,
        probability_delta
    ):

        if probability_delta > 0.015:

            transition = "UP"

        elif probability_delta < -0.015:

            transition = "DOWN"

        else:

            transition = "STABLE"

        continuity_event = {

            "timestamp":
                time.time(),

            "cycle":
                self.cycles_alive,

            "transition":
                transition,

            "probability_delta":
                round(
                    probability_delta,
                    4
                ),

            "current_probability":
                round(
                    self.current_probability,
                    3
                )
        }

        self.continuity_sequence.append(
            continuity_event
        )

        # prevent uncontrolled growth
        self.continuity_sequence = (
            self.continuity_sequence[-50:]
        )

    # ==================================================
    # 🔥 BEHAVIORAL TRACE
    # ==================================================

    def _store_behavioral_trace(self):

        current_timestamp = time.time()

        trace = {

            "timestamp":
                current_timestamp,

            "datetime":
                time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.gmtime(current_timestamp)
                ),

            "trade_id":
                self.trade_id,

            "symbol":
                self.symbol,

            "direction":
                self.direction,

            "state":
                self.state,

            "trade_type":
                self.trade_type,

            "cycles_alive":
                self.cycles_alive,

            "continuation_mature":
                self.continuation_mature,

            "current_probability":
                round(
                    self.current_probability,
                    3
                ),

            "deterioration_score":
                round(
                    self.deterioration_score,
                    3
                ),

            "weak_cycles":
                self.consecutive_weak_cycles,

            "recovery_cycles":
                self.consecutive_recovery_cycles,

            "exit_pending":
                self.exit_pending,

            "exit_confirmed":
                self.exit_confirmed,

            "exit_reason":
                self.exit_reason
        }

        self.behavioral_trace.append(trace)

        # ==========================================
        # 🔥 PASSIVE TRACE PERSISTENCE
        # ==========================================

        append_trace(trace)

        # prevent uncontrolled growth
        self.behavioral_trace = (
            self.behavioral_trace[-50:]
        )

    # ==================================================
    # 🔥 UPDATE STATE
    # ==================================================

    def update(self, signal):

        self.last_update = time.time()

        self.cycles_alive += 1

        new_probability = float(
            signal.get("probability", 0.5)
        )

        previous_probability = (
            self.current_probability
        )

        self.current_probability = (
            new_probability
        )

        self.highest_probability = max(
            self.highest_probability,
            new_probability
        )

        self.lowest_probability = min(
            self.lowest_probability,
            new_probability
        )

        # ==========================================
        # 🔥 RAW CONTINUITY DELTA
        # ==========================================

        delta = (
            new_probability
            - previous_probability
        )

        self._store_continuity_transition(
            delta
        )

        # ==========================================
        # 🔥 DETERIORATION TRACKING
        # ==========================================

        if delta < -0.015:

            self.consecutive_weak_cycles += 1

            self.consecutive_recovery_cycles = 0

            self.warning_count += 1

            self.deterioration_score += abs(
                delta
            )

        elif delta > 0.015:

            self.consecutive_recovery_cycles += 1

            self.consecutive_weak_cycles = 0

            self.recovery_count += 1

            self.deterioration_score *= 0.8

        else:

            self.deterioration_score *= 0.97

        # ==========================================
        # 🔥 CONTINUATION MATURITY
        # ==========================================

        if (
            self.trade_type == "TREND"
            and self.cycles_alive >= 4
            and self.consecutive_recovery_cycles >= 2
            and self.current_probability
                >= self.initial_probability
        ):

            self.continuation_mature = True

        # ==========================================
        # 🔥 STRUCTURE UPDATE
        # ==========================================

        self.last_trend = signal.get(
            "trend",
            self.last_trend
        )

        self.last_setup = signal.get(
            "setup",
            self.last_setup
        )

        self.last_confidence = signal.get(
            "confidence_label",
            self.last_confidence
        )

        self.last_reason = signal.get(
            "reasons",
            self.last_reason
        )

        # ==========================================
        # 🔥 EXIT WATCH
        # ==========================================

        self._evaluate_exit_watch(signal)

        # ==========================================
        # 🔥 STORE SNAPSHOT
        # ==========================================

        self._store_snapshot(signal)

        # ==========================================
        # 🔥 STORE OBSERVABILITY TRACE
        # ==========================================

        self._store_behavioral_trace()

    # ==================================================
    # 🔥 EXIT WATCH
    # ==================================================

    def _evaluate_exit_watch(self, signal):

        """
        Runtime compatibility layer.

        Important:
        This remains execution-oriented logic
        and should eventually migrate outside
        raw lifecycle continuity storage.
        """

        decision = signal.get(
            "decision",
            "IGNORE"
        )

        setup = signal.get(
            "setup",
            "unknown"
        )

        confidence = signal.get(
            "confidence_label",
            "LOW"
        )

        if (
            decision == "IGNORE"
            or setup == "fake"
            or confidence == "LOW"
        ):

            self.exit_pending = True

        else:

            self.exit_pending = False

        if (
            self.exit_pending
            and self.consecutive_weak_cycles >= 2
        ):

            self.exit_confirmed = True

            self.state = "EXIT"

            self.exit_cycle = self.cycles_alive

            self.exit_reason = (
                "deterioration_confirmed"
            )

    # ==================================================
    # 🔥 STATUS
    # ==================================================

    def is_active(self):

        return (
            self.state == "ACTIVE"
            and not self.exit_confirmed
        )

    # ==================================================
    # 🔥 EXPORT
    # ==================================================

    def export_state(self):

        return {

            # ======================================
            # 🔥 IDENTITY
            # ======================================

            "trade_id":
                self.trade_id,

            "symbol":
                self.symbol,

            "direction":
                self.direction,

            "trade_type":
                self.trade_type,

            "entry_type":
                self.entry_type,

            # ======================================
            # 🔥 LIFECYCLE STATE
            # ======================================

            "state":
                self.state,

            "cycles_alive":
                self.cycles_alive,

            "created_at":
                self.created_at,

            "last_update":
                self.last_update,

            # ======================================
            # 🔥 RAW CONTINUITY PRIMITIVES
            # ======================================

            "continuity_primitives": {

                "initial_probability":
                    round(
                        self.initial_probability,
                        3
                    ),

                "current_probability":
                    round(
                        self.current_probability,
                        3
                    ),

                "highest_probability":
                    round(
                        self.highest_probability,
                        3
                    ),

                "lowest_probability":
                    round(
                        self.lowest_probability,
                        3
                    ),

                "deterioration_score":
                    round(
                        self.deterioration_score,
                        3
                    ),

                "warning_count":
                    self.warning_count,

                "recovery_count":
                    self.recovery_count,

                "weak_cycles":
                    self.consecutive_weak_cycles,

                "recovery_cycles":
                    self.consecutive_recovery_cycles,

                "continuity_sequence":
                    self.continuity_sequence
            },

            # ======================================
            # 🔥 STRUCTURE MEMORY
            # ======================================

            "structure_memory": {

                "trend":
                    self.last_trend,

                "setup":
                    self.last_setup,

                "confidence":
                    self.last_confidence,

                "reasons":
                    self.last_reason
            },

            # ======================================
            # 🔥 EXECUTION STATE
            # ======================================

            "execution_state": {

                "exit_pending":
                    self.exit_pending,

                "exit_confirmed":
                    self.exit_confirmed,

                "exit_reason":
                    self.exit_reason,

                "continuation_mature":
                    self.continuation_mature
            },

            # ======================================
            # 🔥 LEGACY COMPATIBILITY
            # ======================================

            """
            Preserved temporarily
            for runtime compatibility.
            """

            "continuation_mature":
                self.continuation_mature,

            "initial_probability":
                round(
                    self.initial_probability,
                    3
                ),

            "current_probability":
                round(
                    self.current_probability,
                    3
                ),

            "highest_probability":
                round(
                    self.highest_probability,
                    3
                ),

            "lowest_probability":
                round(
                    self.lowest_probability,
                    3
                ),

            "deterioration_score":
                round(
                    self.deterioration_score,
                    3
                ),

            "warning_count":
                self.warning_count,

            "recovery_count":
                self.recovery_count,

            "weak_cycles":
                self.consecutive_weak_cycles,

            "recovery_cycles":
                self.consecutive_recovery_cycles,

            "trend":
                self.last_trend,

            "setup":
                self.last_setup,

            "confidence":
                self.last_confidence,

            "reasons":
                self.last_reason,

            "exit_pending":
                self.exit_pending,

            "exit_confirmed":
                self.exit_confirmed,

            "exit_reason":
                self.exit_reason
        }

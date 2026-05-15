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

    Architectural Boundary:
    This object MUST remain:
    - execution-oriented
    - continuity-preserving
    - sequence-aware
    - behaviorally neutral

    This object MUST NOT evolve into:
    - semantic interpreter
    - behavioral predictor
    - adaptive continuity engine
    - execution optimizer
    """

    # ==================================================
    # 🔥 INIT
    # ==================================================

    def __init__(self, signal):

        init_timestamp = time.time()

        self.trade_id = (
            f"{signal.get('symbol', 'UNKNOWN')}_"
            f"{int(init_timestamp)}"
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

        self.created_at = init_timestamp

        self.last_update = init_timestamp

        self.cycles_alive = 0

        # ==========================================
        # 🔥 CONTINUATION MATURITY
        # ==========================================

        """
        NOTE:
        Preserved for runtime compatibility only.

        This is currently a lifecycle heuristic,
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

        It does NOT imply:
        - collapse certainty
        - structural failure
        - market truth
        - behavioral certainty

        This remains a raw lifecycle heuristic.
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
        - topology-preserving
        - non-semantic
        - non-predictive
        - no execution authority
        """

        self.continuity_sequence = []

        # ==========================================
        # 🔥 STRUCTURE MEMORY
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

        self.last_reason = list(
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
        Passive observability trace storage.

        Important:
        - Read-only
        - No execution authority
        - No lifecycle mutation
        - No adaptive behavior
        - No observer influence on execution
        """

        self.behavioral_trace = []

        self._store_snapshot(
            signal,
            init_timestamp
        )

        self._store_behavioral_trace(
            init_timestamp
        )

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

    def _store_snapshot(
        self,
        signal,
        timestamp
    ):

        snapshot = {

            "timestamp":
                timestamp,

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

        # prevent uncontrolled growth
        self.history = self.history[-25:]

    # ==================================================
    # 🔥 RAW CONTINUITY STORAGE
    # ==================================================

    def _store_continuity_transition(
        self,
        probability_delta,
        previous_probability,
        timestamp
    ):

        if probability_delta > 0.015:

            transition = "UP"

        elif probability_delta < -0.015:

            transition = "DOWN"

        else:

            transition = "STABLE"

        continuity_event = {

            "timestamp":
                timestamp,

            "cycle":
                self.cycles_alive,

            "transition":
                transition,

            "previous_probability":
                round(
                    previous_probability,
                    3
                ),

            "current_probability":
                round(
                    self.current_probability,
                    3
                ),

            "probability_delta":
                round(
                    probability_delta,
                    4
                ),

            "delta_magnitude":
                round(
                    abs(probability_delta),
                    4
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

    def _store_behavioral_trace(
        self,
        timestamp
    ):

        trace = {

            "timestamp":
                timestamp,

            "datetime":
                time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.gmtime(timestamp)
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

        self.behavioral_trace.append(
            trace
        )

        # ==========================================
        # 🔥 PASSIVE TRACE PERSISTENCE
        # ==========================================

        append_trace(dict(trace))

        # prevent uncontrolled growth
        self.behavioral_trace = (
            self.behavioral_trace[-50:]
        )

    # ==================================================
    # 🔥 UPDATE STATE
    # ==================================================

    def update(self, signal):

        cycle_timestamp = time.time()

        self.last_update = cycle_timestamp

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
            probability_delta=delta,
            previous_probability=previous_probability,
            timestamp=cycle_timestamp
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

        self.last_reason = list(
            signal.get(
                "reasons",
                self.last_reason
            )
        )

        # ==========================================
        # 🔥 EXIT WATCH
        # ==========================================

        self._evaluate_exit_watch(signal)

        # ==========================================
        # 🔥 STORE SNAPSHOT
        # ==========================================

        self._store_snapshot(
            signal,
            cycle_timestamp
        )

        # ==========================================
        # 🔥 STORE OBSERVABILITY TRACE
        # ==========================================

        self._store_behavioral_trace(
            cycle_timestamp
        )

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

        This logic MUST NOT be interpreted as:
        - market truth
        - predictive intelligence
        - behavioral certainty
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
    # 🔥 EXPORT HELPERS
    # ==================================================

    def _export_continuity_sequence(self):

        return [
            dict(event)
            for event in self.continuity_sequence
        ]

    def _export_structure_memory(self):

        return {

            "trend":
                self.last_trend,

            "setup":
                self.last_setup,

            "confidence":
                self.last_confidence,

            "reasons":
                list(self.last_reason)
        }

    # ==================================================
    # 🔥 EXPORT
    # ==================================================

    def export_state(self):

        continuity_primitives = {

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
                self._export_continuity_sequence()
        }

        structure_memory = (
            self._export_structure_memory()
        )

        execution_state = {

            "exit_pending":
                self.exit_pending,

            "exit_confirmed":
                self.exit_confirmed,

            "exit_reason":
                self.exit_reason,

            "continuation_mature":
                self.continuation_mature
        }

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

            "continuity_primitives":
                continuity_primitives,

            # ======================================
            # 🔥 STRUCTURE MEMORY
            # ======================================

            "structure_memory":
                structure_memory,

            # ======================================
            # 🔥 EXECUTION STATE
            # ======================================

            "execution_state":
                execution_state,

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
                list(self.last_reason),

            "exit_pending":
                self.exit_pending,

            "exit_confirmed":
                self.exit_confirmed,

            "exit_reason":
                self.exit_reason
        }

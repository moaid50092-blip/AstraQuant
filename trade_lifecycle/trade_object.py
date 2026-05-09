# trade_lifecycle/trade_object.py

import time


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

        self.deterioration_score = 0.0

        self.warning_count = 0

        self.recovery_count = 0

        self.consecutive_weak_cycles = 0

        self.consecutive_recovery_cycles = 0

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

        self._store_snapshot(signal)

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
            "timestamp": time.time(),

            "probability": round(
                float(signal.get("probability", 0)),
                3
            ),

            "strength": round(
                float(signal.get("strength", 0)),
                3
            ),

            "trend": signal.get(
                "trend",
                "unknown"
            ),

            "setup": signal.get(
                "setup",
                "unknown"
            ),

            "confidence": signal.get(
                "confidence_label",
                "LOW"
            ),

            "decision": signal.get(
                "decision",
                "IGNORE"
            )
        }

        self.history.append(snapshot)

        # prevent uncontrolled growth
        self.history = self.history[-25:]

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
        # 🔥 DETERIORATION TRACKING
        # ==========================================

        delta = (
            new_probability
            - previous_probability
        )

        if delta < -0.015:

            self.consecutive_weak_cycles += 1

            self.consecutive_recovery_cycles = 0

            self.warning_count += 1

            self.deterioration_score += abs(delta)

        elif delta > 0.015:

            self.consecutive_recovery_cycles += 1

            self.consecutive_weak_cycles = 0

            self.recovery_count += 1

            self.deterioration_score *= 0.8

        else:

            self.deterioration_score *= 0.97

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

    # ==================================================
    # 🔥 EXIT WATCH
    # ==================================================

    def _evaluate_exit_watch(self, signal):

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

        # ==========================================
        # 🔥 EXIT WARNING
        # ==========================================

        if (
            decision == "IGNORE"
            or setup == "fake"
            or confidence == "LOW"
        ):

            self.exit_pending = True

        # ==========================================
        # 🔥 RECOVERY
        # ==========================================

        else:

            self.exit_pending = False

        # ==========================================
        # 🔥 EXIT CONFIRMATION
        # ==========================================

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
            # 🔥 CORE
            # ======================================

            "trade_id": self.trade_id,

            "symbol": self.symbol,

            "direction": self.direction,

            "trade_type": self.trade_type,

            "entry_type": self.entry_type,

            "state": self.state,

            # ======================================
            # 🔥 CONVICTION
            # ======================================

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

            # ======================================
            # 🔥 LIFECYCLE
            # ======================================

            "cycles_alive":
                self.cycles_alive,

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

            # ======================================
            # 🔥 STRUCTURE
            # ======================================

            "trend":
                self.last_trend,

            "setup":
                self.last_setup,

            "confidence":
                self.last_confidence,

            "reasons":
                self.last_reason,

            # ======================================
            # 🔥 EXIT
            # ======================================

            "exit_pending":
                self.exit_pending,

            "exit_confirmed":
                self.exit_confirmed,

            "exit_reason":
                self.exit_reason,

            # ======================================
            # 🔥 TIMING
            # ======================================

            "created_at":
                self.created_at,

            "last_update":
                self.last_update
        }

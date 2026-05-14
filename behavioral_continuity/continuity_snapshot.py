import time


class ContinuitySnapshot:

    """
    Passive behavioral continuity snapshot.

    Responsibilities:
    - Normalize lifecycle continuity state
    - Extract sequence-readable behavioral signals
    - Remain fully descriptive
    - Avoid ALL interpretation authority

    This layer does NOT:
    - generate scores
    - generate decisions
    - modify trades
    - predict outcomes
    - affect execution
    """

    # ==================================================
    # 🔥 INIT
    # ==================================================

    def __init__(self, trade):

        self.timestamp = time.time()

        self.trade_id = trade.trade_id

        self.symbol = trade.symbol

        self.direction = trade.direction

        self.trade_type = trade.trade_type

        self.state = trade.state

        # ==============================================
        # 🔥 CONTINUITY STATE
        # ==============================================

        self.cycles_alive = (
            trade.cycles_alive
        )

        self.continuation_mature = (
            trade.continuation_mature
        )

        # ==============================================
        # 🔥 PROBABILITY CONTINUITY
        # ==============================================

        self.initial_probability = (
            trade.initial_probability
        )

        self.current_probability = (
            trade.current_probability
        )

        self.highest_probability = (
            trade.highest_probability
        )

        self.lowest_probability = (
            trade.lowest_probability
        )

        self.probability_position = (
            self._compute_probability_position()
        )

        # ==============================================
        # 🔥 DETERIORATION CONTINUITY
        # ==============================================

        self.deterioration_score = (
            trade.deterioration_score
        )

        self.warning_count = (
            trade.warning_count
        )

        self.recovery_count = (
            trade.recovery_count
        )

        # ==============================================
        # 🔥 CONTINUITY MEMORY
        # ==============================================

        self.weak_cycles = (
            trade.consecutive_weak_cycles
        )

        self.recovery_cycles = (
            trade.consecutive_recovery_cycles
        )

        # ==============================================
        # 🔥 STRUCTURAL CONTINUITY
        # ==============================================

        self.last_trend = (
            trade.last_trend
        )

        self.last_setup = (
            trade.last_setup
        )

        self.last_confidence = (
            trade.last_confidence
        )

        # ==============================================
        # 🔥 EXIT PRESSURE
        # ==============================================

        self.exit_pending = (
            trade.exit_pending
        )

        self.exit_confirmed = (
            trade.exit_confirmed
        )

        self.exit_reason = (
            trade.exit_reason
        )

        # ==============================================
        # 🔥 DESCRIPTIVE SEMANTICS
        # ==============================================

        self.continuity_pressure = (
            self._compute_continuity_pressure()
        )

        self.directional_memory = (
            self._detect_directional_memory()
        )

        self.recovery_behavior = (
            self._detect_recovery_behavior()
        )

        self.weakness_behavior = (
            self._detect_weakness_behavior()
        )

        self.persistence_state = (
            self._detect_persistence_state()
        )

    # ==================================================
    # 🔥 PROBABILITY POSITION
    # ==================================================

    def _compute_probability_position(self):

        probability_range = (
            self.highest_probability
            - self.lowest_probability
        )

        if probability_range <= 0:
            return 0.5

        relative_position = (
            self.current_probability
            - self.lowest_probability
        ) / probability_range

        return round(
            max(0.0, min(1.0, relative_position)),
            3
        )

    # ==================================================
    # 🔥 CONTINUITY PRESSURE
    # ==================================================

    def _compute_continuity_pressure(self):

        pressure = 0.0

        pressure += (
            self.deterioration_score * 0.6
        )

        pressure += (
            self.weak_cycles * 0.15
        )

        if self.exit_pending:
            pressure += 0.2

        return round(
            max(0.0, min(1.0, pressure)),
            3
        )

    # ==================================================
    # 🔥 DIRECTIONAL MEMORY
    # ==================================================

    def _detect_directional_memory(self):

        if (
            self.current_probability
            >= self.initial_probability
        ):
            return "RETAINED"

        if (
            self.current_probability
            >= (
                self.initial_probability - 0.03
            )
        ):
            return "STRESSED"

        return "WEAKENING"

    # ==================================================
    # 🔥 RECOVERY BEHAVIOR
    # ==================================================

    def _detect_recovery_behavior(self):

        if self.recovery_cycles >= 2:
            return "SUSTAINED"

        if self.recovery_cycles == 1:
            return "ATTEMPTING"

        return "ABSENT"

    # ==================================================
    # 🔥 WEAKNESS BEHAVIOR
    # ==================================================

    def _detect_weakness_behavior(self):

        if self.weak_cycles >= 2:
            return "PERSISTENT"

        if self.weak_cycles == 1:
            return "EMERGING"

        return "STABLE"

    # ==================================================
    # 🔥 PERSISTENCE STATE
    # ==================================================

    def _detect_persistence_state(self):

        if (
            self.continuation_mature
            and self.directional_memory
                == "RETAINED"
        ):
            return "MATURE"

        if (
            self.recovery_cycles > 0
            and self.weak_cycles > 0
        ):
            return "CONTESTED"

        if self.continuity_pressure > 0.45:
            return "STRESSED"

        return "ACTIVE"

    # ==================================================
    # 🔥 EXPORT
    # ==================================================

    def export(self):

        return {

            "timestamp":
                self.timestamp,

            "trade_id":
                self.trade_id,

            "symbol":
                self.symbol,

            "direction":
                self.direction,

            "trade_type":
                self.trade_type,

            "state":
                self.state,

            "cycles_alive":
                self.cycles_alive,

            "continuation_mature":
                self.continuation_mature,

            "current_probability":
                round(
                    self.current_probability,
                    3
                ),

            "probability_position":
                self.probability_position,

            "deterioration_score":
                round(
                    self.deterioration_score,
                    3
                ),

            "continuity_pressure":
                self.continuity_pressure,

            "weak_cycles":
                self.weak_cycles,

            "recovery_cycles":
                self.recovery_cycles,

            "directional_memory":
                self.directional_memory,

            "recovery_behavior":
                self.recovery_behavior,

            "weakness_behavior":
                self.weakness_behavior,

            "persistence_state":
                self.persistence_state,

            "exit_pending":
                self.exit_pending,

            "exit_confirmed":
                self.exit_confirmed,

            "exit_reason":
                self.exit_reason
        }

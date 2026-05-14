# behavioral_continuity/continuity_snapshot.py

import time


class ContinuitySnapshot:

    """
    Passive behavioral continuity snapshot.

    Responsibilities:
    - Normalize lifecycle continuity state
    - Preserve sequence-aware continuity primitives
    - Extract descriptive continuity topology
    - Remain fully observational

    This layer does NOT:
    - generate execution decisions
    - modify trades
    - mutate lifecycle state
    - predict outcomes
    - affect execution behavior
    """

    # ==================================================
    # 🔥 INIT
    # ==================================================

    def __init__(self, trade):

        self.timestamp = time.time()

        # ==============================================
        # 🔥 IDENTITY
        # ==============================================

        self.trade_id = trade.trade_id

        self.symbol = trade.symbol

        self.direction = trade.direction

        self.trade_type = trade.trade_type

        self.state = trade.state

        # ==============================================
        # 🔥 LIFECYCLE STATE
        # ==============================================

        self.cycles_alive = (
            trade.cycles_alive
        )

        # ==============================================
        # 🔥 RAW CONTINUITY PRIMITIVES
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

        self.deterioration_score = (
            trade.deterioration_score
        )

        self.warning_count = (
            trade.warning_count
        )

        self.recovery_count = (
            trade.recovery_count
        )

        self.weak_cycles = (
            trade.consecutive_weak_cycles
        )

        self.recovery_cycles = (
            trade.consecutive_recovery_cycles
        )

        # ==============================================
        # 🔥 RAW CONTINUITY SEQUENCE
        # ==============================================

        """
        Important:
        This is the primary continuity source.

        Sequence-first continuity preservation
        is preferred over scalar-only compression.
        """

        self.continuity_sequence = list(
            getattr(
                trade,
                "continuity_sequence",
                []
            )
        )

        self.latest_transition = (
            self._extract_latest_transition()
        )

        self.transition_balance = (
            self._compute_transition_balance()
        )

        self.transition_stability = (
            self._compute_transition_stability()
        )

        # ==============================================
        # 🔥 STRUCTURE MEMORY
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
        # 🔥 EXECUTION VISIBILITY
        # ==============================================

        """
        Important:
        These are treated as execution visibility fields,
        NOT behavioral truth descriptors.
        """

        self.exit_pending = (
            trade.exit_pending
        )

        self.exit_confirmed = (
            trade.exit_confirmed
        )

        self.exit_reason = (
            trade.exit_reason
        )

        self.continuation_mature = (
            trade.continuation_mature
        )

        # ==============================================
        # 🔥 DESCRIPTIVE CONTINUITY SEMANTICS
        # ==============================================

        """
        These remain:
        - descriptive
        - observational
        - non-authoritative

        They should NOT become:
        - execution directives
        - predictive certainty
        - adaptive intelligence
        """

        self.probability_position = (
            self._compute_probability_position()
        )

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
    # 🔥 LATEST TRANSITION
    # ==================================================

    def _extract_latest_transition(self):

        if not self.continuity_sequence:
            return "UNKNOWN"

        return self.continuity_sequence[-1].get(
            "transition",
            "UNKNOWN"
        )

    # ==================================================
    # 🔥 TRANSITION BALANCE
    # ==================================================

    def _compute_transition_balance(self):

        if not self.continuity_sequence:
            return 0.0

        recent = self.continuity_sequence[-10:]

        up_count = sum(
            1
            for x in recent
            if x.get("transition") == "UP"
        )

        down_count = sum(
            1
            for x in recent
            if x.get("transition") == "DOWN"
        )

        total = max(
            1,
            len(recent)
        )

        balance = (
            up_count - down_count
        ) / total

        return round(balance, 3)

    # ==================================================
    # 🔥 TRANSITION STABILITY
    # ==================================================

    def _compute_transition_stability(self):

        if len(self.continuity_sequence) < 4:
            return "UNDEFINED"

        recent = self.continuity_sequence[-6:]

        transitions = [
            x.get("transition")
            for x in recent
        ]

        unique = len(set(transitions))

        if unique == 1:
            return "STABLE"

        if unique == 2:
            return "CONTESTED"

        return "FRAGMENTED"

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
            max(
                0.0,
                min(
                    1.0,
                    relative_position
                )
            ),
            3
        )

    # ==================================================
    # 🔥 CONTINUITY PRESSURE
    # ==================================================

    def _compute_continuity_pressure(self):

        """
        Important:
        Pressure is NOT collapse.

        This remains:
        continuity stress visibility only.
        """

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
            max(
                0.0,
                min(1.0, pressure)
            ),
            3
        )

    # ==================================================
    # 🔥 DIRECTIONAL MEMORY
    # ==================================================

    def _detect_directional_memory(self):

        """
        Important:
        This remains descriptive continuity retention,
        NOT trend certainty.
        """

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

        """
        Important:
        This is descriptive topology only.

        NOT:
        - execution confidence
        - market truth
        - predictive validity
        """

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

        if self.transition_stability == (
            "FRAGMENTED"
        ):
            return "FRAGMENTED"

        if self.continuity_pressure > 0.45:
            return "STRESSED"

        return "ACTIVE"

    # ==================================================
    # 🔥 EXPORT
    # ==================================================

    def export(self):

        return {

            # ==========================================
            # 🔥 IDENTITY
            # ==========================================

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

            # ==========================================
            # 🔥 LIFECYCLE STATE
            # ==========================================

            "cycles_alive":
                self.cycles_alive,

            # ==========================================
            # 🔥 RAW CONTINUITY
            # ==========================================

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
                    self.weak_cycles,

                "recovery_cycles":
                    self.recovery_cycles,

                "continuity_sequence":
                    self.continuity_sequence,

                "latest_transition":
                    self.latest_transition,

                "transition_balance":
                    self.transition_balance,

                "transition_stability":
                    self.transition_stability
            },

            # ==========================================
            # 🔥 STRUCTURE MEMORY
            # ==========================================

            "structure_memory": {

                "trend":
                    self.last_trend,

                "setup":
                    self.last_setup,

                "confidence":
                    self.last_confidence
            },

            # ==========================================
            # 🔥 EXECUTION VISIBILITY
            # ==========================================

            "execution_visibility": {

                "exit_pending":
                    self.exit_pending,

                "exit_confirmed":
                    self.exit_confirmed,

                "exit_reason":
                    self.exit_reason,

                "continuation_mature":
                    self.continuation_mature
            },

            # ==========================================
            # 🔥 DESCRIPTIVE CONTINUITY
            # ==========================================

            "continuity_semantics": {

                "probability_position":
                    self.probability_position,

                "continuity_pressure":
                    self.continuity_pressure,

                "directional_memory":
                    self.directional_memory,

                "recovery_behavior":
                    self.recovery_behavior,

                "weakness_behavior":
                    self.weakness_behavior,

                "persistence_state":
                    self.persistence_state
            }
        }

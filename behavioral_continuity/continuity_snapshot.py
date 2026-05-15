import time


class ContinuitySnapshot:

    """
    Passive behavioral continuity normalization layer.

    Responsibilities:
    - Normalize lifecycle continuity state
    - Preserve sequence-aware continuity primitives
    - Preserve topology visibility
    - Provide passive observational derivations
    - Remain fully execution-neutral

    This layer does NOT:
    - generate execution decisions
    - modify trades
    - mutate lifecycle state
    - predict outcomes
    - affect execution behavior
    - provide behavioral authority
    - provide semantic truth

    Architectural Boundary:
    This layer MUST remain:
    - passive
    - descriptive
    - sequence-preserving
    - execution-neutral

    This layer MUST NOT evolve into:
    - intelligence engine
    - prediction layer
    - adaptive observer
    - execution participant
    - semantic authority
    """

    # ==================================================
    # 🔥 INIT
    # ==================================================

    def __init__(self, trade):

        self.timestamp = time.time()

        # ==============================================
        # 🔥 NORMALIZATION LAYER
        # ==============================================

        if isinstance(trade, dict):

            self._normalize_dict_trade(
                trade
            )

        else:

            self._normalize_object_trade(
                trade
            )

        # ==============================================
        # 🔥 RAW SEQUENCE DERIVATIONS
        # ==============================================

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
        # 🔥 OBSERVATIONAL DESCRIPTORS
        # ==============================================

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

        # ==============================================
        # 🔥 HIGHER-ORDER OBSERVATIONAL DERIVATIONS
        # ==============================================

        self.evolution_phase = (
            self._derive_evolution_phase()
        )

        self.continuation_status = (
            self._derive_continuation_status()
        )

        self.structural_drift = (
            self._derive_structural_drift()
        )

        self.behavioral_commentary = (
            self._derive_behavioral_commentary()
        )

    # ==================================================
    # 🔥 NORMALIZATION HELPERS
    # ==================================================

    def _normalize_dict_trade(
        self,
        trade
    ):

        continuity = trade.get(
            "continuity_primitives",
            {}
        )

        structure = trade.get(
            "structure_memory",
            {}
        )

        execution = trade.get(
            "execution_visibility",
            trade.get(
                "execution_state",
                {}
            )
        )

        self.trade_id = trade.get(
            "trade_id"
        )

        self.symbol = trade.get(
            "symbol"
        )

        self.direction = trade.get(
            "direction"
        )

        self.trade_type = trade.get(
            "trade_type"
        )

        self.state = trade.get(
            "state"
        )

        self.cycles_alive = trade.get(
            "cycles_alive",
            0
        )

        self.initial_probability = continuity.get(
            "initial_probability",
            0.5
        )

        self.current_probability = continuity.get(
            "current_probability",
            0.5
        )

        self.highest_probability = continuity.get(
            "highest_probability",
            0.5
        )

        self.lowest_probability = continuity.get(
            "lowest_probability",
            0.5
        )

        self.deterioration_score = continuity.get(
            "deterioration_score",
            0.0
        )

        self.warning_count = continuity.get(
            "warning_count",
            0
        )

        self.recovery_count = continuity.get(
            "recovery_count",
            0
        )

        self.weak_cycles = continuity.get(
            "weak_cycles",
            0
        )

        self.recovery_cycles = continuity.get(
            "recovery_cycles",
            0
        )

        self.continuity_sequence = self._safe_sequence_copy(
            continuity.get(
                "continuity_sequence",
                []
            )
        )

        self.last_trend = structure.get(
            "trend",
            "unknown"
        )

        self.last_setup = structure.get(
            "setup",
            "unknown"
        )

        self.last_confidence = structure.get(
            "confidence",
            "LOW"
        )

        self.exit_pending = execution.get(
            "exit_pending",
            False
        )

        self.exit_confirmed = execution.get(
            "exit_confirmed",
            False
        )

        self.exit_reason = execution.get(
            "exit_reason"
        )

        self.continuation_mature = execution.get(
            "continuation_mature",
            False
        )

    # ==================================================
    # 🔥 OBJECT NORMALIZATION
    # ==================================================

    def _normalize_object_trade(
        self,
        trade
    ):

        self.trade_id = trade.trade_id

        self.symbol = trade.symbol

        self.direction = trade.direction

        self.trade_type = trade.trade_type

        self.state = trade.state

        self.cycles_alive = (
            trade.cycles_alive
        )

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

        self.continuity_sequence = (
            self._safe_sequence_copy(
                getattr(
                    trade,
                    "continuity_sequence",
                    []
                )
            )
        )

        self.last_trend = (
            trade.last_trend
        )

        self.last_setup = (
            trade.last_setup
        )

        self.last_confidence = (
            trade.last_confidence
        )

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

    # ==================================================
    # 🔥 SAFE COPY HELPERS
    # ==================================================

    def _safe_sequence_copy(
        self,
        sequence
    ):

        return [
            dict(item)
            for item in sequence
        ]

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

        if self.transition_stability == (
            "FRAGMENTED"
        ):
            return "FRAGMENTED"

        if self.continuity_pressure > 0.45:
            return "STRESSED"

        return "ACTIVE"

    # ==================================================
    # 🔥 EVOLUTION PHASE
    # ==================================================

    def _derive_evolution_phase(self):

        if (
            self.recovery_behavior
            in [
                "ATTEMPTING",
                "SUSTAINED"
            ]
        ):

            return "RECOVERING"

        if (
            self.transition_stability
            == "FRAGMENTED"
        ):

            return "FRAGMENTING"

        if (
            self.directional_memory
            == "WEAKENING"
        ):

            return "DETERIORATING"

        if (
            self.persistence_state
            == "ACTIVE"
        ):

            return "STABILIZING"

        if (
            self.persistence_state
            == "CONTESTED"
        ):

            return "TRANSITIONAL"

        return "REABSORBING"

    # ==================================================
    # 🔥 CONTINUATION STATUS
    # ==================================================

    def _derive_continuation_status(self):

        if (
            self.transition_stability
            == "FRAGMENTED"
            and self.continuity_pressure >= 0.7
        ):

            return "COLLAPSING"

        if self.continuation_mature:

            return "MATURE"

        if self.cycles_alive >= 5:

            return "BUILDING"

        if self.continuity_pressure >= 0.75:

            return "EXHAUSTING"

        return "ACTIVE"

    # ==================================================
    # 🔥 STRUCTURAL DRIFT
    # ==================================================

    def _derive_structural_drift(self):

        if (
            self.transition_stability
            == "FRAGMENTED"
            and self.continuity_pressure >= 0.75
        ):

            return "CHAOTIC"

        if (
            self.transition_stability
            == "FRAGMENTED"
        ):

            return "FRAGMENTING"

        if (
            self.transition_stability
            == "CONTESTED"
        ):

            return "CONTESTED"

        return "STABLE"

    # ==================================================
    # 🔥 BEHAVIORAL COMMENTARY
    # ==================================================

    def _derive_behavioral_commentary(self):

        if (
            self.continuation_status
            == "COLLAPSING"
        ):

            return (
                "POSSIBLE FALSE EXPANSION"
            )

        if (
            self.recovery_behavior
            in [
                "ATTEMPTING",
                "SUSTAINED"
            ]
        ):

            return (
                "RECOVERY ATTEMPT VISIBLE"
            )

        if (
            self.transition_stability
            == "FRAGMENTED"
        ):

            return (
                "FRAGMENTATION ESCALATING"
            )

        if (
            self.continuity_pressure >= 0.6
        ):

            return (
                "CONTINUITY PRESSURE INCREASING"
            )

        return (
            "ROTATIONAL RETENTION HOLDING"
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

        if self.transition_stability == (
            "FRAGMENTED"
        ):
            return "FRAGMENTED"

        if self.continuity_pressure > 0.45:
            return "STRESSED"

        return "ACTIVE"

    # ==================================================
    # 🔥 EVOLUTION PHASE
    # ==================================================

    def _derive_evolution_phase(self):

        if (
            self.recovery_behavior
            in [
                "ATTEMPTING",
                "SUSTAINED"
            ]
        ):

            return "RECOVERING"

        if (
            self.transition_stability
            == "FRAGMENTED"
        ):

            return "FRAGMENTING"

        if (
            self.directional_memory
            == "WEAKENING"
        ):

            return "DETERIORATING"

        if (
            self.persistence_state
            == "ACTIVE"
        ):

            return "STABILIZING"

        if (
            self.persistence_state
            == "CONTESTED"
        ):

            return "TRANSITIONAL"

        return "REABSORBING"

    # ==================================================
    # 🔥 CONTINUATION STATUS
    # ==================================================

    def _derive_continuation_status(self):

        if (
            self.transition_stability
            == "FRAGMENTED"
            and self.continuity_pressure >= 0.7
        ):

            return "COLLAPSING"

        if self.continuation_mature:

            return "MATURE"

        if self.cycles_alive >= 5:

            return "BUILDING"

        if self.continuity_pressure >= 0.75:

            return "EXHAUSTING"

        return "ACTIVE"

    # ==================================================
    # 🔥 STRUCTURAL DRIFT
    # ==================================================

    def _derive_structural_drift(self):

        if (
            self.transition_stability
            == "FRAGMENTED"
            and self.continuity_pressure >= 0.75
        ):

            return "CHAOTIC"

        if (
            self.transition_stability
            == "FRAGMENTED"
        ):

            return "FRAGMENTING"

        if (
            self.transition_stability
            == "CONTESTED"
        ):

            return "CONTESTED"

        return "STABLE"

    # ==================================================
    # 🔥 BEHAVIORAL COMMENTARY
    # ==================================================

    def _derive_behavioral_commentary(self):

        if (
            self.continuation_status
            == "COLLAPSING"
        ):

            return (
                "POSSIBLE FALSE EXPANSION"
            )

        if (
            self.recovery_behavior
            in [
                "ATTEMPTING",
                "SUSTAINED"
            ]
        ):

            return (
                "RECOVERY ATTEMPT VISIBLE"
            )

        if (
            self.transition_stability
            == "FRAGMENTED"
        ):

            return (
                "FRAGMENTATION ESCALATING"
            )

        if (
            self.continuity_pressure >= 0.6
        ):

            return (
                "CONTINUITY PRESSURE INCREASING"
            )

        return (
            "ROTATIONAL RETENTION HOLDING"
        )

from collections import deque

from behavioral_continuity.continuity_snapshot import (
    ContinuitySnapshot
)


class ContinuityObserver:

    """
    Passive sequence-aware behavioral observer.

    Responsibilities:
    - Preserve continuity topology across time
    - Observe longitudinal sequence persistence
    - Detect descriptive continuity archetypes
    - Maintain passive behavioral visibility

    This layer does NOT:
    - predict outcomes
    - generate execution directives
    - mutate lifecycle state
    - modify probability
    - optimize behavior
    - generate adaptive intelligence
    - provide semantic authority

    Architectural Boundary:
    This layer MUST remain:
    - observational only
    - sequence-first
    - execution-neutral
    - behaviorally isolated

    This layer MUST NOT evolve into:
    - prediction engine
    - execution advisor
    - scoring engine
    - adaptive intelligence system
    - market analysis authority
    """

    # ==================================================
    # 🔥 INIT
    # ==================================================

    def __init__(self):

        # trade_id -> deque[snapshots]
        self.snapshot_memory = {}

        self.max_memory = 30

    # ==================================================
    # 🔥 OBSERVE
    # ==================================================

    def observe(self, trade):

        """
        Important:
        Observer consumes lifecycle state passively.

        Observer NEVER modifies:
        - trade state
        - execution logic
        - lifecycle behavior

        Observer outputs MUST NOT influence:
        - execution decisions
        - lifecycle heuristics
        - probability weighting
        - adaptive behavior
        """

        snapshot = ContinuitySnapshot(
            trade
        )

        trade_id = snapshot.trade_id

        memory = self._get_trade_memory(
            trade_id
        )

        memory.append(snapshot)

        sequence = self._build_sequence_view(
            memory
        )

        archetypes = (
            self._detect_archetypes(
                sequence
            )
        )

        # ==============================================
        # 🔥 EVOLUTION VISIBILITY
        # ==============================================

        evolution_visibility = {

            "evolution_phase":
                snapshot.evolution_phase,

            "continuation_status":
                snapshot.continuation_status,

            "structural_drift":
                snapshot.structural_drift,

            "behavioral_commentary":
                snapshot.behavioral_commentary
        }

        observational_descriptors = {

            "current_state":
                snapshot.persistence_state,

            "continuity_pressure":
                snapshot.continuity_pressure,

            "directional_memory":
                snapshot.directional_memory,

            "evolution_phase":
                snapshot.evolution_phase,

            "continuation_status":
                snapshot.continuation_status,

            "structural_drift":
                snapshot.structural_drift,

            "behavioral_commentary":
                snapshot.behavioral_commentary
        }

        topology_visibility = {

            "latest_transition":
                snapshot.latest_transition,

            "transition_balance":
                snapshot.transition_balance,

            "transition_stability":
                snapshot.transition_stability
        }

        return {

            # ==========================================
            # 🔥 IDENTITY
            # ==========================================

            "trade_id":
                snapshot.trade_id,

            "symbol":
                snapshot.symbol,

            "direction":
                snapshot.direction,

            "trade_type":
                snapshot.trade_type,

            # ==========================================
            # 🔥 OBSERVATION STATE
            # ==========================================

            "cycles_alive":
                snapshot.cycles_alive,

            "sequence_depth":
                len(sequence),

            # ==========================================
            # 🔥 TOPOLOGY VISIBILITY
            # ==========================================

            "topology_visibility":
                topology_visibility,

            # ==========================================
            # 🔥 OBSERVATIONAL DESCRIPTORS
            # ==========================================

            "observational_descriptors":
                observational_descriptors,

            # ==========================================
            # 🔥 EVOLUTION VISIBILITY
            # ==========================================

            "evolution_visibility":
                evolution_visibility,

            # ==========================================
            # 🔥 ARCHETYPAL DESCRIPTORS
            # ==========================================

            "archetypes":
                archetypes,

            # ==========================================
            # 🔥 LEGACY COMPATIBILITY
            # ==========================================

            "latest_transition":
                snapshot.latest_transition,

            "transition_balance":
                snapshot.transition_balance,

            "transition_stability":
                snapshot.transition_stability,

            "current_state":
                snapshot.persistence_state,

            "continuity_pressure":
                snapshot.continuity_pressure,

            "directional_memory":
                snapshot.directional_memory,

            # ==========================================
            # 🔥 EVOLUTION LEGACY VISIBILITY
            # ==========================================

            "evolution_phase":
                snapshot.evolution_phase,

            "continuation_status":
                snapshot.continuation_status,

            "structural_drift":
                snapshot.structural_drift,

            "behavioral_commentary":
                snapshot.behavioral_commentary
        }

    # ==================================================
    # 🔥 MEMORY HELPERS
    # ==================================================

    def _get_trade_memory(
        self,
        trade_id
    ):

        """
        Runtime-safe sequence memory retrieval.
        """

        if trade_id not in self.snapshot_memory:

            self.snapshot_memory[
                trade_id
            ] = deque(
                maxlen=self.max_memory
            )

        return self.snapshot_memory[
            trade_id
        ]

    # ==================================================
    # 🔥 BUILD SEQUENCE VIEW
    # ==================================================

    def _build_sequence_view(
        self,
        memory
    ):

        """
        Builds a normalized sequence view.
        """

        return list(memory)
# ==================================================
    # 🔥 ARCHETYPE DETECTION
    # ==================================================

    def _detect_archetypes(
        self,
        sequence
    ):

        """
        Archetypes are descriptive continuity
        topology labels only.
        """

        archetypes = []

        if len(sequence) < 3:
            return archetypes

        if self._is_stressed_persistence(
            sequence
        ):
            archetypes.append(
                "STRESSED_PERSISTENCE"
            )

        if self._is_recovery_retention(
            sequence
        ):
            archetypes.append(
                "RECOVERY_RETENTION"
            )

        if self._is_continuity_decay(
            sequence
        ):
            archetypes.append(
                "CONTINUITY_DECAY"
            )

        if self._is_fragmented_continuation(
            sequence
        ):
            archetypes.append(
                "FRAGMENTED_CONTINUATION"
            )

        if self._is_entropy_reabsorption(
            sequence
        ):
            archetypes.append(
                "ENTROPY_REABSORPTION"
            )

        return list(archetypes)

    # ==================================================
    # 🔥 STRESSED PERSISTENCE
    # ==================================================

    def _is_stressed_persistence(
        self,
        sequence
    ):

        recent = sequence[-5:]

        weak_presence = any(

            s.weak_cycles > 0

            for s in recent
        )

        recovery_presence = any(

            s.recovery_cycles > 0

            for s in recent
        )

        directional_memory_alive = all(

            s.directional_memory
            != "WEAKENING"

            for s in recent
        )

        fragmented_structure = any(

            s.transition_stability
            == "CONTESTED"

            or
            s.transition_stability
            == "FRAGMENTED"

            for s in recent
        )

        return (

            weak_presence
            and recovery_presence
            and directional_memory_alive
            and fragmented_structure
        )

    # ==================================================
    # 🔥 RECOVERY RETENTION
    # ==================================================

    def _is_recovery_retention(
        self,
        sequence
    ):

        recent = sequence[-5:]

        recovery_presence = sum(

            1
            for s in recent

            if s.recovery_cycles > 0
        )

        retained_memory = sum(

            1
            for s in recent

            if (
                s.directional_memory
                == "RETAINED"
            )
        )

        stable_transitions = sum(

            1
            for s in recent

            if (
                s.transition_stability
                == "STABLE"
            )
        )

        return (

            recovery_presence >= 2
            and retained_memory >= 2
            and stable_transitions >= 1
        )

    # ==================================================
    # 🔥 CONTINUITY DECAY
    # ==================================================

    def _is_continuity_decay(
        self,
        sequence
    ):

        recent = sequence[-6:]

        increasing_pressure = (

            recent[-1].continuity_pressure
            >
            recent[0].continuity_pressure
        )

        weakening_memory = sum(

            1
            for s in recent

            if (
                s.directional_memory
                == "WEAKENING"
            )
        )

        unstable_transitions = sum(

            1
            for s in recent

            if (
                s.transition_stability
                != "STABLE"
            )
        )

        return (

            increasing_pressure
            and weakening_memory >= 3
            and unstable_transitions >= 3
        )

    # ==================================================
    # 🔥 FRAGMENTED CONTINUATION
    # ==================================================

    def _is_fragmented_continuation(
        self,
        sequence
    ):

        recent = sequence[-6:]

        alternating_behavior = False

        transitions = 0

        for i in range(
            1,
            len(recent)
        ):

            previous = recent[i - 1]
            current = recent[i]

            previous_state = (
                previous.recovery_behavior
            )

            current_state = (
                current.recovery_behavior
            )

            if previous_state != current_state:

                transitions += 1

        if transitions >= 3:
            alternating_behavior = True

        continuity_alive = any(

            s.directional_memory
            in [
                "RETAINED",
                "STRESSED"
            ]

            for s in recent
        )

        fragmented_transition_presence = any(

            s.transition_stability
            == "FRAGMENTED"

            for s in recent
        )

        return (

            alternating_behavior
            and continuity_alive
            and fragmented_transition_presence
        )
# ==================================================
    # 🔥 ENTROPY REABSORPTION
    # ==================================================

    def _is_entropy_reabsorption(
        self,
        sequence
    ):

        recent = sequence[-6:]

        persistent_weakness = all(

            s.weakness_behavior
            != "STABLE"

            for s in recent
        )

        absent_recovery = all(

            s.recovery_behavior
            == "ABSENT"

            for s in recent
        )

        weakened_memory = all(

            s.directional_memory
            == "WEAKENING"

            for s in recent
        )

        fragmented_transitions = all(

            s.transition_stability
            != "STABLE"

            for s in recent
        )

        return (

            persistent_weakness
            and absent_recovery
            and weakened_memory
            and fragmented_transitions
        )

    # ==================================================
    # 🔥 EXPORT SEQUENCE
    # ==================================================

    def export_sequence(
        self,
        trade_id
    ):

        """
        Passive sequence export only.
        """

        if (
            trade_id
            not in self.snapshot_memory
        ):
            return []

        return [

            snapshot.export()

            for snapshot in self.snapshot_memory[
                trade_id
            ]
        ]

    # ==================================================
    # 🔥 CLEANUP CLOSED SEQUENCES
    # ==================================================

    def cleanup_closed_sequences(
        self,
        active_trade_ids
    ):

        """
        Runtime-safe observer memory cleanup.
        """

        removable = []

        active_ids = set()

        for item in active_trade_ids:

            if isinstance(item, dict):

                trade_id = item.get(
                    "trade_id"
                )

                if trade_id:
                    active_ids.add(trade_id)

            else:

                active_ids.add(item)

        for trade_id in list(
            self.snapshot_memory.keys()
        ):

            if trade_id not in active_ids:

                removable.append(
                    trade_id
                )

        for trade_id in removable:

            del self.snapshot_memory[
                trade_id
            ]

    # ==================================================
    # 🔥 BACKWARD COMPATIBILITY
    # ==================================================

    def cleanup(
        self,
        active_trade_ids
    ):

        self.cleanup_closed_sequences(
            active_trade_ids
        )

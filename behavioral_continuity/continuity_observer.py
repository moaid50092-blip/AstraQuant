from collections import deque

from behavioral_continuity.continuity_snapshot import (
    ContinuitySnapshot
)


class ContinuityObserver:

    """
    Passive sequence-aware behavioral observer.

    Responsibilities:
    - Read continuity snapshots across time
    - Observe behavioral persistence patterns
    - Detect primitive continuity archetypes
    - Produce descriptive semantic traces

    This layer does NOT:
    - predict outcomes
    - modify execution
    - mutate lifecycle state
    - generate scores
    - optimize behavior
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

        snapshot = ContinuitySnapshot(
            trade
        )

        trade_id = snapshot.trade_id

        if trade_id not in self.snapshot_memory:

            self.snapshot_memory[
                trade_id
            ] = deque(
                maxlen=self.max_memory
            )

        self.snapshot_memory[
            trade_id
        ].append(snapshot)

        sequence = list(
            self.snapshot_memory[trade_id]
        )

        archetypes = (
            self._detect_archetypes(
                sequence
            )
        )

        return {

            "trade_id":
                snapshot.trade_id,

            "symbol":
                snapshot.symbol,

            "direction":
                snapshot.direction,

            "trade_type":
                snapshot.trade_type,

            "cycles_alive":
                snapshot.cycles_alive,

            "archetypes":
                archetypes,

            "sequence_depth":
                len(sequence),

            "current_state":
                snapshot.persistence_state,

            "continuity_pressure":
                snapshot.continuity_pressure
        }

    # ==================================================
    # 🔥 ARCHETYPE DETECTION
    # ==================================================

    def _detect_archetypes(
        self,
        sequence
    ):

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

        return archetypes

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
            s.directional_memory != "WEAKENING"
            for s in recent
        )

        return (

            weak_presence
            and recovery_presence
            and directional_memory_alive
        )

    # ==================================================
    # 🔥 RECOVERY RETENTION
    # ==================================================

    def _is_recovery_retention(
        self,
        sequence
    ):

        recent = sequence[-4:]

        recovery_count = sum(

            1 for s in recent

            if s.recovery_cycles > 0
        )

        retained_memory = sum(

            1 for s in recent

            if s.directional_memory
                == "RETAINED"
        )

        return (

            recovery_count >= 2
            and retained_memory >= 2
        )

    # ==================================================
    # 🔥 CONTINUITY DECAY
    # ==================================================

    def _is_continuity_decay(
        self,
        sequence
    ):

        recent = sequence[-5:]

        increasing_pressure = (

            recent[-1].continuity_pressure
            >
            recent[0].continuity_pressure
        )

        weakening_memory = sum(

            1 for s in recent

            if s.directional_memory
                == "WEAKENING"
        )

        return (

            increasing_pressure
            and weakening_memory >= 3
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

        for i in range(1, len(recent)):

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

        return (

            alternating_behavior
            and continuity_alive
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

        return (

            persistent_weakness
            and absent_recovery
            and weakened_memory
        )

    # ==================================================
    # 🔥 CLEANUP CLOSED SEQUENCES
    # ==================================================

    def cleanup_closed_sequences(
        self,
        active_trade_ids
    ):

        removable = []

        for trade_id in list(
            self.snapshot_memory.keys()
        ):

            if trade_id not in active_trade_ids:

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

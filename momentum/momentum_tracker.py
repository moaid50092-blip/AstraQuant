from collections import deque
import numpy as np


class MomentumTracker:

    def __init__(
        self,
        window_size=6,
        min_strength=0.42,
        min_velocity=0.008
    ):

        self.window_size = window_size

        self.min_strength = min_strength
        self.min_velocity = min_velocity

        self.history = {}

    # =================================================
    # 🔥 SAFE HISTORY INIT
    # =================================================

    def _ensure_symbol(self, symbol):

        if symbol not in self.history:

            self.history[symbol] = deque(
                maxlen=self.window_size
            )

    # =================================================
    # 🔥 UPDATE
    # =================================================

    def update(self, symbol, base_score):

        self._ensure_symbol(symbol)

        try:
            value = float(base_score)

        except Exception:
            value = 0.5

        # حماية من القيم الشاذة
        value = max(0.0, min(1.0, value))

        self.history[symbol].append(value)

    # =================================================
    # 🔥 SAFE DIFFS
    # =================================================

    def _compute_diffs(self, values):

        if len(values) < 2:
            return np.array([])

        return np.diff(values)

    # =================================================
    # 🔥 DIRECTION ENGINE
    # =================================================

    def _compute_direction(self, diffs):

        pos = np.sum([d for d in diffs if d > 0])
        neg = abs(np.sum([d for d in diffs if d < 0]))

        # Noise protection
        dominance_gap = abs(pos - neg)

        if dominance_gap < 0.015:
            return "neutral", pos, neg

        if pos > neg:
            return "up", pos, neg

        if neg > pos:
            return "down", pos, neg

        return "neutral", pos, neg

    # =================================================
    # 🔥 STRENGTH ENGINE
    # =================================================

    def _compute_strength(self, pos, neg):

        total_move = pos + neg

        if total_move <= 0:
            return 0.0

        directional_move = max(pos, neg)

        strength = directional_move / total_move

        return float(
            max(0.0, min(1.0, strength))
        )

    # =================================================
    # 🔥 VELOCITY ENGINE
    # =================================================

    def _compute_velocity(self, diffs):

        if len(diffs) == 0:
            return 0.0

        velocity = np.mean(np.abs(diffs))

        return float(velocity)

    # =================================================
    # 🔥 ACCELERATION ENGINE
    # =================================================

    def _compute_acceleration(self, diffs):

        if len(diffs) < 3:
            return False

        d1 = abs(diffs[-1])
        d2 = abs(diffs[-2])
        d3 = abs(diffs[-3])

        # تسارع نظيف وليس spike عشوائي
        acceleration = (
            d1 > d2 > d3
            and d1 > 0.01
        )

        return bool(acceleration)

    # =================================================
    # 🔥 STABILITY ENGINE
    # =================================================

    def _compute_stability(self, diffs):

        if len(diffs) < 2:
            return 0.0

        signs = np.sign(diffs)

        stable_moves = 0

        for i in range(1, len(signs)):

            if signs[i] == signs[i - 1]:
                stable_moves += 1

        stability = stable_moves / (len(signs) - 1)

        return float(
            max(0.0, min(1.0, stability))
        )

    # =================================================
    # 🔥 EARLY INTELLIGENCE
    # =================================================

    def _detect_early_entry(
        self,
        direction,
        strength,
        velocity,
        acceleration,
        stability
    ):

        if direction == "neutral":
            return False

        # =============================================
        # 🔥 PRIMARY EARLY
        # =============================================

        strong_flow = (
            strength >= self.min_strength
            and velocity >= self.min_velocity
            and stability >= 0.5
        )

        # =============================================
        # 🔥 ACCELERATION EARLY
        # =============================================

        acceleration_flow = (
            acceleration
            and strength >= 0.5
            and velocity >= 0.01
        )

        return strong_flow or acceleration_flow

    # =================================================
    # 🔥 MAIN MOMENTUM ENGINE
    # =================================================

    def get_momentum_info(self, symbol):

        values = list(
            self.history.get(symbol, [])
        )

        # ---------------------------------------------
        # SAFETY
        # ---------------------------------------------

        if len(values) < 3:

            return {
                "direction": "neutral",
                "strength": 0.0,
                "acceleration": False,
                "early_entry": False,
                "velocity": 0.0,
                "stability": 0.0,
                "history": values
            }

        # ---------------------------------------------
        # DIFFS
        # ---------------------------------------------

        diffs = self._compute_diffs(values)

        # ---------------------------------------------
        # DIRECTION
        # ---------------------------------------------

        direction, pos, neg = (
            self._compute_direction(diffs)
        )

        # ---------------------------------------------
        # STRENGTH
        # ---------------------------------------------

        strength = self._compute_strength(
            pos,
            neg
        )

        # ---------------------------------------------
        # VELOCITY
        # ---------------------------------------------

        velocity = self._compute_velocity(
            diffs
        )

        # ---------------------------------------------
        # ACCELERATION
        # ---------------------------------------------

        acceleration = (
            self._compute_acceleration(diffs)
        )

        # ---------------------------------------------
        # STABILITY
        # ---------------------------------------------

        stability = self._compute_stability(
            diffs
        )

        # ---------------------------------------------
        # EARLY ENTRY
        # ---------------------------------------------

        early_entry = (
            self._detect_early_entry(
                direction,
                strength,
                velocity,
                acceleration,
                stability
            )
        )

        # =============================================
        # 🔥 OUTPUT
        # =============================================

        return {
            "direction": direction,

            "strength": round(
                float(strength),
                2
            ),

            "acceleration": acceleration,

            "early_entry": early_entry,

            "velocity": round(
                float(velocity),
                4
            ),

            "stability": round(
                float(stability),
                3
            ),

            "history": [
                round(float(v), 3)
                for v in values
            ]
        }

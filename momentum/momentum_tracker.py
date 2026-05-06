from collections import deque
import numpy as np


class MomentumTracker:

    def __init__(self, window_size=6):
        self.window_size = window_size
        self.history = {}

    # -----------------------------------------
    def update(self, symbol, base_score):

        if symbol not in self.history:
            self.history[symbol] = deque(maxlen=self.window_size)

        self.history[symbol].append(float(base_score))

    # -----------------------------------------
    def get_momentum_info(self, symbol):

        values = list(self.history.get(symbol, []))

        if len(values) < 3:
            return {
                "direction": "neutral",
                "strength": 0.0,
                "acceleration": False,
                "early_entry": False,
                "velocity": 0.0,
                "history": values
            }

        diffs = np.diff(values)

        # =========================================
        # 🔥 Direction (weighted)
        # =========================================

        pos = np.sum([d for d in diffs if d > 0])
        neg = abs(np.sum([d for d in diffs if d < 0]))

        if pos > neg:
            direction = "up"
        elif neg > pos:
            direction = "down"
        else:
            direction = "neutral"

        total_move = pos + neg if (pos + neg) != 0 else 1
        strength = max(pos, neg) / total_move

        # =========================================
        # 🔥 Velocity (سرعة الحركة)
        # =========================================

        velocity = np.mean(np.abs(diffs))

        # =========================================
        # 🔥 Acceleration (تسارع)
        # =========================================

        accel = False
        if len(diffs) >= 3:
            accel = (
                abs(diffs[-1]) > abs(diffs[-2]) > abs(diffs[-3])
            )

        # =========================================
        # 🔥 EARLY DETECTION
        # =========================================

        early_entry = False

        if direction != "neutral":
            # بداية اتجاه + حركة نظيفة
            if strength > 0.55 and velocity > 0.01:
                early_entry = True

            # تسارع واضح
            if accel and strength > 0.5:
                early_entry = True

        # =========================================

        return {
            "direction": direction,
            "strength": round(float(strength), 2),
            "acceleration": accel,
            "early_entry": early_entry,
            "velocity": round(float(velocity), 4),
            "history": values
        }

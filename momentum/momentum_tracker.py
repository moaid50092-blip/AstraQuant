from collections import deque


class MomentumTracker:

    def __init__(self, window_size=4):
        self.window_size = window_size
        self.history = {}

    def update(self, symbol, base_score):

        if symbol not in self.history:
            self.history[symbol] = deque(maxlen=self.window_size)

        self.history[symbol].append(float(base_score))

    def get_momentum_info(self, symbol):

        values = list(self.history.get(symbol, []))

        if len(values) < 2:
            return {
                "direction": "neutral",
                "strength": 0.0,
                "history": values
            }

        increases = 0
        decreases = 0

        for i in range(1, len(values)):
            if values[i] > values[i - 1]:
                increases += 1
            elif values[i] < values[i - 1]:
                decreases += 1

        total_moves = increases + decreases

        if increases > decreases:
            direction = "up"
        elif decreases > increases:
            direction = "down"
        else:
            direction = "neutral"

        strength = increases / total_moves if total_moves > 0 else 0.0

        return {
            "direction": direction,
            "strength": round(strength, 2),
            "history": values
        }

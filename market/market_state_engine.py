class MarketStateEngine:

    def evaluate(self, all_signals):

        if not all_signals:
            return "UNKNOWN", "no data"

        total = len(all_signals)

        # -----------------------------
        # Metrics
        # -----------------------------
        avg_strength = sum(s.get("strength", 0) for s in all_signals) / total
        avg_prob = sum(s.get("probability", 0.5) for s in all_signals) / total

        breakout_count = sum(1 for s in all_signals if s.get("breakout"))
        trend_count = sum(1 for s in all_signals if s.get("trend") in ["up", "down"])
        range_count = sum(1 for s in all_signals if s.get("trend") == "range")

        breakout_ratio = breakout_count / total
        trend_ratio = trend_count / total
        range_ratio = range_count / total

        # -----------------------------
        # STATE LOGIC
        # -----------------------------
        # 🟥 DEAD MARKET
        if avg_strength < 0.25 and breakout_ratio < 0.2:
            return "DEAD", "low strength + no breakouts"

        # 🟨 RANGE MARKET
        if range_ratio > 0.6 and breakout_ratio < 0.3:
            return "RANGE", "sideways structure"

        # 🟩 TREND MARKET
        if trend_ratio > 0.6 and breakout_ratio > 0.3 and avg_strength > 0.35:
            return "TREND", "aligned trend + breakout activity"

        # fallback
        return "MIXED", "unclear structure"

import numpy as np


class ContextAnalyzerV2:

    def __init__(self):

        # =============================================
        # 🔥 TREND WEIGHTS
        # =============================================

        self.w_short = 0.4
        self.w_mid = 0.35
        self.w_long = 0.25

        # =============================================
        # 🔥 THRESHOLDS
        # =============================================

        self.align_threshold = 0.6

        self.high_confidence = 0.72
        self.medium_confidence = 0.54

    # =================================================
    # 🔥 SAFE TREND SCORE
    # =================================================

    def _trend_score(self, closes, n):

        if len(closes) < n:
            return "range", 0.0

        seq = closes[-n:]

        diffs = np.diff(seq)

        if len(diffs) == 0:
            return "range", 0.0

        up_moves = np.sum(diffs > 0)
        down_moves = np.sum(diffs < 0)

        total = up_moves + down_moves

        if total == 0:
            return "range", 0.0

        up_ratio = up_moves / total
        down_ratio = down_moves / total

        strength = max(
            up_ratio,
            down_ratio
        )

        # =============================================
        # 🔥 DIRECTION FILTER
        # =============================================

        directional_move = (
            seq[-1] - seq[0]
        ) / seq[0]

        move_abs = abs(directional_move)

        # =============================================
        # 🔥 NOISY OSCILLATION DETECTION
        # =============================================

        sign_flips = np.sum(
            np.diff(np.sign(diffs)) != 0
        )

        flip_ratio = (
            sign_flips / len(diffs)
            if len(diffs) > 0
            else 0
        )

        avg_move = np.mean(
            np.abs(diffs)
        )

        net_efficiency = (
            abs(seq[-1] - seq[0])
            /
            (np.sum(np.abs(diffs)) + 1e-9)
        )

        # 🔥 dead rotational churn
        if move_abs < 0.001:
            return "range", float(
                max(0.25, strength * 0.7)
            )

        # 🔥 fragmented oscillation
        if (
            flip_ratio > 0.58
            and net_efficiency < 0.42
        ):
            return "range", float(
                max(0.3, strength * 0.72)
            )

        # 🔥 unstable directional structure
        if (
            avg_move > 0
            and move_abs < (
                avg_move * 1.8
            ) / seq[0]
        ):
            return "range", float(
                max(0.32, strength * 0.78)
            )

        if up_ratio >= self.align_threshold:
            return "up", float(strength)

        if down_ratio >= self.align_threshold:
            return "down", float(strength)

        return "range", float(strength)

    # =================================================
    # 🔥 VOLATILITY ENGINE
    # =================================================

    def _volatility(self, highs, lows):

        ranges = highs - lows

        if len(ranges) == 0:
            return 0.0

        if len(ranges) < 20:
            return float(np.mean(ranges))

        return float(np.mean(ranges[-20:]))

    # =================================================
    # 🔥 TREND AGREEMENT SCORE
    # =================================================

    def _score_layer(
        self,
        trend,
        strength,
        weight,
        momentum_dir,
        layer_name
    ):

        # ---------------------------------------------
        # ALIGN
        # ---------------------------------------------

        if trend == momentum_dir:

            score = weight * strength

            return score, f"{layer_name} ALIGN"

        # ---------------------------------------------
        # RANGE
        # ---------------------------------------------

        if trend == "range":

            # 🔥 fragmented/range penalty strengthened
            score = -weight * 0.18

            return score, f"{layer_name} RANGE"

        # ---------------------------------------------
        # MISALIGN
        # ---------------------------------------------

        score = -weight * 0.48

        return score, f"{layer_name} MISALIGN"

    # =================================================
    # 🔥 BREAKOUT INTELLIGENCE
    # =================================================

    def _breakout_score(
        self,
        highs,
        lows,
        avg_vol
    ):

        recent_high = np.max(highs[-10:])
        recent_low = np.min(lows[-10:])

        recent_range = float(
            recent_high - recent_low
        )

        recent_close_position = (
            highs[-1] - lows[-1]
        )

        breakout_efficiency = (
            recent_range / (avg_vol + 1e-9)
        )

        # 🔥 weak expansion
        if breakout_efficiency < 1.0:
            return -0.03, "WEAK BREAKOUT"

        # 🔥 chaotic breakout
        if breakout_efficiency > 2.8:
            return -0.04, "CHAOTIC EXPANSION"

        # 🔥 exhaustion breakout
        if (
            recent_close_position
            <
            (avg_vol * 0.25)
        ):
            return -0.05, "BREAKOUT EXHAUSTION"

        # 🔥 valid breakout
        if breakout_efficiency > 1.7:
            return 0.12, "STRONG BREAKOUT"

        if breakout_efficiency > 1.25:
            return 0.07, "VALID BREAKOUT"

        return 0.02, "WEAK EXPANSION"

    # =================================================
    # 🔥 VOLATILITY FILTER
    # =================================================

    def _volatility_adjustment(
        self,
        vol,
        avg_vol
    ):

        if avg_vol <= 0:
            return 0.0, None

        ratio = vol / avg_vol

        # =============================================
        # 🔥 DEAD MARKET
        # =============================================

        if ratio < 0.58:
            return -0.14, "DEAD MARKET"

        # =============================================
        # 🔥 HEALTHY EXPANSION
        # =============================================

        if (
            ratio >= 1.05
            and ratio <= 1.8
        ):
            return 0.06, "HEALTHY EXPANSION"

        # =============================================
        # 🔥 CHAOTIC VOLATILITY
        # =============================================

        if ratio > 2.2:
            return -0.08, "CHAOTIC VOLATILITY"

        # =============================================
        # 🔥 OVERHEATED VOLATILITY
        # =============================================

        if ratio > 1.8:
            return -0.03, "OVERHEATED EXPANSION"

        return 0.0, None

    # =================================================
    # 🔥 CONFIDENCE LABEL
    # =================================================

    def _label(self, score):

        if score >= self.high_confidence:
            return "HIGH"

        if score >= self.medium_confidence:
            return "MEDIUM"

        return "LOW"

    # =================================================
    # 🔥 MAIN ANALYSIS ENGINE
    # =================================================

    def analyze(
        self,
        df,
        momentum_dir,
        momentum_strength,
        base_context
    ):

        closes = df["close"].values
        highs = df["high"].values
        lows = df["low"].values

        # =============================================
        # 🔥 SAFETY
        # =============================================

        if len(closes) < 10:

            return {
                "confidence_score": 0.3,
                "confidence_label": "LOW",

                "short_trend": "range",
                "mid_trend": "range",
                "long_trend": "range",

                "reasons": ["LOW DATA"]
            }

        # =============================================
        # 🔥 NO CLEAR MOMENTUM
        # =============================================

        if momentum_dir not in ["up", "down"]:

            return {
                "confidence_score": 0.32,
                "confidence_label": "LOW",

                "short_trend": "range",
                "mid_trend": "range",
                "long_trend": "range",

                "reasons": ["NO MOMENTUM"]
            }

        # =============================================
        # 🔥 TREND LAYERS
        # =============================================

        short_trend, short_strength = (
            self._trend_score(closes, 6)
        )

        mid_trend, mid_strength = (
            self._trend_score(closes, 20)
        )

        long_trend, long_strength = (
            self._trend_score(closes, 80)
        )

        # =============================================
        # 🔥 VOLATILITY
        # =============================================

        vol = self._volatility(
            highs,
            lows
        )

        avg_vol = float(
            np.mean(highs - lows)
        )

        # =============================================
        # 🔥 BASE SCORE
        # =============================================

        score = 0.5

        reasons = []

        # =============================================
        # 🔥 SHORT LAYER
        # =============================================

        s, r = self._score_layer(
            short_trend,
            short_strength,
            self.w_short,
            momentum_dir,
            "SHORT"
        )

        score += s
        reasons.append(r)

        # =============================================
        # 🔥 MID LAYER
        # =============================================

        s, r = self._score_layer(
            mid_trend,
            mid_strength,
            self.w_mid,
            momentum_dir,
            "MID"
        )

        score += s
        reasons.append(r)

        # =============================================
        # 🔥 LONG LAYER
        # =============================================

        s, r = self._score_layer(
            long_trend,
            long_strength,
            self.w_long,
            momentum_dir,
            "LONG"
        )

        score += s
        reasons.append(r)

        # =============================================
        # 🔥 MOMENTUM BOOST
        # =============================================

        if momentum_strength >= 0.72:

            score += 0.14

            reasons.append(
                "STRONG MOMENTUM"
            )

        elif momentum_strength >= 0.6:

            score += 0.08

            reasons.append(
                "GOOD MOMENTUM"
            )

        elif momentum_strength < 0.48:

            score -= 0.08

            reasons.append(
                "WEAK MOMENTUM"
            )

        # =============================================
        # 🔥 ZONE INTELLIGENCE
        # =============================================

        zone = base_context.get("zone")

        if (
            momentum_dir == "up"
            and zone == "high"
        ):

            score -= 0.14

            reasons.append(
                "BUYING INTO RESISTANCE"
            )

        elif (
            momentum_dir == "down"
            and zone == "low"
        ):

            score -= 0.14

            reasons.append(
                "SELLING INTO SUPPORT"
            )

        elif (
            momentum_dir == "up"
            and zone == "low"
        ):

            score += 0.06

            reasons.append(
                "GOOD BUY ZONE"
            )

        elif (
            momentum_dir == "down"
            and zone == "high"
        ):

            score += 0.06

            reasons.append(
                "GOOD SELL ZONE"
            )

        # =============================================
        # 🔥 BREAKOUT INTELLIGENCE
        # =============================================

        if base_context.get("breakout"):

            breakout_score, breakout_reason = (
                self._breakout_score(
                    highs,
                    lows,
                    avg_vol
                )
            )

            score += breakout_score

            reasons.append(
                breakout_reason
            )

        # =============================================
        # 🔥 VOLATILITY FILTER
        # =============================================

        vol_adj, vol_reason = (
            self._volatility_adjustment(
                vol,
                avg_vol
            )
        )

        score += vol_adj

        if vol_reason:
            reasons.append(vol_reason)

        # =============================================
        # 🔥 TREND CONSISTENCY
        # =============================================

        aligned_count = sum([
            short_trend == momentum_dir,
            mid_trend == momentum_dir,
            long_trend == momentum_dir
        ])

        range_count = sum([
            short_trend == "range",
            mid_trend == "range",
            long_trend == "range"
        ])

        if aligned_count == 3:

            score += 0.08

            reasons.append(
                "FULL ALIGNMENT"
            )

        elif aligned_count == 2:

            score += 0.03

            reasons.append(
                "PARTIAL ALIGNMENT"
            )

        elif aligned_count == 0:

            score -= 0.16

            reasons.append(
                "FULL MISALIGNMENT"
            )

        # =============================================
        # 🔥 FRAGMENTATION DETECTION
        # =============================================

        if range_count >= 2:

            score -= 0.08

            reasons.append(
                "FRAGMENTED STRUCTURE"
            )

        # 🔥 mixed structural environment
        if (
            aligned_count == 1
            and range_count >= 1
        ):

            score -= 0.06

            reasons.append(
                "MIXED CONTEXT"
            )

        # =============================================
        # 🔥 FINAL CLAMP
        # =============================================

        score = max(
            0.0,
            min(1.0, score)
        )

        # =============================================
        # 🔥 LABEL
        # =============================================

        label = self._label(score)

        # =============================================
        # 🔥 OUTPUT
        # =============================================

        return {
            "confidence_score": round(
                float(score),
                3
            ),

            "confidence_label": label,

            "short_trend": short_trend,
            "mid_trend": mid_trend,
            "long_trend": long_trend,

            "reasons": reasons
        }

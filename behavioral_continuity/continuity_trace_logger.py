import json
import os
import time


class ContinuityTraceLogger:

    """
    Passive behavioral continuity trace recorder.

    Responsibilities:
    - Persist semantic continuity observations
    - Preserve chronological behavioral evolution
    - Produce research-friendly trace archives
    - Remain fully observational

    This layer does NOT:
    - modify lifecycle state
    - influence execution
    - generate predictions
    - optimize behavior
    """

    # ==================================================
    # 🔥 INIT
    # ==================================================

    def __init__(self):

        self.base_path = (
            "observability/continuity_traces"
        )

        os.makedirs(
            self.base_path,
            exist_ok=True
        )

    # ==================================================
    # 🔥 LOG OBSERVATION
    # ==================================================

    def log_observation(
        self,
        observation
    ):

        current_time = time.time()

        readable_time = time.strftime(
            "%Y-%m-%d %H:%M:%S",
            time.gmtime(current_time)
        )

        semantic_trace = {

            # ==========================================
            # 🔥 CORE
            # ==========================================

            "timestamp":
                current_time,

            "datetime":
                readable_time,

            "trade_id":
                observation.get(
                    "trade_id"
                ),

            "symbol":
                observation.get(
                    "symbol"
                ),

            "direction":
                observation.get(
                    "direction"
                ),

            "trade_type":
                observation.get(
                    "trade_type"
                ),

            # ==========================================
            # 🔥 CONTINUITY
            # ==========================================

            "cycles_alive":
                observation.get(
                    "cycles_alive"
                ),

            "sequence_depth":
                observation.get(
                    "sequence_depth"
                ),

            "current_state":
                observation.get(
                    "current_state"
                ),

            "continuity_pressure":
                observation.get(
                    "continuity_pressure"
                ),

            # ==========================================
            # 🔥 ARCHETYPES
            # ==========================================

            "archetypes":
                observation.get(
                    "archetypes",
                    []
                ),

            # ==========================================
            # 🔥 HUMAN READABLE
            # ==========================================

            "semantic_summary":
                self._build_summary(
                    observation
                )
        }

        self._persist_trace(
            semantic_trace
        )

    # ==================================================
    # 🔥 BUILD SUMMARY
    # ==================================================

    def _build_summary(
        self,
        observation
    ):

        symbol = observation.get(
            "symbol",
            "UNKNOWN"
        )

        archetypes = observation.get(
            "archetypes",
            []
        )

        current_state = observation.get(
            "current_state",
            "UNKNOWN"
        )

        cycles_alive = observation.get(
            "cycles_alive",
            0
        )

        continuity_pressure = observation.get(
            "continuity_pressure",
            0
        )

        # ==============================================
        # 🔥 ARCHETYPE TEXT
        # ==============================================

        if archetypes:

            archetype_text = (
                ", ".join(archetypes)
            )

        else:

            archetype_text = (
                "NO_DOMINANT_PATTERN"
            )

        # ==============================================
        # 🔥 PRESSURE TEXT
        # ==============================================

        if continuity_pressure >= 0.7:

            pressure_text = (
                "high continuity pressure"
            )

        elif continuity_pressure >= 0.4:

            pressure_text = (
                "moderate continuity pressure"
            )

        else:

            pressure_text = (
                "stable continuity pressure"
            )

        # ==============================================
        # 🔥 SUMMARY
        # ==============================================

        summary = (

            f"{symbol} exhibiting "
            f"{archetype_text} "

            f"while maintaining "

            f"{current_state} persistence "

            f"across {cycles_alive} cycles "

            f"under {pressure_text}."
        )

        return summary

    # ==================================================
    # 🔥 PERSIST TRACE
    # ==================================================

    def _persist_trace(
        self,
        trace
    ):

        current_date = time.strftime(
            "%Y-%m-%d",
            time.gmtime()
        )

        path = (
            f"{self.base_path}/"
            f"{current_date}.jsonl"
        )

        with open(
            path,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                json.dumps(trace)
            )

            f.write("\n")

    # ==================================================
    # 🔥 EXPORT FRIENDLY VIEW
    # ==================================================

    def build_review_view(
        self,
        traces
    ):

        review = []

        for trace in traces:

            review.append({

                "datetime":
                    trace.get(
                        "datetime"
                    ),

                "symbol":
                    trace.get(
                        "symbol"
                    ),

                "archetypes":
                    trace.get(
                        "archetypes",
                        []
                    ),

                "state":
                    trace.get(
                        "current_state"
                    ),

                "summary":
                    trace.get(
                        "semantic_summary"
                    )
            })

        return review

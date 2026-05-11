# observability/tactical_memory_sink.py

import json
import os

from datetime import datetime, timezone


class TacticalMemorySink:

    """
    Passive semantic tactical memory sink.

    Responsibilities:
    - Preserve tactical semantic observations
    - Append event-based JSONL traces
    - Remain fully isolated from:
        - execution authority
        - lifecycle logic
        - adaptive behavior
        - scoring systems
        - analytics infrastructure

    Important:
    - Append-only
    - Read-only
    - Zero-authority
    - No feedback loops
    """

    # ==================================================
    # 🔥 INIT
    # ==================================================

    def __init__(self):

        self.base_path = (
            "observability/memory"
        )

        self.file_name = (
            "tactical_range_memory.jsonl"
        )

        os.makedirs(
            self.base_path,
            exist_ok=True
        )

    # ==================================================
    # 🔥 STORE EVENT
    # ==================================================

    def store_event(
        self,
        symbol,
        signal,
        range_confidence,
        rotation_stability,
        context_state,
        rotational_behavior
    ):

        """
        Append semantic tactical observation.

        Important:
        - No interpretation mutation
        - No ranking
        - No filtering
        - No execution influence
        """

        timestamp = time_now()

        event = {

            # ======================================
            # 🔥 TEMPORAL
            # ======================================

            "timestamp":
                timestamp,

            "datetime":
                utc_datetime(),

            # ======================================
            # 🔥 CORE
            # ======================================

            "symbol":
                symbol,

            "signal":
                signal,

            "range_confidence":
                round(
                    float(range_confidence),
                    3
                ),

            # ======================================
            # 🔥 SEMANTICS
            # ======================================

            "rotation_stability":
                rotation_stability,

            "context_state":
                context_state,

            "rotational_behavior":
                rotational_behavior
        }

        file_path = (
            f"{self.base_path}/"
            f"{self.file_name}"
        )

        with open(
            file_path,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                json.dumps(
                    event,
                    ensure_ascii=False
                )
                + "\n"
            )


# ======================================================
# 🔥 HELPERS
# ======================================================

def time_now():

    return round(
        datetime.now(
            timezone.utc
        ).timestamp(),
        3
    )


def utc_datetime():

    return datetime.now(
        timezone.utc
    ).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )

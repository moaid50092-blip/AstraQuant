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

    def store_event(self, event):

        """
        Append semantic tactical observation.

        Important:
        - No interpretation mutation
        - No ranking
        - No filtering
        - No execution influence
        """

        normalized_event = {

            # ======================================
            # 🔥 TEMPORAL
            # ======================================

            "timestamp":
                time_now(),

            "datetime":
                utc_datetime(),

            # ======================================
            # 🔥 CORE
            # ======================================

            "symbol":
                event.get("symbol"),

            "signal":
                event.get("signal"),

            "range_confidence":
                round(
                    float(
                        event.get(
                            "confidence",
                            0
                        )
                    ),
                    3
                ),

            # ======================================
            # 🔥 SEMANTICS
            # ======================================

            "rotation_stability":
                event.get(
                    "rotation_stability"
                ),

            "context_state":
                event.get(
                    "context_state"
                ),

            "rotational_behavior":
                event.get(
                    "rotational_behavior"
                )
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
                    normalized_event,
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

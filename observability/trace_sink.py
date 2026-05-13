# observability/trace_sink.py

import os
import json
import time


TRACE_DIR = "observability/traces"


def _ensure_trace_directory():

    os.makedirs(
        TRACE_DIR,
        exist_ok=True
    )


def append_trace(trace):

    """
    Passive behavioral persistence.

    Important:
    - Append-only
    - No interpretation
    - No analytics
    - No execution influence
    - No lifecycle authority
    """

    try:

        _ensure_trace_directory()

        filename = (
            f"{time.strftime('%Y-%m-%d')}.jsonl"
        )

        filepath = os.path.join(
            TRACE_DIR,
            filename
        )

        # -----------------------------------
        # DEBUG VISIBILITY
        # -----------------------------------

        print(
            "\n[TRACE FILE]",
            os.path.abspath(filepath)
        )

        print(
            "[TRACE APPEND]",
            json.dumps(
                trace,
                ensure_ascii=False
            )
        )

        # -----------------------------------

        with open(
            filepath,
            "a",
            encoding="utf-8"
        ) as trace_file:

            trace_file.write(
                json.dumps(
                    trace,
                    ensure_ascii=False
                )
                + "\n"
            )

    except Exception as e:

        # observability must NEVER
        # affect runtime behavior

        print(
            "[TRACE ERROR]",
            str(e)
        )

        pass

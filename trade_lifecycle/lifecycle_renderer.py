# trade_lifecycle/lifecycle_renderer.py


def render_lifecycle_events(
    lifecycle_events
):

    """
    Pure lifecycle presentation layer.

    Responsibilities:
    - Render lifecycle transitions
    - Display deterioration visibility
    - Display continuity state
    - Keep execution environment readable

    This layer does NOT:
    - think
    - interpret market
    - mutate signals
    - control execution
    """

    if not lifecycle_events:
        return

    print("\n=== Trade Lifecycle ===")

    for event in lifecycle_events:

        event_type = event.get("type")

        # ==========================================
        # 🔥 TRADE CREATED
        # ==========================================

        if event_type == "TRADE_CREATED":

            symbol = event.get(
                "symbol",
                "UNKNOWN"
            )

            direction = event.get(
                "direction",
                "?"
            )

            trade_type = event.get(
                "trade_type",
                "UNKNOWN"
            )

            entry_type = event.get(
                "entry_type",
                "STANDARD"
            )

            probability = event.get(
                "probability",
                0
            )

            print(
                f"🟢 OPENED | "
                f"{symbol} | "
                f"{direction.upper()} | "
                f"{trade_type} | "
                f"{entry_type} | "
                f"conviction={probability}"
            )

        # ==========================================
        # 🔥 EXIT WATCH
        # ==========================================

        elif event_type == "EXIT_WATCH":

            symbol = event.get(
                "symbol",
                "UNKNOWN"
            )

            trade_type = event.get(
                "trade_type",
                "UNKNOWN"
            )

            deterioration = event.get(
                "deterioration",
                0
            )

            weak_cycles = event.get(
                "weak_cycles",
                0
            )

            probability = event.get(
                "probability",
                0
            )

            print(
                f"🟡 EXIT WATCH | "
                f"{symbol} | "
                f"{trade_type} | "
                f"conviction={probability} | "
                f"deterioration={deterioration} | "
                f"weak_cycles={weak_cycles}"
            )

        # ==========================================
        # 🔥 EXIT CONFIRMED
        # ==========================================

        elif event_type == "EXIT_CONFIRMED":

            symbol = event.get(
                "symbol",
                "UNKNOWN"
            )

            trade_type = event.get(
                "trade_type",
                "UNKNOWN"
            )

            direction = event.get(
                "direction",
                "?"
            )

            held_cycles = event.get(
                "held_cycles",
                0
            )

            peak_probability = event.get(
                "peak_probability",
                0
            )

            final_probability = event.get(
                "final_probability",
                0
            )

            reason = event.get(
                "reason",
                "unknown"
            )

            print(
                f"🔴 EXIT | "
                f"{symbol} | "
                f"{direction.upper()} | "
                f"{trade_type} | "
                f"held={held_cycles} cycles | "
                f"peak={peak_probability} | "
                f"final={final_probability} | "
                f"reason={reason}"
            )

        # ==========================================
        # 🔥 RECOVERY
        # ==========================================

        elif event_type == "TRADE_RECOVERED":

            symbol = event.get(
                "symbol",
                "UNKNOWN"
            )

            trade_type = event.get(
                "trade_type",
                "UNKNOWN"
            )

            probability = event.get(
                "probability",
                0
            )

            print(
                f"🔵 RECOVERED | "
                f"{symbol} | "
                f"{trade_type} | "
                f"conviction={probability}"
            )

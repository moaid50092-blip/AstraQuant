def analyze(self, df, momentum=None, strength=0.0):

    if df is None or len(df) < 5:  # 🔥 بدل 20
        return self._empty()

    # 🔥 adaptive lookback
    lookback = min(self.lookback, len(df))

    highs = df["high"].values[-lookback:]
    lows = df["low"].values[-lookback:]
    closes = df["close"].values

    current_price = closes[-1]

    # -----------------------------
    # Trend (مرن)
    # -----------------------------
    recent_closes = closes[-min(5, len(closes)):]

    if len(recent_closes) >= 3:
        if all(x < y for x, y in zip(recent_closes, recent_closes[1:])):
            trend = "up"
        elif all(x > y for x, y in zip(recent_closes, recent_closes[1:])):
            trend = "down"
        else:
            trend = "range"
    else:
        trend = "range"

    # -----------------------------
    # Zone
    # -----------------------------
    highest = np.max(highs)
    lowest = np.min(lows)

    range_size = highest - lowest if highest != lowest else 1
    position = (current_price - lowest) / range_size

    if position <= 0.3:
        zone = "low"
    elif position >= 0.7:
        zone = "high"
    else:
        zone = "middle"

    # -----------------------------
    # Breakout
    # -----------------------------
    if len(highs) >= 2:
        prev_high = np.max(highs[:-1])
        prev_low = np.min(lows[:-1])

        breakout_up = current_price > prev_high
        breakout_down = current_price < prev_low
    else:
        breakout_up = breakout_down = False

    breakout = breakout_up or breakout_down

    # -----------------------------
    # Setup
    # -----------------------------
    setup = "unknown"

    if momentum is not None:

        if momentum == "up":
            if strength >= 0.6 and breakout_up:
                setup = "real"
            elif strength >= 0.4:
                setup = "weak"
            else:
                setup = "fake"

        elif momentum == "down":
            if strength >= 0.6 and breakout_down:
                setup = "real"
            elif strength >= 0.4:
                setup = "weak"
            else:
                setup = "fake"

        else:
            setup = "fake"

    return {
        "trend": trend,
        "zone": zone,
        "breakout": breakout,
        "setup": setup
    }

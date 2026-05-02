# context/mtf_analyzer.py

class MTFAnalyzer:

    def __init__(self):
        pass

    def analyze(self, df_1m, df_5m, df_15m):

        def get_trend(df):
            if df is None or len(df) < 5:
                return "unknown"

            closes = df["close"].values[-5:]

            if all(x < y for x, y in zip(closes, closes[1:])):
                return "up"
            elif all(x > y for x, y in zip(closes, closes[1:])):
                return "down"
            else:
                return "range"

        trend_1m = get_trend(df_1m)
        trend_5m = get_trend(df_5m)
        trend_15m = get_trend(df_15m)

        # -----------------------------------------
        # Alignment Logic
        # -----------------------------------------

        if trend_1m == trend_5m == trend_15m:
            alignment = "strong"
        elif trend_1m == trend_5m:
            alignment = "medium"
        else:
            alignment = "weak"

        return {
            "trend_1m": trend_1m,
            "trend_5m": trend_5m,
            "trend_15m": trend_15m,
            "alignment": alignment
        }

from collections import defaultdict


class EdgeTracker:

    def __init__(self):

        # تخزين البيانات
        self.trades = []

        # تجميع حسب السكور
        self.buckets = defaultdict(lambda: {
            "total": 0,
            "wins": 0,
            "losses": 0
        })

    # -------------------------------------------------
    # 🧠 تسجيل الصفقة
    # -------------------------------------------------
    def log_trade(self, signal):

        trade = {
            "symbol": signal.get("symbol"),
            "score": signal.get("score"),
            "probability": signal.get("probability"),
            "confidence": signal.get("confidence_label"),
            "mode": signal.get("mode"),
            "direction": signal.get("direction"),
            "result": None  # سيتم تحديثها لاحقًا
        }

        self.trades.append(trade)

        return len(self.trades) - 1  # trade_id

    # -------------------------------------------------
    # 🎯 تحديث نتيجة الصفقة
    # -------------------------------------------------
    def update_result(self, trade_id, result):

        if trade_id >= len(self.trades):
            return

        trade = self.trades[trade_id]
        trade["result"] = result

        bucket_key = self._score_bucket(trade["score"])

        self.buckets[bucket_key]["total"] += 1

        if result == "WIN":
            self.buckets[bucket_key]["wins"] += 1
        else:
            self.buckets[bucket_key]["losses"] += 1

    # -------------------------------------------------
    # 📊 تقسيم السكور (هنا السحر)
    # -------------------------------------------------
    def _score_bucket(self, score):

        if score is None:
            return "unknown"

        # 🔥 نطاقات ذكية
        if score < 2:
            return "0-2"
        elif score < 4:
            return "2-4"
        elif score < 6:
            return "4-6"
        elif score < 8:
            return "6-8"
        else:
            return "8+"

    # -------------------------------------------------
    # 📈 استخراج الإحصائيات
    # -------------------------------------------------
    def get_statistics(self):

        report = {}

        for bucket, data in self.buckets.items():

            total = data["total"]
            wins = data["wins"]

            winrate = (wins / total) if total > 0 else 0

            report[bucket] = {
                "total_trades": total,
                "wins": wins,
                "losses": data["losses"],
                "winrate": round(winrate, 3)
            }

        return report

    # -------------------------------------------------
    # 🔥 كشف الـ Edge الحقيقي
    # -------------------------------------------------
    def detect_edges(self, min_trades=10, min_winrate=0.6):

        edges = []

        for bucket, data in self.buckets.items():

            total = data["total"]
            wins = data["wins"]

            if total < min_trades:
                continue

            winrate = wins / total

            if winrate >= min_winrate:
                edges.append({
                    "bucket": bucket,
                    "winrate": round(winrate, 3),
                    "trades": total
                })

        return edges

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class AlertEngine:
    def __init__(self):
        self.window_minutes = 30
        self.threshold_zscore = 3
        self.data = pd.DataFrame(columns=["timestamp", "status", "count"])

    def add_event(self, timestamp, status, count):
        row = {
            "timestamp": timestamp,
            "status": status,
            "count": count
        }

        self.data = pd.concat(
            [self.data, pd.DataFrame([row])],
            ignore_index=True
        )

        cutoff = datetime.utcnow() - timedelta(minutes=self.window_minutes)
        self.data = self.data[self.data["timestamp"] >= cutoff]

    def check_anomaly(self, status):
        df = self.data[self.data["status"] == status]

        if len(df) < 10:
            return False, None

        mean = df["count"].mean()
        std = df["count"].std()

        if std is None or std == 0:
            return False, None

        current = df.iloc[-1]["count"]
        zscore = (current - mean) / std

        if zscore >= self.threshold_zscore:
            return True, {
                "mean": round(mean, 2),
                "std": round(std, 2),
                "current": current,
                "zscore": round(zscore, 2)
            }

        return False, None

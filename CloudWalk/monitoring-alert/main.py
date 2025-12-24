from fastapi import FastAPI
from models import TransactionEvent, AlertResponse
from alert_engine import AlertEngine
import logging

app = FastAPI(title="Transaction Monitoring Alert System")

engine = AlertEngine()

logging.basicConfig(level=logging.INFO)

ALERT_STATUSES = ["failed", "denied", "reversed"]

@app.post("/monitor/transaction", response_model=AlertResponse)
def monitor_transaction(event: TransactionEvent):
    engine.add_event(event.timestamp, event.status, event.count)

    if event.status in ALERT_STATUSES:
        is_anomaly, details = engine.check_anomaly(event.status)

        if is_anomaly:
            logging.error(
                f"🚨 ALERT [{event.status.upper()}] | "
                f"count={details['current']} | "
                f"zscore={details['zscore']}"
            )

            return AlertResponse(
                alert=True,
                reason=f"{event.status} transactions above normal",
                severity="high"
            )

    return AlertResponse(alert=False)

@app.get("/metrics")
def get_metrics():
    """
    Endpoint usado por dashboards / gráficos em tempo real
    """
    return engine.data.groupby(["status"]).tail(10).to_dict(orient="records")

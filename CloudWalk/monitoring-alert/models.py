from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionEvent(BaseModel):
    timestamp: datetime
    status: str  # approved, failed, denied, reversed
    count: int

class AlertResponse(BaseModel):
    alert: bool
    reason: Optional[str] = None
    severity: Optional[str] = None

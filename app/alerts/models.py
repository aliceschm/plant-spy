from dataclasses import dataclass
from datetime import datetime


ALERT_STATUS_OPEN = "open"
ALERT_STATUS_ACKNOWLEDGED = "acknowledged"
ALERT_STATUS_RESOLVED = "resolved"

ALERT_SEVERITY_LOW = "low"
ALERT_SEVERITY_MEDIUM = "medium"
ALERT_SEVERITY_HIGH = "high"


@dataclass
class Alert:
    id: str
    component_id: str
    reading_id: str
    anomaly_type: str
    severity: str
    occurrence_count: int
    message: str
    status: str
    created_at: datetime


@dataclass
class AnomalyState:
    component_id: str
    anomaly_type: str
    occurrence_count: int
    last_reading_id: str
    alert_id: str | None
    created_at: datetime
    updated_at: datetime
from dataclasses import dataclass
from datetime import datetime


ALERT_STATUS_OPEN = "open"
ALERT_STATUS_ACKNOWLEDGED = "acknowledged"
ALERT_STATUS_RESOLVED = "resolved"


@dataclass
class Alert:
    id: str
    component_id: str
    reading_id: str
    message: str
    status: str
    created_at: datetime
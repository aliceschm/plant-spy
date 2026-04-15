from dataclasses import dataclass
from datetime import datetime


WORK_ORDER_STATUS_OPEN = "open"
WORK_ORDER_STATUS_IN_PROGRESS = "in_progress"
WORK_ORDER_STATUS_DONE = "done"
WORK_ORDER_STATUS_CANCELED = "canceled"


@dataclass
class WorkOrder:
    id: str
    alert_id: str
    title: str
    description: str
    status: str
    created_at: datetime
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Reading:
    id: str
    component_id: str
    recorded_at: datetime
    value: float
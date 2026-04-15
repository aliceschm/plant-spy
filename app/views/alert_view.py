from dataclasses import dataclass


@dataclass
class AlertView:
    alert_id: str
    component_id: str
    message: str
    status: str
    path: str
from dataclasses import dataclass


@dataclass
class WorkOrderView:
    work_order_id: str
    alert_id: str
    title: str
    description: str
    status: str
    component_id: str
    path: str
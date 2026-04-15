import uuid

from app.alerts.repository import get_alert_by_id
from app.work_orders.models import (
    WORK_ORDER_STATUS_CANCELED,
    WORK_ORDER_STATUS_DONE,
    WORK_ORDER_STATUS_IN_PROGRESS,
    WorkOrder,
)
from app.work_orders.repository import (
    create_work_order,
    exists_work_order_for_alert,
    load_work_orders,
    update_work_order_status,
)


class WorkOrderService:
    def load_work_orders(self) -> list[WorkOrder]:
        return load_work_orders()

    def create_from_alert(self, alert_id: str) -> bool:
        alert = get_alert_by_id(alert_id)

        if alert is None:
            return False

        if exists_work_order_for_alert(alert_id):
            return False

        create_work_order(
            work_order_id=str(uuid.uuid4()),
            alert_id=alert.id,
            title=f"Investigate alert for component {alert.component_id}",
            description=alert.message,
        )
        return True

    def start_work_order(self, work_order_id: str) -> bool:
        return update_work_order_status(work_order_id, WORK_ORDER_STATUS_IN_PROGRESS)

    def complete_work_order(self, work_order_id: str) -> bool:
        return update_work_order_status(work_order_id, WORK_ORDER_STATUS_DONE)

    def cancel_work_order(self, work_order_id: str) -> bool:
        return update_work_order_status(work_order_id, WORK_ORDER_STATUS_CANCELED)
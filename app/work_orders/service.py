import uuid

from app.alerts.repository import get_alert_by_id
from app.hierarchy.service import HierarchyService
from app.views.work_order_view import WorkOrderView
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
    def __init__(self) -> None:
        self.hierarchy_service = HierarchyService()

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

    def get_work_order_views(self) -> list[WorkOrderView]:
        work_orders = self.load_work_orders()
        views: list[WorkOrderView] = []

        for work_order in work_orders:
            alert = get_alert_by_id(work_order.alert_id)

            if alert is None:
                continue

            path = self.hierarchy_service.get_path_string_for_node(
                alert.component_id
            )

            views.append(
                WorkOrderView(
                    work_order_id=work_order.id,
                    alert_id=work_order.alert_id,
                    title=work_order.title,
                    description=work_order.description,
                    status=work_order.status,
                    component_id=alert.component_id,
                    path=path,
                )
            )

        return views

    def get_work_order_views_by_node(self, node_id: str) -> list[WorkOrderView]:
        component_ids = self.hierarchy_service.get_component_ids_in_subtree(node_id)
        views: list[WorkOrderView] = []

        for work_order_view in self.get_work_order_views():
            if work_order_view.component_id not in component_ids:
                continue

            views.append(work_order_view)

        return views
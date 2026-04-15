from app.alerts.models import (
    ALERT_STATUS_ACKNOWLEDGED,
    ALERT_STATUS_OPEN,
    ALERT_STATUS_RESOLVED,
    Alert,
)
from app.alerts.repository import load_alerts, load_open_alerts, update_alert_status
from app.hierarchy.service import HierarchyService
from app.views.alert_view import AlertView

class AlertService:
    def __init__(self) -> None:
        self.hierarchy_service = HierarchyService()

    def load_alerts(self) -> list[Alert]:
        return load_alerts()

    def load_open_alerts(self) -> list[Alert]:
        return load_open_alerts()

    def acknowledge_alert(self, alert_id: str) -> bool:
        return update_alert_status(alert_id, ALERT_STATUS_ACKNOWLEDGED)

    def resolve_alert(self, alert_id: str) -> bool:
        return update_alert_status(alert_id, ALERT_STATUS_RESOLVED)
    
    def get_alert_views(self) -> list[AlertView]:
        alerts = self.load_alerts()

        views = []

        for alert in alerts:
            path = self.hierarchy_service.get_path_string_for_node(
                alert.component_id
            )

            views.append(
                AlertView(
                    alert_id=alert.id,
                    component_id=alert.component_id,
                    message=alert.message,
                    status=alert.status,
                    path=path,
                )
            )

        return views
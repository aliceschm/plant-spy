from app.alerts.models import (
    ALERT_STATUS_ACKNOWLEDGED,
    ALERT_STATUS_OPEN,
    ALERT_STATUS_RESOLVED,
    Alert,
)
from app.alerts.repository import load_alerts, load_open_alerts, update_alert_status


class AlertService:
    def load_alerts(self) -> list[Alert]:
        return load_alerts()

    def load_open_alerts(self) -> list[Alert]:
        return load_open_alerts()

    def acknowledge_alert(self, alert_id: str) -> bool:
        return update_alert_status(alert_id, ALERT_STATUS_ACKNOWLEDGED)

    def resolve_alert(self, alert_id: str) -> bool:
        return update_alert_status(alert_id, ALERT_STATUS_RESOLVED)
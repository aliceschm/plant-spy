import uuid

from app.alerts.models import (
    ALERT_STATUS_ACKNOWLEDGED,
    ALERT_STATUS_RESOLVED,
    Alert,
)
from app.alerts.repository import (
    create_alert,
    get_alert_by_id,
    get_open_alert_by_component_and_anomaly,
    load_alerts,
    load_open_alerts,
    update_alert_details,
    update_alert_status,
)
from app.alerts.rules import build_alert_message, calculate_severity
from app.hierarchy.service import HierarchyService
from app.shared.event_bus import event_bus
from app.shared.events import AlertCreated, AnomalyDetected
from app.views.alert_view import AlertView


class AlertService:
    """Application service for alert lifecycle, event reactions, and alert queries."""

    def __init__(self) -> None:
        self.hierarchy_service = HierarchyService()

    # Core alert lifecycle

    def load_alerts(self) -> list[Alert]:
        return load_alerts()

    def load_open_alerts(self) -> list[Alert]:
        return load_open_alerts()

    def acknowledge_alert(self, alert_id: str) -> bool:
        return update_alert_status(alert_id, ALERT_STATUS_ACKNOWLEDGED)

    def resolve_alert(self, alert_id: str) -> bool:
        return update_alert_status(alert_id, ALERT_STATUS_RESOLVED)

    # Event handlers

    def handle_anomaly_detected(self, event: AnomalyDetected) -> None:
        existing_alert = get_open_alert_by_component_and_anomaly(
            event.component_id,
            event.anomaly_type,
        )

        if existing_alert is None:
            occurrence_count = 1
            severity = calculate_severity(occurrence_count)
            message = build_alert_message(event.anomaly_type, event.value)
            alert_id = str(uuid.uuid4())

            create_alert(
                alert_id=alert_id,
                component_id=event.component_id,
                reading_id=event.reading_id,
                anomaly_type=event.anomaly_type,
                severity=severity,
                occurrence_count=occurrence_count,
                message=message,
            )

            event_bus.publish(
                AlertCreated(
                    alert_id=alert_id,
                    component_id=event.component_id,
                    reading_id=event.reading_id,
                    severity=severity,
                )
            )
            return

        occurrence_count = existing_alert.occurrence_count + 1
        severity = calculate_severity(occurrence_count)
        message = build_alert_message(event.anomaly_type, event.value)

        update_alert_details(
            alert_id=existing_alert.id,
            reading_id=event.reading_id,
            severity=severity,
            occurrence_count=occurrence_count,
            message=message,
        )

    def register_event_handlers(self) -> None:
        event_bus.subscribe(AnomalyDetected, self.handle_anomaly_detected)

    # Read models / contextual queries

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

    def get_alert_views_by_node(self, node_id: str) -> list[AlertView]:
        component_ids = self.hierarchy_service.get_component_ids_in_subtree(
            node_id
        )

        alerts = self.load_alerts()
        views = []

        for alert in alerts:
            if alert.component_id not in component_ids:
                continue

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
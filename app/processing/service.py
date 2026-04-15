import uuid

from app.alerts.repository import exists_open_alert_for_component
from app.hierarchy.service import HierarchyService
from app.processing.rules import build_alert_message, is_anomalous
from app.readings.repository import load_latest_readings_by_component
from app.shared.event_bus import event_bus
from app.shared.events import AnomalyDetected


class ProcessingService:
    def __init__(self) -> None:
        self.hierarchy_service = HierarchyService()

    def process_latest_readings(self) -> None:
        components = self.hierarchy_service.load_components()
        components_by_id = {component.id: component for component in components}

        latest_readings = load_latest_readings_by_component()

        for reading in latest_readings:
            component = components_by_id.get(reading.component_id)

            if component is None:
                continue

            if not is_anomalous(component.sensor_type, reading):
                continue

            if exists_open_alert_for_component(component.id):
                continue

            message = build_alert_message(component.sensor_type, reading)

            event_bus.publish(
                AnomalyDetected(
                    component_id=component.id,
                    reading_id=reading.id,
                    message=message,
                )
            )
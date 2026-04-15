import uuid

from app.alerts.repository import create_alert
from app.hierarchy.service import HierarchyService
from app.processing.rules import build_alert_message, is_anomalous
from app.readings.repository import load_latest_readings_by_component


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

            message = build_alert_message(component.sensor_type, reading)

            create_alert(
                alert_id=str(uuid.uuid4()),
                component_id=component.id,
                reading_id=reading.id,
                message=message,
            )
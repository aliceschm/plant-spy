from app.hierarchy.service import HierarchyService
from app.processing.rules import build_alert_message, is_anomalous
from app.readings.repository import load_reading_by_id
from app.shared.event_bus import event_bus
from app.shared.events import AnomalyDetected, ReadingRecorded


class ProcessingService:
    """Application service for evaluating recorded readings and publishing anomalies."""

    def __init__(self) -> None:
        self.hierarchy_service = HierarchyService()

    def handle_reading_recorded(self, event: ReadingRecorded) -> None:
        reading = load_reading_by_id(event.reading_id)

        if reading is None:
            return

        component = self.hierarchy_service.get_component_by_id(reading.component_id)

        if component is None:
            return

        if not is_anomalous(component.sensor_type, reading):
            return

        message = build_alert_message(component.sensor_type, reading)

        event_bus.publish(
            AnomalyDetected(
                component_id=component.id,
                reading_id=reading.id,
                message=message,
            )
        )

    def register_event_handlers(self) -> None:
        event_bus.subscribe(ReadingRecorded, self.handle_reading_recorded)
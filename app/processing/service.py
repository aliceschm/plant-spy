from app.hierarchy.service import HierarchyService
from app.processing.rules import get_anomaly_type
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

        anomaly_type = get_anomaly_type(component.sensor_type, reading)

        if anomaly_type is None:
            return

        event_bus.publish(
            AnomalyDetected(
                component_id=component.id,
                reading_id=reading.id,
                anomaly_type=anomaly_type,
                value=reading.value,
            )
        )

    def register_event_handlers(self) -> None:
        event_bus.subscribe(ReadingRecorded, self.handle_reading_recorded)
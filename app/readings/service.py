import uuid
from datetime import datetime

from app.readings.models import Reading
from app.readings.repository import (
    load_latest_readings_by_component,
    load_readings,
    save_reading,
)
from app.shared.event_bus import event_bus
from app.shared.events import ReadingRecorded


class ReadingsService:
    """Application service for recording and querying sensor readings."""

    def load_readings(self) -> list[Reading]:
        return load_readings()

    def load_latest_readings_by_component(self) -> list[Reading]:
        return load_latest_readings_by_component()

    def record_reading(
        self,
        component_id: str,
        value: float,
        recorded_at: datetime | None = None,
    ) -> Reading:
        reading = Reading(
            id=str(uuid.uuid4()),
            component_id=component_id,
            recorded_at=recorded_at or datetime.utcnow(),
            value=value,
        )

        save_reading(reading)

        event_bus.publish(
            ReadingRecorded(
                reading_id=reading.id,
                component_id=reading.component_id,
            )
        )

        return reading
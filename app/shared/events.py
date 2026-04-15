from dataclasses import dataclass

from app.shared.event_bus import Event


@dataclass(frozen=True)
class ReadingRecorded(Event):
    reading_id: str
    component_id: str


@dataclass(frozen=True)
class AnomalyDetected(Event):
    component_id: str
    reading_id: str
    anomaly_type: str
    value: float


@dataclass(frozen=True)
class AlertCreated(Event):
    alert_id: str
    component_id: str
    reading_id: str
    severity: str
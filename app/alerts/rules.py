from app.alerts.models import (
    ALERT_SEVERITY_HIGH,
    ALERT_SEVERITY_LOW,
    ALERT_SEVERITY_MEDIUM,
)


def should_create_alert(occurrence_count: int) -> bool:
    return occurrence_count >= 3


def calculate_severity(occurrence_count: int) -> str:
    if occurrence_count >= 5:
        return ALERT_SEVERITY_HIGH

    if occurrence_count >= 4:
        return ALERT_SEVERITY_MEDIUM

    return ALERT_SEVERITY_LOW


def build_alert_message(anomaly_type: str, value: float) -> str:
    if anomaly_type == "high_vibration":
        return f"High vibration detected: {value}"

    if anomaly_type == "high_energy":
        return f"High energy consumption detected: {value}"

    return f"Anomalous reading detected: {value}"
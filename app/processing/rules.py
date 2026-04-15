from app.hierarchy.models import SENSOR_ENERGY, SENSOR_VIBRATION
from app.readings.models import Reading


def is_anomalous(sensor_type: str, reading: Reading) -> bool:
    if sensor_type == SENSOR_VIBRATION:
        return reading.value > 1.0

    if sensor_type == SENSOR_ENERGY:
        return reading.value > 250.0

    return False


def build_alert_message(sensor_type: str, reading: Reading) -> str:
    if sensor_type == SENSOR_VIBRATION:
        return f"High vibration detected: {reading.value}"

    if sensor_type == SENSOR_ENERGY:
        return f"High energy consumption detected: {reading.value}"

    return f"Anomalous reading detected: {reading.value}"
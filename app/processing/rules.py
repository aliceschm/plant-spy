from app.hierarchy.models import SENSOR_ENERGY, SENSOR_VIBRATION
from app.readings.models import Reading


ANOMALY_TYPE_HIGH_VIBRATION = "high_vibration"
ANOMALY_TYPE_HIGH_ENERGY = "high_energy"


def get_anomaly_type(sensor_type: str, reading: Reading) -> str | None:
    if sensor_type == SENSOR_VIBRATION and reading.value > 1.0:
        return ANOMALY_TYPE_HIGH_VIBRATION

    if sensor_type == SENSOR_ENERGY and reading.value > 250.0:
        return ANOMALY_TYPE_HIGH_ENERGY

    return None


def is_anomalous(sensor_type: str, reading: Reading) -> bool:
    return get_anomaly_type(sensor_type, reading) is not None
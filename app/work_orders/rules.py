from app.alerts.models import ALERT_SEVERITY_HIGH


def should_auto_create_work_order(severity: str) -> bool:
    return severity == ALERT_SEVERITY_HIGH
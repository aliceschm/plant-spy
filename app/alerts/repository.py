from app.alerts.models import (
    ALERT_STATUS_OPEN,
    Alert,
)
from app.shared.db import get_connection


def create_alert(
    alert_id: str,
    component_id: str,
    reading_id: str,
    message: str,
) -> None:
    query = """
        INSERT INTO alerts (id, component_id, reading_id, message, status)
        VALUES (%s, %s, %s, %s, %s);
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                query,
                (alert_id, component_id, reading_id, message, ALERT_STATUS_OPEN),
            )
        conn.commit()


def load_alerts() -> list[Alert]:
    query = """
        SELECT id, component_id, reading_id, message, status, created_at
        FROM alerts
        ORDER BY created_at;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    return [
        Alert(
            id=row[0],
            component_id=row[1],
            reading_id=row[2],
            message=row[3],
            status=row[4],
            created_at=row[5],
        )
        for row in rows
    ]

def exists_open_alert_for_component(component_id: str) -> bool:
    query = """
        SELECT 1
        FROM alerts
        WHERE component_id = %s
          AND status = 'open'
        LIMIT 1;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (component_id,))
            result = cur.fetchone()

    return result is not None
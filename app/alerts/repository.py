from app.alerts.models import (
    ALERT_STATUS_ACKNOWLEDGED,
    ALERT_STATUS_OPEN,
    ALERT_STATUS_RESOLVED,
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


def load_open_alerts() -> list[Alert]:
    query = """
        SELECT id, component_id, reading_id, message, status, created_at
        FROM alerts
        WHERE status = %s
        ORDER BY created_at;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (ALERT_STATUS_OPEN,))
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
          AND status = %s
        LIMIT 1;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (component_id, ALERT_STATUS_OPEN))
            result = cur.fetchone()

    return result is not None


def update_alert_status(alert_id: str, new_status: str) -> bool:
    query = """
        UPDATE alerts
        SET status = %s
        WHERE id = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (new_status, alert_id))
            updated_rows = cur.rowcount
        conn.commit()

    return updated_rows > 0

def get_alert_by_id(alert_id: str) -> Alert | None:
    query = """
        SELECT id, component_id, reading_id, message, status, created_at
        FROM alerts
        WHERE id = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (alert_id,))
            row = cur.fetchone()

    if row is None:
        return None

    return Alert(
        id=row[0],
        component_id=row[1],
        reading_id=row[2],
        message=row[3],
        status=row[4],
        created_at=row[5],
    )
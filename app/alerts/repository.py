from app.alerts.models import (
    ALERT_STATUS_OPEN,
    Alert,
)
from app.shared.db import get_connection


def create_alert(
    alert_id: str,
    component_id: str,
    reading_id: str,
    anomaly_type: str,
    severity: str,
    occurrence_count: int,
    message: str,
) -> None:
    query = """
        INSERT INTO alerts (
            id,
            component_id,
            reading_id,
            anomaly_type,
            severity,
            occurrence_count,
            message,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                query,
                (
                    alert_id,
                    component_id,
                    reading_id,
                    anomaly_type,
                    severity,
                    occurrence_count,
                    message,
                    ALERT_STATUS_OPEN,
                ),
            )
        conn.commit()


def load_alerts() -> list[Alert]:
    query = """
        SELECT
            id,
            component_id,
            reading_id,
            anomaly_type,
            severity,
            occurrence_count,
            message,
            status,
            created_at
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
            anomaly_type=row[3],
            severity=row[4],
            occurrence_count=row[5],
            message=row[6],
            status=row[7],
            created_at=row[8],
        )
        for row in rows
    ]


def load_open_alerts() -> list[Alert]:
    query = """
        SELECT
            id,
            component_id,
            reading_id,
            anomaly_type,
            severity,
            occurrence_count,
            message,
            status,
            created_at
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
            anomaly_type=row[3],
            severity=row[4],
            occurrence_count=row[5],
            message=row[6],
            status=row[7],
            created_at=row[8],
        )
        for row in rows
    ]


def get_open_alert_by_component_and_anomaly(
    component_id: str,
    anomaly_type: str,
) -> Alert | None:
    query = """
        SELECT
            id,
            component_id,
            reading_id,
            anomaly_type,
            severity,
            occurrence_count,
            message,
            status,
            created_at
        FROM alerts
        WHERE component_id = %s
          AND anomaly_type = %s
          AND status = %s
        LIMIT 1;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                query,
                (component_id, anomaly_type, ALERT_STATUS_OPEN),
            )
            row = cur.fetchone()

    if row is None:
        return None

    return Alert(
        id=row[0],
        component_id=row[1],
        reading_id=row[2],
        anomaly_type=row[3],
        severity=row[4],
        occurrence_count=row[5],
        message=row[6],
        status=row[7],
        created_at=row[8],
    )


def update_alert_details(
    alert_id: str,
    reading_id: str,
    severity: str,
    occurrence_count: int,
    message: str,
) -> bool:
    query = """
        UPDATE alerts
        SET reading_id = %s,
            severity = %s,
            occurrence_count = %s,
            message = %s
        WHERE id = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                query,
                (
                    reading_id,
                    severity,
                    occurrence_count,
                    message,
                    alert_id,
                ),
            )
            updated_rows = cur.rowcount
        conn.commit()

    return updated_rows > 0


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
        SELECT
            id,
            component_id,
            reading_id,
            anomaly_type,
            severity,
            occurrence_count,
            message,
            status,
            created_at
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
        anomaly_type=row[3],
        severity=row[4],
        occurrence_count=row[5],
        message=row[6],
        status=row[7],
        created_at=row[8],
    )
from app.readings.models import Reading
from app.shared.db import get_connection


def load_readings() -> list[Reading]:
    query = """
        SELECT id, component_id, recorded_at, value
        FROM readings
        ORDER BY recorded_at;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    return [
        Reading(
            id=row[0],
            component_id=row[1],
            recorded_at=row[2],
            value=row[3],
        )
        for row in rows
    ]

def load_latest_readings_by_component() -> list[Reading]:
    query = """
        SELECT DISTINCT ON (component_id)
            id,
            component_id,
            recorded_at,
            value
        FROM readings
        ORDER BY component_id, recorded_at DESC;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    return [
        Reading(
            id=row[0],
            component_id=row[1],
            recorded_at=row[2],
            value=row[3],
        )
        for row in rows
    ]

def save_reading(reading: Reading) -> None:
    query = """
        INSERT INTO readings (id, component_id, recorded_at, value)
        VALUES (%s, %s, %s, %s);
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                query,
                (
                    reading.id,
                    reading.component_id,
                    reading.recorded_at,
                    reading.value,
                ),
            )
        conn.commit()
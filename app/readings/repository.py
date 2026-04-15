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
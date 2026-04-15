from app.hierarchy.models import Asset, Component, Location
from app.shared.db import get_connection


def load_locations() -> list[Location]:
    query = """
        SELECT id, name, parent_id
        FROM locations
        ORDER BY id;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    return [
        Location(
            id=row[0],
            name=row[1],
            parent_id=row[2],
        )
        for row in rows
    ]


def load_assets() -> list[Asset]:
    query = """
        SELECT id, name, location_id, parent_id
        FROM assets
        ORDER BY id;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    return [
        Asset(
            id=row[0],
            name=row[1],
            location_id=row[2],
            parent_id=row[3],
        )
        for row in rows
    ]


def load_components() -> list[Component]:
    query = """
        SELECT id, name, parent_id, sensor_type, status
        FROM components
        ORDER BY id;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    return [
        Component(
            id=row[0],
            name=row[1],
            parent_id=row[2],
            sensor_type=row[3],
            status=row[4],
        )
        for row in rows
    ]
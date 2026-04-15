from app.shared.db import get_connection
from app.work_orders.models import (
    WORK_ORDER_STATUS_OPEN,
    WorkOrder,
)


def create_work_order(
    work_order_id: str,
    alert_id: str,
    title: str,
    description: str,
) -> None:
    query = """
        INSERT INTO work_orders (id, alert_id, title, description, status)
        VALUES (%s, %s, %s, %s, %s);
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                query,
                (
                    work_order_id,
                    alert_id,
                    title,
                    description,
                    WORK_ORDER_STATUS_OPEN,
                ),
            )
        conn.commit()


def load_work_orders() -> list[WorkOrder]:
    query = """
        SELECT id, alert_id, title, description, status, created_at
        FROM work_orders
        ORDER BY created_at;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    return [
        WorkOrder(
            id=row[0],
            alert_id=row[1],
            title=row[2],
            description=row[3],
            status=row[4],
            created_at=row[5],
        )
        for row in rows
    ]


def exists_work_order_for_alert(alert_id: str) -> bool:
    query = """
        SELECT 1
        FROM work_orders
        WHERE alert_id = %s
        LIMIT 1;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (alert_id,))
            result = cur.fetchone()

    return result is not None


def update_work_order_status(work_order_id: str, new_status: str) -> bool:
    query = """
        UPDATE work_orders
        SET status = %s
        WHERE id = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (new_status, work_order_id))
            updated_rows = cur.rowcount
        conn.commit()

    return updated_rows > 0
"""
db/cancel_queries.py — Queries for Cancellation Analysis analytical view.
"""

from db.connection import run_query


def get_cancellation_by_origin():
    """Return top 20 origin cities ranked by cancellation rate."""
    sql = """
        SELECT
            s.origin,
            COUNT(*) AS total_shipments,
            COUNT(CASE WHEN ss.status_name = 'Cancelled' THEN 1 END) AS cancellations,
            ROUND(COUNT(CASE WHEN ss.status_name = 'Cancelled' THEN 1 END) * 100.0 / COUNT(*), 2) AS cancellation_rate
        FROM shipments s
        JOIN shipment_statuses ss ON s.status_id = ss.status_id
        GROUP BY s.origin
        ORDER BY cancellation_rate DESC
        LIMIT 20
    """
    return run_query(sql)


def get_cancellation_by_courier():
    """Return top 20 couriers ranked by cancellation rate."""
    sql = """
        SELECT
            cs.name AS courier,
            COUNT(*) AS total_shipments,
            COUNT(CASE WHEN ss.status_name = 'Cancelled' THEN 1 END) AS cancellations,
            ROUND(COUNT(CASE WHEN ss.status_name = 'Cancelled' THEN 1 END) * 100.0 / COUNT(*), 2) AS cancellation_rate
        FROM shipments s
        JOIN courier_staff cs     ON s.courier_id = cs.courier_id
        JOIN shipment_statuses ss ON s.status_id  = ss.status_id
        GROUP BY cs.courier_id, cs.name
        ORDER BY cancellation_rate DESC
        LIMIT 20
    """
    return run_query(sql)


def get_time_to_cancellation():
    """
    Return number of days between order placement and cancellation
    for each cancelled shipment.
    """
    sql = """
        SELECT
            s.shipment_id,
            DATEDIFF(
                MIN(CASE WHEN ts.status_name = 'Cancelled'    THEN st.timestamp END),
                MIN(CASE WHEN ts.status_name = 'Order Placed' THEN st.timestamp END)
            ) AS days_to_cancel
        FROM shipments s
        JOIN shipment_tracking st ON s.shipment_id = st.shipment_id
        JOIN tracking_statuses ts ON st.status_id  = ts.status_id
        JOIN shipment_statuses ss ON s.status_id   = ss.status_id
        WHERE ss.status_name = 'Cancelled'
        GROUP BY s.shipment_id
        HAVING days_to_cancel IS NOT NULL
    """
    return run_query(sql)

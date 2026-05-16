"""
db/kpi_queries.py — Queries for the 5 Key Performance Indicators.
"""

from db.connection import run_query


def get_kpis():
    """
    Return a single-row DataFrame with all 5 KPIs:
    - total_shipments
    - delivery_pct
    - cancellation_pct
    - avg_delivery_days
    - total_cost
    """
    sql = """
        SELECT
            COUNT(*) AS total_shipments,
            ROUND(COUNT(CASE WHEN ss.status_name = 'Delivered' THEN 1 END) * 100.0 / COUNT(*), 2) AS delivery_pct,
            ROUND(COUNT(CASE WHEN ss.status_name = 'Cancelled' THEN 1 END) * 100.0 / COUNT(*), 2) AS cancellation_pct,
            ROUND(AVG(CASE WHEN ss.status_name = 'Delivered' THEN DATEDIFF(s.delivery_date, s.order_date) END), 2) AS avg_delivery_days,
            ROUND((SELECT SUM(fuel_cost + labor_cost + misc_cost) FROM costs), 2) AS total_cost
        FROM shipments s
        JOIN shipment_statuses ss ON s.status_id = ss.status_id
    """
    return run_query(sql)

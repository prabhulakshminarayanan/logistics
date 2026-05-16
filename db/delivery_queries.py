"""
db/delivery_queries.py — Queries for Delivery Performance analytical view.
"""

from db.connection import run_query


def get_delivery_over_time():
    """Return monthly shipment counts broken down by status."""
    sql = """
        SELECT
            DATE_FORMAT(s.order_date, '%Y-%m') AS month,
            COUNT(CASE WHEN ss.status_name = 'Delivered'  THEN 1 END) AS Delivered,
            COUNT(CASE WHEN ss.status_name = 'Cancelled'  THEN 1 END) AS Cancelled,
            COUNT(CASE WHEN ss.status_name = 'In Transit' THEN 1 END) AS In_Transit,
            COUNT(CASE WHEN ss.status_name = 'Pending'    THEN 1 END) AS Pending,
            COUNT(*) AS Total
        FROM shipments s
        JOIN shipment_statuses ss ON s.status_id = ss.status_id
        GROUP BY month
        ORDER BY month
    """
    return run_query(sql)


def get_most_delayed_routes():
    """Return top 15 routes with the highest average delivery time."""
    sql = """
        SELECT
            s.origin, s.destination,
            ROUND(AVG(DATEDIFF(s.delivery_date, s.order_date)), 2) AS avg_delivery_days,
            COUNT(*) AS shipment_count
        FROM shipments s
        JOIN shipment_statuses ss ON s.status_id = ss.status_id
        WHERE ss.status_name = 'Delivered'
        GROUP BY s.origin, s.destination
        ORDER BY avg_delivery_days DESC
        LIMIT 15
    """
    return run_query(sql)


def get_route_delivery_efficiency():
    """Return delivery efficiency (% delivered vs cancelled) per route — top 20 by shipment volume."""
    sql = """
        SELECT
            s.origin, s.destination,
            COUNT(*) AS total_shipments,
            COUNT(CASE WHEN ss.status_name = 'Delivered' THEN 1 END) AS delivered,
            COUNT(CASE WHEN ss.status_name = 'Cancelled' THEN 1 END) AS cancelled,
            ROUND(COUNT(CASE WHEN ss.status_name = 'Delivered' THEN 1 END) * 100.0 / COUNT(*), 2) AS delivery_rate
        FROM shipments s
        JOIN shipment_statuses ss ON s.status_id = ss.status_id
        GROUP BY s.origin, s.destination
        ORDER BY total_shipments DESC
        LIMIT 20
    """
    return run_query(sql)


def get_delivery_time_vs_distance():
    """Return average delivery time grouped by route distance for scatter plot."""
    sql = """
        SELECT
            r.distance_km,
            ROUND(AVG(DATEDIFF(s.delivery_date, s.order_date)), 2) AS avg_delivery_days
        FROM shipments s
        JOIN shipment_statuses ss ON s.status_id = ss.status_id
        JOIN routes r ON s.origin = r.origin AND s.destination = r.destination
        WHERE ss.status_name = 'Delivered'
        GROUP BY r.distance_km
        ORDER BY r.distance_km
    """
    return run_query(sql)

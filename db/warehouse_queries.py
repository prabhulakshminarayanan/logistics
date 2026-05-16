"""
db/warehouse_queries.py — Queries for Warehouse Insights analytical view.
"""

from db.connection import run_query


def get_warehouse_capacity():
    """Return all warehouses sorted by capacity with capacity share percentage."""
    sql = """
        SELECT
            w.warehouse_id, w.city, w.state, w.capacity,
            ROUND(w.capacity * 100.0 / SUM(w.capacity) OVER (), 2) AS capacity_share_pct
        FROM warehouses w
        ORDER BY w.capacity DESC
    """
    return run_query(sql)


def get_high_traffic_warehouses():
    """
    Identify high-traffic warehouses by matching warehouse cities
    against shipment origin and destination cities.
    Returns shipment volume passing through each warehouse city.
    """
    sql = """
        SELECT
            w.warehouse_id,
            w.city,
            w.state,
            w.capacity,
            COUNT(s.shipment_id) AS shipment_traffic
        FROM warehouses w
        LEFT JOIN shipments s
            ON s.origin = w.city OR s.destination = w.city
        GROUP BY w.warehouse_id, w.city, w.state, w.capacity
        ORDER BY shipment_traffic DESC
    """
    return run_query(sql)

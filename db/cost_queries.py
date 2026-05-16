"""
db/cost_queries.py — Queries for Cost Analytics analytical view.
"""

from db.connection import run_query


def get_cost_by_status():
    """Return average fuel, labor and misc cost grouped by shipment status."""
    sql = """
        SELECT
            ss.status_name AS status,
            ROUND(AVG(c.fuel_cost),  2) AS avg_fuel_cost,
            ROUND(AVG(c.labor_cost), 2) AS avg_labor_cost,
            ROUND(AVG(c.misc_cost),  2) AS avg_misc_cost,
            ROUND(AVG(c.fuel_cost + c.labor_cost + c.misc_cost), 2) AS avg_total_cost
        FROM shipments s
        JOIN costs c              ON s.shipment_id = c.shipment_id
        JOIN shipment_statuses ss ON s.status_id   = ss.status_id
        GROUP BY ss.status_name
    """
    return run_query(sql)


def get_high_cost_shipments():
    """Return the top 20 most expensive shipments with full cost breakdown."""
    sql = """
        SELECT
            s.shipment_id, s.origin, s.destination,
            ss.status_name AS status,
            c.fuel_cost, c.labor_cost, c.misc_cost,
            ROUND(c.fuel_cost + c.labor_cost + c.misc_cost, 2) AS total_cost
        FROM shipments s
        JOIN costs c              ON s.shipment_id = c.shipment_id
        JOIN shipment_statuses ss ON s.status_id   = ss.status_id
        ORDER BY total_cost DESC
        LIMIT 20
    """
    return run_query(sql)


def get_route_cost():
    """Return top 15 routes by average total shipment cost."""
    sql = """
        SELECT
            s.origin, s.destination,
            ROUND(AVG(c.fuel_cost + c.labor_cost + c.misc_cost), 2) AS avg_cost,
            COUNT(*) AS shipment_count
        FROM shipments s
        JOIN costs c ON s.shipment_id = c.shipment_id
        GROUP BY s.origin, s.destination
        ORDER BY avg_cost DESC
        LIMIT 15
    """
    return run_query(sql)

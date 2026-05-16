"""
db/courier_queries.py — Queries for Courier Performance analytical view.
"""

from db.connection import run_query


def get_courier_performance():
    """Return top 20 couriers with shipment volume, delivery rate and rating."""
    sql = """
        SELECT
            cs.name,
            cs.rating,
            vt.type_name AS vehicle_type,
            COUNT(s.shipment_id) AS total_shipments,
            COUNT(CASE WHEN ss.status_name = 'Delivered' THEN 1 END) AS delivered,
            COUNT(CASE WHEN ss.status_name = 'Cancelled' THEN 1 END) AS cancelled,
            ROUND(COUNT(CASE WHEN ss.status_name = 'Delivered' THEN 1 END) * 100.0 / COUNT(*), 2) AS delivery_rate
        FROM courier_staff cs
        JOIN shipments s          ON cs.courier_id      = s.courier_id
        JOIN shipment_statuses ss  ON s.status_id        = ss.status_id
        JOIN vehicle_types vt     ON cs.vehicle_type_id = vt.vehicle_type_id
        GROUP BY cs.courier_id, cs.name, cs.rating, vt.type_name
        ORDER BY total_shipments DESC
        LIMIT 20
    """
    return run_query(sql)

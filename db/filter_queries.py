"""
db/filter_queries.py — Queries for populating sidebar filter dropdowns.
"""

import pandas as pd
from db.connection import run_query


def get_statuses():
    """Return list of all shipment status names."""
    df = run_query("SELECT status_name FROM shipment_statuses ORDER BY status_name")
    return df["status_name"].tolist() if not df.empty else []


def get_origins():
    """Return list of all unique shipment origin cities."""
    df = run_query("SELECT DISTINCT origin FROM shipments ORDER BY origin")
    return df["origin"].tolist() if not df.empty else []


def get_destinations():
    """Return list of all unique shipment destination cities."""
    df = run_query("SELECT DISTINCT destination FROM shipments ORDER BY destination")
    return df["destination"].tolist() if not df.empty else []


def get_couriers():
    """Return DataFrame of courier_id and name for all couriers."""
    return run_query("SELECT courier_id, name FROM courier_staff ORDER BY name")


def search_shipments(shipment_id=None, status=None, origin=None,
                     destination=None, start_date=None, end_date=None,
                     courier_id=None):
    """
    Return filtered shipment records based on provided criteria.
    All parameters are optional — omitting them returns all records (max 500).
    """
    try:
        conditions = []
        params     = []

        if shipment_id:
            conditions.append("s.shipment_id LIKE %s")
            params.append(f"%{shipment_id}%")
        if status:
            conditions.append("ss.status_name = %s")
            params.append(status)
        if origin:
            conditions.append("s.origin = %s")
            params.append(origin)
        if destination:
            conditions.append("s.destination = %s")
            params.append(destination)
        if start_date:
            conditions.append("s.order_date >= %s")
            params.append(str(start_date))
        if end_date:
            conditions.append("s.order_date <= %s")
            params.append(str(end_date))
        if courier_id:
            conditions.append("s.courier_id = %s")
            params.append(courier_id)

        where = "WHERE " + " AND ".join(conditions) if conditions else ""

        sql = f"""
            SELECT
                s.shipment_id, s.order_date, s.origin, s.destination,
                s.weight, cs.name AS courier,
                ss.status_name AS status, s.delivery_date
            FROM shipments s
            JOIN shipment_statuses ss ON s.status_id  = ss.status_id
            JOIN courier_staff cs     ON s.courier_id = cs.courier_id
            {where}
            ORDER BY s.order_date DESC
            LIMIT 500
        """
        return run_query(sql, params)

    except Exception as e:
        print(f"[SEARCH ERROR] {e}")
        return pd.DataFrame()

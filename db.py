"""
db.py — Database query functions for the Smart Logistics Dashboard.
All functions connect to MariaDB, run a query, and return a pandas DataFrame.
"""

import mysql.connector
import pandas as pd

# ── Database config ───────────────────────────────────────────
DB_CONFIG = {
    "host"    : "127.0.0.1",
    "port"    : 3306,
    "user"    : "root",
    "password": "tiger",
    "database": "logistics_db"
}


def get_connection():
    """Create and return a new database connection."""
    return mysql.connector.connect(**DB_CONFIG)


def run_query(sql, params=None):
    """
    Execute a SQL query and return results as a pandas DataFrame.
    Handles connection open/close and basic error reporting.
    """
    try:
        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        rows   = cursor.fetchall()
        cursor.close()
        conn.close()
        return pd.DataFrame(rows)
    except mysql.connector.Error as e:
        print(f"[DB ERROR] {e}")
        return pd.DataFrame()


# ── Filter options (for sidebar dropdowns) ────────────────────

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


# ── KPIs ──────────────────────────────────────────────────────

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


# ── Search & Filter shipments ─────────────────────────────────

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


# ── Analytical View 1: Delivery Performance ───────────────────

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


# ── Analytical View 2: Courier Performance ────────────────────

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


# ── Analytical View 3: Cost Analytics ────────────────────────

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


# ── Analytical View 4: Cancellation Analysis ──────────────────

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


# ── Analytical View 5: Warehouse Insights ────────────────────

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

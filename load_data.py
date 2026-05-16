import pandas as pd
import mysql.connector

# ── Database connection ───────────────────────────────────────
conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="tiger",
    database="logistics_db"
)
cursor = conn.cursor()
print("Connected to logistics_db successfully.")

# ── Helper ────────────────────────────────────────────────────
def load_table(table_name, rows, sql):
    cursor.executemany(sql, rows)
    conn.commit()
    print(f"  Loaded {cursor.rowcount} rows into {table_name}")

# ── Step 1: Load vehicle_types mapping (for courier_staff) ────
cursor.execute("SELECT type_name, vehicle_type_id FROM vehicle_types")
vehicle_type_map = {row[0]: row[1] for row in cursor.fetchall()}

# ── Step 2: Load shipment_statuses mapping ────────────────────
cursor.execute("SELECT status_name, status_id FROM shipment_statuses")
shipment_status_map = {row[0]: row[1] for row in cursor.fetchall()}

# ── Step 3: Load tracking_statuses mapping ────────────────────
cursor.execute("SELECT status_name, status_id FROM tracking_statuses")
tracking_status_map = {row[0]: row[1] for row in cursor.fetchall()}

print("\nLookup maps loaded.")
print(f"  vehicle_type_map     : {vehicle_type_map}")
print(f"  shipment_status_map  : {shipment_status_map}")
print(f"  tracking_status_map  : {tracking_status_map}")

# ── Step 4: Load courier_staff ────────────────────────────────
print("\nLoading courier_staff...")
couriers = pd.read_csv("data/courier_staff.csv")
courier_rows = [
    (
        row["courier_id"],
        row["name"],
        row["rating"],
        vehicle_type_map[row["vehicle_type"]]
    )
    for _, row in couriers.iterrows()
]
load_table("courier_staff",
    courier_rows,
    "INSERT IGNORE INTO courier_staff (courier_id, name, rating, vehicle_type_id) VALUES (%s, %s, %s, %s)"
)

# ── Step 5: Load warehouses ───────────────────────────────────
print("\nLoading warehouses...")
warehouses = pd.read_json("data/warehouses.json")
warehouse_rows = [
    (row["warehouse_id"], row["city"], row["state"], row["capacity"])
    for _, row in warehouses.iterrows()
]
load_table("warehouses",
    warehouse_rows,
    "INSERT IGNORE INTO warehouses (warehouse_id, city, state, capacity) VALUES (%s, %s, %s, %s)"
)

# ── Step 6: Load routes ───────────────────────────────────────
print("\nLoading routes...")
routes = pd.read_csv("data/routes.csv")
route_rows = [
    (row["route_id"], row["origin"], row["destination"], row["distance_km"], row["avg_time_hours"])
    for _, row in routes.iterrows()
]
load_table("routes",
    route_rows,
    "INSERT IGNORE INTO routes (route_id, origin, destination, distance_km, avg_time_hours) VALUES (%s, %s, %s, %s, %s)"
)

# ── Step 7: Load shipments ────────────────────────────────────
print("\nLoading shipments (70,000 records - this may take a moment)...")
shipments = pd.read_json("data/shipments.json")
shipment_rows = [
    (
        row["shipment_id"],
        row["order_date"],
        row["origin"],
        row["destination"],
        row["weight"],
        row["courier_id"],
        shipment_status_map[row["status"]],
        None if pd.isna(row["delivery_date"]) else row["delivery_date"]
    )
    for _, row in shipments.iterrows()
]
load_table("shipments",
    shipment_rows,
    "INSERT IGNORE INTO shipments (shipment_id, order_date, origin, destination, weight, courier_id, status_id, delivery_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
)

# ── Step 8: Load shipment_tracking ───────────────────────────
print("\nLoading shipment_tracking (209,570 records - this may take a moment)...")
tracking = pd.read_csv("data/shipment_tracking.csv")
tracking_rows = [
    (
        row["tracking_id"],
        row["shipment_id"],
        tracking_status_map[row["status"]],
        row["timestamp"]
    )
    for _, row in tracking.iterrows()
]
load_table("shipment_tracking",
    tracking_rows,
    "INSERT IGNORE INTO shipment_tracking (tracking_id, shipment_id, status_id, timestamp) VALUES (%s, %s, %s, %s)"
)

# ── Step 9: Load costs ────────────────────────────────────────
print("\nLoading costs...")
costs = pd.read_csv("data/costs.csv")
cost_rows = [
    (row["shipment_id"], row["fuel_cost"], row["labor_cost"], row["misc_cost"])
    for _, row in costs.iterrows()
]
load_table("costs",
    cost_rows,
    "INSERT IGNORE INTO costs (shipment_id, fuel_cost, labor_cost, misc_cost) VALUES (%s, %s, %s, %s)"
)

# ── Done ──────────────────────────────────────────────────────
cursor.close()
conn.close()
print("\nAll data loaded successfully. Connection closed.")

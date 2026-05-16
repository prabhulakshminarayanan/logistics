import pandas as pd

# Helper to print a section header
def section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

# ── 1. SHIPMENTS (JSON) ──────────────────────────────────────
section("SHIPMENTS (shipments.json)")
shipments = pd.read_json("data/shipments.json")
print(f"Rows: {len(shipments)}")
print(f"Columns: {list(shipments.columns)}")
print("\nFirst 3 rows:")
print(shipments.head(3).to_string())
print("\nData types:")
print(shipments.dtypes)
print("\nMissing values:")
print(shipments.isnull().sum())

# ── 2. SHIPMENT TRACKING (CSV) ────────────────────────────────
section("SHIPMENT TRACKING (shipment_tracking.csv)")
tracking = pd.read_csv("data/shipment_tracking.csv")
print(f"Rows: {len(tracking)}")
print(f"Columns: {list(tracking.columns)}")
print("\nFirst 3 rows:")
print(tracking.head(3).to_string())
print("\nData types:")
print(tracking.dtypes)
print("\nMissing values:")
print(tracking.isnull().sum())

# ── 3. COURIER STAFF (CSV) ────────────────────────────────────
section("COURIER STAFF (courier_staff.csv)")
couriers = pd.read_csv("data/courier_staff.csv")
print(f"Rows: {len(couriers)}")
print(f"Columns: {list(couriers.columns)}")
print("\nFirst 3 rows:")
print(couriers.head(3).to_string())
print("\nData types:")
print(couriers.dtypes)
print("\nMissing values:")
print(couriers.isnull().sum())

# ── 4. ROUTES (CSV) ───────────────────────────────────────────
section("ROUTES (routes.csv)")
routes = pd.read_csv("data/routes.csv")
print(f"Rows: {len(routes)}")
print(f"Columns: {list(routes.columns)}")
print("\nFirst 3 rows:")
print(routes.head(3).to_string())
print("\nData types:")
print(routes.dtypes)
print("\nMissing values:")
print(routes.isnull().sum())

# ── 5. WAREHOUSES (JSON) ──────────────────────────────────────
section("WAREHOUSES (warehouses.json)")
warehouses = pd.read_json("data/warehouses.json")
print(f"Rows: {len(warehouses)}")
print(f"Columns: {list(warehouses.columns)}")
print("\nFirst 3 rows:")
print(warehouses.head(3).to_string())
print("\nData types:")
print(warehouses.dtypes)
print("\nMissing values:")
print(warehouses.isnull().sum())

# ── 6. COSTS (CSV) ────────────────────────────────────────────
section("COSTS (costs.csv)")
costs = pd.read_csv("data/costs.csv")
print(f"Rows: {len(costs)}")
print(f"Columns: {list(costs.columns)}")
print("\nFirst 3 rows:")
print(costs.head(3).to_string())
print("\nData types:")
print(costs.dtypes)
print("\nMissing values:")
print(costs.isnull().sum())

print("\n" + "="*60)
print("  EXPLORATION COMPLETE")
print("="*60)

-- ============================================================
-- Smart Logistics Management & Analytics Platform
-- SQL Queries — KPIs & Analytical Views
-- ============================================================

USE logistics_db;

-- ============================================================
-- SECTION 1: KPIs
-- ============================================================

-- KPI 1: Delivery Percentage
-- How many shipments were successfully delivered out of total?
SELECT
    ROUND(
        COUNT(CASE WHEN ss.status_name = 'Delivered' THEN 1 END) * 100.0 / COUNT(*),
    2) AS delivery_percentage
FROM shipments s
JOIN shipment_statuses ss ON s.status_id = ss.status_id;


-- KPI 2: Cancellation Percentage
-- How many shipments were cancelled out of total?
SELECT
    ROUND(
        COUNT(CASE WHEN ss.status_name = 'Cancelled' THEN 1 END) * 100.0 / COUNT(*),
    2) AS cancellation_percentage
FROM shipments s
JOIN shipment_statuses ss ON s.status_id = ss.status_id;


-- KPI 3: Average Delivery Time (in days)
-- How many days on average does it take to deliver a shipment?
SELECT
    ROUND(AVG(DATEDIFF(s.delivery_date, s.order_date)), 2) AS avg_delivery_days
FROM shipments s
JOIN shipment_statuses ss ON s.status_id = ss.status_id
WHERE ss.status_name = 'Delivered';


-- KPI 4: Total Operational Cost
-- What is the total cost across all shipments?
SELECT
    ROUND(SUM(fuel_cost + labor_cost + misc_cost), 2) AS total_operational_cost
FROM costs;


-- ============================================================
-- SECTION 2: ANALYTICAL VIEWS
-- ============================================================

-- VIEW 1: Delivery Performance Over Time
-- How many shipments were delivered vs cancelled each month?
SELECT
    DATE_FORMAT(s.order_date, '%Y-%m') AS month,
    COUNT(CASE WHEN ss.status_name = 'Delivered'  THEN 1 END) AS delivered,
    COUNT(CASE WHEN ss.status_name = 'Cancelled'  THEN 1 END) AS cancelled,
    COUNT(CASE WHEN ss.status_name = 'In Transit' THEN 1 END) AS in_transit,
    COUNT(CASE WHEN ss.status_name = 'Pending'    THEN 1 END) AS pending,
    COUNT(*) AS total
FROM shipments s
JOIN shipment_statuses ss ON s.status_id = ss.status_id
GROUP BY month
ORDER BY month;


-- VIEW 2: Courier Efficiency
-- How is each courier performing? Deliveries, cancellations, avg rating
SELECT
    cs.courier_id,
    cs.name,
    cs.rating,
    vt.type_name AS vehicle_type,
    COUNT(s.shipment_id) AS total_shipments,
    COUNT(CASE WHEN ss.status_name = 'Delivered' THEN 1 END) AS delivered,
    COUNT(CASE WHEN ss.status_name = 'Cancelled' THEN 1 END) AS cancelled,
    ROUND(
        COUNT(CASE WHEN ss.status_name = 'Delivered' THEN 1 END) * 100.0 / COUNT(*),
    2) AS delivery_rate
FROM courier_staff cs
JOIN shipments s ON cs.courier_id = s.courier_id
JOIN shipment_statuses ss ON s.status_id = ss.status_id
JOIN vehicle_types vt ON cs.vehicle_type_id = vt.vehicle_type_id
GROUP BY cs.courier_id, cs.name, cs.rating, vt.type_name
ORDER BY delivery_rate DESC;


-- VIEW 3: Cost Analysis
-- What is the cost breakdown per shipment and overall?
SELECT
    s.shipment_id,
    s.origin,
    s.destination,
    ss.status_name AS status,
    c.fuel_cost,
    c.labor_cost,
    c.misc_cost,
    ROUND(c.fuel_cost + c.labor_cost + c.misc_cost, 2) AS total_cost
FROM shipments s
JOIN costs c ON s.shipment_id = c.shipment_id
JOIN shipment_statuses ss ON s.status_id = ss.status_id
ORDER BY total_cost DESC;


-- VIEW 3b: Cost Summary by Status
-- Which status (delivered/cancelled) costs more on average?
SELECT
    ss.status_name AS status,
    ROUND(AVG(c.fuel_cost), 2)   AS avg_fuel_cost,
    ROUND(AVG(c.labor_cost), 2)  AS avg_labor_cost,
    ROUND(AVG(c.misc_cost), 2)   AS avg_misc_cost,
    ROUND(AVG(c.fuel_cost + c.labor_cost + c.misc_cost), 2) AS avg_total_cost
FROM shipments s
JOIN costs c ON s.shipment_id = c.shipment_id
JOIN shipment_statuses ss ON s.status_id = ss.status_id
GROUP BY ss.status_name;


-- VIEW 4: Cancellation Patterns
-- Where are cancellations happening the most? By origin city
SELECT
    s.origin,
    COUNT(*) AS total_shipments,
    COUNT(CASE WHEN ss.status_name = 'Cancelled' THEN 1 END) AS cancellations,
    ROUND(
        COUNT(CASE WHEN ss.status_name = 'Cancelled' THEN 1 END) * 100.0 / COUNT(*),
    2) AS cancellation_rate
FROM shipments s
JOIN shipment_statuses ss ON s.status_id = ss.status_id
GROUP BY s.origin
ORDER BY cancellation_rate DESC
LIMIT 20;


-- VIEW 5: Warehouse Capacity
-- How much capacity does each warehouse have? Which states have most coverage?
SELECT
    w.warehouse_id,
    w.city,
    w.state,
    w.capacity,
    ROUND(w.capacity * 100.0 / SUM(w.capacity) OVER (), 2) AS capacity_share_pct
FROM warehouses w
ORDER BY w.capacity DESC;

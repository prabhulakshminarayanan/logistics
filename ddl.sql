-- ============================================================
-- Smart Logistics Management & Analytics Platform
-- DDL - Database & Table Structure
-- ============================================================

CREATE DATABASE IF NOT EXISTS logistics_db;
USE logistics_db;

-- ── LOOKUP TABLES ─────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS shipment_statuses (
    status_id   INT          PRIMARY KEY AUTO_INCREMENT,
    status_name VARCHAR(50)  NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS tracking_statuses (
    status_id   INT          PRIMARY KEY AUTO_INCREMENT,
    status_name VARCHAR(50)  NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS vehicle_types (
    vehicle_type_id INT         PRIMARY KEY AUTO_INCREMENT,
    type_name       VARCHAR(50) NOT NULL UNIQUE
);

-- ── CORE TABLES ───────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS courier_staff (
    courier_id      VARCHAR(50)  PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    rating          DECIMAL(2,1) NOT NULL,
    vehicle_type_id INT          NOT NULL,

    FOREIGN KEY (vehicle_type_id) REFERENCES vehicle_types(vehicle_type_id)
);

CREATE TABLE IF NOT EXISTS warehouses (
    warehouse_id VARCHAR(50)  PRIMARY KEY,
    city         VARCHAR(100) NOT NULL,
    state        VARCHAR(50)  NOT NULL,
    capacity     INT          NOT NULL
);

CREATE TABLE IF NOT EXISTS routes (
    route_id       VARCHAR(50)  PRIMARY KEY,
    origin         VARCHAR(100) NOT NULL,
    destination    VARCHAR(100) NOT NULL,
    distance_km    DECIMAL(8,2) NOT NULL,
    avg_time_hours DECIMAL(6,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS shipments (
    shipment_id   VARCHAR(50)  PRIMARY KEY,
    order_date    DATE         NOT NULL,
    origin        VARCHAR(100) NOT NULL,
    destination   VARCHAR(100) NOT NULL,
    weight        DECIMAL(6,2) NOT NULL,
    courier_id    VARCHAR(50)  NOT NULL,
    status_id     INT          NOT NULL,
    delivery_date DATE         NULL,

    FOREIGN KEY (courier_id) REFERENCES courier_staff(courier_id),
    FOREIGN KEY (status_id)  REFERENCES shipment_statuses(status_id)
);

CREATE TABLE IF NOT EXISTS shipment_tracking (
    tracking_id INT         PRIMARY KEY,
    shipment_id VARCHAR(50) NOT NULL,
    status_id   INT         NOT NULL,
    timestamp   DATETIME    NOT NULL,

    FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id),
    FOREIGN KEY (status_id)   REFERENCES tracking_statuses(status_id)
);

CREATE TABLE IF NOT EXISTS costs (
    shipment_id VARCHAR(50)  PRIMARY KEY,
    fuel_cost   DECIMAL(8,2) NOT NULL,
    labor_cost  DECIMAL(8,2) NOT NULL,
    misc_cost   DECIMAL(8,2) NOT NULL,

    FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id)
);

-- ── INDEXES for query optimization ────────────────────────────
-- Added on columns frequently used in WHERE, JOIN, and ORDER BY clauses

CREATE INDEX IF NOT EXISTS idx_shipments_status_id    ON shipments (status_id);
CREATE INDEX IF NOT EXISTS idx_shipments_courier_id   ON shipments (courier_id);
CREATE INDEX IF NOT EXISTS idx_shipments_order_date   ON shipments (order_date);
CREATE INDEX IF NOT EXISTS idx_shipments_origin       ON shipments (origin);
CREATE INDEX IF NOT EXISTS idx_shipments_destination  ON shipments (destination);

CREATE INDEX IF NOT EXISTS idx_tracking_shipment_id   ON shipment_tracking (shipment_id);
CREATE INDEX IF NOT EXISTS idx_tracking_status_id     ON shipment_tracking (status_id);
CREATE INDEX IF NOT EXISTS idx_tracking_timestamp     ON shipment_tracking (timestamp);

CREATE INDEX IF NOT EXISTS idx_costs_shipment_id      ON costs (shipment_id);

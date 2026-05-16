-- ============================================================
-- Smart Logistics Management & Analytics Platform
-- DML - Seed Lookup Tables
-- ============================================================

USE logistics_db;

INSERT IGNORE INTO shipment_statuses (status_name) VALUES
    ('Delivered'),
    ('Cancelled'),
    ('In Transit'),
    ('Pending');

INSERT IGNORE INTO tracking_statuses (status_name) VALUES
    ('Order Placed'),
    ('Picked Up'),
    ('In Transit'),
    ('Out for Delivery'),
    ('Delivered'),
    ('Cancelled');

INSERT IGNORE INTO vehicle_types (type_name) VALUES
    ('Car'),
    ('Van'),
    ('Truck'),
    ('Bike');

"""
config.py — Central configuration for the Smart Logistics Platform.
All environment-specific settings are defined here.
"""

# ── Database configuration ────────────────────────────────────
DB_CONFIG = {
    "host"    : "127.0.0.1",
    "port"    : 3306,
    "user"    : "root",
    "password": "tiger",
    "database": "logistics_db"
}

# ── App configuration ─────────────────────────────────────────
APP_TITLE    = "Smart Logistics Management & Analytics Platform"
APP_ICON     = "🚚"
MAX_RECORDS  = 500

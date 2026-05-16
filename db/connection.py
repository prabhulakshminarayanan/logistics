"""
db/connection.py — Handles database connection and query execution.
All other query modules import from here.
"""

import mysql.connector
import pandas as pd
from config import DB_CONFIG


def get_connection():
    """Create and return a new MariaDB connection."""
    return mysql.connector.connect(**DB_CONFIG)


def run_query(sql, params=None):
    """
    Execute a SQL query and return results as a pandas DataFrame.
    Automatically opens and closes the connection.
    Returns an empty DataFrame on error.
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

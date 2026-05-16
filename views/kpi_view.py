"""
views/kpi_view.py — KPI metrics section UI.
"""

import streamlit as st
from db.kpi_queries import get_kpis


def render_kpis():
    """Render the 5 KPI metric cards at the top of the dashboard."""
    st.subheader("📊 Key Performance Indicators")
    try:
        kpis = get_kpis().iloc[0]
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Shipments",        f"{int(kpis['total_shipments']):,}")
        col2.metric("Delivered %",            f"{kpis['delivery_pct']}%")
        col3.metric("Cancelled %",            f"{kpis['cancellation_pct']}%")
        col4.metric("Avg Delivery Time",      f"{kpis['avg_delivery_days']} days")
        col5.metric("Total Operational Cost", f"${kpis['total_cost']:,.2f}")
    except Exception as e:
        st.error(f"Error loading KPIs: {e}")

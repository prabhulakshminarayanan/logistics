"""
views/warehouse_view.py — Warehouse Insights tab UI.
"""

import streamlit as st
import plotly.express as px
from db.warehouse_queries import get_warehouse_capacity, get_high_traffic_warehouses


def render_warehouse_view():
    """Render the Warehouse Insights analytical tab."""
    try:
        st.markdown("### Warehouse Capacity Overview")
        warehouses = get_warehouse_capacity()
        if not warehouses.empty:
            fig = px.bar(warehouses, x="city", y="capacity",
                         title="Warehouse Capacity by City",
                         labels={"capacity": "Capacity", "city": "City"})
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### Capacity Share — Top 10 Warehouses")
            fig2 = px.pie(warehouses.head(10), values="capacity", names="city",
                          title="Top 10 Warehouses — Capacity Share")
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### High-Traffic Warehouses")
        st.caption("Shipment traffic = number of shipments passing through each warehouse city")
        traffic = get_high_traffic_warehouses()
        if not traffic.empty:
            fig3 = px.bar(traffic, x="city", y="shipment_traffic",
                          title="Warehouse Cities by Shipment Traffic",
                          labels={"shipment_traffic": "Shipment Traffic", "city": "City"})
            fig3.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("### Warehouse Details Table")
        if not warehouses.empty:
            st.dataframe(warehouses, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading warehouse data: {e}")

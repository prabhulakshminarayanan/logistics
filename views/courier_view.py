"""
views/courier_view.py — Courier Performance tab UI.
"""

import streamlit as st
import plotly.express as px
from db.courier_queries import get_courier_performance


def render_courier_view():
    """Render the Courier Performance analytical tab."""
    try:
        st.markdown("### Courier Performance Overview")
        couriers = get_courier_performance()
        if not couriers.empty:
            fig = px.bar(couriers, x="name", y="total_shipments",
                         color="delivery_rate",
                         title="Shipment Volume per Courier (coloured by Delivery Rate %)",
                         labels={"name": "Courier", "total_shipments": "Total Shipments",
                                 "delivery_rate": "Delivery Rate %"},
                         color_continuous_scale="RdYlGn")
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### Courier Rating Comparison")
            fig2 = px.scatter(couriers, x="rating", y="delivery_rate",
                              size="total_shipments", hover_name="name",
                              color="vehicle_type",
                              title="Rating vs Delivery Rate (bubble size = shipment volume)",
                              labels={"rating": "Courier Rating",
                                      "delivery_rate": "Delivery Rate %"})
            st.plotly_chart(fig2, use_container_width=True)

            st.markdown("### Detailed Courier Table")
            st.dataframe(couriers, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading courier data: {e}")

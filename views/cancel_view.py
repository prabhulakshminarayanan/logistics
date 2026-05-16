"""
views/cancel_view.py — Cancellation Analysis tab UI.
"""

import streamlit as st
import plotly.express as px
from db.cancel_queries import (
    get_cancellation_by_origin,
    get_cancellation_by_courier,
    get_time_to_cancellation
)


def render_cancel_view():
    """Render the Cancellation Analysis analytical tab."""
    try:
        st.markdown("### Cancellation Rate by Origin City")
        cancel_origin = get_cancellation_by_origin()
        if not cancel_origin.empty:
            fig = px.bar(cancel_origin, x="cancellation_rate", y="origin",
                         orientation="h",
                         title="Top 20 Origins by Cancellation Rate",
                         labels={"cancellation_rate": "Cancellation Rate %", "origin": "Origin City"})
            fig.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Cancellation Rate by Courier")
        cancel_courier = get_cancellation_by_courier()
        if not cancel_courier.empty:
            fig2 = px.bar(cancel_courier, x="courier", y="cancellation_rate",
                          title="Top 20 Couriers by Cancellation Rate",
                          labels={"cancellation_rate": "Cancellation Rate %", "courier": "Courier"})
            fig2.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### Time-to-Cancellation Pattern")
        ttc = get_time_to_cancellation()
        if not ttc.empty:
            ttc_grouped = ttc.groupby("days_to_cancel").size().reset_index(name="shipment_count")
            fig3 = px.bar(ttc_grouped, x="days_to_cancel", y="shipment_count",
                          title="How Many Days After Order Placement Do Cancellations Happen?",
                          labels={"days_to_cancel": "Days to Cancel",
                                  "shipment_count": "Number of Shipments"})
            st.plotly_chart(fig3, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading cancellation data: {e}")

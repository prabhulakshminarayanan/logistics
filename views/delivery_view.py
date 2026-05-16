"""
views/delivery_view.py — Delivery Performance tab UI.
"""

import streamlit as st
import plotly.express as px
from db.delivery_queries import (
    get_delivery_over_time,
    get_most_delayed_routes,
    get_delivery_time_vs_distance
)


def render_delivery_view():
    """Render the Delivery Performance analytical tab."""
    try:
        st.markdown("### Delivery Performance Over Time")
        perf = get_delivery_over_time()
        if not perf.empty:
            fig = px.line(perf, x="month",
                          y=["Delivered", "Cancelled", "In_Transit", "Pending"],
                          title="Monthly Shipment Status Trend",
                          labels={"value": "Shipments", "variable": "Status"})
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Most Delayed Routes")
        delayed = get_most_delayed_routes()
        if not delayed.empty:
            delayed["route"] = delayed["origin"] + " → " + delayed["destination"]
            fig2 = px.bar(delayed, x="avg_delivery_days", y="route",
                          orientation="h",
                          title="Top 15 Most Delayed Routes (Avg Days)",
                          labels={"avg_delivery_days": "Avg Delivery Days", "route": "Route"})
            fig2.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### Delivery Time vs Distance")
        dvd = get_delivery_time_vs_distance()
        if not dvd.empty:
            fig3 = px.scatter(dvd, x="distance_km", y="avg_delivery_days",
                              title="Delivery Time vs Route Distance",
                              labels={"distance_km": "Distance (km)",
                                      "avg_delivery_days": "Avg Delivery Days"})
            st.plotly_chart(fig3, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading delivery performance data: {e}")

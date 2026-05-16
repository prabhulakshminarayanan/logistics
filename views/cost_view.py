"""
views/cost_view.py — Cost Analytics tab UI.
"""

import streamlit as st
import plotly.express as px
from db.cost_queries import get_cost_by_status, get_high_cost_shipments, get_route_cost


def render_cost_view():
    """Render the Cost Analytics analytical tab."""
    try:
        st.markdown("### Average Cost Breakdown by Status")
        cost_status = get_cost_by_status()
        if not cost_status.empty:
            fig = px.bar(cost_status, x="status",
                         y=["avg_fuel_cost", "avg_labor_cost", "avg_misc_cost"],
                         barmode="stack",
                         title="Fuel vs Labour vs Misc Cost by Shipment Status",
                         labels={"value": "Avg Cost ($)", "variable": "Cost Type"})
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### Overall Fuel vs Labour Proportions")
            totals = cost_status[["avg_fuel_cost", "avg_labor_cost", "avg_misc_cost"]].mean()
            fig2 = px.pie(values=totals.values,
                          names=["Fuel", "Labour", "Misc"],
                          title="Overall Cost Proportion")
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### Top 20 High-Cost Shipments")
        high_cost = get_high_cost_shipments()
        if not high_cost.empty:
            st.dataframe(high_cost, use_container_width=True)

        st.markdown("### Top 15 Most Expensive Routes (Avg Cost)")
        route_cost = get_route_cost()
        if not route_cost.empty:
            route_cost["route"] = route_cost["origin"] + " → " + route_cost["destination"]
            fig3 = px.bar(route_cost, x="avg_cost", y="route",
                          orientation="h",
                          title="Route-specific Average Cost",
                          labels={"avg_cost": "Avg Cost ($)", "route": "Route"})
            fig3.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig3, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading cost data: {e}")

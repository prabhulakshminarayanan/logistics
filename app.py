import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import db
import mysql.connector

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Logistics Dashboard",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 Smart Logistics Management & Analytics Platform")
st.markdown("---")


# ── Sidebar — Filters ─────────────────────────────────────────
st.sidebar.header("🔍 Search & Filter")

try:
    shipment_id  = st.sidebar.text_input("Search by Shipment ID")

    statuses     = ["All"] + db.get_statuses()
    status       = st.sidebar.selectbox("Filter by Status", statuses)

    origins      = ["All"] + db.get_origins()
    origin       = st.sidebar.selectbox("Filter by Origin", origins)

    destinations = ["All"] + db.get_destinations()
    destination  = st.sidebar.selectbox("Filter by Destination", destinations)

    couriers_df  = db.get_couriers()
    courier_opts = {"All": None} | dict(zip(couriers_df["name"], couriers_df["courier_id"]))
    courier_name = st.sidebar.selectbox("Filter by Courier", list(courier_opts.keys()))

    st.sidebar.markdown("**Date Range**")
    start_date = st.sidebar.date_input("From", value=None)
    end_date   = st.sidebar.date_input("To",   value=None)

except Exception as e:
    st.sidebar.error(f"Error loading filters: {e}")
    st.stop()

# Resolve filter values
selected_status      = None if status      == "All" else status
selected_origin      = None if origin      == "All" else origin
selected_destination = None if destination == "All" else destination
selected_courier_id  = courier_opts[courier_name]


# ── KPI Section ───────────────────────────────────────────────
st.subheader("📊 Key Performance Indicators")
try:
    kpis = db.get_kpis().iloc[0]
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Shipments",        f"{int(kpis['total_shipments']):,}")
    col2.metric("Delivered %",            f"{kpis['delivery_pct']}%")
    col3.metric("Cancelled %",            f"{kpis['cancellation_pct']}%")
    col4.metric("Avg Delivery Time",      f"{kpis['avg_delivery_days']} days")
    col5.metric("Total Operational Cost", f"${kpis['total_cost']:,.2f}")
except Exception as e:
    st.error(f"Error loading KPIs: {e}")

st.markdown("---")


# ── Shipment Search Results ───────────────────────────────────
st.subheader("📦 Shipment Records")
try:
    results = db.search_shipments(
        shipment_id  = shipment_id         or None,
        status       = selected_status,
        origin       = selected_origin,
        destination  = selected_destination,
        start_date   = start_date          or None,
        end_date     = end_date            or None,
        courier_id   = selected_courier_id
    )
    if results.empty:
        st.info("No shipments found matching the selected filters.")
    else:
        st.caption(f"Showing {len(results)} records (max 500)")
        st.dataframe(results, use_container_width=True)
except Exception as e:
    st.error(f"Error loading shipment records: {e}")

st.markdown("---")


# ── Analytical Tabs ───────────────────────────────────────────
st.subheader("📈 Analytical Views")
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🚀 Delivery Performance",
    "👤 Courier Performance",
    "💰 Cost Analytics",
    "❌ Cancellation Analysis",
    "🏭 Warehouse Insights"
])


# ── Tab 1: Delivery Performance ───────────────────────────────
with tab1:
    try:
        st.markdown("### Delivery Performance Over Time")
        perf = db.get_delivery_over_time()
        if not perf.empty:
            fig = px.line(perf, x="month",
                          y=["Delivered", "Cancelled", "In_Transit", "Pending"],
                          title="Monthly Shipment Status Trend",
                          labels={"value": "Shipments", "variable": "Status"})
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Most Delayed Routes")
        delayed = db.get_most_delayed_routes()
        if not delayed.empty:
            delayed["route"] = delayed["origin"] + " → " + delayed["destination"]
            fig2 = px.bar(delayed, x="avg_delivery_days", y="route",
                          orientation="h",
                          title="Top 15 Most Delayed Routes (Avg Days)",
                          labels={"avg_delivery_days": "Avg Delivery Days", "route": "Route"})
            fig2.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### Delivery Time vs Distance")
        dvd = db.get_delivery_time_vs_distance()
        if not dvd.empty:
            fig3 = px.scatter(dvd, x="distance_km", y="avg_delivery_days",
                              title="Delivery Time vs Route Distance",
                              labels={"distance_km": "Distance (km)",
                                      "avg_delivery_days": "Avg Delivery Days"})
            st.plotly_chart(fig3, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading delivery performance data: {e}")


# ── Tab 2: Courier Performance ────────────────────────────────
with tab2:
    try:
        st.markdown("### Courier Performance Overview")
        couriers = db.get_courier_performance()
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


# ── Tab 3: Cost Analytics ─────────────────────────────────────
with tab3:
    try:
        st.markdown("### Average Cost Breakdown by Status")
        cost_status = db.get_cost_by_status()
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
        high_cost = db.get_high_cost_shipments()
        if not high_cost.empty:
            st.dataframe(high_cost, use_container_width=True)

        st.markdown("### Top 15 Most Expensive Routes (Avg Cost)")
        route_cost = db.get_route_cost()
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


# ── Tab 4: Cancellation Analysis ──────────────────────────────
with tab4:
    try:
        st.markdown("### Cancellation Rate by Origin City")
        cancel_origin = db.get_cancellation_by_origin()
        if not cancel_origin.empty:
            fig = px.bar(cancel_origin, x="cancellation_rate", y="origin",
                         orientation="h",
                         title="Top 20 Origins by Cancellation Rate",
                         labels={"cancellation_rate": "Cancellation Rate %", "origin": "Origin City"})
            fig.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Cancellation Rate by Courier")
        cancel_courier = db.get_cancellation_by_courier()
        if not cancel_courier.empty:
            fig2 = px.bar(cancel_courier, x="courier", y="cancellation_rate",
                          title="Top 20 Couriers by Cancellation Rate",
                          labels={"cancellation_rate": "Cancellation Rate %", "courier": "Courier"})
            fig2.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### Time-to-Cancellation Pattern")
        ttc = db.get_time_to_cancellation()
        if not ttc.empty:
            ttc_grouped = ttc.groupby("days_to_cancel").size().reset_index(name="shipment_count")
            fig3 = px.bar(ttc_grouped, x="days_to_cancel", y="shipment_count",
                          title="How Many Days After Order Placement Do Cancellations Happen?",
                          labels={"days_to_cancel": "Days to Cancel", "shipment_count": "Number of Shipments"})
            st.plotly_chart(fig3, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading cancellation data: {e}")


# ── Tab 5: Warehouse Insights ─────────────────────────────────
with tab5:
    try:
        st.markdown("### Warehouse Capacity Overview")
        warehouses = db.get_warehouse_capacity()
        if not warehouses.empty:
            fig = px.bar(warehouses, x="city", y="capacity",
                         color="state",
                         title="Warehouse Capacity by City",
                         labels={"capacity": "Capacity", "city": "City"})
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### Capacity Share — Top 10 Warehouses")
            fig2 = px.pie(warehouses.head(10), values="capacity", names="city",
                          title="Top 10 Warehouses — Capacity Share")
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### High-Traffic Warehouses")
        st.caption("Shipment traffic = number of shipments passing through each warehouse city (as origin or destination)")
        traffic = db.get_high_traffic_warehouses()
        if not traffic.empty:
            fig3 = px.bar(traffic, x="city", y="shipment_traffic",
                          color="state",
                          title="Warehouse Cities by Shipment Traffic",
                          labels={"shipment_traffic": "Shipment Traffic", "city": "City"})
            fig3.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("### Warehouse Details Table")
        st.dataframe(warehouses, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading warehouse data: {e}")

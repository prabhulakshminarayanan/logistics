"""
app.py — Main entry point for the Smart Logistics Dashboard.
Assembles all views and renders the Streamlit application.
"""

import streamlit as st
from config import APP_TITLE, APP_ICON
from views.sidebar       import render_sidebar
from views.kpi_view      import render_kpis
from views.shipment_view import render_shipments
from views.delivery_view import render_delivery_view
from views.courier_view  import render_courier_view
from views.cost_view     import render_cost_view
from views.cancel_view   import render_cancel_view
from views.warehouse_view import render_warehouse_view

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide"
)

st.title(f"{APP_ICON} {APP_TITLE}")
st.markdown("---")

# ── Sidebar filters ───────────────────────────────────────────
filters = render_sidebar()

# ── KPIs ──────────────────────────────────────────────────────
render_kpis()
st.markdown("---")

# ── Shipment search results ───────────────────────────────────
render_shipments(filters)
st.markdown("---")

# ── Analytical tabs ───────────────────────────────────────────
st.subheader("📈 Analytical Views")
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🚀 Delivery Performance",
    "👤 Courier Performance",
    "💰 Cost Analytics",
    "❌ Cancellation Analysis",
    "🏭 Warehouse Insights"
])

with tab1: render_delivery_view()
with tab2: render_courier_view()
with tab3: render_cost_view()
with tab4: render_cancel_view()
with tab5: render_warehouse_view()

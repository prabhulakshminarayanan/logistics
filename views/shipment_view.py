"""
views/shipment_view.py — Shipment search results table UI.
"""

import streamlit as st
from db.filter_queries import search_shipments


def render_shipments(filters):
    """Render the filtered shipment records table."""
    st.subheader("📦 Shipment Records")
    try:
        results = search_shipments(
            shipment_id = filters["shipment_id"],
            status      = filters["status"],
            origin      = filters["origin"],
            destination = filters["destination"],
            start_date  = filters["start_date"],
            end_date    = filters["end_date"],
            courier_id  = filters["courier_id"]
        )
        if results.empty:
            st.info("No shipments found matching the selected filters.")
        else:
            st.caption(f"Showing {len(results)} records (max 500)")
            st.dataframe(results, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading shipment records: {e}")

"""
views/sidebar.py — Sidebar filter UI and filter value resolution.
"""

import streamlit as st
from db.filter_queries import get_statuses, get_origins, get_destinations, get_couriers


def render_sidebar():
    """
    Render the sidebar search and filter controls.
    Returns a dictionary of selected filter values.
    """
    st.sidebar.header("🔍 Search & Filter")

    try:
        shipment_id  = st.sidebar.text_input("Search by Shipment ID")

        statuses     = ["All"] + get_statuses()
        status       = st.sidebar.selectbox("Filter by Status", statuses)

        origins      = ["All"] + get_origins()
        origin       = st.sidebar.selectbox("Filter by Origin", origins)

        destinations = ["All"] + get_destinations()
        destination  = st.sidebar.selectbox("Filter by Destination", destinations)

        couriers_df  = get_couriers()
        courier_opts = {"All": None} | dict(zip(couriers_df["name"], couriers_df["courier_id"]))
        courier_name = st.sidebar.selectbox("Filter by Courier", list(courier_opts.keys()))

        st.sidebar.markdown("**Date Range**")
        start_date = st.sidebar.date_input("From", value=None)
        end_date   = st.sidebar.date_input("To",   value=None)

        return {
            "shipment_id" : shipment_id or None,
            "status"      : None if status      == "All" else status,
            "origin"      : None if origin      == "All" else origin,
            "destination" : None if destination == "All" else destination,
            "courier_id"  : courier_opts[courier_name],
            "start_date"  : start_date or None,
            "end_date"    : end_date   or None,
        }

    except Exception as e:
        st.sidebar.error(f"Error loading filters: {e}")
        st.stop()

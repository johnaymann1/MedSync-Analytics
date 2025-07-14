# components/sidebar.py
"""
Sidebar components for filtering data and PDF export
"""

import streamlit as st
from components.pdf_export import PDFExport

class Sidebar:
    """Handles sidebar filters and controls."""
    @staticmethod
    def create_filters(df):
        """Create sidebar filters and return filter values."""
        st.sidebar.markdown('### Dashboard Controls')
        filters = {}
        with st.sidebar.expander("🔍 Data Filters", expanded=True):
            filters['doctor'] = Sidebar._create_doctor_filter(df)
            filters['date_range'] = Sidebar._create_date_filter(df)
        with st.sidebar.expander("📊 Status Filters", expanded=True):
            filters['eligibility'] = Sidebar._create_eligibility_filter(df)
            filters['authorization'] = Sidebar._create_authorization_filter(df)
        st.sidebar.markdown("### Quick Actions")
        if st.sidebar.button("Clear All Filters", help="Reset all filters to default values", use_container_width=True):
            filter_keys = ['doctor_filter', 'eligibility_filter', 'authorization_filter', 'date_filter']
            for key in filter_keys:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        return filters
    @staticmethod
    def _create_doctor_filter(df):
        """Create doctor selection filter."""
        if "Doctor" not in df.columns:
            return "All"
        doctors = ["All"] + sorted(df["Doctor"].dropna().unique().tolist())
        return st.sidebar.selectbox("Select Doctor", doctors, key="doctor_filter")
    @staticmethod
    def _create_eligibility_filter(df):
        """Create eligibility status filter."""
        if "Eligibility Status" not in df.columns:
            return "All"
        eligibility_statuses = ["All"] + sorted(df["Eligibility Status"].dropna().unique().tolist())
        return st.sidebar.selectbox("Select Eligibility Status", eligibility_statuses, key="eligibility_filter")
    @staticmethod
    def _create_authorization_filter(df):
        """Create authorization status filter."""
        if "Authorization Status" not in df.columns:
            return "All"
        auth_statuses = ["All"] + sorted(df["Authorization Status"].dropna().unique().tolist())
        return st.sidebar.selectbox("Select Authorization Status", auth_statuses, key="authorization_filter")
    @staticmethod
    def _create_date_filter(df):
        """Create date range filter."""
        if "Today's Date" not in df.columns or not df["Today's Date"].notna().any():
            return None
        min_date = df["Today's Date"].min().date()
        max_date = df["Today's Date"].max().date()
        return st.sidebar.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="date_filter"
        )

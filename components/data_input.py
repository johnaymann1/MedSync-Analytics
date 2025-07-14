# components/data_input.py
"""
Data input components for the dashboard
"""

import streamlit as st

class DataInput:
    """Handles data source input components."""
    @staticmethod
    def create_data_source_section():
        """Create the data source input section."""
        st.markdown('<div class="section-header">Data Source</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])
        gsheet_url = st.text_input(
            "Or enter a public Google Sheet CSV export link",
            help="File > Share > Anyone with link, then File > Download > Comma-separated values"
        )
        return uploaded_file, gsheet_url

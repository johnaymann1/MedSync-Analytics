# components/data_table.py
"""
Data table display and export functionality
"""

import streamlit as st
from datetime import datetime

class DataTable:
    """Handles data table display and export."""
    @staticmethod
    def create_data_table_section(filtered_df):
        """Create the filtered data table section."""
        st.markdown('<div class="section-header">Filtered Data</div>', unsafe_allow_html=True)
        with st.expander(f"View Filtered Data ({len(filtered_df)} rows)", expanded=False):
            st.dataframe(filtered_df, use_container_width=True)
            DataTable._create_export_button(filtered_df)
    @staticmethod
    def _create_export_button(filtered_df):
        """Create CSV export button."""
        if st.button("Download Filtered Data as CSV"):
            csv = filtered_df.to_csv(index=False)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"filtered_medsync_data_{timestamp}.csv"
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=filename,
                mime="text/csv"
            )

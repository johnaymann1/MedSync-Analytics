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
        """Create the filtered data table section with Medsync calculation column and only relevant columns, plus a summary of combinations."""
        st.markdown('<div class="section-header">Filtered Data</div>', unsafe_allow_html=True)
        # Only keep relevant columns
        elig_col = None
        auth_col = None
        name_col = None
        for col in ["Eligibility Status", "Eligibility"]:
            if col in filtered_df.columns:
                elig_col = col
                break
        for col in ["Authorization Status", "Authorization"]:
            if col in filtered_df.columns:
                auth_col = col
                break
        for col in ["Patient Name", "Name"]:
            if col in filtered_df.columns:
                name_col = col
                break
        display_cols = []
        if name_col:
            display_cols.append(name_col)
        if elig_col:
            display_cols.append(elig_col)
        if auth_col:
            display_cols.append(auth_col)
        # Calculate Medsync calculation column
        if elig_col and auth_col:
            elig = filtered_df[elig_col].fillna("").str.strip().str.lower()
            auth = filtered_df[auth_col].fillna("").str.strip().str.lower()
            def patient_score(e, a):
                score = 0.0
                # Eligibility
                if e == "checked":
                    score += 0.5
                elif e == "see notes":
                    score += 0.25
                # Authorization
                if a in ["done", "pending"]:
                    score += 0.5
                elif a == "see notes":
                    score += 0.25
                return score
            medsync_calc = [patient_score(e, a) for e, a in zip(elig, auth)]
            filtered_df = filtered_df.copy()
            filtered_df["Medsync calculation"] = medsync_calc
            display_cols.append("Medsync calculation")
            # Show only the selected columns
            display_df = filtered_df[display_cols] if display_cols else filtered_df
            with st.expander(f"View Filtered Data ({len(display_df)} rows)", expanded=True):
                st.dataframe(display_df, use_container_width=True)
                DataTable._create_export_button(display_df)
            # Remove the old summary and instead show a static calculation rules table
            # Split into two tables side by side
            eligibility_rules = [
                ["Eligibility Status", "Score"],
                ["Checked", "+0.5"],
                ["See Notes", "+0.25"],
                ["No Access / Not Checked / Blank", "0"],
            ]
            
            authorization_rules = [
                ["Authorization Status", "Score"],
                ["Done / Pending", "+0.5"],
                ["See Notes", "+0.25"],
                ["Not Required / No Access / Blank", "0"],
            ]
            
            st.markdown('<div class="section-header">How We Calculate Patients</div>', unsafe_allow_html=True)
            
            # Create two columns for side-by-side tables
            col1, col2 = st.columns(2)
            
            with col1:
                st.table(eligibility_rules)
            
            with col2:
                st.table(authorization_rules)
        else:
            # Show only the selected columns
            display_df = filtered_df[display_cols] if display_cols else filtered_df
            with st.expander(f"View Filtered Data ({len(display_df)} rows)", expanded=True):
                st.dataframe(display_df, use_container_width=True)
                DataTable._create_export_button(display_df)
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

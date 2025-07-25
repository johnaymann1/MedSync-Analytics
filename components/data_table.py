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
                if e == "checked":
                    if a in ["done", "pending", "not required"]:
                        return 1.0
                    elif a in ["see notes", "no access"]:
                        return 0.5
                    elif a == "":
                        return 0.0
                    else:
                        return 0.0
                elif e == "see notes":
                    return 0.25
                elif e == "no access" and a in ["done", "pending"]:
                    return 0.5
                else:
                    return 0.0
            medsync_calc = [patient_score(e, a) for e, a in zip(elig, auth)]
            filtered_df = filtered_df.copy()
            filtered_df["Medsync calculation"] = medsync_calc
            display_cols.append("Medsync calculation")
            # Show only the selected columns
            display_df = filtered_df[display_cols] if display_cols else filtered_df
            with st.expander(f"View Filtered Data ({len(display_df)} rows)", expanded=True):
                st.dataframe(display_df, use_container_width=True)
                DataTable._create_export_button(display_df)
            # Add summary table for combinations
            def combo_label(e, a):
                if e == "checked":
                    if a in ["done", "pending", "not required"]:
                        return ("Checked", "Done/Pending/Not Required", 1.0)
                    elif a in ["see notes", "no access"]:
                        return ("Checked", "See Notes/No Access", 0.5)
                    elif a == "":
                        return ("Checked", "Blank", 0.0)
                    else:
                        return ("Checked", "Other", 0.0)
                elif e == "see notes":
                    return ("See Notes", "Any", 0.25)
                elif e == "no access" and a in ["done", "pending"]:
                    return ("No Access", "Done/Pending", 0.5)
                else:
                    return ("Other", "Any", 0.0)
            combos = [combo_label(e, a) for e, a in zip(elig, auth)]
            import pandas as pd
            combo_df = pd.DataFrame(combos, columns=["Eligibility", "Authorization", "Medsync calculation"])
            # Use groupby to count combinations and aggregate Medsync calculation
            summary = combo_df.groupby(["Eligibility", "Authorization", "Medsync calculation"]).size().reset_index(name="Count")
            summary["Weighted Count"] = summary["Medsync calculation"].astype(float) * summary["Count"].astype(float)
            total_weighted = summary["Weighted Count"].sum()
            total_row = pd.DataFrame({
                "Eligibility": ["Total"],
                "Authorization": [""],
                "Medsync calculation": [""],
                "Count": [summary["Count"].sum()],
                "Weighted Count": [total_weighted]
            })
            summary = pd.concat([summary, total_row], ignore_index=True)
            st.markdown('<div class="section-header">Eligibility/Authorization Combination Summary</div>', unsafe_allow_html=True)
            # Rearrange the summary table for logical order
            def sort_key(row):
                elig, auth, calc = row["Eligibility"], row["Authorization"], row["Medsync calculation"]
                if elig == "Checked" and auth == "Done/Pending/Not Required":
                    return (0, 0)
                if elig == "Checked" and auth == "See Notes/No Access":
                    return (0, 1)
                if elig == "Checked" and auth == "Blank":
                    return (0, 2)
                if elig == "Checked":
                    return (0, 3)
                if elig == "See Notes":
                    return (1, 0)
                if elig == "No Access":
                    return (2, 0)
                if elig == "Other":
                    return (3, 0)
                if elig == "Total":
                    return (99, 0)
                return (4, 0)
            summary = summary.sort_values(by=["Eligibility", "Authorization"], key=lambda col: summary.apply(sort_key, axis=1)).reset_index(drop=True)
            st.dataframe(summary, use_container_width=True)
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

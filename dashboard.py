# dashboard.py
"""
MedSync Patient Processing Dashboard - Main Application
Modular and organized dashboard for patient data analysis
"""

import streamlit as st
import pandas as pd
from config import PAGE_CONFIG
from styles import get_custom_css
from components.header import Header
from components.data_input import DataInput
from components.sidebar import Sidebar
from components.data_table import DataTable
from utils.data_processor import DataProcessor
from utils.metrics import MetricsCalculator
from charts.chart_factory import ChartFactory
from charts.status_charts import StatusCharts

class MedSyncDashboard:
    """Main dashboard application class"""
    def __init__(self):
        self.setup_page()

    def setup_page(self):
        """Configure the Streamlit page"""
        st.set_page_config(**PAGE_CONFIG)
        st.markdown(get_custom_css(), unsafe_allow_html=True)

    def run(self):
        """Run the main dashboard application"""
        Header.create_header()
        uploaded_file, gsheet_url = DataInput.create_data_source_section()
        df = DataProcessor.load_data(uploaded_file, gsheet_url)
        if df is None:
            return
        filters = Sidebar.create_filters(df)
        filtered_df = DataProcessor.apply_filters(df, filters)
        st.session_state.filtered_df = filtered_df
        st.session_state.filters = filters
        from components.pdf_export import PDFExport
        PDFExport.create_export_section()
        PDFExport.create_export_info()
        self._display_main_content(filtered_df)

    def _display_main_content(self, filtered_df):
        """Display the main dashboard content"""
        st.markdown('<div class="section-header">Summary Metrics</div>', unsafe_allow_html=True)
        MetricsCalculator.create_summary_metrics(filtered_df)
        col1, col2 = st.columns(2)
        with col1:
            StatusCharts.create_eligibility_status_section(filtered_df)
        with col2:
            StatusCharts.create_authorization_status_section(filtered_df)
        self._display_charts(filtered_df)
        if "Month" in filtered_df.columns and filtered_df["Month"].notna().any():
            # Calculate fully processed patients per month using the new logic
            months = filtered_df["Month"].dropna().unique()
            months = sorted(months)
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
            fully_processed_per_month = []
            for m in months:
                month_df = filtered_df[filtered_df["Month"] == m]
                elig_col = None
                auth_col = None
                for col in ["Eligibility Status", "Eligibility"]:
                    if col in month_df.columns:
                        elig_col = col
                        break
                for col in ["Authorization Status", "Authorization"]:
                    if col in month_df.columns:
                        auth_col = col
                        break
                if elig_col and auth_col:
                    elig = month_df[elig_col].fillna("").str.strip().str.lower()
                    auth = month_df[auth_col].fillna("").str.strip().str.lower()
                    count = sum(patient_score(e, a) for e, a in zip(elig, auth))
                else:
                    count = 0
                fully_processed_per_month.append(count)
            months_formatted = [
                pd.Period(m).strftime('%B %Y') if m else str(m)
                for m in months
            ]
            above_700_col = [count - 700 if count > 700 else 0 for count in fully_processed_per_month]
            df_all_months = pd.DataFrame({
                "Month": months_formatted,
                "Fully Processed Patient Count": fully_processed_per_month,
                "Above 700": above_700_col
            })
            total_patients = sum(fully_processed_per_month)
            total_above_700 = sum(above_700_col)
            total_row = pd.DataFrame({
                "Month": ["Total"],
                "Fully Processed Patient Count": [total_patients],
                "Above 700": [total_above_700]
            })
            df_all_months = pd.concat([df_all_months, total_row], ignore_index=True)
            st.markdown('<div class="section-header">Monthly Patient Counts (with Above 700)</div>', unsafe_allow_html=True)
            st.dataframe(df_all_months, use_container_width=True)
        MetricsCalculator.create_performance_metrics(filtered_df, use_fully_processed=True)
        DataTable.create_data_table_section(filtered_df)

    def _display_charts(self, filtered_df):
        """Display all dashboard charts"""
        st.markdown('<div class="section-header">Data Visualizations</div>', unsafe_allow_html=True)
        chart_functions = [
            ChartFactory.create_doctor_distribution,
            ChartFactory.create_eligibility_status_chart,
            ChartFactory.create_authorization_status_chart,
            ChartFactory.create_patient_status_heatmap,
            ChartFactory.create_processing_efficiency_chart,
            ChartFactory.create_time_trend_chart,
            ChartFactory.create_weekly_trend_chart,
            ChartFactory.create_monthly_trend_chart,
            ChartFactory.create_status_combination_chart,
            ChartFactory.create_days_scheduled_distribution,
            ChartFactory.create_processing_timeline_chart
        ]
        for chart_func in chart_functions:
            fig = chart_func(filtered_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)

def main():
    """Main application entry point"""
    dashboard = MedSyncDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()

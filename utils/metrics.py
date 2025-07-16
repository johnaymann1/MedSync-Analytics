# utils/metrics.py
"""
Metrics calculation utilities for MedSync Dashboard
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from config import WORKING_DAYS

class MetricsCalculator:
    """Handles calculation of various dashboard metrics."""
    @staticmethod
    def count_fully_processed_patients(df):
        """Count patients so that each is counted only once, using eligibility and authorization rules with partial credit for 'See Notes'."""
        elig_col = MetricsCalculator._get_column_variant(df, ["Eligibility Status", "Eligibility"])
        auth_col = MetricsCalculator._get_column_variant(df, ["Authorization Status", "Authorization"])
        if not (elig_col and auth_col):
            return 0

        elig = df[elig_col].fillna("").str.strip().str.lower()
        auth = df[auth_col].fillna("").str.strip().str.lower()

        # Eligibility logic
        elig_checked = elig == "checked"
        elig_see_notes = elig == "see notes"
        elig_no_access = elig == "no access"
        elig_valid = elig_checked | elig_see_notes

        # Authorization logic
        auth_done = auth == "done"
        auth_pending = auth == "pending"
        auth_not_required = auth == "not required"
        auth_see_notes = auth == "see notes"
        auth_no_access = auth == "no access"

        # Per-patient eligibility value
        elig_value = elig_checked.astype(float) + elig_see_notes.astype(float) / 6

        # Per-patient authorization value (only if eligibility is valid)
        auth_value = (
            (auth_done | auth_pending | auth_not_required).astype(float) * elig_valid.astype(float)
            + (auth_see_notes | auth_no_access).astype(float) * elig_valid.astype(float) / 6
        )

        # For each patient, take the maximum of eligibility and authorization value
        patient_value = pd.DataFrame({'elig': elig_value, 'auth': auth_value}).max(axis=1)
        return patient_value.sum()
    @staticmethod
    def _get_column_variant(df, possible_names):
        """Get the first available column name from a list of possibilities."""
        for name in possible_names:
            if name in df.columns:
                return name
        return None
    @staticmethod
    def create_summary_metrics(df):
        """Display summary metrics cards."""
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Patients", len(df))
        with col2:
            doctor_count = df["Doctor"].nunique() if "Doctor" in df.columns else 0
            st.metric("Number of Doctors", doctor_count)
        with col3:
            processed_count = MetricsCalculator.count_fully_processed_patients(df)
            st.metric("Fully Processed Patients", processed_count)
    @staticmethod
    def create_performance_metrics(df, use_fully_processed=False):
        """Display performance metrics section. If use_fully_processed is True, use fully processed patient counts for averages."""
        st.markdown('<div class="section-header">Performance Metrics</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        if use_fully_processed:
            count_func = MetricsCalculator.count_fully_processed_patients
        else:
            count_func = lambda d: len(d)
        with col1:
            avg_per_day = MetricsCalculator._calculate_avg_per_working_day(df, count_func)
            st.metric("Avg Fully Processed Patients per Working Day (Sun-Thurs)", avg_per_day)
        with col2:
            avg_per_month = MetricsCalculator._calculate_avg_per_month(df, count_func)
            st.metric("Avg Fully Processed Patients per Month", avg_per_month)
        with col3:
            avg_per_year = MetricsCalculator._calculate_avg_per_year(df, count_func)
            st.metric("Avg Fully Processed Patients per Year", avg_per_year)

    @staticmethod
    def _calculate_avg_per_working_day(df, count_func=None):
        """Calculate average patients per working day."""
        if count_func is None:
            count_func = lambda d: len(d)
        if "Today's Date" not in df.columns or not df["Today's Date"].notna().any():
            return "N/A"
        min_date = df["Today's Date"].min().date()
        max_date = df["Today's Date"].max().date()
        all_days = pd.date_range(min_date, max_date)
        working_days = [d for d in all_days if d.weekday() in WORKING_DAYS]
        if len(working_days) > 0:
            avg = count_func(df) / len(working_days)
            return f"{avg:.1f}"
        return "N/A"
    @staticmethod
    def _calculate_avg_per_month(df, count_func=None):
        """Calculate average patients per month."""
        if count_func is None:
            count_func = lambda d: len(d)
        if "Today's Date" not in df.columns or not df["Today's Date"].notna().any():
            return "N/A"
        min_date = df["Today's Date"].min()
        max_date = df["Today's Date"].max()
        all_months = pd.period_range(min_date, max_date, freq='M')
        if len(all_months) > 0:
            avg = count_func(df) / len(all_months)
            return f"{avg:.1f}"
        return "N/A"
    @staticmethod
    def _calculate_avg_per_year(df, count_func=None):
        """Calculate average patients per year."""
        if count_func is None:
            count_func = lambda d: len(d)
        if "Today's Date" not in df.columns or not df["Today's Date"].notna().any():
            return "N/A"
        min_date = df["Today's Date"].min()
        max_date = df["Today's Date"].max()
        all_years = pd.period_range(min_date, max_date, freq='Y')
        if len(all_years) > 0:
            avg = count_func(df) / len(all_years)
            return f"{avg:.1f}"
        return "N/A"

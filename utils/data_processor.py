# utils/data_processor.py
"""
Data loading and processing utilities for MedSync Dashboard
"""

import pandas as pd
import streamlit as st
from datetime import datetime
from config import EXPECTED_COLUMNS, DATE_FILTER_THRESHOLD

class DataProcessor:
    """Handles data loading, cleaning, and preprocessing."""
    @staticmethod
    def load_data(uploaded_file, gsheet_url):
        """Load and preprocess the Excel or Google Sheet data."""
        try:
            df = None
            if uploaded_file is not None:
                df = pd.read_excel(uploaded_file)
            elif gsheet_url:
                if 'docs.google.com' in gsheet_url:
                    if '/edit' in gsheet_url:
                        gsheet_url = gsheet_url.split('/edit')[0] + '/export?format=csv'
                    elif not gsheet_url.endswith('export?format=csv'):
                        gsheet_url += '/export?format=csv'
                df = pd.read_csv(gsheet_url)
            else:
                st.warning("Please upload an Excel file or provide a Google Sheet link.")
                return None
            df = DataProcessor._clean_data(df)
            if df is not None:
                st.success(f"Loaded {len(df)} records ready for analysis")
            return df
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return None
    @staticmethod
    def _clean_data(df):
        """Clean and preprocess the dataframe."""
        df = df.dropna(how='all')
        df.columns = df.columns.str.strip()
        df = DataProcessor._map_columns(df)
        df = DataProcessor._process_dates(df)
        if "Days Scheduled" in df.columns:
            df["Days Scheduled"] = pd.to_numeric(df["Days Scheduled"], errors='coerce')
        df = DataProcessor._add_derived_columns(df)
        return df
    @staticmethod
    def _map_columns(df):
        """Map similar column names to expected columns."""
        if not all(col in df.columns for col in EXPECTED_COLUMNS):
            column_mapping = {}
            for expected_col in EXPECTED_COLUMNS:
                for actual_col in df.columns:
                    if expected_col.lower().replace(" ", "") in actual_col.lower().replace(" ", ""):
                        column_mapping[actual_col] = expected_col
                        break
            if column_mapping:
                df = df.rename(columns=column_mapping)
        return df
    @staticmethod
    def _process_dates(df):
        """Process date columns and filter future dates."""
        if "Today's Date" not in df.columns:
            return df
        df["Today's Date"] = pd.to_datetime(df["Today's Date"], errors='coerce')
        invalid_dates = df["Today's Date"].isna().sum()
        if invalid_dates > len(df) * DATE_FILTER_THRESHOLD:
            st.warning(f"⚠️ Found {invalid_dates} rows with invalid dates")
        valid_dates = df[df["Today's Date"].notna()]["Today's Date"]
        if len(valid_dates) > 0:
            today = datetime.now().date()
            future_count = (valid_dates.dt.date > today).sum()
            if future_count > 0:
                st.warning(f"Found {future_count} rows with future dates")
        today = datetime.now().date()
        before_date_filter = len(df)
        df = df[df["Today's Date"].notna() & (df["Today's Date"].dt.date <= today)]
        after_date_filter = len(df)
        if before_date_filter != after_date_filter:
            removed_count = before_date_filter - after_date_filter
            if removed_count > 0:
                st.info(f"Filtered out {removed_count} rows with invalid/future dates")
        return df
    @staticmethod
    def _add_derived_columns(df):
        """Add derived columns for analysis."""
        if "Today's Date" in df.columns:
            df['Month'] = df["Today's Date"].dt.to_period('M').astype(str)
            df['Week'] = df["Today's Date"].dt.to_period('W').astype(str)
        else:
            df['Month'] = None
            df['Week'] = None
        return df
    @staticmethod
    def apply_filters(df, filters):
        """Apply sidebar filters to the dataframe."""
        filtered_df = df.copy()
        if filters.get('doctor') != "All" and "Doctor" in df.columns:
            filtered_df = filtered_df[filtered_df["Doctor"] == filters['doctor']]
        if filters.get('eligibility') != "All" and "Eligibility Status" in df.columns:
            filtered_df = filtered_df[filtered_df["Eligibility Status"] == filters['eligibility']]
        if filters.get('authorization') != "All" and "Authorization Status" in df.columns:
            filtered_df = filtered_df[filtered_df["Authorization Status"] == filters['authorization']]
        if filters.get('date_range') and "Today's Date" in df.columns and len(filters['date_range']) == 2:
            start_date, end_date = filters['date_range']
            filtered_df = filtered_df[
                (filtered_df["Today's Date"].dt.date >= start_date) & 
                (filtered_df["Today's Date"].dt.date <= end_date)
            ]
        return filtered_df

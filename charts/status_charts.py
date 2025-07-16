# charts/status_charts.py
"""
Specialized charts for status analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px


class StatusCharts:
    """Specialized charts for eligibility and authorization status"""
    
    @staticmethod
    def create_eligibility_status_section(df):
        """Create eligibility status counts and percentage chart (case-insensitive)."""
        st.markdown('<div class="section-header">Eligibility Status Counts</div>', 
                   unsafe_allow_html=True)
        
        elig_col = StatusCharts._get_eligibility_column(df)
        if not elig_col:
            st.info("No eligibility column found in the data.")
            return
        
        # Normalize case for status values
        elig_normalized = df[elig_col].fillna("").str.strip().str.lower()
        elig_counts = elig_normalized.value_counts(dropna=False)
        elig_df = elig_counts.reset_index().rename(
            columns={"index": elig_col, elig_col: "Count"}
        )
        st.dataframe(elig_df, use_container_width=True, height=250)
        
        # Create percentage pie chart
        StatusCharts._create_eligibility_pie_chart(df, elig_col)
    
    @staticmethod
    def create_authorization_status_section(df):
        """Create authorization status counts and percentage chart (case-insensitive)."""
        st.markdown('<div class="section-header">Authorization Status Counts</div>', 
                   unsafe_allow_html=True)
        
        auth_col = StatusCharts._get_authorization_column(df)
        if not auth_col:
            st.info("No authorization column found in the data.")
            return
        
        # Normalize case for status values
        auth_normalized = df[auth_col].fillna("").str.strip().str.lower()
        auth_counts = auth_normalized.value_counts(dropna=False)
        auth_df = auth_counts.reset_index().rename(
            columns={"index": auth_col, auth_col: "Count"}
        )
        st.dataframe(auth_df, use_container_width=True, height=250)
        
        # Create percentage pie chart
        StatusCharts._create_authorization_pie_chart(df, auth_col)
    
    @staticmethod
    def _get_eligibility_column(df):
        """Get the eligibility column name"""
        for col in ['Eligibility', 'Eligibility Status']:
            if col in df.columns:
                return col
        return None
    
    @staticmethod
    def _get_authorization_column(df):
        """Get the authorization column name"""
        for col in ['Authorization', 'Authorization Status']:
            if col in df.columns:
                return col
        return None
    
    @staticmethod
    def _create_eligibility_pie_chart(df, elig_col):
        """Create eligibility status pie chart"""
        total_patients = len(df)
        if total_patients == 0:
            return
            
        elig_status_lower = df[elig_col].fillna("").str.strip().str.lower()
        checked_count = (elig_status_lower == "checked").sum()
        not_required_count = (elig_status_lower == "not required").sum()
        processed_count = checked_count + not_required_count
        processed_percentage = (processed_count / total_patients * 100)
        unprocessed_percentage = 100 - processed_percentage
        
        fig_elig = px.pie(
            values=[processed_percentage, unprocessed_percentage],
            names=['Done', 'Not Done'],
            title=f"Eligibility Rate: {processed_percentage:.1f}%",
            color_discrete_sequence=['#08519c', '#3182bd']
        )
        
        StatusCharts._update_pie_chart_layout(fig_elig)
        st.plotly_chart(fig_elig, use_container_width=True)
    
    @staticmethod
    def _create_authorization_pie_chart(df, auth_col):
        """Create authorization status pie chart"""
        total_patients = len(df)
        if total_patients == 0:
            return
            
        auth_status_lower = df[auth_col].fillna("").str.strip().str.lower()
        done_count = (auth_status_lower == "done").sum()
        not_required_count = (auth_status_lower == "not required").sum()
        pending_count = (auth_status_lower == "pending").sum()
        processed_count = done_count + not_required_count + pending_count
        processed_percentage = (processed_count / total_patients * 100)
        unprocessed_percentage = 100 - processed_percentage
        
        fig_auth = px.pie(
            values=[processed_percentage, unprocessed_percentage],
            names=['Done', 'Not Done'],
            title=f"Authorization Rate: {processed_percentage:.1f}%",
            color_discrete_sequence=['#08519c', '#3182bd']
        )
        
        StatusCharts._update_pie_chart_layout(fig_auth)
        st.plotly_chart(fig_auth, use_container_width=True)
    
    @staticmethod
    def _update_pie_chart_layout(fig):
        """Update pie chart layout with consistent styling"""
        fig.update_traces(
            textposition='inside', 
            textinfo='percent',
            textfont=dict(size=14, color='white'),
            marker=dict(line=dict(color='rgba(255,255,255,0.2)', width=1))
        )
        fig.update_layout(
            height=350,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(color='white', size=12)
            ),
            title=dict(
                font=dict(size=16, color='white'),
                x=0.5,
                xanchor='center'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

# charts/chart_factory.py
"""
Chart creation utilities for MedSync Dashboard
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import CHART_HEIGHT, TALL_CHART_HEIGHT, COLOR_SCHEMES


class ChartFactory:
    """Factory class for creating dashboard charts"""
    
    @staticmethod
    def create_doctor_distribution(df):
        """Bar chart: Patients per doctor"""
        if "Doctor" not in df.columns:
            return None
            
        doctor_counts = df["Doctor"].value_counts()
        fig = px.bar(
            x=doctor_counts.index,
            y=doctor_counts.values,
            title="Patients per Doctor",
            labels={"x": "Doctor", "y": "Patients"}
        )
        fig.update_layout(showlegend=False, height=CHART_HEIGHT)
        return fig
    
    @staticmethod
    def create_eligibility_status_chart(df):
        """Pie chart: Eligibility status distribution"""
        if "Eligibility Status" not in df.columns:
            return None
            
        status_counts = df["Eligibility Status"].value_counts()
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Eligibility Status"
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=CHART_HEIGHT)
        return fig
    
    @staticmethod
    def create_authorization_status_chart(df):
        """Bar chart: Authorization status distribution"""
        if "Authorization Status" not in df.columns:
            return None
            
        status_counts = df["Authorization Status"].value_counts()
        fig = px.bar(
            x=status_counts.index,
            y=status_counts.values,
            title="Authorization Status",
            labels={"x": "Status", "y": "Count"},
            color=status_counts.values,
            color_continuous_scale=COLOR_SCHEMES["plasma"]
        )
        fig.update_layout(showlegend=False, height=CHART_HEIGHT)
        return fig
    
    @staticmethod
    def create_patient_status_heatmap(df):
        """Heatmap: Patient eligibility status by doctor"""
        if "Doctor" not in df.columns or "Eligibility Status" not in df.columns:
            return None
            
        eligibility_doctor = pd.crosstab(df['Doctor'], df['Eligibility Status'])
        fig = px.imshow(
            eligibility_doctor.values,
            x=eligibility_doctor.columns,
            y=eligibility_doctor.index,
            title="Patient Eligibility Status by Doctor (Heatmap)",
            color_continuous_scale=COLOR_SCHEMES["rdylbu"],
            text_auto=True
        )
        fig.update_layout(
            height=CHART_HEIGHT, 
            xaxis_title="Eligibility Status", 
            yaxis_title="Doctor"
        )
        return fig
    
    @staticmethod
    def create_processing_efficiency_chart(df):
        """Bar chart: Authorization completion rate by doctor"""
        if "Doctor" not in df.columns or "Authorization Status" not in df.columns:
            return None
            
        doctor_stats = df.groupby('Doctor').agg(
            Total_Patients=('Authorization Status', 'count'),
            Completed=('Authorization Status', 
                      lambda x: x.fillna('').astype(str).str.strip().str.lower().eq('done').sum())
        ).reset_index()
        
        doctor_stats['Completion_Rate'] = (
            doctor_stats['Completed'] / doctor_stats['Total_Patients'] * 100
        ).round(1)
        
        fig = px.bar(
            doctor_stats,
            x='Doctor',
            y='Completion_Rate',
            title="Authorization Completion Rate by Doctor (%)",
            labels={"Completion_Rate": "Completion Rate (%)", "Doctor": "Doctor"},
            color='Completion_Rate',
            color_continuous_scale=COLOR_SCHEMES["greens"],
            text='Completion_Rate'
        )
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        fig.update_layout(showlegend=False, height=CHART_HEIGHT)
        return fig
    
    @staticmethod
    def create_time_trend_chart(df):
        """Line chart: Daily processing trend"""
        if "Today's Date" not in df.columns or not df["Today's Date"].notna().any():
            return None
            
        daily_counts = df.groupby(df["Today's Date"].dt.date).size().reset_index()
        daily_counts.columns = ["Date", "Patients Processed"]
        
        fig = px.line(
            daily_counts,
            x="Date",
            y="Patients Processed",
            title="Processing Trend",
            markers=True
        )
        fig.update_layout(height=CHART_HEIGHT)
        return fig
    
    @staticmethod
    def create_weekly_trend_chart(df):
        """Bar chart: Weekly patient processing trend"""
        if "Today's Date" not in df.columns or not df["Today's Date"].notna().any():
            return None
            
        df_temp = df.copy()
        df_temp['Week_Start'] = df_temp["Today's Date"].dt.to_period('W').dt.start_time
        weekly_counts = df_temp.groupby('Week_Start').size().reset_index()
        weekly_counts.columns = ["Week_Start", "Patients_Processed"]
        
        fig = px.bar(
            weekly_counts,
            x="Week_Start",
            y="Patients_Processed",
            title="Weekly Patient Processing Trend",
            labels={"Patients_Processed": "Patients Processed", "Week_Start": "Week"},
            color="Patients_Processed",
            color_continuous_scale=COLOR_SCHEMES["blues"]
        )
        fig.update_layout(showlegend=False, height=CHART_HEIGHT)
        return fig
    
    @staticmethod
    def create_monthly_trend_chart(df):
        """Bar chart: Monthly patient processing trend"""
        if "Month" not in df.columns or not df["Month"].notna().any():
            return None
            
        monthly_counts = df["Month"].value_counts().sort_index()
        fig = px.bar(
            x=monthly_counts.index,
            y=monthly_counts.values,
            title="Patients Processed per Month",
            labels={"x": "Month", "y": "Number of Patients"},
            color=monthly_counts.values,
            color_continuous_scale=COLOR_SCHEMES["blues"]
        )
        fig.update_layout(showlegend=False, height=CHART_HEIGHT)
        return fig
    
    @staticmethod
    def create_status_combination_chart(df):
        """Bar chart: Top combinations of eligibility and authorization status"""
        required_cols = ["Eligibility Status", "Authorization Status"]
        if not all(col in df.columns for col in required_cols):
            return None
            
        df_temp = df.copy()
        df_temp['Combined_Status'] = (
            df_temp['Eligibility Status'] + ' + ' + df_temp['Authorization Status']
        )
        status_counts = df_temp['Combined_Status'].value_counts().head(10)
        
        fig = px.bar(
            x=status_counts.values,
            y=status_counts.index,
            orientation='h',
            title="Top Status Combinations (Eligibility + Authorization)",
            labels={"x": "Count", "y": "Status Combination"},
            color=status_counts.values,
            color_continuous_scale=COLOR_SCHEMES["viridis"]
        )
        fig.update_layout(
            showlegend=False, 
            height=TALL_CHART_HEIGHT, 
            yaxis={'categoryorder':'total ascending'}
        )
        return fig
    
    @staticmethod
    def create_days_scheduled_distribution(df):
        """Histogram: Distribution of days scheduled"""
        if "Days Scheduled" not in df.columns or not df["Days Scheduled"].notna().any():
            return None
            
        # Remove outliers using IQR
        q1 = df["Days Scheduled"].quantile(0.25)
        q3 = df["Days Scheduled"].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        filtered_data = df[
            (df["Days Scheduled"] >= lower_bound) & 
            (df["Days Scheduled"] <= upper_bound)
        ]
        
        fig = px.histogram(
            filtered_data,
            x="Days Scheduled",
            title="Distribution of Days Scheduled",
            labels={"Days Scheduled": "Days Scheduled", "count": "Number of Patients"},
            nbins=20,
            color_discrete_sequence=["#636EFA"]
        )
        fig.update_layout(height=CHART_HEIGHT, showlegend=False)
        return fig
    
    @staticmethod
    def create_processing_timeline_chart(df):
        """Line chart: Patient processing by hour of day"""
        if "Today's Date" not in df.columns or not df["Today's Date"].notna().any():
            return None
            
        df_temp = df.copy()
        df_temp['Hour'] = df_temp["Today's Date"].dt.hour
        hourly_counts = df_temp.groupby('Hour').size().reset_index()
        hourly_counts.columns = ["Hour", "Count"]
        
        fig = px.line(
            hourly_counts,
            x="Hour",
            y="Count",
            title="Patient Processing by Hour of Day",
            markers=True,
            labels={"Hour": "Hour of Day", "Count": "Patients Processed"}
        )
        fig.update_layout(height=CHART_HEIGHT, xaxis=dict(tickmode='linear', dtick=2))
        return fig

    @staticmethod
    def create_months_above_700_chart(df):
        """Bar chart: Number of patients per month (only months >700), and show total sum as annotation."""
        if "Month" not in df.columns or not df["Month"].notna().any():
            return None
        
        monthly_counts = df["Month"].value_counts().sort_index()
        above_700 = monthly_counts[monthly_counts > 700]
        total_above_700 = above_700.sum()
        if above_700.empty:
            return None
        fig = px.bar(
            x=above_700.index,
            y=above_700.values,
            title=f"Months with >700 Patients (Total: {total_above_700})",
            labels={"x": "Month", "y": "Number of Patients"},
            color=above_700.values,
            color_continuous_scale=COLOR_SCHEMES["blues"]
        )
        fig.add_annotation(
            text=f"Total patients in months >700: {total_above_700}",
            xref="paper", yref="paper",
            x=0.5, y=1.08, showarrow=False,
            font=dict(size=16, color="#08519c")
        )
        fig.update_layout(showlegend=False, height=CHART_HEIGHT)
        return fig

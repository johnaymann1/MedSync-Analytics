# utils/pdf_generator.py
"""
PDF report generation utilities for MedSync Dashboard
"""

import io
import base64
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio
from PIL import Image as PILImage
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend


class PDFReportGenerator:
    """Handles PDF report generation for MedSync Dashboard"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the report"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1f77b4')
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#2c3e50')
        ))
        
        # Subsection header style
        self.styles.add(ParagraphStyle(
            name='SubsectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=12,
            textColor=colors.HexColor('#34495e')
        ))
    
    def generate_report(self, filtered_df, filters, charts_data=None):
        """Generate a complete PDF report"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch)
        story = []
        
        # Add header and title
        story.extend(self._create_header())
        
        # Add executive summary
        story.extend(self._create_executive_summary(filtered_df))
        
        # Add filters section
        story.extend(self._create_filters_section(filters))
        
        # Add metrics section
        story.extend(self._create_metrics_section(filtered_df))
        
        # Add data analysis section
        story.extend(self._create_data_analysis_section(filtered_df))
        
        # Add detailed data table
        story.extend(self._create_data_table_section(filtered_df))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _create_header(self):
        """Create report header"""
        elements = []
        
        # Title
        title = Paragraph("MedSync Patient Processing Report", self.styles['CustomTitle'])
        elements.append(title)
        
        # Generation date
        date_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        date_para = Paragraph(f"Generated on: {date_str}", self.styles['Normal'])
        elements.append(date_para)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_executive_summary(self, df):
        """Create executive summary section"""
        elements = []
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        
        # Calculate key metrics
        total_patients = len(df)
        processed_patients = self._count_fully_processed_patients(df)
        processing_rate = (processed_patients / total_patients * 100) if total_patients > 0 else 0
        
        # Create summary text
        summary_text = f"""
        This report provides a comprehensive analysis of patient processing data for MedSync.
        
        <b>Key Highlights:</b><br/>
        • Total Patients Analyzed: {total_patients:,}<br/>
        • Fully Processed Patients: {processed_patients:,}<br/>
        • Overall Processing Rate: {processing_rate:.1f}%<br/>
        • Report Period: {self._get_date_range(df)}<br/>
        """
        
        summary_para = Paragraph(summary_text, self.styles['Normal'])
        elements.append(summary_para)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_filters_section(self, filters):
        """Create applied filters section"""
        elements = []
        elements.append(Paragraph("Applied Filters", self.styles['SectionHeader']))
        
        filter_text = "<b>The following filters were applied to generate this report:</b><br/><br/>"
        
        for filter_name, filter_value in filters.items():
            if filter_value:
                if filter_name == 'date_range' and isinstance(filter_value, (list, tuple)) and len(filter_value) == 2:
                    filter_text += f"• Date Range: {filter_value[0].strftime('%m/%d/%Y')} to {filter_value[1].strftime('%m/%d/%Y')}<br/>"
                elif isinstance(filter_value, list) and len(filter_value) > 0:
                    filter_text += f"• {filter_name.title()}: {', '.join(map(str, filter_value))}<br/>"
                elif not isinstance(filter_value, list):
                    filter_text += f"• {filter_name.title()}: {filter_value}<br/>"
        
        if not any(filters.values()):
            filter_text += "• No filters applied - showing all data<br/>"
        
        filter_para = Paragraph(filter_text, self.styles['Normal'])
        elements.append(filter_para)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_metrics_section(self, df):
        """Create key metrics section"""
        elements = []
        elements.append(Paragraph("Key Performance Metrics", self.styles['SectionHeader']))
        
        # Calculate metrics
        metrics = self._calculate_key_metrics(df)
        
        # Create metrics table
        metrics_data = [
            ['Metric', 'Value', 'Description'],
            ['Total Patients', f"{metrics['total_patients']:,}", 'Total number of patients in dataset'],
            ['Fully Processed', f"{metrics['processed_patients']:,}", 'Patients with complete processing'],
            ['Processing Rate', f"{metrics['processing_rate']:.1f}%", 'Percentage of patients fully processed'],
            ['Avg Days to Process', f"{metrics['avg_processing_days']:.1f}", 'Average days from entry to completion'],
            ['Unique Doctors', f"{metrics['unique_doctors']:,}", 'Number of different doctors'],
        ]
        
        metrics_table = Table(metrics_data, colWidths=[2.5*inch, 1.5*inch, 3*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        elements.append(metrics_table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_data_analysis_section(self, df):
        """Create data analysis section with status breakdowns"""
        elements = []
        elements.append(Paragraph("Data Analysis", self.styles['SectionHeader']))
        
        # Eligibility Status Analysis
        elements.append(Paragraph("Eligibility Status Breakdown", self.styles['SubsectionHeader']))
        elig_analysis = self._create_status_breakdown(df, 'Eligibility Status', 'Eligibility')
        elements.append(elig_analysis)
        elements.append(Spacer(1, 10))
        
        # Authorization Status Analysis
        elements.append(Paragraph("Authorization Status Breakdown", self.styles['SubsectionHeader']))
        auth_analysis = self._create_status_breakdown(df, 'Authorization Status', 'Authorization')
        elements.append(auth_analysis)
        elements.append(Spacer(1, 10))
        
        # Doctor Distribution
        elements.append(Paragraph("Doctor Distribution", self.styles['SubsectionHeader']))
        doctor_analysis = self._create_doctor_distribution(df)
        elements.append(doctor_analysis)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_status_breakdown(self, df, primary_col, secondary_col):
        """Create a status breakdown table"""
        # Try primary column first, then secondary
        status_col = primary_col if primary_col in df.columns else secondary_col
        
        if status_col not in df.columns:
            return Paragraph(f"Status column not found in data", self.styles['Normal'])
        
        status_counts = df[status_col].value_counts().fillna('Unknown')
        total = len(df)
        
        # Create table data
        table_data = [['Status', 'Count', 'Percentage']]
        for status, count in status_counts.items():
            percentage = (count / total * 100) if total > 0 else 0
            table_data.append([str(status), f"{count:,}", f"{percentage:.1f}%"])
        
        # Add total row
        table_data.append(['Total', f"{total:,}", "100.0%"])
        
        # Create table
        table = Table(table_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.lightgrey]),
        ]))
        
        return table
    
    def _create_doctor_distribution(self, df):
        """Create doctor distribution table"""
        doctor_col = 'Doctor' if 'Doctor' in df.columns else 'Provider'
        
        if doctor_col not in df.columns:
            return Paragraph("Doctor/Provider column not found in data", self.styles['Normal'])
        
        doctor_counts = df[doctor_col].value_counts().head(10)  # Top 10 doctors
        total = len(df)
        
        # Create table data
        table_data = [['Doctor', 'Patients', 'Percentage']]
        for doctor, count in doctor_counts.items():
            percentage = (count / total * 100) if total > 0 else 0
            table_data.append([str(doctor)[:30], f"{count:,}", f"{percentage:.1f}%"])  # Truncate long names
        
        # Create table
        table = Table(table_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        return table
    
    def _create_data_table_section(self, df):
        """Create detailed data table section"""
        elements = []
        elements.append(PageBreak())  # Start on new page
        elements.append(Paragraph("Detailed Data", self.styles['SectionHeader']))
        
        # Limit to first 50 rows for PDF space
        display_df = df.head(50)
        
        if len(df) > 50:
            note_text = f"<i>Note: Showing first 50 records of {len(df)} total records</i>"
            elements.append(Paragraph(note_text, self.styles['Normal']))
            elements.append(Spacer(1, 10))
        
        # Select key columns for display
        key_columns = []
        for col in ['Patient ID', 'Patient Name', 'Doctor', 'Provider', 'Eligibility Status', 'Authorization Status', 'Date Scheduled']:
            if col in df.columns:
                key_columns.append(col)
        
        if not key_columns:
            key_columns = df.columns[:6].tolist()  # First 6 columns if no standard columns found
        
        # Create table data
        table_data = [key_columns]  # Header row
        
        for _, row in display_df.iterrows():
            row_data = []
            for col in key_columns:
                value = str(row[col]) if pd.notna(row[col]) else ''
                # Truncate long values
                if len(value) > 20:
                    value = value[:20] + '...'
                row_data.append(value)
            table_data.append(row_data)
        
        # Calculate column widths
        col_width = 7*inch / len(key_columns)
        col_widths = [col_width] * len(key_columns)
        
        # Create table
        data_table = Table(table_data, colWidths=col_widths)
        data_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8e44ad')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        elements.append(data_table)
        
        return elements
    
    def _calculate_key_metrics(self, df):
        """Calculate key metrics for the report"""
        metrics = {}
        
        metrics['total_patients'] = len(df)
        metrics['processed_patients'] = self._count_fully_processed_patients(df)
        metrics['processing_rate'] = (metrics['processed_patients'] / metrics['total_patients'] * 100) if metrics['total_patients'] > 0 else 0
        
        # Calculate average processing days if date columns exist
        metrics['avg_processing_days'] = self._calculate_avg_processing_days(df)
        
        # Count unique doctors
        doctor_col = 'Doctor' if 'Doctor' in df.columns else 'Provider'
        if doctor_col in df.columns:
            metrics['unique_doctors'] = df[doctor_col].nunique()
        else:
            metrics['unique_doctors'] = 0
        
        return metrics
    
    def _count_fully_processed_patients(self, df):
        """Count patients using the new additive calculation logic everywhere in the PDF report."""
        elig_col = self._get_column_variant(df, ["Eligibility Status", "Eligibility"])
        auth_col = self._get_column_variant(df, ["Authorization Status", "Authorization"])
        if not (elig_col and auth_col):
            return 0

        elig = df[elig_col].fillna("").str.strip().str.lower()
        auth = df[auth_col].fillna("").str.strip().str.lower()
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
        return sum(patient_score(e, a) for e, a in zip(elig, auth))
    
    def _get_column_variant(self, df, possible_names):
        """Get the first available column name from a list of possibilities"""
        for name in possible_names:
            if name in df.columns:
                return name
        return None
    
    def _calculate_avg_processing_days(self, df):
        """Calculate average processing days"""
        # Look for date columns
        date_columns = []
        for col in df.columns:
            if 'date' in col.lower() or 'scheduled' in col.lower():
                date_columns.append(col)
        
        if date_columns:
            try:
                # Try to calculate days from first date column to today
                date_col = date_columns[0]
                df_dates = pd.to_datetime(df[date_col], errors='coerce')
                valid_dates = df_dates.dropna()
                if len(valid_dates) > 0:
                    avg_days = (datetime.now() - valid_dates).dt.days.mean()
                    return max(0, avg_days)  # Don't return negative days
            except:
                pass
        
        return 0.0
    
    def _get_date_range(self, df):
        """Get the date range of the data"""
        date_columns = []
        for col in df.columns:
            if 'date' in col.lower() or 'scheduled' in col.lower():
                date_columns.append(col)
        
        if date_columns:
            try:
                date_col = date_columns[0]
                df_dates = pd.to_datetime(df[date_col], errors='coerce')
                valid_dates = df_dates.dropna()
                if len(valid_dates) > 0:
                    min_date = valid_dates.min().strftime('%m/%d/%Y')
                    max_date = valid_dates.max().strftime('%m/%d/%Y')
                    return f"{min_date} to {max_date}"
            except:
                pass
        
        return "Date range not available"
    
    @staticmethod
    def create_download_link(buffer, filename="medsync_report.pdf"):
        """Create a download link for the PDF"""
        b64 = base64.b64encode(buffer.getvalue()).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">📄 Download PDF Report</a>'
        return href

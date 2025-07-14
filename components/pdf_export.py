# components/pdf_export.py
"""
PDF Export component for MedSync Dashboard
"""

import streamlit as st
from utils.pdf_generator import PDFReportGenerator

class PDFExport:
    """Handles PDF export functionality."""
    @staticmethod
    def create_export_section(filtered_df=None, filters=None):
        """Create PDF export section in sidebar."""
        if filtered_df is None and hasattr(st.session_state, 'filtered_df'):
            filtered_df = st.session_state.filtered_df
        if filters is None and hasattr(st.session_state, 'filters'):
            filters = st.session_state.filters
        st.sidebar.markdown("### 📄 Export Reports")
        if filtered_df is None or len(filtered_df) == 0:
            st.sidebar.info("Load data to enable export")
            return
        st.sidebar.markdown(f"**{len(filtered_df)}** records ready")
        if st.sidebar.button("Generate PDF Report", key="pdf_export", use_container_width=True):
            PDFExport._generate_and_download_pdf(filtered_df, filters or {})
    @staticmethod
    def _generate_and_download_pdf(filtered_df, filters):
        """Generate PDF report and provide download link."""
        try:
            with st.spinner("Generating PDF report..."):
                pdf_generator = PDFReportGenerator()
                pdf_buffer = pdf_generator.generate_report(filtered_df, filters)
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"medsync_report_{timestamp}.pdf"
                st.sidebar.download_button(
                    label="Download PDF Report",
                    data=pdf_buffer.getvalue(),
                    file_name=filename,
                    mime="application/pdf",
                    key="download_pdf",
                    use_container_width=True
                )
                st.sidebar.success("PDF report generated successfully!")
        except ImportError as e:
            st.sidebar.error("PDF generation requires additional packages. Please install reportlab, matplotlib, and Pillow.")
            st.sidebar.code("pip install reportlab matplotlib Pillow")
        except Exception as e:
            st.sidebar.error(f"Error generating PDF: {str(e)}")
            st.sidebar.info("Please check your data and try again.")
    @staticmethod
    def create_export_info():
        """Create information section about PDF export."""
        with st.sidebar.expander("Report Details"):
            st.markdown("""
            **PDF includes:**
            - Key metrics & rates
            - Applied filters  
            - Status breakdowns
            - Sample data table
            
            *Generated with current filters*
            """)

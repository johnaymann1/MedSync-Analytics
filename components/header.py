# components/header.py
"""
Header component for the dashboard
"""

import streamlit as st
from utils.logo_utils import display_logo

class Header:
    """Handles the dashboard header display."""
    @staticmethod
    def create_header():
        """Create the main dashboard header."""
        st.markdown(f"""
        <div class="main-header-container">
            <div class="logo-container">
                {display_logo()}
            </div>
            <div class="main-subtitle">Office visits Analytics</div>
        </div>
        """, unsafe_allow_html=True)

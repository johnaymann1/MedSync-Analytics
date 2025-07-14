# utils/logo_utils.py
"""
Logo handling utilities for MedSync Dashboard
"""

import os
import base64
import streamlit as st
from config import LOGO_FILES

def get_logo_base64(logo_path):
    """Convert logo image to base64 string."""
    try:
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    except Exception as e:
        st.error(f"Error loading logo: {e}")
    return None

def display_logo():
    """Display company logo or fallback."""
    for logo_file in LOGO_FILES:
        logo_base64 = get_logo_base64(logo_file)
        if logo_base64:
            file_extension = logo_file.split('.')[-1].lower()
            mime_type = f"image/{file_extension if file_extension != 'svg' else 'svg+xml'}"
            return f'''<img src="data:{mime_type};base64,{logo_base64}" style="width: 120px; height: 120px; border-radius: 12px; object-fit: cover; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">'''
    return '<div class="logo-placeholder">🏥</div>'

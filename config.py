# config.py
"""
Configuration settings for MedSync Dashboard
"""

PAGE_CONFIG = {
    "page_title": "MedSync Patient Processing Dashboard",
    "page_icon": "🏥",
    "layout": "wide",
    "initial_sidebar_state": "collapsed"
}

EXPECTED_COLUMNS = [
    "Patient Name", 
    "Doctor", 
    "Eligibility Status", 
    "Authorization Status", 
    "Notes / Questions", 
    "Today's Date", 
    "Days Scheduled"
]

LOGO_FILES = [
    "company_logo.png"
]

CHART_HEIGHT = 400
HEATMAP_HEIGHT = 400
TALL_CHART_HEIGHT = 600

COLOR_SCHEMES = {
    "primary": "#667eea",
    "secondary": "#764ba2",
    "success": "#08519c",
    "info": "#3182bd",
    "plasma": "plasma",
    "blues": "blues",
    "greens": "Greens",
    "viridis": "Viridis",
    "rdylbu": "RdYlBu_r"
}

WORKING_DAYS = [6, 0, 1, 2, 3]
DATE_FILTER_THRESHOLD = 0.1

# styles.py
"""
CSS styling for MedSync Dashboard
"""

def get_custom_css():
    """Return the custom CSS for the dashboard."""
    return """
<style>
    .main-header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
        border-radius: 12px;
        margin-bottom: 2.5rem;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
    }
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .logo-placeholder {
        font-size: 3rem;
        color: #ffffff;
    }
    .main-subtitle {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.8);
        margin-top: 0.5rem;
        font-weight: 300;
    }
    .section-header {
        font-size: 1.4rem;
        font-weight: 500;
        color: #ffffff;
        background: rgba(255, 255, 255, 0.05);
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        margin: 2.2rem 0 1.2rem 0;
        border-left: 3px solid #667eea;
        backdrop-filter: blur(10px);
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        backdrop-filter: blur(10px);
    }
    .filter-header {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 1rem;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    }
    .stButton button {
        background: #667eea;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 500;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        background: #5a6fd8;
        transform: translateY(-1px);
    }
    .sidebar .stButton button:contains("Clear All Filters") {
        background: #dc3545 !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        width: 100% !important;
        margin-bottom: 1rem !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    .sidebar .stButton button:contains("Clear All Filters"):hover {
        background: #c82333 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 8px rgba(220, 53, 69, 0.3) !important;
    }
    .stInfo {
        background: rgba(103, 126, 234, 0.1);
        border: 1px solid rgba(103, 126, 234, 0.3);
        border-radius: 6px;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .plotly-graph-div {
        margin: 1.5rem 0;
    }
</style>
"""

#!/bin/bash
# Run MedSync Dashboard

# Navigate to dashboard directory
cd "$(dirname "$0")"

# Activate virtual environment
source new_medsync_env/bin/activate

# Run the modular dashboard
streamlit run dashboard.py
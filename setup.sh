#!/bin/bash

# MedSync Dashboard Setup Script
echo "🏥 Setting up MedSync Patient Processing Dashboard..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv medsync_env

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source medsync_env/bin/activate

# Install required packages
echo "📥 Installing required packages..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To run the dashboard:"
echo "1. Activate the virtual environment: source medsync_env/bin/activate"
echo "2. Run the dashboard: streamlit run medsync_dashboard.py"
echo ""
echo "The dashboard will open in your web browser at http://localhost:8501"

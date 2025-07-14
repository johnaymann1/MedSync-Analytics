# MedSync Patient Processing Dashboard

A modular and organized dashboard for patient data analysis, built with Streamlit.

## 🚀 Overview

The MedSync Dashboard helps visualize and analyze patient processing data for healthcare providers. It offers:
- Data upload from files or Google Sheets
- Interactive filters and summary metrics
- Visual charts for eligibility, authorization, and patient status
- Export to PDF functionality

## 🖥️ Live Demo

You can try the dashboard live here:  
*(Add your Streamlit Cloud link after deployment)*

## 📦 Features

- **Data Input:** Upload CSV files or connect to Google Sheets
- **Filtering:** Filter patient data by various criteria
- **Charts:** Visualize key metrics and trends
- **PDF Export:** Download filtered data and charts as a PDF
- **Responsive UI:** Clean, modern interface

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/johnaymann1/MedSync-Analytics.git
   cd MedSync-Analytics
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard:**
   ```bash
   streamlit run dashboard.py
   ```

## 📁 Project Structure

```
.
├── charts/           # Chart generation modules
├── components/       # UI components (header, sidebar, data input, etc.)
├── utils/            # Data processing and utility functions
├── styles.py         # Custom CSS for Streamlit
├── config.py         # Page configuration
├── dashboard.py      # Main application file
├── requirements.txt  # Python dependencies
```

## ⚙️ Usage

- Launch the dashboard locally or deploy it on [Streamlit Cloud](https://streamlit.io/cloud).
- Upload your patient data (CSV or Google Sheet).
- Use the sidebar to filter and explore the data.
- View summary metrics, charts, and export results as PDF.

## 🌐 Deployment

**Deploy for free on Streamlit Cloud:**
1. Make sure your repo is public.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud).
3. Click “New app”, select this repo, and set `dashboard.py` as the main file.
4. Click “Deploy”.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 📄 License

MIT License

---

*Created by [John Ayman](https://github.com/johnaymann1)* 
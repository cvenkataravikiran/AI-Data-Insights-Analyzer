# Getting Started with InsightLens AI

Welcome to **InsightLens AI**! This guide will help you get up and running quickly.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [First Run](#first-run)
4. [Basic Workflow](#basic-workflow)
5. [Common Issues](#common-issues)
6. [Next Steps](#next-steps)

---

## Prerequisites

Before you begin, ensure you have the following installed:

### Required
- **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/)
- **pip**: Usually comes with Python
- **Git** (for cloning): Download from [git-scm.com](https://git-scm.com/)

### Optional
- **OpenAI API Key**: For AI-powered insights ([Get one here](https://platform.openai.com/api-keys))
  - Not required! The app works great with rule-based analysis

### Verify Installation
```bash
# Check Python version
python --version
# Should show Python 3.8.0 or higher

# Check pip
pip --version
```

---

## Installation

### Method 1: Clone from GitHub (Recommended)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/InsightLens-AI.git
   cd InsightLens-AI
   ```

2. **Create Virtual Environment**
   
   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   
   You should see `(venv)` in your terminal prompt.

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   This will install:
   - Streamlit (web framework)
   - Pandas (data processing)
   - Plotly (visualizations)
   - Scikit-learn (ML models)
   - OpenAI (optional AI features)
   - Other supporting libraries

4. **Configure Environment** (Optional - for AI features)
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env with your favorite text editor
   # Add your OpenAI API key (or leave as is for rule-based mode)
   notepad .env  # Windows
   nano .env     # macOS/Linux
   ```
   
   Your `.env` should look like:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   USE_OPENAI=true
   ```

### Method 2: Download ZIP

1. Download ZIP from GitHub
2. Extract to desired location
3. Follow steps 2-4 above

---

## First Run

### Start the Application

```bash
streamlit run app.py
```

**What happens:**
- Streamlit starts a local web server
- Your default browser opens automatically
- App loads at `http://localhost:8501`

**Terminal output will show:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.1.x:8501
```

### Troubleshooting First Run

**Issue: "Command not found: streamlit"**
```bash
# Ensure virtual environment is activated
# You should see (venv) in terminal

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Re-run
streamlit run app.py
```

**Issue: "ModuleNotFoundError: No module named 'streamlit'"**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**Issue: Port 8501 already in use**
```bash
# Use different port
streamlit run app.py --server.port 8502
```

---

## Basic Workflow

### Step 1: Launch Application

```bash
streamlit run app.py
```

### Step 2: Explore Landing Page

The landing page showcases:
- ✨ Key features
- 📁 Supported formats
- 🔄 How it works
- 🛠️ Technology stack

**Action:** Click **"🚀 Get Started - Upload Your Data"**

### Step 3: Upload Dataset

1. Click **"📁 Upload Data"** in sidebar
2. Choose CSV or Excel file
3. System automatically:
   - Validates file format
   - Detects encodings
   - Maps columns
   - Displays preview

**Example datasets:**
- Sales data with Date, Product, Sales, Profit columns
- Any CSV with at least one numeric column
- Excel files with multiple sheets (uses first sheet)

**Dataset Preview shows:**
- First 10 rows
- Total rows and columns
- Memory usage
- Detected column mappings

### Step 4: Clean Data

1. Navigate to **"🧹 Data Cleaning"**
2. Review data quality report:
   - Missing values count
   - Duplicate rows
   - Column summary
3. Select cleaning options:
   - ✅ Remove duplicates
   - ✅ Handle missing values (drop/mean/median)
4. Click **"✨ Clean Data"**
5. Review before/after statistics

### Step 5: Assess Data Quality

1. Go to **"📊 Data Quality"**
2. View comprehensive assessment:
   - **Overall Score** (0-100%)
   - **Dimension Scores:**
     - Completeness
     - Consistency
     - Uniqueness
     - Validity
3. Review column-wise quality metrics
4. Read actionable recommendations

### Step 6: Generate Executive Summary

1. Navigate to **"📋 Executive Summary"**
2. Click **"🚀 Generate Executive Summary"**
3. Review AI-generated insights:
   - Business overview
   - Positive findings
   - Areas of concern
   - Growth opportunities
   - Business risks
   - Strategic recommendations
   - AI conclusion

### Step 7: Explore KPI Dashboard

1. Go to **"📈 KPI Dashboard"**
2. View automatically detected KPIs:
   - Total Sales/Revenue
   - Total Profit
   - Average metrics
   - Top products/regions
3. Review AI-generated business insights
4. Explore performance charts

### Step 8: Analyze Visualizations

1. Navigate to **"📉 Visualizations"**
2. Select visualization type:
   - Sales Trends (time series)
   - Distribution Analysis (histograms, box plots)
   - Correlation Heatmap
   - Regional Performance
   - Product Analysis
3. Interact with charts (zoom, pan, hover)

### Step 9: Generate Forecasts

1. Go to **"🔮 Forecasting"**
2. Configure forecast:
   - Select periods (1-12 months)
   - Review model (Linear Regression)
3. Click **"🚀 Generate Forecast"**
4. Analyze results:
   - Model accuracy (R² score)
   - Forecast chart
   - Predictions table

### Step 10: Ask Questions (Conversational Analytics)

1. Navigate to **"🤖 Ask Your Data"**
2. Review example questions
3. Type your question:
   - "Which region had highest revenue?"
   - "What is the profit margin?"
   - "Show top 5 products"
4. Get instant answers with:
   - Text explanation
   - Supporting data
   - Visualizations

### Step 11: Generate Report

1. Go to **"📑 Generate Report"**
2. Configure report:
   - Report title
   - Company name
   - Include charts ✓
   - Include forecast ✓
3. Click **"📊 Generate PDF Report"**
4. Download professional report

### Step 12: Export Data

1. Navigate to **"💾 Export"**
2. Export options:
   - **Cleaned Dataset** (CSV)
   - **Analytics Summary** (CSV)
3. Download for further analysis

---

## Common Issues

### 1. File Upload Errors

**Problem:** "Unable to read file"

**Solutions:**
- Ensure file is valid CSV/Excel format
- Check file encoding (UTF-8 preferred)
- Verify file size < 50MB
- Try saving Excel as CSV first

**Problem:** "No numeric columns found"

**Solution:**
- Dataset needs at least one numeric column
- Check that numeric values aren't stored as text
- Remove currency symbols ($ , etc.) from Excel

### 2. Visualization Errors

**Problem:** "Date column not found"

**Solution:**
- Ensure you have a date column
- Date formats: YYYY-MM-DD, DD/MM/YYYY, etc.
- Column name should contain "date" or "time"

**Problem:** "Not enough data for analysis"

**Solution:**
- Minimum 10-20 rows recommended
- Need at least 2 months for trends
- Add more data if possible

### 3. Forecasting Issues

**Problem:** "Cannot generate forecast"

**Solutions:**
- Requires date column AND numeric column
- Need at least 3 months of historical data
- Ensure dates are properly formatted
- Check for missing values in key columns

### 4. AI Features Not Working

**Problem:** "Insights seem generic"

**Solution:**
- Add OpenAI API key to `.env` file
- Verify `USE_OPENAI=true` in `.env`
- Restart application after adding key
- Rule-based mode still provides good insights!

**Problem:** "OpenAI API error"

**Solutions:**
- Check API key is valid
- Verify you have API credits
- Check internet connection
- App will fallback to rule-based mode

### 5. Performance Issues

**Problem:** "App is slow with large files"

**Solutions:**
- Use smaller datasets (< 10,000 rows for testing)
- Clean data to remove unnecessary rows/columns
- Close other applications
- Use CSV instead of Excel for better performance

---

## Next Steps

### Learn More

📖 **Documentation:**
- [Data Cleaning Guide](data-cleaning.md)
- [Creating Custom KPIs](custom-kpis.md)
- [Advanced Forecasting](forecasting.md)
- [Report Customization](reports.md)

### Sample Datasets

Try these sample datasets to explore features:

1. **E-commerce Sales**
   - Columns: Date, Product, Category, Region, Sales, Profit
   - Features: All visualizations, forecasting, insights

2. **Financial Data**
   - Columns: Date, Transaction, Amount, Type
   - Features: Trends, distribution, anomaly detection

3. **Customer Data**
   - Columns: Customer, Region, Purchase, Revenue
   - Features: Segmentation, regional analysis

### Customize Your Experience

1. **Add Custom CSS**
   - Edit `styles/custom.css`
   - Modify colors, fonts, spacing

2. **Configure Streamlit**
   - Edit `.streamlit/config.toml`
   - Change theme, port, etc.

3. **Extend Functionality**
   - Add new services in `services/`
   - Create custom visualizations
   - Implement new ML models

### Deploy Your App

Ready to share with others?

- **Streamlit Cloud**: Free, easiest option ([Guide](https://docs.streamlit.io/streamlit-community-cloud/get-started))
- **Heroku**: Free tier available ([Guide](https://devcenter.heroku.com/articles/getting-started-with-python))
- **Docker**: For containerized deployment
- **AWS/Azure/GCP**: For enterprise scale

---

## Getting Help

### Resources

- 📖 **Documentation**: [Full Documentation](README.md)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/InsightLens-AI/discussions)
- 🐛 **Issues**: [Report Bug](https://github.com/yourusername/InsightLens-AI/issues)
- 📧 **Email**: support@insightlens-ai.com

### Community

- Share your dashboards
- Contribute improvements
- Help other users
- Suggest features

---

## Tips for Success

✅ **Best Practices:**
1. Start with clean, well-formatted data
2. Use descriptive column names
3. Include date columns for trend analysis
4. Have at least one numeric metric
5. Remove unnecessary columns before upload
6. Test with sample data first
7. Review data quality before analysis
8. Generate reports for stakeholders

🚀 **Pro Tips:**
- Use keyboard shortcuts (Streamlit supports many)
- Bookmark frequently used sections
- Export cleaned data for reuse
- Save reports for comparison
- Ask specific questions in "Ask Your Data"
- Experiment with different visualizations
- Review executive summaries for quick insights

---

<div align="center">

**Ready to transform your data into insights?**

[🚀 Start Analyzing Now](../README.md)

---

**InsightLens AI** - Autonomous Data Analytics Copilot

Made with ❤️ for Data Analysts

</div>

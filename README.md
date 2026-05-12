# 📊 AI Data Insights Analyzer

> A production-quality Python dashboard for automated data analysis, visualization, and AI-powered business insights.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)

[Live Demo](#) 

## 🎯 Overview

Upload any CSV or Excel dataset and get instant analytics with KPIs, interactive visualizations, ML forecasting and AI-generated insights. Built for data analysts, business intelligence, and portfolio projects.

**Key Features:**
- 🔄 Works with **any dataset** - automatic column detection
- 📊 Real-time KPI dashboard with performance metrics
- 📈 Interactive visualizations (Plotly charts)
- 🤖 AI-powered insights (OpenAI GPT-3.5 optional)
- 🔮 Sales forecasting with Linear Regression
- 💾 Export cleaned data and analytics reports

---

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/cvenkataravikiran/AI-Data-Insights-Analyzer.git
cd AI-Data-Insights-Analyzer
```

2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate the virtual environment**

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Run the application**
```bash
streamlit run app.py
```

6. **Open your browser**
The app will automatically open at `http://localhost:8501`

## ✨ Features

### 1. Smart File Upload
- Supports CSV and Excel files
- Automatic encoding detection (UTF-8, Latin-1, etc.)
- Intelligent column mapping
- Dataset preview and metadata

### 2. Data Cleaning
- Missing value detection and handling
- Duplicate removal
- Multiple cleaning strategies
- Data quality reports

### 3. KPI Dashboard
- Total Sales, Profit, Revenue metrics
- Growth rate and profit margins
- Top products, regions, categories
- Performance overview charts

### 4. Interactive Visualizations
- Sales trends over time
- Distribution analysis
- Correlation heatmaps
- Regional performance
- Product analysis

### 5. ML Forecasting
- Linear Regression model
- 1-12 month predictions
- Model accuracy metrics (R²)
- Interactive forecast charts

### 6. AI Insights (Optional)
- OpenAI GPT-3.5 integration
- Automated business insights
- Automatic fallback to rule-based analysis
- No API key required to use

### 7. Export Features
- Download cleaned datasets
- Export analytics summaries
- CSV format for further analysis

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web framework |
| **Pandas** | Data manipulation |
| **Plotly** | Interactive charts |
| **Scikit-learn** | Machine learning |
| **OpenAI** | AI insights (optional) |
| **NumPy** | Numerical computing |

---

## 📊 Dataset Requirements

**Minimum:** At least one numeric column

**Recommended columns:**
- Date/Time column (for trends and forecasting)
- Numeric columns (sales, revenue, profit, quantity)
- Categorical columns (product, category, region)


**Works with ANY column names!** The system auto-detects your data structure.

---

## 🤖 OpenAI Setup (Optional)

1. Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create `.env` file:
```bash
OPENAI_API_KEY=your_key_here
USE_OPENAI=true
```
3. Restart the app

**Note:** App works perfectly without OpenAI using rule-based insights.

---

## 🌐 Deployment

### Streamlit Cloud (Recommended - Free)

1. Push code to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Select your repository
5. Set main file: `app.py`
6. Deploy!

**Optional:** Add OpenAI key in app secrets:
```toml
OPENAI_API_KEY = "your-key-here"
USE_OPENAI = "true"
```
---

## 🎯 Use Cases

- **Portfolio Projects** - Showcase data analysis skills
- **Business Analytics** - Real-world sales analysis
- **Data Exploration** - Quick insights from any dataset
- **Client Demos** - Professional analytics presentations
- **Learning** - Understand data analysis workflows

---
## ✨ Features

### 1. File Upload System
- Support for CSV and Excel files (.csv, .xlsx, .xls)
- File validation and size checking
- Dataset preview and metadata display
- Automatic data type detection

### 2. Data Cleaning Module
- Detect and handle missing values
- Remove duplicate records
- Multiple strategies for handling nulls (drop, fill with mean/median)
- Automatic column name cleaning
- Data type conversion

### 3. KPI Dashboard
- **Total Sales**: Aggregate revenue metrics
- **Total Profit**: Profitability analysis
- **Average Revenue**: Per-transaction insights
- **Growth Rate**: Period-over-period performance
- **Top Products**: Best-selling items
- **Best Regions**: Geographic performance leaders

### 4. Data Visualizations
- **Interactive Charts**: Built with Plotly for dynamic exploration
- **Line Charts**: Trend analysis over time
- **Bar Charts**: Comparative analysis
- **Pie Charts**: Distribution visualization
- **Correlation Heatmaps**: Relationship analysis
- **Scatter Plots**: Multi-dimensional insights
- **Box Plots**: Distribution and outlier detection

### 5. Trend Analysis
- Monthly growth tracking
- Sales trend identification
- Seasonal performance analysis
- Category-wise performance metrics

### 6. Predictive Analytics
- Linear Regression forecasting
- Future sales predictions (1-12 months)
- Model accuracy metrics (R² score)
- Interactive forecast visualizations

### 7. AI Business Insights
- **🤖 NEW: OpenAI GPT-3.5 Integration** (optional)
- Automated insight generation
- Top performer identification
- Regional performance analysis
- Profitability recommendations
- Category preference insights
- Automatic fallback to rule-based insights

### 8. Export Features
- Download cleaned datasets (CSV)
- Export analytics summaries
- Save reports for further analysis

## 🔮 Future Improvements

- [ ] Add more ML models (ARIMA, Prophet, LSTM)
- [ ] Implement user authentication
- [ ] Add database integration (PostgreSQL, MongoDB)
- [ ] Create custom report templates
- [ ] Add email notification for insights
- [ ] Implement real-time data streaming
- [ ] Add more chart types (Sankey, Sunburst)
- [ ] Multi-language support
- [ ] Dark mode theme
- [ ] API integration for external data sources

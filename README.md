# 🔮 InsightLens AI - Autonomous Data Analytics Copilot

<div align="center">

![InsightLens AI Banner](https://via.placeholder.com/1200x300/3b82f6/ffffff?text=InsightLens+AI+-+Autonomous+Data+Analytics+Copilot)

**Transform Raw Data into Actionable Business Intelligence using AI**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-green.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[Demo](https://insightlens-ai.streamlit.app/) • [Features](#-features) • [Installation](#-installation) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 🎯 Overview

**InsightLens AI** is a production-grade, autonomous data analytics platform that transforms raw CSV/Excel data into comprehensive business intelligence reports. Built for data analysts, business intelligence professionals, and decision-makers, it combines automated data cleaning, quality assessment, interactive visualizations, ML forecasting, and AI-powered insights into a single powerful application.

### Problem Statement

Modern businesses generate vast amounts of data, but extracting actionable insights requires:
- ⏱️ Hours of manual data cleaning and preparation
- 📊 Complex analytics skills and tool expertise
- 💰 Expensive business intelligence software
- 🤖 Technical knowledge of machine learning

### Solution

InsightLens AI eliminates these barriers by providing:
- ✅ **Automatic Data Cleaning** - Instant detection and handling of missing values, duplicates, and anomalies
- 📊 **Instant Analytics** - Auto-generated KPIs, trends, and visualizations in seconds
- 🤖 **AI-Powered Insights** - GPT-3.5 powered business intelligence and recommendations
- 🔮 **Predictive Forecasting** - ML-based sales predictions with confidence metrics
- 📑 **Executive Reports** - Professional PDF/HTML reports for stakeholders

---

## ✨ Features

### 🎨 Modern SaaS-Style Interface
- **Professional Landing Page** with feature showcase and workflow explanation
- **Responsive Design** with modern UI components (cards, tabs, expanders)
- **Dark/Light Theme** support with custom CSS styling
- **Interactive Navigation** with intuitive sidebar menu

### 📁 Smart Data Ingestion
- ✅ **Multi-format Support**: CSV, Excel (.xlsx, .xls)
- ✅ **Single or Multiple File Upload**: Upload one file or multiple files at once
- ✅ **Merge or Analyze Separately**: Combine files into one dataset or analyze each individually
- ✅ **Dataset Switcher**: Easy switching between loaded datasets
- 🔍 **Automatic Column Detection**: Dates, numerics, categories, currency, percentages
- ⚡ **Intelligent Encoding**: Auto-handles UTF-8, Latin-1, ISO-8859-1
- 📊 **Dataset Validation**: File size checks, format verification, preview display

### 🧹 Advanced Data Cleaning
- **Automated Cleaning Pipeline**:
  - Remove duplicate records
  - Handle missing values (drop, mean, median imputation)
  - Trim whitespace and normalize formatting
  - Standardize date formats
  - Detect invalid entries
- **Before/After Comparison** with visual statistics
- **Quality Metrics** showing cleaning impact

### 📊 Comprehensive Data Quality Assessment
- **Quality Scoring System** (0-100%)
  - Completeness Score
  - Consistency Score
  - Uniqueness Score
  - Validity Score
- **Visual Quality Dashboard** with color-coded grades
- **Column-wise Analysis** with detailed metrics
- **Actionable Recommendations** for data improvement

### 📋 AI-Generated Executive Summary
- **Business Overview** with key metrics
- **Positive Findings** highlighting successes
- **Areas of Concern** identifying issues
- **Growth Opportunities** suggesting expansion areas
- **Business Risks** flagging potential problems
- **Strategic Recommendations** with actionable steps
- **AI-Generated Conclusions** synthesizing insights

### 📈 Intelligent KPI Engine
- **Auto-detected Metrics**:
  - 💰 Total Revenue/Sales
  - 📊 Total Profit & Margins
  - 📈 Average Order Value
  - 🔄 Growth Rates
  - 🏆 Top Products/Categories/Regions
  - 👥 Customer Metrics
- **Modern KPI Cards** with visual indicators
- **Trend Analysis** with period-over-period comparisons

### 📉 Interactive Visualizations (15+ Chart Types)
- **Time Series Analysis**: Sales trends over time
- **Distribution Charts**: Histograms, box plots
- **Comparative Analysis**: Bar charts, grouped comparisons
- **Composition**: Pie charts, stacked areas
- **Correlation Analysis**: Heatmaps, scatter plots
- **Geographic Performance**: Regional breakdowns
- **Product Analysis**: Category performance
- **All Built with Plotly**: Fully interactive and exportable

### 🤖 AI-Powered Analytics
- **OpenAI GPT-3.5 Integration** for intelligent insights
- **Automatic Fallback** to rule-based analysis (no API key required)
- **Context-Aware Analysis** understanding business domains
- **Natural Language Generation** for business-friendly insights
- **Trend Interpretation** explaining what the data means
- **Anomaly Explanations** identifying unusual patterns

### 💬 Ask Your Data (Conversational Analytics)
Natural language interface for dataset queries:
- "Which region generated the highest revenue?"
- "What is the average profit margin?"
- "Show me top 5 products by sales"
- "How does profit correlate with sales?"
- "Identify any anomalies or outliers"

Includes supporting visualizations and data tables for answers.

### 🔮 Machine Learning Forecasting
- **Linear Regression Model** for sales prediction
- **Configurable Forecast Periods** (1-12 months)
- **Model Performance Metrics** (R² Score)
- **Interactive Forecast Charts** with confidence indicators
- **Forecast Explanation** with business interpretation
- **Trend Analysis** and limitations assessment

### 🔍 Automatic Anomaly Detection
- **Statistical Outlier Detection** (IQR method)
- **Spike/Drop Identification** in time series
- **Business Impact Analysis** for each anomaly
- **Possible Causes** and suggested actions
- **Visual Highlighting** of anomalies in charts

### 📑 Professional Report Generation
- **Executive PDF Reports** with cover page
- **Comprehensive HTML Reports** for web viewing
- **Includes**:
  - Executive Summary
  - KPI Dashboard
  - Key Insights
  - Data Quality Assessment
  - Detailed Analysis Tables
  - Charts & Visualizations
  - Strategic Recommendations
- **Professional Styling** suitable for stakeholder presentations

### 💾 Flexible Export Options
- **CSV Export**: Cleaned datasets
- **Excel Export**: Multi-sheet reports
- **PDF Reports**: Executive summaries
- **Chart Images**: PNG downloads for presentations
- **HTML Reports**: Interactive web reports

---

## 🏗️ Architecture

```
InsightLens AI Architecture

┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                        │
│  (Landing Page, Navigation, Interactive Components)         │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│                   Core Services Layer                        │
├─────────────────────────────────────────────────────────────┤
│  • Data Quality Assessor    • Executive Summary Generator   │
│  • Data Analyzer            • Ask Data Agent                │
│  • Data Cleaner             • Report Generator              │
│  • Sales Forecaster         • Insight Generator             │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│                 AI & ML Integration                          │
├─────────────────────────────────────────────────────────────┤
│  • OpenAI GPT-3.5 (Optional)  • Scikit-learn (Forecasting) │
│  • Rule-based Fallback        • Statistical Analysis       │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│              Data Processing Layer                           │
├─────────────────────────────────────────────────────────────┤
│  • Pandas (Data Manipulation)  • NumPy (Numerical Computing)│
│  • Plotly (Visualizations)     • Validators & Helpers       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
InsightLens-AI/
├── 📄 app.py                      # Main Streamlit application
├── 📋 requirements.txt            # Python dependencies
├── 📖 README.md                   # This file
├── 🔐 .env                        # Environment variables (API keys)
├── 🚫 .gitignore                  # Git ignore rules
│
├── 📁 components/                 # UI Components
│   ├── charts.py                  # Visualization components
│   ├── dashboard.py               # Dashboard layouts
│   ├── metrics.py                 # KPI card components
│   └── __init__.py
│
├── 📁 services/                   # Business Logic Layer
│   ├── analyzer.py                # Data analysis engine
│   ├── ask_data.py                # Conversational analytics
│   ├── cleaner.py                 # Data cleaning service
│   ├── data_quality.py            # Quality assessment
│   ├── executive_summary.py       # Summary generation
│   ├── forecasting.py             # ML forecasting service
│   ├── insights.py                # AI insight generation
│   ├── report_generator.py        # PDF/HTML reports
│   └── __init__.py
│
├── 📁 utils/                      # Utility Functions
│   ├── helpers.py                 # Helper functions
│   ├── validators.py              # Input validation
│   └── __init__.py
│
├── 📁 styles/                     # Custom Styling
│   └── custom.css                 # CSS overrides
│
├── 📁 .streamlit/                 # Streamlit Config
│   └── config.toml                # App configuration
│
├── 📁 datasets/                   # Sample datasets (optional)
├── 📁 exports/                    # Generated reports
└── 📁 assets/                     # Images, icons, etc.
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/InsightLens-AI.git
cd InsightLens-AI
```

### Step 2: Create Virtual Environment
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

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment (Optional)
Create a `.env` file for OpenAI integration:
```bash
OPENAI_API_KEY=your_openai_api_key_here
USE_OPENAI=true
```

**Note**: The application works perfectly without OpenAI using intelligent rule-based analysis.

### Step 5: Run the Application
```bash
streamlit run app.py
```

The application will automatically open at `http://localhost:8501`

---

## 💻 Usage

### Quick Start Guide

1. **Launch Application**
   ```bash
   streamlit run app.py
   ```

2. **Upload Your Dataset**
   - Navigate to "📁 Upload Data"
   - Drop your CSV or Excel file
   - Review automatic column detection

3. **Clean Your Data**
   - Go to "🧹 Data Cleaning"
   - Review quality report
   - Apply cleaning options
   - Download cleaned dataset

4. **Assess Data Quality**
   - Visit "📊 Data Quality"
   - View overall quality score
   - Review dimension scores
   - Check recommendations

5. **Generate Executive Summary**
   - Go to "📋 Executive Summary"
   - Click "Generate Summary"
   - Review business insights
   - Export if needed

6. **Explore KPI Dashboard**
   - Navigate to "📈 KPI Dashboard"
   - View auto-generated metrics
   - Analyze AI insights

7. **Create Visualizations**
   - Visit "📉 Visualizations"
   - Explore interactive charts
   - Filter and drill down

8. **Generate Forecasts**
   - Go to "🔮 Forecasting"
   - Select forecast period
   - Generate predictions
   - Review model accuracy

9. **Ask Questions**
   - Navigate to "🤖 Ask Your Data"
   - Type natural language questions
   - Get instant answers with charts

10. **Generate Reports**
    - Go to "📑 Generate Report"
    - Configure report settings
    - Download PDF/HTML report

---

## 🛠️ Technology Stack

| Category | Technologies |
|----------|-------------|
| **Frontend** | Streamlit, HTML/CSS, JavaScript |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly, Matplotlib |
| **Machine Learning** | Scikit-learn (Linear Regression) |
| **AI Integration** | OpenAI GPT-3.5 (Optional) |
| **File Processing** | openpyxl (Excel), python-dotenv |
| **Statistical Analysis** | SciPy, Statistical Methods |

---

## 📊 Dataset Requirements

### Minimum Requirements
- At least **1 numeric column** (for basic analysis)
- Valid CSV or Excel format
- Maximum file size: **50MB**

### Recommended Structure
For optimal feature utilization, include:

| Column Type | Examples | Purpose |
|-------------|----------|---------|
| **Date/Time** | Order Date, Transaction Date | Trend analysis, forecasting |
| **Numeric** | Sales, Revenue, Profit, Quantity | KPIs, calculations, ML |
| **Categorical** | Product, Category, Region | Grouping, segmentation |
| **ID Fields** | Order ID, Customer ID | Uniqueness validation |

### Supported Column Names
The system auto-detects columns regardless of naming. Common patterns:
- **Sales**: Revenue, Total, Amount, Sales, Value
- **Profit**: Profit, Margin, Earnings, Net Income
- **Date**: Date, Order Date, Transaction Date, Created
- **Product**: Product, Item, SKU, Product Name
- **Region**: Region, Location, Territory, State, Country
- **Category**: Category, Type, Class, Group

---

## 🤖 AI Features

### OpenAI Integration (Optional)
When configured with an OpenAI API key, InsightLens AI leverages GPT-3.5 for:
- Natural language business insights
- Context-aware trend interpretation
- Intelligent anomaly explanations
- Conversational data queries
- Executive summary generation

### Intelligent Fallback
Without OpenAI, the system uses:
- Advanced rule-based analytics
- Statistical pattern recognition
- Heuristic insight generation
- Template-based summaries

Both modes deliver professional-quality insights suitable for business decision-making.

---

## 🌐 Deployment

### Streamlit Cloud (Recommended - Free)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set main file: `app.py`
   - Click "Deploy"

3. **Configure Secrets** (Optional)
   In Streamlit Cloud dashboard, add secrets:
   ```toml
   OPENAI_API_KEY = "your-key-here"
   USE_OPENAI = "true"
   ```

### Alternative Deployment Options

**Docker:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

**Heroku**, **AWS**, **Azure**, **Google Cloud** - See [deployment guide](docs/deployment.md)

---

## 📈 Use Cases

### Business Analytics
- Sales performance tracking
- Revenue trend analysis
- Profitability assessment
- Market segmentation

### Portfolio Projects
- Data analytics portfolio showcase
- Google Data Analytics Apprenticeship
- Data science job applications
- Academic projects

### Client Presentations
- Executive stakeholder reports
- Business intelligence demos
- Data-driven recommendations
- Performance dashboards

### Data Exploration
- Quick dataset insights
- Hypothesis validation
- Pattern discovery
- Quality assessment

---

## 🔮 Future Roadmap

### Phase 1: Enhanced ML (Q3 2026)
- ARIMA time series forecasting
- Prophet for seasonal predictions
- LSTM neural networks
- Ensemble model selection

### Phase 2: Enterprise Features (Q4 2026)
- User authentication & multi-tenancy
- Database integration (PostgreSQL, MongoDB)
- Real-time data streaming
- Scheduled report generation
- Email notifications

### Phase 3: Advanced Analytics (Q1 2027)
- Cohort analysis
- Customer segmentation (K-means, DBSCAN)
- Churn prediction
- Recommendation engine
- A/B test analysis

### Phase 4: UI/UX Enhancements (Q2 2027)
- Custom dashboard builder
- Drag-and-drop report designer
- Dark mode toggle
- Multi-language support
- Mobile-responsive design

### Phase 5: Integration & APIs (Q3 2027)
- REST API endpoints
- Google Sheets integration
- Salesforce connector
- Slack/Teams notifications
- Webhook support

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute
- 🐛 **Report Bugs**: Open an issue with detailed reproduction steps
- 💡 **Suggest Features**: Share ideas for new capabilities
- 📖 **Improve Documentation**: Fix typos, add examples
- 🔧 **Submit Pull Requests**: Contribute code improvements

### Contribution Guidelines

1. **Fork the Repository**
   ```bash
   git fork https://github.com/yourusername/InsightLens-AI.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Changes**
   - Follow PEP8 style guidelines
   - Add type hints where applicable
   - Include docstrings for functions
   - Write meaningful commit messages

4. **Test Your Changes**
   ```bash
   # Run the application
   streamlit run app.py
   
   # Test with sample datasets
   # Verify all features work
   ```

5. **Submit Pull Request**
   - Provide clear description
   - Reference related issues
   - Include screenshots if UI changes

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Streamlit** - Amazing framework for data apps
- **OpenAI** - Powerful AI capabilities
- **Plotly** - Interactive visualization library
- **Scikit-learn** - Machine learning tools
- **Pandas & NumPy** - Data processing backbone

---

## 📞 Support & Contact

### Get Help
- 📖 **Documentation**: [docs/README.md](docs/README.md)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/InsightLens-AI/discussions)
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/InsightLens-AI/issues)

### Connect
- 🌐 **Website**: [insightlens-ai.com](#)
---

## 📸 Screenshots

---

## 🎓 Learning Resources

### Google Data Analytics Certificate
This project demonstrates skills from the Google Data Analytics Professional Certificate:
- Data cleaning and preparation
- Data analysis and visualization
- Statistical analysis and forecasting
- Business intelligence reporting
- Communication of insights

### Tutorial Series
- [Getting Started Guide](docs/getting-started.md)
- [Data Cleaning Best Practices](docs/data-cleaning.md)
- [Creating Custom KPIs](docs/custom-kpis.md)
- [Advanced Forecasting](docs/forecasting.md)
- [Report Customization](docs/reports.md)

---

<div align="center">

### ⭐ Star this repository if InsightLens AI helped you!

**Made with ❤️ by Data Analysts, for Data Analysts**

[⬆ Back to Top](#-insightlens-ai)

</div>

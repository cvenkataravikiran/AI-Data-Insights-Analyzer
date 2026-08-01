# InsightLens AI - Quick Reference Card

**Version 1.0** | Autonomous Data Analytics Copilot

---

## 🚀 Quick Start (30 seconds)

```bash
# 1. Activate virtual environment
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux

# 2. Run application
streamlit run app.py

# 3. Open browser
http://localhost:8501
```

---

## 📁 Supported File Formats

| Format | Extensions | Max Size | Notes |
|--------|-----------|----------|-------|
| CSV | `.csv` | 50MB | UTF-8 preferred |
| Excel | `.xlsx`, `.xls` | 50MB | Uses first sheet |

---

## 🔑 Minimum Dataset Requirements

✅ **Required**: At least 1 numeric column

📊 **Recommended Structure**:
- Date/Time column → Enables trend analysis & forecasting
- Numeric columns → Sales, Revenue, Profit, Quantity
- Categorical columns → Product, Category, Region
- ID columns → Order ID, Customer ID

---

## 🎯 Navigation Menu

| Icon | Section | Purpose |
|------|---------|---------|
| 🏠 | Home | Landing page & features |
| 📁 | Upload Data | File upload & preview |
| 🧹 | Data Cleaning | Clean & prepare data |
| 📊 | Data Quality | Quality assessment |
| 📋 | Executive Summary | AI business overview |
| 📈 | KPI Dashboard | Key metrics & insights |
| 📉 | Visualizations | Interactive charts |
| 🔮 | Forecasting | ML predictions |
| 🤖 | Ask Your Data | Natural language queries |
| 📑 | Generate Report | PDF/HTML export |
| 💾 | Export | Download data |

---

## 📊 Available Visualizations

### Time Series
- **Sales Trends**: Line charts over time
- **Monthly Analysis**: Aggregated monthly data
- **Growth Patterns**: Period-over-period trends

### Distribution
- **Histograms**: Value distribution
- **Box Plots**: Outlier detection
- **By Category**: Distribution by groups

### Comparative
- **Bar Charts**: Compare products/regions
- **Pie Charts**: Market share
- **Scatter Plots**: Correlation analysis

### Advanced
- **Heatmaps**: Correlation matrices
- **Treemaps**: Hierarchical data
- **Multi-metric**: Combined views

---

## 🤖 AI Features

### Requires OpenAI API Key
✅ Natural language insights  
✅ Context-aware analysis  
✅ Business recommendations  
✅ Conversational queries

### Works Without API Key
✅ Rule-based insights  
✅ Statistical analysis  
✅ Pattern detection  
✅ All other features

**Setup API Key**:
```bash
# Edit .env file
OPENAI_API_KEY=sk-your-key-here
USE_OPENAI=true
```

---

## 💬 Ask Your Data - Example Questions

### Top Performers
- "Which region generated the highest revenue?"
- "What are the top 5 products by sales?"
- "Show me the best performing category"

### Metrics
- "What is the average profit margin?"
- "Calculate total sales for each region"
- "What percentage comes from top category?"

### Trends
- "How have sales changed over time?"
- "Is there a growth trend?"
- "Which month had best performance?"

### Analysis
- "How does profit correlate with sales?"
- "Identify any anomalies or outliers"
- "Compare regional performance"

---

## 🔮 Forecasting

**Model**: Linear Regression  
**Forecast Periods**: 1-12 months  
**Requirements**: Date column + Numeric column  
**Output**: Predictions + R² score + Chart

**Interpreting R² Score**:
- **> 0.7**: Good predictive power
- **0.5-0.7**: Moderate accuracy
- **< 0.5**: Low confidence

---

## 📋 Data Quality Scores

### Overall Score: 0-100%

| Score | Grade | Meaning |
|-------|-------|---------|
| 80-100 | ⭐ Excellent | High quality, minimal issues |
| 60-79 | ✅ Good | Acceptable quality, minor improvements |
| 40-59 | ⚠️ Fair | Quality issues, needs attention |
| 0-39 | ❌ Poor | Major issues, significant cleanup needed |

### Quality Dimensions

**Completeness** (30% weight)
- Percentage of non-null values
- Target: >95%

**Consistency** (25% weight)
- Format standardization
- Pattern adherence
- Target: >80%

**Uniqueness** (20% weight)
- Duplicate detection
- Record uniqueness
- Target: >95%

**Validity** (25% weight)
- Range validation
- Type correctness
- Target: >90%

---

## 🧹 Data Cleaning Options

### Remove Duplicates
- ✅ Exact row matches
- Keeps first occurrence
- Shows count removed

### Handle Missing Values

| Strategy | Action | Best For |
|----------|--------|----------|
| Keep as is | No changes | Initial review |
| Drop rows | Remove nulls | Small % missing |
| Fill with mean | Average value | Normally distributed |
| Fill with median | Middle value | Skewed data |

---

## 📑 Report Sections

### Executive PDF/HTML Report Includes:

1. **Cover Page**
   - Title, company, timestamp
   - Professional branding

2. **Executive Summary**
   - Business overview
   - Key findings

3. **KPI Dashboard**
   - Total Sales, Profit
   - Averages, margins

4. **Key Insights**
   - Top performers
   - Geographic analysis
   - Profitability

5. **Data Quality**
   - Quality score
   - Completeness metrics

6. **Detailed Analysis**
   - Top 10 products
   - Regional breakdowns
   - Summary statistics

---

## 💾 Export Options

| Type | Format | Contents |
|------|--------|----------|
| Cleaned Data | CSV | Processed dataset |
| Analytics Summary | CSV | KPI metrics |
| Executive Report | PDF/HTML | Full analysis |
| Charts | PNG | Individual charts |

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+R` / `⌘+R` | Rerun app |
| `Ctrl+Shift+R` | Clear cache & rerun |
| `Ctrl+K` | Focus search |
| `Ctrl+Shift+S` | Take screenshot |

---

## 🐛 Common Issues & Solutions

### Upload Errors

**Problem**: "Unable to read file"  
**Fix**: Check encoding, try UTF-8, convert Excel to CSV

**Problem**: "No numeric columns"  
**Fix**: Ensure at least one column has numbers

### Visualization Errors

**Problem**: "Date column not found"  
**Fix**: Add column with 'date' or 'time' in name

**Problem**: "Not enough data"  
**Fix**: Need minimum 10-20 rows, prefer 100+

### Forecasting Errors

**Problem**: "Cannot generate forecast"  
**Fix**: Requires date + numeric column, min 3 months data

### Performance Issues

**Problem**: "App is slow"  
**Fix**: Use datasets <10K rows, CSV format, clean data first

---

## 🎨 Color Coding

### KPI Metrics
- 🔵 **Blue**: Primary metrics (sales, revenue)
- 🟢 **Green**: Profit, positive growth
- 🟡 **Yellow**: Warnings, moderate performance
- 🔴 **Red**: Issues, negative trends

### Quality Scores
- 🌟 **Purple/Blue** (80-100): Excellent
- ✅ **Blue** (60-79): Good
- ⚠️ **Orange** (40-59): Fair
- ❌ **Red** (0-39): Poor

---

## 📊 Automatic Column Detection

**Date Columns** (triggers trend analysis):
- Keywords: `date`, `time`, `created`, `order_date`
- Formats: YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY

**Sales Columns** (primary metric):
- Keywords: `sales`, `revenue`, `total`, `amount`, `value`
- Type: Numeric

**Profit Columns** (profitability):
- Keywords: `profit`, `margin`, `earnings`, `net_income`
- Type: Numeric

**Product Columns** (grouping):
- Keywords: `product`, `item`, `sku`, `product_name`
- Type: Text/Categorical

**Region Columns** (geographic):
- Keywords: `region`, `location`, `territory`, `state`, `country`
- Type: Text/Categorical

**Category Columns** (classification):
- Keywords: `category`, `type`, `class`, `group`
- Type: Text/Categorical

---

## 🔧 Configuration Files

### .env (API Keys)
```
OPENAI_API_KEY=your_key_here
USE_OPENAI=true
```

### .streamlit/config.toml (App Settings)
```toml
[server]
port = 8501
headless = false

[theme]
primaryColor = "#3b82f6"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

---

## 📦 Dependencies

**Core**:
```
streamlit>=1.28.0
pandas>=2.2.0
numpy>=1.26.0
plotly>=5.17.0
scikit-learn>=1.3.0
```

**Optional**:
```
openai>=1.0.0           # AI features
openpyxl>=3.1.0         # Excel support
python-dotenv>=1.0.0    # Environment vars
```

---

## 🌐 Deployment Quick Start

### Streamlit Cloud (Free)

1. Push to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select repo, set `app.py`
5. Deploy!

**Add Secrets** (optional):
```toml
OPENAI_API_KEY = "your-key"
USE_OPENAI = "true"
```

---

## 📞 Getting Help

| Resource | URL |
|----------|-----|
| 📖 Full Docs | [README.md](../README.md) |
| 🚀 Getting Started | [getting-started.md](getting-started.md) |
| 🏗️ Architecture | [ARCHITECTURE.md](ARCHITECTURE.md) |
| 🐛 Bug Reports | [GitHub Issues](https://github.com/yourusername/InsightLens-AI/issues) |
| 💬 Discussions | [GitHub Discussions](https://github.com/yourusername/InsightLens-AI/discussions) |
| 📧 Email | support@insightlens-ai.com |

---

## 📏 Best Practices

### Data Preparation
✅ Clean column names (no special chars)  
✅ Consistent date formats  
✅ Remove currency symbols in Excel  
✅ Check for duplicates  
✅ Handle missing values  
✅ Use UTF-8 encoding for CSV

### Analysis Workflow
1. Upload → Preview data
2. Clean → Review quality
3. Assess → Check scores
4. Analyze → Explore dashboards
5. Visualize → Create charts
6. Forecast → Generate predictions
7. Report → Download PDF
8. Export → Save results

### Performance Tips
✅ Start with small datasets (<1000 rows)  
✅ Clean data before analysis  
✅ Use CSV for faster loading  
✅ Close unused tabs  
✅ Clear cache regularly  
✅ Limit forecast periods

---

## 🎓 Learning Path

### Beginner (30 min)
1. Launch app
2. Upload sample dataset
3. Explore all menu sections
4. Generate one report

### Intermediate (1 hour)
1. Clean your own dataset
2. Assess data quality
3. Generate executive summary
4. Create forecasts
5. Ask data questions

### Advanced (2+ hours)
1. Customize workflows
2. Integrate with OpenAI
3. Deploy to Streamlit Cloud
4. Create custom visualizations
5. Contribute to project

---

## 🔐 Security Checklist

✅ Store API keys in `.env` file  
✅ Never commit `.env` to Git  
✅ Use HTTPS in production  
✅ Keep dependencies updated  
✅ Validate file uploads  
✅ Limit file sizes  
✅ Review data before sharing

---

<div align="center">

## Quick Tips

💡 **Stuck?** Check the example questions in "Ask Your Data"  
💡 **Slow?** Try a smaller dataset or CSV format  
💡 **Errors?** Review the data quality assessment first  
💡 **Need help?** Visit GitHub Discussions

---

**Print this card for quick reference!**

**InsightLens AI** v1.0 | [Full Documentation](../README.md)

Transform Raw Data into Actionable Business Intelligence

Made with ❤️ by Data Analysts, for Data Analysts

</div>

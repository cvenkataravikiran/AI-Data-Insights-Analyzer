# InsightLens AI - Architecture Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Layers](#architecture-layers)
3. [Component Diagram](#component-diagram)
4. [Data Flow](#data-flow)
5. [Module Descriptions](#module-descriptions)
6. [Design Patterns](#design-patterns)
7. [Technology Stack](#technology-stack)
8. [Security Architecture](#security-architecture)
9. [Scalability Considerations](#scalability-considerations)

---

## System Overview

InsightLens AI is a **layered architecture** application built using the MVC (Model-View-Controller) pattern, adapted for data analytics workflows. The system processes raw data through multiple stages: ingestion, cleaning, analysis, visualization, and reporting.

### Key Architectural Principles

1. **Separation of Concerns**: UI, business logic, and data processing are isolated
2. **Modularity**: Each service is independent and reusable
3. **Extensibility**: Easy to add new analytics modules
4. **Fail-Safe Design**: Graceful fallbacks when external services unavailable
5. **Data Immutability**: Original data preserved through transformations

---

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                          │
│                        (Streamlit UI)                           │
├─────────────────────────────────────────────────────────────────┤
│  • Landing Page            • KPI Dashboard                      │
│  • Data Upload Interface   • Visualizations                     │
│  • Data Cleaning UI        • Forecasting UI                     │
│  • Quality Assessment UI   • Report Generation                  │
└────────────────────┬────────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────────┐
│                    COMPONENT LAYER                               │
│                  (Reusable UI Components)                       │
├─────────────────────────────────────────────────────────────────┤
│  • MetricCards            • ChartComponents                     │
│  • DashboardLayouts       • TableViews                          │
│  • FormControls           • ExportButtons                       │
└────────────────────┬────────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────────┐
│                     SERVICE LAYER                                │
│                  (Business Logic)                               │
├─────────────────────────────────────────────────────────────────┤
│  • DataAnalyzer           • ForecastingService                  │
│  • DataCleaner            • InsightGenerator                    │
│  • DataQualityAssessor    • ExecutiveSummaryGenerator          │
│  • AskDataAgent           • ReportGenerator                     │
└────────────────────┬────────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────────┐
│                   AI & ML LAYER                                  │
│              (External Integrations)                            │
├─────────────────────────────────────────────────────────────────┤
│  • OpenAI GPT-3.5         • Scikit-learn Models                │
│  • Statistical Analysis   • Rule-based Fallbacks               │
└────────────────────┬────────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────────┐
│                    DATA LAYER                                    │
│               (Data Processing)                                 │
├─────────────────────────────────────────────────────────────────┤
│  • Pandas (DataFrame ops) • NumPy (Numerical)                  │
│  • File Parsers (CSV/Excel)• Data Validators                   │
│  • Plotly (Visualization) • Type Converters                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Diagram

### High-Level Components

```
                    ┌─────────────────┐
                    │   Streamlit     │
                    │   Application   │
                    └────────┬────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
        ┌───────▼─────┐ ┌───▼────┐ ┌───▼──────┐
        │  Components │ │Services│ │  Utils   │
        │   Module    │ │ Module │ │  Module  │
        └─────────────┘ └────┬───┘ └──────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
    ┌─────▼─────┐     ┌─────▼─────┐     ┌────▼─────┐
    │  Data     │     │    AI     │     │   ML     │
    │ Processing│     │  Services │     │  Models  │
    └───────────┘     └───────────┘     └──────────┘
```

### Detailed Service Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        app.py                                 │
│  (Main Application & Route Handler)                          │
└────────────────┬─────────────────────────────────────────────┘
                 │
   ┌─────────────┼─────────────┐
   │             │             │
┌──▼──────┐  ┌──▼──────┐  ┌──▼──────┐
│Dashboard│  │Cleaning │  │ Quality │
│ Service │  │ Service │  │ Service │
└─────────┘  └─────────┘  └─────────┘
                 │
        ┌────────┼────────┐
        │                 │
    ┌───▼────┐      ┌────▼─────┐
    │Analyzer│      │Forecaster│
    │Service │      │ Service  │
    └────────┘      └──────────┘
        │                 │
        └────────┬────────┘
                 │
         ┌───────▼────────┐
         │ Insight        │
         │ Generator      │
         └────────────────┘
```

---

## Data Flow

### 1. Upload & Ingestion Flow

```
User Upload
    │
    ▼
File Validation
    │
    ├─► Format Check (CSV/Excel)
    ├─► Size Check (< 50MB)
    └─► Encoding Detection
    │
    ▼
Parse File (Pandas)
    │
    ▼
Auto-detect Columns
    │
    ├─► Numeric columns
    ├─► Date columns
    └─► Categorical columns
    │
    ▼
Store in Session State
    │
    ▼
Display Preview
```

### 2. Data Cleaning Flow

```
Raw DataFrame
    │
    ▼
DataCleaner.get_missing_summary()
    │
    ▼
User Selects Options
    │
    ├─► Remove Duplicates
    └─► Handle Missing Values
    │
    ▼
DataCleaner.clean_data()
    │
    ├─► Drop duplicates
    ├─► Fill/drop nulls
    ├─► Clean column names
    └─► Convert data types
    │
    ▼
Store Cleaned Data
    │
    ▼
Display Before/After Stats
```

### 3. Analysis Flow

```
Cleaned DataFrame
    │
    ▼
DataAnalyzer.__init__()
    │
    ├─► Auto-detect columns
    └─► Convert date types
    │
    ▼
Calculate Metrics
    │
    ├─► get_summary_stats()
    ├─► get_top_products()
    ├─► get_region_performance()
    └─► get_monthly_trend()
    │
    ▼
Display KPI Dashboard
    │
    ▼
Generate Visualizations
    │
    ▼
InsightGenerator.generate_insights()
    │
    ├─► Try OpenAI
    │   ├─► _prepare_data_summary()
    │   ├─► Call GPT-3.5 API
    │   └─► Parse response
    │
    └─► Fallback to Rules
        ├─► _get_top_performer_insight()
        ├─► _get_regional_insight()
        ├─► _get_trend_insight()
        └─► _get_profitability_insight()
    │
    ▼
Display Insights
```

### 4. Forecasting Flow

```
DataFrame + Config
    │
    ▼
SalesForecaster.__init__()
    │
    ├─► Detect date column
    └─► Detect sales column
    │
    ▼
User Sets Parameters
    │
    └─► Forecast periods (1-12)
    │
    ▼
forecast_sales()
    │
    ├─► Sort by date
    ├─► Group by month
    ├─► Create features (Month_Num)
    └─► Train LinearRegression
    │
    ├─► Fit model
    ├─► Calculate R² score
    ├─► Predict future
    └─► Generate dates
    │
    ▼
_create_forecast_plot()
    │
    ├─► Plot historical
    ├─► Plot fitted values
    └─► Plot forecast
    │
    ▼
Return (forecast_df, score, chart)
    │
    ▼
Display Results
```

### 5. Report Generation Flow

```
DataFrame + Config
    │
    ▼
ReportGenerator.__init__()
    │
    ▼
User Configures Report
    │
    ├─► Title
    ├─► Company name
    ├─► Include charts
    └─► Include forecast
    │
    ▼
generate_pdf_report()
    │
    ├─► generate_html_report()
    │   ├─► _generate_executive_summary_html()
    │   ├─► _generate_kpi_section_html()
    │   ├─► _generate_insights_section_html()
    │   ├─► _generate_data_quality_html()
    │   └─► _generate_detailed_analysis_html()
    │
    └─► Save to exports/
    │
    ▼
Offer Download
```

---

## Module Descriptions

### Core Application (app.py)

**Purpose**: Main entry point and route orchestration

**Key Functions**:
- `main()`: Application entry point
- `initialize_session_state()`: Setup session variables
- `show_landing_page()`: Render SaaS-style homepage
- `handle_upload()`: File upload and validation
- `handle_cleaning()`: Data cleaning interface
- `handle_data_quality()`: Quality assessment UI
- `handle_executive_summary()`: Summary generation
- `handle_dashboard()`: KPI dashboard
- `handle_visualizations()`: Chart display
- `handle_forecasting()`: ML prediction interface
- `handle_ask_data()`: Conversational analytics
- `handle_generate_report()`: Report creation
- `handle_export()`: Data export

**Session State Variables**:
```python
{
    'data': pd.DataFrame,              # Original dataset
    'cleaned_data': pd.DataFrame,      # Cleaned version
    'file_uploaded': bool,             # Upload status
    'column_mapping': dict,            # Auto-detected columns
    'show_landing': bool,              # Landing page toggle
    'data_quality_score': float,       # Quality score (0-100)
    'executive_summary': dict          # Generated summary
}
```

### Components Module

#### components/metrics.py
**Purpose**: KPI card components

**Main Function**:
```python
display_kpi_cards(analyzer: DataAnalyzer)
```
- Displays 4-column KPI grid
- Shows Total Sales, Profit, Average, Records
- Includes Top Product/Region/Category badges

#### components/dashboard.py
**Purpose**: Dashboard layout components

**Main Function**:
```python
render_dashboard(analyzer: DataAnalyzer)
```
- Top products bar chart
- Regional pie chart
- Monthly trend line chart
- Category performance
- Product scatter plot

#### components/charts.py
**Purpose**: Advanced visualization components

**Main Functions**:
- `render_sales_trends()`: Time series analysis
- `render_distribution_analysis()`: Histograms & box plots
- `render_correlation_heatmap()`: Correlation matrix
- `render_regional_performance()`: Geographic analysis
- `render_product_analysis()`: Product-level insights

### Services Module

#### services/analyzer.py
**Class**: `DataAnalyzer`

**Purpose**: Core analytics engine

**Key Methods**:
```python
__init__(df, config)           # Initialize with data
_auto_detect_columns()         # Smart column detection
get_summary_stats()            # Overall KPIs
get_top_products(n)            # Top N products
get_region_performance()       # Regional metrics
get_monthly_trend()            # Time-based trends
get_category_performance()     # Category analysis
get_profit_margin_by_product() # Profitability analysis
```

#### services/cleaner.py
**Class**: `DataCleaner`

**Purpose**: Data cleaning and preparation

**Key Methods**:
```python
__init__(df)                   # Initialize with data
get_missing_summary()          # Missing value report
clean_data(options)            # Apply cleaning steps
_clean_column_names()          # Normalize names
_convert_data_types()          # Type conversion
detect_outliers(column)        # Outlier detection
```

#### services/data_quality.py
**Class**: `DataQualityAssessor`

**Purpose**: Comprehensive quality assessment

**Key Methods**:
```python
assess_quality()               # Full quality report
_calculate_completeness()      # Non-null percentage
_calculate_consistency()       # Format consistency
_calculate_uniqueness()        # Duplicate detection
_calculate_validity()          # Range validation
_get_missing_summary()         # Missing value analysis
_get_column_quality()          # Per-column metrics
_generate_recommendations()    # Actionable suggestions
```

**Quality Dimensions**:
- **Completeness**: % of non-null values
- **Consistency**: Format and pattern adherence
- **Uniqueness**: Duplicate rate
- **Validity**: Range and type correctness

#### services/forecasting.py
**Class**: `SalesForecaster`

**Purpose**: ML-based sales prediction

**Key Methods**:
```python
__init__(df, config)           # Initialize
forecast_sales(periods)        # Generate forecast
_create_forecast_plot()        # Visualization
```

**Algorithm**: Linear Regression
- Features: Month number (sequential)
- Target: Aggregated sales
- Metrics: R² score
- Output: Future predictions + confidence

#### services/insights.py
**Class**: `InsightGenerator`

**Purpose**: AI-powered insight generation

**Key Methods**:
```python
generate_insights()            # Main entry point
_generate_ai_insights()        # OpenAI GPT-3.5
_prepare_data_summary()        # Context preparation
_generate_rule_based_insights()# Fallback logic
_get_top_performer_insight()   # Best performers
_get_regional_insight()        # Geographic insights
_get_trend_insight()           # Time-based patterns
_get_profitability_insight()   # Margin analysis
_get_category_insight()        # Category patterns
```

**AI Integration**:
- Uses GPT-3.5-turbo model
- Provides data summary as context
- Parses structured responses
- Automatic fallback to rules

#### services/executive_summary.py
**Class**: `ExecutiveSummaryGenerator`

**Purpose**: Executive-level business summary

**Output Structure**:
```python
{
    'overview': str,              # Business overview
    'positive_findings': list,    # Success indicators
    'concerns': list,             # Problem areas
    'opportunities': list,        # Growth potential
    'risks': list,                # Threat factors
    'recommendations': list,      # Action items
    'conclusion': str             # Overall assessment
}
```

#### services/ask_data.py
**Class**: `AskDataAgent`

**Purpose**: Conversational data queries

**Supported Query Types**:
- Top performers
- Averages and totals
- Trends over time
- Comparisons
- Correlations
- Percentages and shares
- Anomalies and outliers

**Response Format**:
```python
{
    'answer': str,                # Text explanation
    'data': pd.DataFrame,         # Supporting data
    'chart': plotly.Figure        # Visualization
}
```

#### services/report_generator.py
**Class**: `ReportGenerator`

**Purpose**: Professional report creation

**Output Formats**:
- HTML (interactive, web-viewable)
- PDF (via HTML conversion)

**Report Sections**:
1. Cover page with branding
2. Executive summary
3. KPI dashboard
4. Key insights
5. Data quality assessment
6. Detailed analysis tables
7. Footer with metadata

### Utils Module

#### utils/validators.py
**Functions**:
```python
validate_file(file)            # Check format, size
check_required_columns(df)     # Verify data structure
get_suggested_columns(df)      # Auto-detect mappings
```

**Validations**:
- File format (CSV, XLSX, XLS)
- File size (max 50MB)
- Minimum columns (at least 1 numeric)
- Encoding detection

#### utils/helpers.py
**Functions**:
```python
save_to_excel(df, filename)    # Export to Excel
create_export_folder()         # Setup exports directory
format_currency(value)         # Format numbers
format_percentage(value)       # Format percentages
```

---

## Design Patterns

### 1. Service Pattern
Each major functionality is encapsulated in a dedicated service class:
- **Analyzer**, **Cleaner**, **Forecaster**, etc.
- Single responsibility
- Reusable across UI components

### 2. Strategy Pattern (AI Fallback)
```python
if self.openai_client:
    return self._generate_ai_insights()
else:
    return self._generate_rule_based_insights()
```
- Switchable algorithms
- Graceful degradation
- Same interface

### 3. Facade Pattern
Complex operations exposed through simple interfaces:
```python
analyzer = DataAnalyzer(df, config)
summary = analyzer.get_summary_stats()  # Hides complexity
```

### 4. Template Method Pattern
```python
class BaseAnalyzer:
    def analyze(self):
        self.load_data()      # Concrete
        self.process()        # Abstract
        self.generate_output() # Concrete
```

### 5. Session State Pattern
Streamlit session state acts as application state manager:
- Persistent across reruns
- Simple key-value store
- Maintains user context

---

## Technology Stack

### Frontend Layer
- **Streamlit** 1.28+: Web framework
- **Plotly** 5.17+: Interactive charts
- **Custom CSS**: Styling enhancements

### Data Processing Layer
- **Pandas** 2.2+: DataFrame operations
- **NumPy** 1.26+: Numerical computing
- **openpyxl** 3.1+: Excel file handling

### Machine Learning Layer
- **Scikit-learn** 1.3+: ML algorithms
- **Linear Regression**: Forecasting model
- **Statistical methods**: Outlier detection, correlation

### AI Integration Layer
- **OpenAI** 1.0+: GPT-3.5 Turbo
- **python-dotenv** 1.0+: Environment management

### Visualization Layer
- **Plotly Express**: Quick charts
- **Plotly Graph Objects**: Custom charts
- **Matplotlib** 3.8+: Statistical plots

---

## Security Architecture

### Data Security
1. **No Cloud Storage**: All data stays local
2. **Session Isolation**: Each user session independent
3. **Temporary Storage**: Data cleared on session end
4. **No Data Logging**: Sensitive data not logged

### API Key Management
1. **Environment Variables**: Keys in .env file
2. **Not Committed**: .env in .gitignore
3. **Optional Integration**: Works without keys
4. **Secrets Management**: Streamlit Cloud secrets

### Input Validation
1. **File Type Check**: Whitelist approach
2. **Size Limits**: 50MB maximum
3. **Data Sanitization**: SQL injection prevention
4. **Error Handling**: Graceful failure, no stack traces

### Access Control
1. **Local Deployment**: No authentication needed
2. **Cloud Deployment**: Streamlit authentication
3. **API Rate Limiting**: OpenAI built-in limits
4. **HTTPS**: Recommended for production

---

## Scalability Considerations

### Current Limitations
- **In-Memory Processing**: Limited by RAM
- **Single-User Sessions**: No true multi-tenancy
- **Synchronous Processing**: Blocking operations
- **No Caching**: Recomputes on every interaction

### Optimization Strategies

#### 1. Data Chunking
```python
# Process large files in chunks
for chunk in pd.read_csv(file, chunksize=10000):
    process_chunk(chunk)
```

#### 2. Streamlit Caching
```python
@st.cache_data
def load_data(file):
    return pd.read_csv(file)
```

#### 3. Lazy Loading
```python
# Load visualizations only when requested
if viz_type == "Correlation":
    render_correlation()  # Computed on-demand
```

#### 4. Database Integration (Future)
```python
# Replace in-memory DataFrames with DB queries
engine = create_engine('postgresql://...')
df = pd.read_sql(query, engine)
```

### Scaling Roadmap

**Phase 1: Vertical Scaling**
- Increase server RAM/CPU
- Optimize pandas operations
- Add result caching

**Phase 2: Horizontal Scaling**
- Containerize with Docker
- Load balancer (Nginx)
- Session store (Redis)

**Phase 3: Distributed Processing**
- Dask for parallel computing
- Spark for big data
- Async processing queues

**Phase 4: Microservices**
- Separate API layer
- Independent service scaling
- Message queue integration

---

## Future Architecture Enhancements

### 1. REST API Layer
```
Frontend (React/Vue)
    ↓ HTTP/REST
Backend API (FastAPI)
    ↓
Services Layer
    ↓
Database (PostgreSQL)
```

### 2. Microservices Architecture
```
API Gateway
    ├─► Upload Service
    ├─► Analysis Service
    ├─► Forecasting Service
    ├─► Report Service
    └─► Notification Service
```

### 3. Real-time Processing
```
Data Stream → Kafka → Processing → WebSockets → UI
```

### 4. ML Pipeline
```
Data → Feature Engineering → Model Training → Model Registry → Prediction Service
```

---

## Diagrams

### Entity Relationship

```
┌────────────┐
│   User     │
└─────┬──────┘
      │ uploads
      ▼
┌────────────┐      ┌──────────────┐
│  Dataset   │─────►│ CleanedData  │
└─────┬──────┘      └──────┬───────┘
      │                    │
      │ analyzes           │ generates
      ▼                    ▼
┌────────────┐      ┌──────────────┐
│  Analysis  │      │   Report     │
└────────────┘      └──────────────┘
```

### Sequence Diagram: Analysis Flow

```
User          UI            Analyzer      Insight
 │            │               │            │
 │───Upload──►│               │            │
 │            │──DataFrame───►│            │
 │            │               │            │
 │            │               │──Analyze──►│
 │            │               │            │
 │            │               │◄──Insights─│
 │            │◄──Display────│            │
 │◄──Show────│               │            │
```

---

## Conclusion

InsightLens AI follows a clean, layered architecture that prioritizes:
- **Maintainability**: Clear separation of concerns
- **Extensibility**: Easy to add new features
- **Reliability**: Graceful failure handling
- **Performance**: Efficient data processing
- **Security**: Safe handling of sensitive data

The architecture supports both current requirements and future scalability needs.

---

<div align="center">

**InsightLens AI Architecture Documentation**

Version 1.0 | Last Updated: August 2026

[Back to Main Documentation](../README.md)

</div>

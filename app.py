import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from components.dashboard import render_dashboard
from components.metrics import display_kpi_cards
from components.charts import render_visualizations
from services.cleaner import DataCleaner
from services.analyzer import DataAnalyzer
from services.forecasting import SalesForecaster
from services.insights import InsightGenerator
from utils.validators import validate_file, check_required_columns, get_suggested_columns
from utils.helpers import save_to_excel, create_export_folder

st.set_page_config(
    page_title="AI Data Insights Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

create_export_folder()

def load_custom_css():
    css_file = Path(__file__).parent / "styles" / "custom.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_custom_css()

def initialize_session_state():
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'cleaned_data' not in st.session_state:
        st.session_state.cleaned_data = None
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False
    if 'column_mapping' not in st.session_state:
        st.session_state.column_mapping = None

def main():
    initialize_session_state()
    
    st.sidebar.markdown("# 📊 AI Data Insights")
    st.sidebar.markdown("**Analytics Dashboard**")
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio(
        "Navigation",
        ["📁 Upload Data", "🧹 Data Cleaning", "📈 KPI Dashboard", "📊 Visualizations", "🔮 Forecasting", "💾 Export"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Tip:** Upload any CSV or Excel file to get started with automated insights and analytics.")
    
    if menu == "📁 Upload Data":
        handle_upload()
    elif menu == "🧹 Data Cleaning":
        handle_cleaning()
    elif menu == "📈 KPI Dashboard":
        handle_dashboard()
    elif menu == "📊 Visualizations":
        handle_visualizations()
    elif menu == "🔮 Forecasting":
        handle_forecasting()
    elif menu == "💾 Export":
        handle_export()

def handle_upload():
    st.title("📁 Upload Dataset")
    st.markdown("Upload your CSV or Excel file to begin automated analysis")
    st.markdown("")
    
    with st.container():
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['csv', 'xlsx', 'xls'],
            help="Supported formats: CSV, Excel (max 50MB)"
        )
    
    if uploaded_file:
        with st.spinner("🔄 Loading and analyzing file..."):
            try:
                file_valid, message = validate_file(uploaded_file)
                
                if not file_valid:
                    st.error(f"❌ {message}")
                    return
                
                if uploaded_file.name.endswith('.csv'):
                    # Try multiple encodings for CSV files
                    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252', 'utf-16']
                    df = None
                    
                    for encoding in encodings:
                        try:
                            uploaded_file.seek(0)  # Reset file pointer
                            df = pd.read_csv(uploaded_file, encoding=encoding)
                            break
                        except (UnicodeDecodeError, UnicodeError):
                            continue
                        except Exception:
                            continue
                    
                    if df is None:
                        st.error("❌ Unable to read file. Please check the file encoding.")
                        st.info("💡 Try saving your CSV file with UTF-8 encoding.")
                        return
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.session_state.data = df
                st.session_state.file_uploaded = True
                
                suggestions = get_suggested_columns(df)
                st.session_state.column_mapping = suggestions
                
                st.success(f"✅ File uploaded successfully: **{uploaded_file.name}**")
                
                st.markdown("---")
                st.markdown("### 📋 Dataset Preview")
                st.dataframe(df.head(10), use_container_width=True)
                
                st.markdown("")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📊 Total Rows", f"{df.shape[0]:,}")
                with col2:
                    st.metric("📋 Total Columns", df.shape[1])
                with col3:
                    st.metric("💾 Memory", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
                
                st.markdown("---")
                st.markdown("### 🔍 Column Mapping")
                st.info("✨ The system has automatically detected your columns. You can proceed to analysis!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🎯 Detected Columns:**")
                    detected_count = 0
                    for key, value in suggestions.items():
                        if value:
                            st.markdown(f"- **{key.title()}**: `{value}`")
                            detected_count += 1
                    if detected_count == 0:
                        st.markdown("*Auto-detection in progress...*")
                
                with col2:
                    st.markdown("**📂 All Columns:**")
                    for col in df.columns:
                        st.markdown(f"- `{col}`")
                
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
                st.info("💡 Please ensure your file is a valid CSV or Excel format.")

def handle_cleaning():
    st.title("🧹 Data Cleaning")
    st.markdown("Clean and prepare your data for analysis")
    st.markdown("")
    
    if not st.session_state.file_uploaded:
        st.warning("⚠️ Please upload a dataset first")
        st.info("👈 Go to **Upload Data** in the sidebar to get started")
        return
    
    df = st.session_state.data
    cleaner = DataCleaner(df)
    
    st.markdown("### 📊 Data Quality Report")
    st.markdown("")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        missing_count = df.isnull().sum().sum()
        st.metric("🔍 Missing Values", f"{missing_count:,}", 
                 delta="Issues found" if missing_count > 0 else "Clean",
                 delta_color="inverse")
    with col2:
        duplicate_count = df.duplicated().sum()
        st.metric("📋 Duplicate Rows", f"{duplicate_count:,}",
                 delta="Issues found" if duplicate_count > 0 else "Clean",
                 delta_color="inverse")
    with col3:
        st.metric("📂 Total Columns", len(df.columns))
    
    if missing_count > 0:
        st.markdown("---")
        st.markdown("### 🔎 Missing Values by Column")
        missing_df = cleaner.get_missing_summary()
        st.dataframe(missing_df, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### ⚙️ Cleaning Options")
    st.markdown("")
    
    col1, col2 = st.columns(2)
    with col1:
        remove_duplicates = st.checkbox("🗑️ Remove duplicate rows", value=True)
    with col2:
        handle_missing = st.selectbox(
            "🔧 Handle missing values",
            ["Keep as is", "Drop rows", "Fill with mean", "Fill with median"]
        )
    
    st.markdown("")
    
    if st.button("✨ Clean Data", type="primary", use_container_width=True):
        with st.spinner("🔄 Cleaning data..."):
            cleaned_df = cleaner.clean_data(
                remove_duplicates=remove_duplicates,
                missing_strategy=handle_missing
            )
            st.session_state.cleaned_data = cleaned_df
            st.success("✅ Data cleaned successfully!")
            
            st.markdown("---")
            st.markdown("### 📋 Cleaned Dataset Preview")
            st.dataframe(cleaned_df.head(10), use_container_width=True)
            
            st.markdown("")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("✅ Rows After Cleaning", f"{cleaned_df.shape[0]:,}")
            with col2:
                rows_removed = df.shape[0] - cleaned_df.shape[0]
                st.metric("🗑️ Rows Removed", f"{rows_removed:,}",
                         delta=f"{(rows_removed/df.shape[0]*100):.1f}% of data" if rows_removed > 0 else "No changes")

def handle_dashboard():
    st.title("📈 KPI Dashboard")
    st.markdown("Real-time insights and performance metrics")
    st.markdown("")
    
    if st.session_state.cleaned_data is None:
        if st.session_state.data is None:
            st.warning("⚠️ Please upload a dataset first")
            st.info("👈 Go to **Upload Data** in the sidebar to get started")
            return
        df = st.session_state.data
    else:
        df = st.session_state.cleaned_data
    
    required, missing = check_required_columns(df)
    if not required:
        st.error("❌ Dataset needs at least one numeric column for analysis")
        st.info("💡 Please upload a dataset with numeric values (sales, revenue, etc.)")
        return
    
    analyzer = DataAnalyzer(df, st.session_state.column_mapping)
    insight_gen = InsightGenerator(df, st.session_state.column_mapping)
    
    with st.container():
        display_kpi_cards(analyzer)
    
    st.markdown("---")
    
    with st.container():
        render_dashboard(analyzer)
    
    st.markdown("---")
    
    st.markdown("### 🤖 AI-Generated Insights")
    
    # Check if using OpenAI
    if hasattr(insight_gen, 'openai_client') and insight_gen.openai_client:
        st.caption("✨ Powered by OpenAI GPT-3.5")
    else:
        st.caption("📊 Using rule-based analysis")
    
    st.markdown("")
    insights = insight_gen.generate_insights()
    
    if insights:
        for i, insight in enumerate(insights, 1):
            st.info(f"**💡 Insight {i}:** {insight}")
    else:
        st.info("📊 Upload a dataset with sales/revenue data to get AI-powered insights")

def handle_visualizations():
    st.title("📊 Data Visualizations")
    st.markdown("Explore your data through interactive charts")
    st.markdown("")
    
    if st.session_state.cleaned_data is None:
        if st.session_state.data is None:
            st.warning("⚠️ Please upload a dataset first")
            st.info("👈 Go to **Upload Data** in the sidebar to get started")
            return
        df = st.session_state.data
    else:
        df = st.session_state.cleaned_data
    
    required, missing = check_required_columns(df)
    if not required:
        st.error("❌ Dataset needs at least one numeric column for visualization")
        return
    
    with st.container():
        render_visualizations(df, st.session_state.column_mapping)

def handle_forecasting():
    st.title("🔮 Sales Forecasting")
    st.markdown("Predict future trends using machine learning")
    st.markdown("")
    
    if st.session_state.cleaned_data is None:
        if st.session_state.data is None:
            st.warning("⚠️ Please upload a dataset first")
            st.info("👈 Go to **Upload Data** in the sidebar to get started")
            return
        df = st.session_state.data
    else:
        df = st.session_state.cleaned_data
    
    required, missing = check_required_columns(df)
    if not required:
        st.error("❌ Dataset needs numeric columns for forecasting")
        return
    
    forecaster = SalesForecaster(df, st.session_state.column_mapping)
    
    st.markdown("### ⚙️ Forecast Configuration")
    st.markdown("")
    
    col1, col2 = st.columns(2)
    with col1:
        forecast_periods = st.slider("📅 Forecast periods (months)", 1, 12, 6)
    with col2:
        st.metric("🤖 Model", "Linear Regression")
    
    st.markdown("")
    
    if st.button("🚀 Generate Forecast", type="primary", use_container_width=True):
        with st.spinner("🔄 Training model and generating forecast..."):
            try:
                forecast_df, score, fig = forecaster.forecast_sales(periods=forecast_periods)
                
                st.success("✅ Forecast generated successfully!")
                
                st.markdown("---")
                st.markdown("### 📊 Model Performance")
                st.markdown("")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("🎯 Model Accuracy (R²)", f"{score:.2%}",
                             delta="Good" if score > 0.7 else "Fair" if score > 0.5 else "Low")
                with col2:
                    st.metric("📅 Forecast Periods", f"{forecast_periods} months")
                
                st.markdown("---")
                st.markdown("### 📈 Forecast Visualization")
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("---")
                st.markdown("### 📋 Forecast Data")
                st.dataframe(forecast_df, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error generating forecast: {str(e)}")
                st.info("💡 Make sure your dataset has a date column and numeric values for forecasting")

def handle_export():
    st.title("💾 Export Data")
    st.markdown("Download your cleaned data and analytics summary")
    st.markdown("")
    
    if st.session_state.cleaned_data is None:
        if st.session_state.data is None:
            st.warning("⚠️ Please upload a dataset first")
            st.info("👈 Go to **Upload Data** in the sidebar to get started")
            return
        df = st.session_state.data
        st.info("💡 **Tip:** Clean your data first for better export results")
    else:
        df = st.session_state.cleaned_data
    
    st.markdown("### 📥 Export Options")
    st.markdown("")
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        with st.container():
            st.markdown("#### 📊 Cleaned Dataset")
            st.markdown("Download your processed data")
            st.markdown("")
            if st.button("📥 Download Dataset", type="primary", use_container_width=True):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name="cleaned_dataset.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    with col2:
        with st.container():
            st.markdown("#### 📈 Analytics Summary")
            st.markdown("Download KPI metrics and stats")
            st.markdown("")
            if st.button("📊 Download Summary", use_container_width=True):
                try:
                    analyzer = DataAnalyzer(df, st.session_state.column_mapping)
                    summary = analyzer.get_summary_stats()
                    
                    summary_csv = pd.DataFrame([summary]).to_csv(index=False)
                    st.download_button(
                        label="💾 Download Summary CSV",
                        data=summary_csv,
                        file_name="analytics_summary.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"❌ Error generating summary: {str(e)}")
    
    st.markdown("---")
    
    st.markdown("### 📋 Dataset Preview")
    st.dataframe(df.head(20), use_container_width=True)
    
    st.markdown("")
    st.info(f"📊 **Total records available for export:** {len(df):,} rows")

if __name__ == "__main__":
    main()

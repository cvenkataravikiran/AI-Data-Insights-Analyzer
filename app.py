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
    page_title="InsightLens AI - Autonomous Data Analytics Copilot",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/insightlens-ai',
        'Report a bug': 'https://github.com/yourusername/insightlens-ai/issues',
        'About': '**InsightLens AI** v1.0 - Transform Raw Data into Actionable Business Intelligence'
    }
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
    if 'show_landing' not in st.session_state:
        st.session_state.show_landing = True
    if 'data_quality_score' not in st.session_state:
        st.session_state.data_quality_score = None
    if 'executive_summary' not in st.session_state:
        st.session_state.executive_summary = None

def main():
    initialize_session_state()
    
    # Show landing page if no file uploaded
    if not st.session_state.file_uploaded and st.session_state.show_landing:
        show_landing_page()
        return
    
    st.sidebar.markdown("# 🔮 InsightLens AI")
    st.sidebar.markdown("**Autonomous Data Analytics Copilot**")
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "📁 Upload Data", "🧹 Data Cleaning", "📊 Data Quality", "📋 Executive Summary", 
         "📈 KPI Dashboard", "📉 Visualizations", "🔮 Forecasting", "🤖 Ask Your Data", 
         "📑 Generate Report", "💾 Export"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Data info sidebar
    if st.session_state.file_uploaded:
        df = st.session_state.cleaned_data if st.session_state.cleaned_data is not None else st.session_state.data
        st.sidebar.success("✅ Dataset Loaded")
        st.sidebar.metric("Rows", f"{len(df):,}")
        st.sidebar.metric("Columns", len(df.columns))
        
        if st.session_state.data_quality_score:
            st.sidebar.metric("Quality Score", f"{st.session_state.data_quality_score:.1f}%")
        
        # Dataset switcher for multiple files
        if 'multiple_datasets' in st.session_state and st.session_state.get('analysis_mode') == 'separate':
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 🔄 Switch Dataset")
            dataset_names = [ds['name'] for ds in st.session_state.multiple_datasets]
            selected = st.sidebar.selectbox(
                "Select dataset:",
                dataset_names,
                key="sidebar_dataset_switcher",
                label_visibility="collapsed"
            )
            
            # Update current dataset if changed
            selected_ds = next(ds for ds in st.session_state.multiple_datasets if ds['name'] == selected)
            if st.session_state.data is not selected_ds['data']:
                st.session_state.data = selected_ds['data']
                st.session_state.cleaned_data = None  # Reset cleaned data
                suggestions = get_suggested_columns(selected_ds['data'])
                st.session_state.column_mapping = suggestions
                st.rerun()
    else:
        st.sidebar.info("💡 **Tip:** Upload a CSV or Excel file to unlock powerful analytics and AI insights.")
    
    if menu == "🏠 Home":
        show_landing_page()
    elif menu == "📁 Upload Data":
        handle_upload()
    elif menu == "🧹 Data Cleaning":
        handle_cleaning()
    elif menu == "📊 Data Quality":
        handle_data_quality()
    elif menu == "📋 Executive Summary":
        handle_executive_summary()
    elif menu == "📈 KPI Dashboard":
        handle_dashboard()
    elif menu == "📉 Visualizations":
        handle_visualizations()
    elif menu == "🔮 Forecasting":
        handle_forecasting()
    elif menu == "🤖 Ask Your Data":
        handle_ask_data()
    elif menu == "📑 Generate Report":
        handle_generate_report()
    elif menu == "💾 Export":
        handle_export()

def show_landing_page():
    """Modern SaaS-style landing page"""
    
    # Hero Section
    st.markdown("""
    <div style='text-align: center; padding: 3rem 0 2rem 0;'>
        <h1 style='font-size: 3.5rem; font-weight: 800; background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem;'>
            🔮 InsightLens AI
        </h1>
        <h2 style='font-size: 1.5rem; color: #64748b; font-weight: 400; margin-bottom: 0.5rem;'>
            Autonomous Data Analytics Copilot
        </h2>
        <p style='font-size: 1.125rem; color: #94a3b8; max-width: 600px; margin: 0 auto 2rem auto;'>
            Transform Raw Data into Actionable Business Intelligence using AI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Get Started - Upload Your Data", type="primary", use_container_width=True, key="landing_cta_top"):
            st.session_state.show_landing = False
            st.rerun()
    
    st.markdown("---")
    
    # Key Features
    st.markdown("### ✨ Why Choose InsightLens AI?")
    st.markdown("")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: white; padding: 1.5rem; border-radius: 1rem; border: 1px solid #e2e8f0; height: 100%;'>
            <div style='font-size: 2rem; margin-bottom: 1rem;'>🤖</div>
            <h4 style='color: #1e293b; margin-bottom: 0.5rem;'>AI-Powered Insights</h4>
            <p style='color: #64748b; font-size: 0.9rem;'>
                Automatically generate business insights, identify trends, and discover hidden patterns using advanced AI.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: white; padding: 1.5rem; border-radius: 1rem; border: 1px solid #e2e8f0; height: 100%;'>
            <div style='font-size: 2rem; margin-bottom: 1rem;'>⚡</div>
            <h4 style='color: #1e293b; margin-bottom: 0.5rem;'>Instant Analytics</h4>
            <p style='color: #64748b; font-size: 0.9rem;'>
                Upload any CSV or Excel file and get immediate KPIs, visualizations, and forecasts in seconds.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: white; padding: 1.5rem; border-radius: 1rem; border: 1px solid #e2e8f0; height: 100%;'>
            <div style='font-size: 2rem; margin-bottom: 1rem;'>🎯</div>
            <h4 style='color: #1e293b; margin-bottom: 0.5rem;'>Enterprise Quality</h4>
            <p style='color: #64748b; font-size: 0.9rem;'>
                Professional-grade data quality assessment, cleaning, and executive reporting capabilities.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Core Capabilities
    st.markdown("### 🎯 Core Capabilities")
    st.markdown("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📊 Data Processing & Quality**
        - Automatic column detection & type inference
        - Data cleaning & validation
        - Quality scoring & assessment
        - Duplicate & anomaly detection
        
        **📈 Analytics & Visualization**
        - Interactive dashboards & KPI cards
        - 15+ chart types with Plotly
        - Trend analysis & correlation matrices
        - Regional & product performance
        """)
    
    with col2:
        st.markdown("""
        **🤖 AI & Machine Learning**
        - AI-generated executive summaries
        - Business insight generation
        - Conversational data queries
        - Sales forecasting (Linear Regression)
        
        **📑 Reporting & Export**
        - Executive PDF reports
        - CSV/Excel exports
        - Chart image downloads
        - Professional formatting
        """)
    
    st.markdown("---")
    
    # Supported Formats
    st.markdown("### 📁 Supported File Formats")
    st.markdown("")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info("**CSV Files**\n\n`.csv`")
    with col2:
        st.info("**Excel Files**\n\n`.xlsx`, `.xls`")
    with col3:
        st.info("**Any Columns**\n\nAuto-detection")
    with col4:
        st.info("**Up to 50MB**\n\nLarge datasets")
    
    st.markdown("---")
    
    # How It Works
    st.markdown("### 🔄 How It Works")
    st.markdown("")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <div style='background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); 
                        color: white; width: 60px; height: 60px; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; 
                        font-size: 1.5rem; font-weight: bold; margin: 0 auto 1rem;'>1</div>
            <h5 style='color: #1e293b; margin-bottom: 0.5rem;'>Upload</h5>
            <p style='color: #64748b; font-size: 0.85rem;'>Drop your CSV or Excel file</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <div style='background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); 
                        color: white; width: 60px; height: 60px; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; 
                        font-size: 1.5rem; font-weight: bold; margin: 0 auto 1rem;'>2</div>
            <h5 style='color: #1e293b; margin-bottom: 0.5rem;'>Clean</h5>
            <p style='color: #64748b; font-size: 0.85rem;'>Auto-clean & validate data</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <div style='background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%); 
                        color: white; width: 60px; height: 60px; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; 
                        font-size: 1.5rem; font-weight: bold; margin: 0 auto 1rem;'>3</div>
            <h5 style='color: #1e293b; margin-bottom: 0.5rem;'>Analyze</h5>
            <p style='color: #64748b; font-size: 0.85rem;'>Get AI insights & forecasts</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                        color: white; width: 60px; height: 60px; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; 
                        font-size: 1.5rem; font-weight: bold; margin: 0 auto 1rem;'>4</div>
            <h5 style='color: #1e293b; margin-bottom: 0.5rem;'>Export</h5>
            <p style='color: #64748b; font-size: 0.85rem;'>Download reports & data</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Technology Stack
    with st.expander("🛠️ Technology Stack", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **Frontend & Framework**
            - Streamlit
            - Plotly
            - Custom CSS
            """)
        
        with col2:
            st.markdown("""
            **Data Processing**
            - Pandas
            - NumPy
            - Scikit-learn
            """)
        
        with col3:
            st.markdown("""
            **AI & Analytics**
            - OpenAI GPT-3.5
            - Linear Regression
            - Statistical Analysis
            """)
    
    st.markdown("---")
    
    # Footer CTA
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h3 style='color: #1e293b; margin-bottom: 1rem;'>Ready to Transform Your Data?</h3>
        <p style='color: #64748b; margin-bottom: 2rem;'>Join hundreds of data analysts leveraging AI for business intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📊 Start Analyzing Now", type="primary", use_container_width=True, key="landing_cta_bottom"):
            st.session_state.show_landing = False
            st.rerun()

def handle_data_quality():
    """Data Quality Assessment module"""
    st.title("📊 Data Quality Assessment")
    st.markdown("Comprehensive data quality analysis and scoring")
    st.markdown("")
    
    if not st.session_state.file_uploaded:
        st.warning("⚠️ Please upload a dataset first")
        st.info("👈 Go to **Upload Data** in the sidebar to get started")
        return
    
    df = st.session_state.data
    
    from services.data_quality import DataQualityAssessor
    assessor = DataQualityAssessor(df)
    quality_report = assessor.assess_quality()
    
    # Overall Quality Score
    st.markdown("### 🎯 Overall Data Quality Score")
    st.markdown("")
    
    score = quality_report['overall_score']
    st.session_state.data_quality_score = score
    
    # Color-coded score display
    if score >= 80:
        color = "#10b981"
        grade = "Excellent"
        icon = "🌟"
    elif score >= 60:
        color = "#3b82f6"
        grade = "Good"
        icon = "✅"
    elif score >= 40:
        color = "#f59e0b"
        grade = "Fair"
        icon = "⚠️"
    else:
        color = "#ef4444"
        grade = "Poor"
        icon = "❌"
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div style='background: white; padding: 2rem; border-radius: 1rem; border: 3px solid {color}; text-align: center;'>
            <div style='font-size: 4rem; font-weight: 800; color: {color};'>{score:.1f}%</div>
            <div style='font-size: 1.5rem; color: #64748b; font-weight: 600;'>{icon} {grade} Quality</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric("📊 Total Rows", f"{len(df):,}")
        st.metric("📋 Total Columns", len(df.columns))
    
    with col3:
        st.metric("✅ Complete Rows", f"{quality_report['complete_rows']:,}")
        st.metric("📈 Valid Data %", f"{quality_report['valid_percentage']:.1f}%")
    
    st.markdown("---")
    
    # Quality Dimensions
    st.markdown("### 📐 Quality Dimensions")
    st.markdown("")
    
    col1, col2, col3, col4 = st.columns(4)
    
    dimensions = quality_report['dimensions']
    
    with col1:
        completeness = dimensions['completeness']
        delta_color = "normal" if completeness >= 80 else "inverse"
        st.metric("✓ Completeness", f"{completeness:.1f}%", 
                 delta="High" if completeness >= 80 else "Low", delta_color=delta_color)
    
    with col2:
        consistency = dimensions['consistency']
        delta_color = "normal" if consistency >= 80 else "inverse"
        st.metric("⚖️ Consistency", f"{consistency:.1f}%",
                 delta="High" if consistency >= 80 else "Low", delta_color=delta_color)
    
    with col3:
        uniqueness = dimensions['uniqueness']
        delta_color = "normal" if uniqueness >= 80 else "inverse"
        st.metric("🔑 Uniqueness", f"{uniqueness:.1f}%",
                 delta="High" if uniqueness >= 80 else "Low", delta_color=delta_color)
    
    with col4:
        validity = dimensions['validity']
        delta_color = "normal" if validity >= 80 else "inverse"
        st.metric("✅ Validity", f"{validity:.1f}%",
                 delta="High" if validity >= 80 else "Low", delta_color=delta_color)
    
    st.markdown("---")
    
    # Detailed Issues
    st.markdown("### 🔍 Data Quality Issues")
    st.markdown("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Missing Values
        missing_summary = quality_report['missing_summary']
        if not missing_summary.empty:
            st.markdown("#### ❌ Missing Values by Column")
            st.dataframe(missing_summary, use_container_width=True)
        else:
            st.success("✅ No missing values detected!")
    
    with col2:
        # Duplicates
        st.markdown("#### 📋 Duplicate Analysis")
        st.metric("Duplicate Rows", f"{quality_report['duplicate_count']:,}")
        if quality_report['duplicate_count'] > 0:
            duplicate_pct = (quality_report['duplicate_count'] / len(df)) * 100
            st.warning(f"⚠️ {duplicate_pct:.1f}% of data is duplicated")
        else:
            st.success("✅ No duplicate rows found!")
    
    st.markdown("---")
    
    # Column-wise Analysis
    st.markdown("### 📊 Column-wise Quality Analysis")
    col_quality = quality_report['column_quality']
    
    st.dataframe(col_quality, use_container_width=True)
    
    st.markdown("---")
    
    # Recommendations
    st.markdown("### 💡 Recommendations")
    
    recommendations = quality_report['recommendations']
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            st.info(f"**{i}.** {rec}")
    else:
        st.success("✅ Your data quality is excellent! No immediate actions required.")

def handle_executive_summary():
    """Generate Executive Summary"""
    st.title("📋 Executive Summary")
    st.markdown("AI-generated business intelligence overview")
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
        return
    
    from services.executive_summary import ExecutiveSummaryGenerator
    summary_gen = ExecutiveSummaryGenerator(df, st.session_state.column_mapping)
    
    if st.button("🚀 Generate Executive Summary", type="primary", use_container_width=True):
        with st.spinner("🔄 Analyzing data and generating executive summary..."):
            summary = summary_gen.generate_summary()
            st.session_state.executive_summary = summary
    
    if st.session_state.executive_summary:
        summary = st.session_state.executive_summary
        
        # Business Overview
        st.markdown("### 📊 Business Overview")
        st.info(summary['overview'])
        
        st.markdown("---")
        
        # Key Findings
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Key Positive Findings")
            for finding in summary['positive_findings']:
                st.success(f"• {finding}")
        
        with col2:
            st.markdown("### ⚠️ Areas of Concern")
            for concern in summary['concerns']:
                st.warning(f"• {concern}")
        
        st.markdown("---")
        
        # Opportunities & Risks
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🚀 Growth Opportunities")
            for opp in summary['opportunities']:
                st.info(f"• {opp}")
        
        with col2:
            st.markdown("### ⚡ Business Risks")
            for risk in summary['risks']:
                st.error(f"• {risk}")
        
        st.markdown("---")
        
        # Recommendations
        st.markdown("### 💡 Strategic Recommendations")
        for i, rec in enumerate(summary['recommendations'], 1):
            st.markdown(f"**{i}.** {rec}")
        
        st.markdown("---")
        
        # AI Conclusion
        st.markdown("### 🤖 AI-Generated Conclusion")
        st.info(summary['conclusion'])

def handle_ask_data():
    """Conversational analytics interface"""
    st.title("🤖 Ask Your Data")
    st.markdown("Natural language queries about your dataset")
    st.markdown("")
    
    if st.session_state.cleaned_data is None:
        if st.session_state.data is None:
            st.warning("⚠️ Please upload a dataset first")
            st.info("👈 Go to **Upload Data** in the sidebar to get started")
            return
        df = st.session_state.data
    else:
        df = st.session_state.cleaned_data
    
    from services.ask_data import AskDataAgent
    agent = AskDataAgent(df, st.session_state.column_mapping)
    
    # Example questions
    with st.expander("💡 Example Questions", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            - Which region generated the highest revenue?
            - What is the average profit margin?
            - Show me top 5 products by sales
            - Which month had the best performance?
            """)
        
        with col2:
            st.markdown("""
            - What percentage of total sales comes from the top category?
            - How does profit correlate with sales?
            - What is the growth trend over time?
            - Identify any anomalies or outliers
            """)
    
    st.markdown("")
    
    # Question input
    question = st.text_area(
        "Ask a question about your data:",
        placeholder="e.g., Which products are most profitable?",
        height=100
    )
    
    if st.button("🔍 Get Answer", type="primary", use_container_width=True):
        if question.strip():
            with st.spinner("🔄 Analyzing your question..."):
                answer = agent.answer_question(question)
                
                st.markdown("---")
                st.markdown("### 💬 Answer")
                st.success(answer['answer'])
                
                # Show supporting data if available
                if 'data' in answer and answer['data'] is not None:
                    st.markdown("---")
                    st.markdown("### 📊 Supporting Data")
                    if isinstance(answer['data'], pd.DataFrame):
                        st.dataframe(answer['data'], use_container_width=True)
                    else:
                        st.write(answer['data'])
                
                # Show visualization if available
                if 'chart' in answer and answer['chart'] is not None:
                    st.markdown("---")
                    st.markdown("### 📈 Visualization")
                    st.plotly_chart(answer['chart'], use_container_width=True)
        else:
            st.warning("⚠️ Please enter a question")

def handle_generate_report():
    """Generate professional PDF report"""
    st.title("📑 Generate Executive Report")
    st.markdown("Create a comprehensive PDF report with all analytics")
    st.markdown("")
    
    if st.session_state.cleaned_data is None:
        if st.session_state.data is None:
            st.warning("⚠️ Please upload a dataset first")
            st.info("👈 Go to **Upload Data** in the sidebar to get started")
            return
        df = st.session_state.data
    else:
        df = st.session_state.cleaned_data
    
    st.markdown("### 📄 Report Configuration")
    st.markdown("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        report_title = st.text_input("Report Title", "Business Analytics Report")
        company_name = st.text_input("Company Name", "Your Company")
    
    with col2:
        include_charts = st.checkbox("Include Charts", value=True)
        include_forecast = st.checkbox("Include Forecast", value=True)
    
    st.markdown("")
    
    if st.button("📊 Generate Report", type="primary", use_container_width=True, key="generate_report_btn"):
        with st.spinner("🔄 Generating professional report..."):
            try:
                from services.report_generator import ReportGenerator
                
                generator = ReportGenerator(df, st.session_state.column_mapping)
                
                # Generate HTML report (PDF requires additional libraries)
                html_report = generator.generate_html_report(report_title, company_name)
                
                st.success("✅ Report generated successfully!")
                st.markdown("---")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.download_button(
                        label="📥 Download HTML Report",
                        data=html_report,
                        file_name=f"{report_title.replace(' ', '_')}.html",
                        mime="text/html",
                        use_container_width=True,
                        key="download_html_report"
                    )
                
            except Exception as e:
                st.error(f"❌ Error generating report: {str(e)}")
                st.info("💡 Please try again or contact support if the issue persists.")

def handle_upload():
    st.title("📁 Upload Dataset")
    st.markdown("Upload your CSV or Excel files to begin automated analysis")
    st.markdown("")
    
    # Option to upload multiple files
    upload_mode = st.radio(
        "Upload Mode",
        ["Single File", "Multiple Files"],
        horizontal=True,
        help="Choose whether to upload one file or multiple files at once"
    )
    
    st.markdown("")
    
    if upload_mode == "Single File":
        with st.container():
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=['csv', 'xlsx', 'xls'],
                help="Supported formats: CSV, Excel (max 50MB)",
                key="dataset_file_uploader"
            )
        
        if uploaded_file:
            handle_single_file_upload(uploaded_file)
    
    else:  # Multiple Files
        with st.container():
            uploaded_files = st.file_uploader(
                "Choose multiple files",
                type=['csv', 'xlsx', 'xls'],
                help="Supported formats: CSV, Excel (max 50MB each)",
                accept_multiple_files=True,
                key="dataset_multiple_file_uploader"
            )
        
        if uploaded_files:
            handle_multiple_files_upload(uploaded_files)

def handle_single_file_upload(uploaded_file):
    """Handle single file upload"""
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
            st.session_state.uploaded_files_info = [{'name': uploaded_file.name, 'rows': len(df), 'cols': len(df.columns)}]
            
            suggestions = get_suggested_columns(df)
            st.session_state.column_mapping = suggestions
            
            st.success(f"✅ File uploaded successfully: **{uploaded_file.name}**")
            
            display_dataset_preview(df, uploaded_file.name, suggestions)
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            st.info("💡 Please ensure your file is a valid CSV or Excel format.")

def handle_multiple_files_upload(uploaded_files):
    """Handle multiple files upload"""
    st.info(f"📊 **{len(uploaded_files)} files selected**")
    
    # Option to merge or analyze separately
    analysis_mode = st.radio(
        "How would you like to analyze multiple files?",
        ["Merge into Single Dataset", "Analyze Each File Separately"],
        help="Merge: Combines all files into one dataset | Separate: Analyze each file individually"
    )
    
    st.markdown("")
    
    if st.button("🚀 Process Files", type="primary", use_container_width=True, key="process_multiple_files"):
        if analysis_mode == "Merge into Single Dataset":
            merge_and_analyze_files(uploaded_files)
        else:
            analyze_files_separately(uploaded_files)

def merge_and_analyze_files(uploaded_files):
    """Merge multiple files into one dataset"""
    with st.spinner(f"🔄 Loading and merging {len(uploaded_files)} files..."):
        try:
            all_dfs = []
            files_info = []
            
            for uploaded_file in uploaded_files:
                file_valid, message = validate_file(uploaded_file)
                
                if not file_valid:
                    st.warning(f"⚠️ Skipping {uploaded_file.name}: {message}")
                    continue
                
                try:
                    if uploaded_file.name.endswith('.csv'):
                        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252', 'utf-16']
                        df = None
                        
                        for encoding in encodings:
                            try:
                                uploaded_file.seek(0)
                                df = pd.read_csv(uploaded_file, encoding=encoding)
                                break
                            except:
                                continue
                        
                        if df is None:
                            st.warning(f"⚠️ Skipping {uploaded_file.name}: Unable to read file")
                            continue
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    # Add source file column
                    df['_source_file'] = uploaded_file.name
                    all_dfs.append(df)
                    files_info.append({'name': uploaded_file.name, 'rows': len(df), 'cols': len(df.columns)})
                    
                except Exception as e:
                    st.warning(f"⚠️ Error loading {uploaded_file.name}: {str(e)}")
                    continue
            
            if not all_dfs:
                st.error("❌ No valid files could be loaded")
                return
            
            # Merge all dataframes
            merged_df = pd.concat(all_dfs, ignore_index=True, sort=False)
            
            st.session_state.data = merged_df
            st.session_state.file_uploaded = True
            st.session_state.uploaded_files_info = files_info
            
            suggestions = get_suggested_columns(merged_df)
            st.session_state.column_mapping = suggestions
            
            st.success(f"✅ Successfully merged {len(all_dfs)} files into one dataset!")
            
            # Show merge summary
            st.markdown("---")
            st.markdown("### 📊 Merge Summary")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📁 Files Merged", len(all_dfs))
            with col2:
                st.metric("📊 Total Rows", f"{len(merged_df):,}")
            with col3:
                st.metric("📋 Total Columns", len(merged_df.columns))
            
            st.markdown("")
            
            # Files included
            with st.expander("📂 Files Included in Merge"):
                for info in files_info:
                    st.markdown(f"- **{info['name']}**: {info['rows']:,} rows × {info['cols']} columns")
            
            display_dataset_preview(merged_df, "Merged Dataset", suggestions)
            
        except Exception as e:
            st.error(f"❌ Error merging files: {str(e)}")

def analyze_files_separately(uploaded_files):
    """Analyze each file separately"""
    with st.spinner(f"🔄 Loading {len(uploaded_files)} files..."):
        try:
            all_datasets = []
            
            for uploaded_file in uploaded_files:
                file_valid, message = validate_file(uploaded_file)
                
                if not file_valid:
                    st.warning(f"⚠️ Skipping {uploaded_file.name}: {message}")
                    continue
                
                try:
                    if uploaded_file.name.endswith('.csv'):
                        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252', 'utf-16']
                        df = None
                        
                        for encoding in encodings:
                            try:
                                uploaded_file.seek(0)
                                df = pd.read_csv(uploaded_file, encoding=encoding)
                                break
                            except:
                                continue
                        
                        if df is None:
                            st.warning(f"⚠️ Skipping {uploaded_file.name}: Unable to read file")
                            continue
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    all_datasets.append({
                        'name': uploaded_file.name,
                        'data': df,
                        'rows': len(df),
                        'cols': len(df.columns)
                    })
                    
                except Exception as e:
                    st.warning(f"⚠️ Error loading {uploaded_file.name}: {str(e)}")
                    continue
            
            if not all_datasets:
                st.error("❌ No valid files could be loaded")
                return
            
            st.success(f"✅ Successfully loaded {len(all_datasets)} files!")
            
            # Store multiple datasets in session state
            st.session_state.multiple_datasets = all_datasets
            st.session_state.file_uploaded = True
            st.session_state.analysis_mode = "separate"
            
            # Select which dataset to analyze
            st.markdown("---")
            st.markdown("### 📊 Select Dataset to Analyze")
            
            dataset_names = [ds['name'] for ds in all_datasets]
            selected_dataset = st.selectbox(
                "Choose a dataset:",
                dataset_names,
                key="selected_dataset_for_analysis"
            )
            
            # Get selected dataset
            selected_ds = next(ds for ds in all_datasets if ds['name'] == selected_dataset)
            
            # Set as current working dataset
            st.session_state.data = selected_ds['data']
            suggestions = get_suggested_columns(selected_ds['data'])
            st.session_state.column_mapping = suggestions
            
            st.info(f"📌 **Currently analyzing**: {selected_dataset}")
            
            # Show all datasets summary
            with st.expander("📂 All Loaded Datasets", expanded=True):
                for ds in all_datasets:
                    is_current = "🔹" if ds['name'] == selected_dataset else "○"
                    st.markdown(f"{is_current} **{ds['name']}**: {ds['rows']:,} rows × {ds['cols']} columns")
            
            display_dataset_preview(selected_ds['data'], selected_dataset, suggestions)
            
        except Exception as e:
            st.error(f"❌ Error loading files: {str(e)}")

def display_dataset_preview(df, filename, suggestions):
    """Display dataset preview and information"""
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
            if not col.startswith('_source_file'):  # Hide internal columns
                st.markdown(f"- `{col}`")

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

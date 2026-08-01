"""
Professional Report Generator
Generate executive PDF and HTML reports
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

class ReportGenerator:
    def __init__(self, df, config=None):
        self.df = df.copy()
        self.config = config or self._auto_detect_columns()
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _auto_detect_columns(self):
        """Auto-detect column mappings"""
        config = {}
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) >= 1:
            config['sales'] = numeric_cols[0]
        if len(numeric_cols) >= 2:
            config['profit'] = numeric_cols[1]
        
        for col in self.df.columns:
            col_lower = col.lower()
            if 'date' in col_lower or 'time' in col_lower:
                config['date'] = col
                break
        
        categorical_cols = self.df.select_dtypes(include=['object']).columns.tolist()
        if len(categorical_cols) >= 1:
            config['product'] = categorical_cols[0]
        if len(categorical_cols) >= 2:
            config['category'] = categorical_cols[1]
        if len(categorical_cols) >= 3:
            config['region'] = categorical_cols[2]
        
        return config
    
    def generate_html_report(self, title="Business Analytics Report", company="Your Company"):
        """Generate comprehensive HTML report"""
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
        }}
        
        .cover {{
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            padding: 100px 50px;
            text-align: center;
            min-height: 400px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        
        .cover h1 {{
            font-size: 3rem;
            margin-bottom: 1rem;
            font-weight: 700;
        }}
        
        .cover .subtitle {{
            font-size: 1.5rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }}
        
        .cover .company {{
            font-size: 1.2rem;
            opacity: 0.8;
        }}
        
        .content {{
            padding: 50px;
        }}
        
        .section {{
            margin-bottom: 40px;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 5px solid #3b82f6;
        }}
        
        h2 {{
            color: #1e293b;
            font-size: 2rem;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #3b82f6;
        }}
        
        h3 {{
            color: #334155;
            font-size: 1.5rem;
            margin: 20px 0 15px 0;
        }}
        
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .kpi-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #3b82f6;
        }}
        
        .kpi-card .label {{
            color: #64748b;
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 8px;
        }}
        
        .kpi-card .value {{
            color: #0f172a;
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 5px;
        }}
        
        .kpi-card .delta {{
            color: #10b981;
            font-size: 0.9rem;
            font-weight: 600;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        th {{
            background: #3b82f6;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        tr:hover {{
            background: #f8fafc;
        }}
        
        .insight {{
            background: white;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            border-left: 4px solid #10b981;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        
        .insight.warning {{
            border-left-color: #f59e0b;
        }}
        
        .insight.error {{
            border-left-color: #ef4444;
        }}
        
        .footer {{
            background: #1e293b;
            color: white;
            padding: 30px 50px;
            text-align: center;
        }}
        
        .footer .timestamp {{
            opacity: 0.7;
            margin-top: 10px;
        }}
        
        @media print {{
            .cover {{
                page-break-after: always;
            }}
            .section {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Cover Page -->
        <div class="cover">
            <h1>📊 {title}</h1>
            <div class="subtitle">Comprehensive Data Analytics & Business Intelligence</div>
            <div class="company">{company}</div>
            <div class="timestamp" style="margin-top: 30px; font-size: 1rem;">Generated: {self.timestamp}</div>
        </div>
        
        <!-- Main Content -->
        <div class="content">
            {self._generate_executive_summary_html()}
            {self._generate_kpi_section_html()}
            {self._generate_insights_section_html()}
            {self._generate_data_quality_html()}
            {self._generate_detailed_analysis_html()}
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 10px;">InsightLens AI</div>
            <div>Autonomous Data Analytics Copilot</div>
            <div class="timestamp">Report Generated: {self.timestamp}</div>
            <div style="margin-top: 15px; opacity: 0.7;">Transform Raw Data into Actionable Business Intelligence</div>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def _generate_executive_summary_html(self):
        """Generate executive summary section"""
        sales_col = self.config.get('sales')
        profit_col = self.config.get('profit')
        
        summary = f"""
        <div class="section">
            <h2>📋 Executive Summary</h2>
            <p style="font-size: 1.1rem; line-height: 1.8; margin: 20px 0;">
                This report analyzes {len(self.df):,} business records across {len(self.df.columns)} data attributes. 
        """
        
        if sales_col and sales_col in self.df.columns:
            total_sales = self.df[sales_col].sum()
            avg_sales = self.df[sales_col].mean()
            summary += f"Total {sales_col} reached <strong>${total_sales:,.2f}</strong> with an average of <strong>${avg_sales:,.2f}</strong> per transaction. "
        
        if profit_col and profit_col in self.df.columns and sales_col and sales_col in self.df.columns:
            total_profit = self.df[profit_col].sum()
            margin = (total_profit / self.df[sales_col].sum() * 100) if self.df[sales_col].sum() > 0 else 0
            summary += f"The business generated <strong>${total_profit:,.2f}</strong> in profit, representing a <strong>{margin:.1f}%</strong> profit margin. "
        
        summary += """
            The analysis reveals key performance indicators, growth opportunities, and strategic recommendations 
            to drive business success.
            </p>
        </div>
        """
        
        return summary
    
    def _generate_kpi_section_html(self):
        """Generate KPI cards section"""
        sales_col = self.config.get('sales')
        profit_col = self.config.get('profit')
        
        kpis = []
        
        if sales_col and sales_col in self.df.columns:
            total_sales = self.df[sales_col].sum()
            kpis.append(f"""
                <div class="kpi-card">
                    <div class="label">💰 Total {sales_col}</div>
                    <div class="value">${total_sales:,.0f}</div>
                    <div class="delta">Across {len(self.df):,} records</div>
                </div>
            """)
            
            avg_sales = self.df[sales_col].mean()
            kpis.append(f"""
                <div class="kpi-card">
                    <div class="label">📊 Average {sales_col}</div>
                    <div class="value">${avg_sales:,.0f}</div>
                    <div class="delta">Per transaction</div>
                </div>
            """)
        
        if profit_col and profit_col in self.df.columns:
            total_profit = self.df[profit_col].sum()
            kpis.append(f"""
                <div class="kpi-card">
                    <div class="label">📈 Total {profit_col}</div>
                    <div class="value">${total_profit:,.0f}</div>
                    <div class="delta">Overall profit</div>
                </div>
            """)
            
            if sales_col and sales_col in self.df.columns:
                margin = (total_profit / self.df[sales_col].sum() * 100) if self.df[sales_col].sum() > 0 else 0
                kpis.append(f"""
                    <div class="kpi-card">
                        <div class="label">💹 Profit Margin</div>
                        <div class="value">{margin:.1f}%</div>
                        <div class="delta">Overall profitability</div>
                    </div>
                """)
        
        if not kpis:
            kpis.append(f"""
                <div class="kpi-card">
                    <div class="label">📊 Total Records</div>
                    <div class="value">{len(self.df):,}</div>
                    <div class="delta">{len(self.df.columns)} columns</div>
                </div>
            """)
        
        return f"""
        <div class="section">
            <h2>🎯 Key Performance Indicators</h2>
            <div class="kpi-grid">
                {''.join(kpis)}
            </div>
        </div>
        """
    
    def _generate_insights_section_html(self):
        """Generate insights section"""
        insights_html = """
        <div class="section">
            <h2>💡 Key Insights & Findings</h2>
        """
        
        # Top performers
        product_col = self.config.get('product')
        sales_col = self.config.get('sales')
        
        if product_col and product_col in self.df.columns and sales_col and sales_col in self.df.columns:
            try:
                grouped = self.df.groupby(product_col)[sales_col].sum()
                if len(grouped) > 0:
                    top_product = grouped.idxmax()
                    top_sales = grouped.max()
                    
                    insights_html += f"""
            <div class="insight">
                <h3>🏆 Top Performer</h3>
                <p>'{top_product}' is the leading {product_col} with <strong>${top_sales:,.2f}</strong> in {sales_col}, 
                demonstrating strong market demand and customer preference.</p>
            </div>
            """
            except:
                pass
        
        # Regional analysis
        region_col = self.config.get('region')
        if region_col and region_col in self.df.columns and sales_col and sales_col in self.df.columns:
            try:
                grouped = self.df.groupby(region_col)[sales_col].sum()
                if len(grouped) > 0:
                    top_region = grouped.idxmax()
                    region_sales = grouped.max()
                    total = self.df[sales_col].sum()
                    pct = (region_sales / total * 100) if total > 0 else 0
                    
                    insights_html += f"""
            <div class="insight">
                <h3>🌍 Geographic Performance</h3>
                <p>The '{top_region}' region leads with <strong>{pct:.1f}%</strong> of total {sales_col} 
                (<strong>${region_sales:,.2f}</strong>), indicating strong market presence and growth potential.</p>
            </div>
            """
            except:
                pass
        
        # Profit margin insight
        profit_col = self.config.get('profit')
        if profit_col and profit_col in self.df.columns and sales_col and sales_col in self.df.columns:
            total_profit = self.df[profit_col].sum()
            total_sales = self.df[sales_col].sum()
            margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
            
            insight_class = "insight" if margin >= 15 else "insight warning"
            margin_desc = "healthy" if margin >= 15 else "moderate"
            
            insights_html += f"""
            <div class="{insight_class}">
                <h3>💹 Profitability Analysis</h3>
                <p>The business maintains a <strong>{margin_desc}</strong> profit margin of <strong>{margin:.1f}%</strong>, 
                {"indicating strong operational efficiency and pricing strategy." if margin >= 15 else "suggesting opportunities for cost optimization and margin improvement."}</p>
            </div>
            """
        
        insights_html += "</div>"
        return insights_html
    
    def _generate_data_quality_html(self):
        """Generate data quality section"""
        missing_pct = (self.df.isnull().sum().sum() / (self.df.shape[0] * self.df.shape[1])) * 100
        duplicate_count = self.df.duplicated().sum()
        
        quality_score = 100 - missing_pct - (duplicate_count / len(self.df) * 20)
        quality_score = max(0, min(100, quality_score))
        
        quality_class = "insight" if quality_score >= 80 else "insight warning" if quality_score >= 60 else "insight error"
        quality_grade = "Excellent" if quality_score >= 80 else "Good" if quality_score >= 60 else "Fair"
        
        return f"""
        <div class="section">
            <h2>📊 Data Quality Assessment</h2>
            <div class="{quality_class}">
                <h3>✓ Overall Quality Score: {quality_score:.1f}% - {quality_grade}</h3>
                <p style="margin-top: 15px;">
                    <strong>Completeness:</strong> {100 - missing_pct:.1f}% of data is complete<br>
                    <strong>Duplicates:</strong> {duplicate_count:,} duplicate records found<br>
                    <strong>Records:</strong> {len(self.df):,} total records analyzed
                </p>
            </div>
        </div>
        """
    
    def _generate_detailed_analysis_html(self):
        """Generate detailed analysis tables"""
        html = """
        <div class="section">
            <h2>📋 Detailed Analysis</h2>
        """
        
        # Top products table
        product_col = self.config.get('product')
        sales_col = self.config.get('sales')
        profit_col = self.config.get('profit')
        
        if product_col and product_col in self.df.columns and sales_col and sales_col in self.df.columns:
            top_products = self.df.groupby(product_col)[sales_col].sum().nlargest(10).reset_index()
            
            html += f"""
            <h3>Top 10 {product_col}s by {sales_col}</h3>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>{product_col}</th>
                        <th>{sales_col}</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            for idx, row in top_products.iterrows():
                html += f"""
                    <tr>
                        <td>{idx + 1}</td>
                        <td>{row[product_col]}</td>
                        <td>${row[sales_col]:,.2f}</td>
                    </tr>
                """
            
            html += """
                </tbody>
            </table>
            """
        
        # Summary statistics
        html += """
            <h3>Dataset Summary Statistics</h3>
            <table>
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        html += f"""
                    <tr>
                        <td>Total Records</td>
                        <td>{len(self.df):,}</td>
                    </tr>
                    <tr>
                        <td>Total Columns</td>
                        <td>{len(self.df.columns)}</td>
                    </tr>
                    <tr>
                        <td>Missing Values</td>
                        <td>{self.df.isnull().sum().sum():,}</td>
                    </tr>
                    <tr>
                        <td>Duplicate Records</td>
                        <td>{self.df.duplicated().sum():,}</td>
                    </tr>
        """
        
        html += """
                </tbody>
            </table>
        </div>
        """
        
        return html
    
    def generate_pdf_report(self, title="Business Analytics Report", company="Your Company", 
                          include_charts=True, include_forecast=True):
        """Generate PDF report (requires additional libraries)"""
        # Note: PDF generation requires libraries like reportlab or weasyprint
        # For now, we'll save HTML and inform user to convert to PDF
        
        html_content = self.generate_html_report(title, company)
        
        # Save HTML file
        exports_dir = Path("exports")
        exports_dir.mkdir(exist_ok=True)
        
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = exports_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath

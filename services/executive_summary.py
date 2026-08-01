"""
Executive Summary Generator
AI-powered business intelligence summarization
"""

import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class ExecutiveSummaryGenerator:
    def __init__(self, df, config=None):
        self.df = df.copy()
        self.config = config or self._auto_detect_columns()
        
        # Initialize OpenAI client if available
        self.use_openai = os.getenv('USE_OPENAI', 'true').lower() == 'true'
        self.openai_client = None
        
        if OPENAI_AVAILABLE and self.use_openai:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key and api_key != 'your_openai_api_key_here':
                try:
                    self.openai_client = OpenAI(api_key=api_key)
                except:
                    self.openai_client = None
    
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
    
    def generate_summary(self):
        """Generate comprehensive executive summary"""
        summary = {
            'overview': '',
            'positive_findings': [],
            'concerns': [],
            'opportunities': [],
            'risks': [],
            'recommendations': [],
            'conclusion': ''
        }
        
        if self.openai_client:
            try:
                return self._generate_ai_summary()
            except Exception as e:
                print(f"OpenAI error: {e}. Falling back to rule-based summary.")
                return self._generate_rule_based_summary()
        else:
            return self._generate_rule_based_summary()
    
    def _generate_ai_summary(self):
        """Generate summary using OpenAI API"""
        # Prepare data analysis
        analysis = self._analyze_data()
        
        prompt = f"""You are a senior business analyst preparing an executive summary for C-level stakeholders.

Dataset Analysis:
{analysis}

Generate a comprehensive executive summary with the following sections:

1. BUSINESS OVERVIEW (2-3 sentences): High-level summary of the business performance and dataset scope.

2. KEY POSITIVE FINDINGS (3-4 bullet points): Major successes, strong performers, positive trends.

3. AREAS OF CONCERN (2-3 bullet points): Issues, declining trends, underperformers.

4. GROWTH OPPORTUNITIES (3-4 bullet points): Untapped potential, expansion possibilities, optimization areas.

5. BUSINESS RISKS (2-3 bullet points): Threats, vulnerabilities, potential problems.

6. STRATEGIC RECOMMENDATIONS (3-5 bullet points): Specific, actionable steps the business should take.

7. CONCLUSION (2-3 sentences): Overall assessment and forward-looking statement.

Use specific numbers and percentages from the data. Be professional, concise, and actionable."""

        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a senior business analyst with expertise in data-driven decision making."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        # Parse the response
        content = response.choices[0].message.content.strip()
        summary = self._parse_ai_response(content)
        
        return summary if summary['overview'] else self._generate_rule_based_summary()
    
    def _parse_ai_response(self, content):
        """Parse AI response into structured summary"""
        summary = {
            'overview': '',
            'positive_findings': [],
            'concerns': [],
            'opportunities': [],
            'risks': [],
            'recommendations': [],
            'conclusion': ''
        }
        
        sections = {
            'overview': ['BUSINESS OVERVIEW', 'OVERVIEW', '1.'],
            'positive_findings': ['POSITIVE FINDINGS', 'KEY POSITIVE', 'SUCCESSES', '2.'],
            'concerns': ['CONCERNS', 'AREAS OF CONCERN', 'ISSUES', '3.'],
            'opportunities': ['OPPORTUNITIES', 'GROWTH OPPORTUNITIES', '4.'],
            'risks': ['RISKS', 'BUSINESS RISKS', '5.'],
            'recommendations': ['RECOMMENDATIONS', 'STRATEGIC RECOMMENDATIONS', '6.'],
            'conclusion': ['CONCLUSION', '7.']
        }
        
        lines = content.split('\n')
        current_section = None
        current_text = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this is a section header
            is_header = False
            for section, keywords in sections.items():
                if any(keyword in line.upper() for keyword in keywords):
                    # Save previous section
                    if current_section and current_text:
                        if current_section in ['overview', 'conclusion']:
                            summary[current_section] = ' '.join(current_text)
                        else:
                            summary[current_section] = current_text.copy()
                    
                    current_section = section
                    current_text = []
                    is_header = True
                    break
            
            if not is_header and current_section:
                # Clean up bullet points
                cleaned = line.strip('- •*123456789.').strip()
                if cleaned:
                    if current_section in ['overview', 'conclusion']:
                        current_text.append(cleaned)
                    else:
                        current_text.append(cleaned)
        
        # Save last section
        if current_section and current_text:
            if current_section in ['overview', 'conclusion']:
                summary[current_section] = ' '.join(current_text)
            else:
                summary[current_section] = current_text.copy()
        
        return summary
    
    def _analyze_data(self):
        """Analyze data for AI context"""
        analysis_parts = []
        
        # Basic info
        analysis_parts.append(f"Dataset: {len(self.df):,} records, {len(self.df.columns)} columns")
        
        # Get numeric columns
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Sales analysis
        sales_col = self.config.get('sales')
        profit_col = self.config.get('profit')
        
        if sales_col and sales_col in self.df.columns:
            total_sales = self.df[sales_col].sum()
            avg_sales = self.df[sales_col].mean()
            analysis_parts.append(f"\nTotal {sales_col}: ${total_sales:,.2f}")
            analysis_parts.append(f"Average {sales_col}: ${avg_sales:,.2f}")
        
        if profit_col and profit_col in self.df.columns:
            total_profit = self.df[profit_col].sum()
            if sales_col and sales_col in self.df.columns:
                margin = (total_profit / self.df[sales_col].sum() * 100) if self.df[sales_col].sum() > 0 else 0
                analysis_parts.append(f"Total {profit_col}: ${total_profit:,.2f}")
                analysis_parts.append(f"Profit Margin: {margin:.1f}%")
        
        # Top performers
        product_col = self.config.get('product')
        if product_col and product_col in self.df.columns and sales_col and sales_col in self.df.columns:
            top_products = self.df.groupby(product_col)[sales_col].sum().nlargest(3)
            analysis_parts.append(f"\nTop 3 by {sales_col}:")
            for prod, val in top_products.items():
                analysis_parts.append(f"- {prod}: ${val:,.2f}")
        
        # Regional performance
        region_col = self.config.get('region')
        if region_col and region_col in self.df.columns and sales_col and sales_col in self.df.columns:
            region_totals = self.df.groupby(region_col)[sales_col].sum().sort_values(ascending=False)
            analysis_parts.append(f"\nBy {region_col}:")
            for reg, val in region_totals.items():
                pct = (val / self.df[sales_col].sum() * 100) if self.df[sales_col].sum() > 0 else 0
                analysis_parts.append(f"- {reg}: ${val:,.2f} ({pct:.1f}%)")
        
        # Trend analysis
        date_col = self.config.get('date')
        if date_col and date_col in self.df.columns and sales_col and sales_col in self.df.columns:
            try:
                df_sorted = self.df.copy()
                df_sorted[date_col] = pd.to_datetime(df_sorted[date_col])
                df_sorted['Period'] = df_sorted[date_col].dt.to_period('M')
                periodic_sales = df_sorted.groupby('Period')[sales_col].sum()
                
                if len(periodic_sales) >= 2:
                    first_half = periodic_sales.iloc[:len(periodic_sales)//2].mean()
                    second_half = periodic_sales.iloc[len(periodic_sales)//2:].mean()
                    change = ((second_half - first_half) / first_half * 100) if first_half > 0 else 0
                    trend = "increasing" if change > 0 else "decreasing"
                    analysis_parts.append(f"\nTrend: {sales_col} {trend} by {abs(change):.1f}%")
            except:
                pass
        
        return '\n'.join(analysis_parts)
    
    def _generate_rule_based_summary(self):
        """Generate summary using rule-based logic"""
        summary = {
            'overview': self._generate_overview(),
            'positive_findings': self._find_positive_findings(),
            'concerns': self._find_concerns(),
            'opportunities': self._find_opportunities(),
            'risks': self._find_risks(),
            'recommendations': self._generate_recommendations(),
            'conclusion': self._generate_conclusion()
        }
        
        return summary
    
    def _generate_overview(self):
        """Generate business overview"""
        sales_col = self.config.get('sales')
        profit_col = self.config.get('profit')
        
        if sales_col and sales_col in self.df.columns:
            total_sales = self.df[sales_col].sum()
            avg_sales = self.df[sales_col].mean()
            
            overview = f"This dataset contains {len(self.df):,} records representing business transactions. "
            overview += f"Total {sales_col} of ${total_sales:,.2f} with an average of ${avg_sales:,.2f} per record. "
            
            if profit_col and profit_col in self.df.columns:
                total_profit = self.df[profit_col].sum()
                margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
                overview += f"Overall profit margin stands at {margin:.1f}%, generating ${total_profit:,.2f} in total profit."
            
            return overview
        
        return f"This dataset contains {len(self.df):,} records across {len(self.df.columns)} different attributes, providing comprehensive business intelligence data for analysis."
    
    def _find_positive_findings(self):
        """Identify positive business findings"""
        findings = []
        
        sales_col = self.config.get('sales')
        profit_col = self.config.get('profit')
        product_col = self.config.get('product')
        region_col = self.config.get('region')
        
        # Top performer
        if product_col and product_col in self.df.columns and sales_col and sales_col in self.df.columns:
            try:
                grouped = self.df.groupby(product_col)[sales_col].sum()
                if len(grouped) > 0:
                    top_product = grouped.idxmax()
                    top_sales = grouped.max()
                    findings.append(f"'{top_product}' is the top performer with ${top_sales:,.2f} in {sales_col}")
            except:
                pass
        
        # Strong margin
        if profit_col and profit_col in self.df.columns and sales_col and sales_col in self.df.columns:
            total_profit = self.df[profit_col].sum()
            total_sales = self.df[sales_col].sum()
            if total_sales > 0:
                margin = (total_profit / total_sales * 100)
                if margin > 15:
                    findings.append(f"Healthy profit margin of {margin:.1f}% indicates strong pricing power and cost management")
        
        # Leading region
        if region_col and region_col in self.df.columns and sales_col and sales_col in self.df.columns:
            try:
                grouped = self.df.groupby(region_col)[sales_col].sum()
                if len(grouped) > 0:
                    top_region = grouped.idxmax()
                    region_sales = grouped.max()
                    total = self.df[sales_col].sum()
                    pct = (region_sales / total * 100) if total > 0 else 0
                    findings.append(f"'{top_region}' region leads with {pct:.1f}% of total {sales_col}")
            except:
                pass
        
        # Growth trend
        date_col = self.config.get('date')
        if date_col and date_col in self.df.columns and sales_col and sales_col in self.df.columns:
            try:
                df_sorted = self.df.copy()
                df_sorted[date_col] = pd.to_datetime(df_sorted[date_col])
                df_sorted['Period'] = df_sorted[date_col].dt.to_period('M')
                periodic_sales = df_sorted.groupby('Period')[sales_col].sum()
                
                if len(periodic_sales) >= 2:
                    first_half = periodic_sales.iloc[:len(periodic_sales)//2].mean()
                    second_half = periodic_sales.iloc[len(periodic_sales)//2:].mean()
                    change = ((second_half - first_half) / first_half * 100) if first_half > 0 else 0
                    if change > 5:
                        findings.append(f"Positive growth trend with {change:.1f}% increase in average {sales_col}")
            except:
                pass
        
        return findings if findings else ["Dataset shows stable business operations with consistent performance metrics"]
    
    def _find_concerns(self):
        """Identify areas of concern"""
        concerns = []
        
        sales_col = self.config.get('sales')
        profit_col = self.config.get('profit')
        product_col = self.config.get('product')
        
        # Low margin
        if profit_col and profit_col in self.df.columns and sales_col and sales_col in self.df.columns:
            total_profit = self.df[profit_col].sum()
            total_sales = self.df[sales_col].sum()
            if total_sales > 0:
                margin = (total_profit / total_sales * 100)
                if margin < 10:
                    concerns.append(f"Low profit margin of {margin:.1f}% suggests need for cost optimization or pricing review")
        
        # Concentration risk
        if product_col and product_col in self.df.columns and sales_col and sales_col in self.df.columns:
            product_sales = self.df.groupby(product_col)[sales_col].sum()
            total = product_sales.sum()
            if len(product_sales) > 0:
                top_share = (product_sales.max() / total * 100) if total > 0 else 0
                if top_share > 40:
                    concerns.append(f"High concentration risk with top {product_col} representing {top_share:.1f}% of {sales_col}")
        
        # Missing data
        missing_pct = (self.df.isnull().sum().sum() / (self.df.shape[0] * self.df.shape[1])) * 100
        if missing_pct > 5:
            concerns.append(f"Data quality concerns with {missing_pct:.1f}% missing values across the dataset")
        
        return concerns if concerns else ["No major concerns identified in current operations"]
    
    def _find_opportunities(self):
        """Identify growth opportunities"""
        opportunities = []
        
        sales_col = self.config.get('sales')
        product_col = self.config.get('product')
        region_col = self.config.get('region')
        category_col = self.config.get('category')
        
        # Underperforming segments
        if region_col and region_col in self.df.columns and sales_col and sales_col in self.df.columns:
            region_sales = self.df.groupby(region_col)[sales_col].sum().sort_values()
            if len(region_sales) > 1:
                bottom_region = region_sales.index[0]
                opportunities.append(f"Potential to increase market share in '{bottom_region}' region through targeted campaigns")
        
        # Product expansion
        if product_col and product_col in self.df.columns:
            product_count = self.df[product_col].nunique()
            opportunities.append(f"Expand product portfolio beyond current {product_count} offerings to capture additional market segments")
        
        # Category optimization
        if category_col and category_col in self.df.columns and sales_col and sales_col in self.df.columns:
            try:
                category_sales = self.df.groupby(category_col)[sales_col].sum()
                if len(category_sales) > 0:
                    top_category = category_sales.idxmax()
                    opportunities.append(f"Focus on high-performing '{top_category}' category for accelerated growth")
            except:
                pass
        
        # Data-driven decisions
        opportunities.append("Leverage data analytics for predictive modeling and customer behavior insights")
        
        return opportunities
    
    def _find_risks(self):
        """Identify business risks"""
        risks = []
        
        sales_col = self.config.get('sales')
        product_col = self.config.get('product')
        
        # Concentration risk
        if product_col and product_col in self.df.columns and sales_col and sales_col in self.df.columns:
            product_sales = self.df.groupby(product_col)[sales_col].sum()
            total = product_sales.sum()
            if len(product_sales) > 0 and total > 0:
                top_share = (product_sales.max() / total * 100)
                if top_share > 30:
                    risks.append(f"Revenue concentration risk with heavy dependence on few key {product_col}s")
        
        # Data quality
        missing_pct = (self.df.isnull().sum().sum() / (self.df.shape[0] * self.df.shape[1])) * 100
        if missing_pct > 10:
            risks.append("Data quality and completeness issues may affect decision-making accuracy")
        
        # Market volatility
        date_col = self.config.get('date')
        if date_col and date_col in self.df.columns and sales_col and sales_col in self.df.columns:
            try:
                df_sorted = self.df.copy()
                df_sorted[date_col] = pd.to_datetime(df_sorted[date_col])
                df_sorted['Period'] = df_sorted[date_col].dt.to_period('M')
                periodic_sales = df_sorted.groupby('Period')[sales_col].sum()
                
                if len(periodic_sales) >= 3:
                    volatility = periodic_sales.std() / periodic_sales.mean() * 100
                    if volatility > 30:
                        risks.append(f"High {sales_col} volatility ({volatility:.1f}%) indicates market or operational instability")
            except:
                pass
        
        return risks if risks else ["No major business risks identified at this time"]
    
    def _generate_recommendations(self):
        """Generate strategic recommendations"""
        recommendations = []
        
        sales_col = self.config.get('sales')
        profit_col = self.config.get('profit')
        product_col = self.config.get('product')
        region_col = self.config.get('region')
        
        # Profitability
        if profit_col and profit_col in self.df.columns and sales_col and sales_col in self.df.columns:
            total_profit = self.df[profit_col].sum()
            total_sales = self.df[sales_col].sum()
            if total_sales > 0:
                margin = (total_profit / total_sales * 100)
                if margin < 15:
                    recommendations.append("Implement cost reduction initiatives and review pricing strategy to improve profit margins")
        
        # Product focus
        if product_col and product_col in self.df.columns and sales_col and sales_col in self.df.columns:
            top_products = self.df.groupby(product_col)[sales_col].sum().nlargest(3)
            recommendations.append(f"Focus marketing and inventory resources on top-performing {product_col}s")
        
        # Geographic expansion
        if region_col and region_col in self.df.columns:
            region_count = self.df[region_col].nunique()
            if region_count < 5:
                recommendations.append("Consider geographic expansion to diversify market presence and reduce regional dependency")
        
        # Data quality
        missing_pct = (self.df.isnull().sum().sum() / (self.df.shape[0] * self.df.shape[1])) * 100
        if missing_pct > 5:
            recommendations.append("Improve data collection processes to ensure complete and accurate business intelligence")
        
        # Analytics
        recommendations.append("Establish regular analytics reviews and KPI monitoring for proactive decision-making")
        
        return recommendations
    
    def _generate_conclusion(self):
        """Generate overall conclusion"""
        sales_col = self.config.get('sales')
        profit_col = self.config.get('profit')
        
        if sales_col and sales_col in self.df.columns:
            total_sales = self.df[sales_col].sum()
            
            conclusion = f"The business demonstrates solid performance with ${total_sales:,.2f} in total {sales_col} across {len(self.df):,} transactions. "
            
            if profit_col and profit_col in self.df.columns:
                total_profit = self.df[profit_col].sum()
                total_sales_val = self.df[sales_col].sum()
                if total_sales_val > 0:
                    margin = (total_profit / total_sales_val * 100)
                    if margin > 15:
                        conclusion += "Strong profitability metrics indicate effective operations. "
                    else:
                        conclusion += "There is room for margin improvement through operational optimization. "
            
            conclusion += "By focusing on identified opportunities and addressing key concerns, the business is well-positioned for sustained growth and market leadership."
            
            return conclusion
        
        return "The data provides valuable insights into business operations. Implementing the recommended strategies will drive improved performance, enhanced profitability, and sustainable competitive advantage in the market."

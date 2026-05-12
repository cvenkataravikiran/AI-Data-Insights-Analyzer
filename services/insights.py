import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class InsightGenerator:
    def __init__(self, df, config=None):
        self.df = df.copy()
        self.config = config or self._auto_detect_columns()
        
        date_col = self.config.get('date')
        if date_col and date_col in self.df.columns:
            try:
                self.df[date_col] = pd.to_datetime(self.df[date_col])
            except:
                pass
        
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
    
    def generate_insights(self):
        """Generate insights using OpenAI or fallback to rule-based"""
        if self.openai_client:
            try:
                return self._generate_ai_insights()
            except Exception as e:
                print(f"OpenAI error: {e}. Falling back to rule-based insights.")
                return self._generate_rule_based_insights()
        else:
            return self._generate_rule_based_insights()
    
    def _generate_ai_insights(self):
        """Generate insights using OpenAI API"""
        # Prepare data summary for AI
        summary = self._prepare_data_summary()
        
        prompt = f"""You are a data analyst. Analyze this business data and provide 5 concise, actionable insights.

Data Summary:
{summary}

Provide exactly 5 insights in this format:
1. [Insight about top performer]
2. [Insight about regional performance]
3. [Insight about trends]
4. [Insight about profitability]
5. [Insight about categories/products]

Keep each insight to one sentence. Be specific with numbers and percentages."""

        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional business data analyst providing concise insights."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        # Parse the response
        insights_text = response.choices[0].message.content.strip()
        insights = []
        
        for line in insights_text.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                # Remove numbering
                insight = line.split('.', 1)[-1].strip() if '.' in line else line.strip('- •')
                if insight:
                    insights.append(insight)
        
        return insights[:5] if insights else self._generate_rule_based_insights()
    
    def _prepare_data_summary(self):
        """Prepare a concise data summary for AI"""
        summary_parts = []
        
        sales_col = self.config.get('sales')
        profit_col = self.config.get('profit')
        product_col = self.config.get('product')
        region_col = self.config.get('region')
        category_col = self.config.get('category')
        date_col = self.config.get('date')
        
        # Total metrics
        if sales_col and sales_col in self.df.columns:
            total_sales = self.df[sales_col].sum()
            summary_parts.append(f"Total Sales: ${total_sales:,.2f}")
        
        if profit_col and profit_col in self.df.columns:
            total_profit = self.df[profit_col].sum()
            summary_parts.append(f"Total Profit: ${total_profit:,.2f}")
            if sales_col and sales_col in self.df.columns:
                margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
                summary_parts.append(f"Profit Margin: {margin:.1f}%")
        
        # Top performers
        if product_col and product_col in self.df.columns and sales_col:
            top_products = self.df.groupby(product_col)[sales_col].sum().nlargest(3)
            summary_parts.append(f"Top 3 Products: {', '.join([f'{p} (${s:,.0f})' for p, s in top_products.items()])}")
        
        if region_col and region_col in self.df.columns and sales_col:
            region_sales = self.df.groupby(region_col)[sales_col].sum().sort_values(ascending=False)
            summary_parts.append(f"Regions: {', '.join([f'{r} (${s:,.0f})' for r, s in region_sales.items()])}")
        
        if category_col and category_col in self.df.columns and sales_col:
            category_sales = self.df.groupby(category_col)[sales_col].sum().nlargest(3)
            summary_parts.append(f"Top Categories: {', '.join([f'{c} (${s:,.0f})' for c, s in category_sales.items()])}")
        
        # Trend
        if date_col and date_col in self.df.columns and sales_col:
            try:
                df_sorted = self.df.sort_values(date_col)
                df_sorted['YearMonth'] = pd.to_datetime(df_sorted[date_col]).dt.to_period('M')
                monthly_sales = df_sorted.groupby('YearMonth')[sales_col].sum()
                if len(monthly_sales) >= 2:
                    first_half = monthly_sales.iloc[:len(monthly_sales)//2].mean()
                    second_half = monthly_sales.iloc[len(monthly_sales)//2:].mean()
                    change = ((second_half - first_half) / first_half * 100) if first_half > 0 else 0
                    trend = "increasing" if change > 0 else "decreasing"
                    summary_parts.append(f"Trend: {trend} by {abs(change):.1f}%")
            except:
                pass
        
        return "\n".join(summary_parts)
    
    def _generate_rule_based_insights(self):
        """Generate insights using rule-based logic (fallback)"""
        insights = []
        
        insight = self._get_top_performer_insight()
        if insight:
            insights.append(insight)
        
        insight = self._get_regional_insight()
        if insight:
            insights.append(insight)
        
        insight = self._get_trend_insight()
        if insight:
            insights.append(insight)
        
        insight = self._get_profitability_insight()
        if insight:
            insights.append(insight)
        
        insight = self._get_category_insight()
        if insight:
            insights.append(insight)
        
        return insights
    
    def _get_top_performer_insight(self):
        product_col = self.config.get('product')
        sales_col = self.config.get('sales')
        
        if not product_col or product_col not in self.df.columns:
            return None
        if not sales_col or sales_col not in self.df.columns:
            return None
        
        try:
            top_product = self.df.groupby(product_col)[sales_col].sum().idxmax()
            top_sales = self.df.groupby(product_col)[sales_col].sum().max()
            
            return f"The product '{top_product}' generated the highest revenue of ${top_sales:,.2f}, making it the top performer."
        except:
            return None
    
    def _get_regional_insight(self):
        region_col = self.config.get('region')
        sales_col = self.config.get('sales')
        
        if not region_col or region_col not in self.df.columns:
            return None
        if not sales_col or sales_col not in self.df.columns:
            return None
        
        try:
            region_sales = self.df.groupby(region_col)[sales_col].sum().sort_values(ascending=False)
            top_region = region_sales.index[0]
            top_sales = region_sales.iloc[0]
            
            total_sales = self.df[sales_col].sum()
            percentage = (top_sales / total_sales) * 100
            
            return f"The {top_region} region leads with ${top_sales:,.2f} in sales, accounting for {percentage:.1f}% of total revenue."
        except:
            return None
    
    def _get_trend_insight(self):
        date_col = self.config.get('date')
        sales_col = self.config.get('sales')
        
        if not date_col or date_col not in self.df.columns:
            return None
        if not sales_col or sales_col not in self.df.columns:
            return None
        
        try:
            df_sorted = self.df.sort_values(date_col)
            df_sorted['YearMonth'] = pd.to_datetime(df_sorted[date_col]).dt.to_period('M')
            
            monthly_sales = df_sorted.groupby('YearMonth')[sales_col].sum()
            
            if len(monthly_sales) < 2:
                return None
            
            first_half = monthly_sales.iloc[:len(monthly_sales)//2].mean()
            second_half = monthly_sales.iloc[len(monthly_sales)//2:].mean()
            
            if second_half > first_half:
                change = ((second_half - first_half) / first_half) * 100
                return f"Sales showed an upward trend with a {change:.1f}% increase in the latter half of the period."
            else:
                change = ((first_half - second_half) / first_half) * 100
                return f"Sales declined by {change:.1f}% in the latter half compared to the first half of the period."
        except:
            return None
    
    def _get_profitability_insight(self):
        sales_col = self.config.get('sales')
        profit_col = self.config.get('profit')
        
        if not sales_col or sales_col not in self.df.columns:
            return None
        if not profit_col or profit_col not in self.df.columns:
            return None
        
        try:
            total_sales = self.df[sales_col].sum()
            total_profit = self.df[profit_col].sum()
            
            if total_sales == 0:
                return None
            
            profit_margin = (total_profit / total_sales) * 100
            
            if profit_margin > 20:
                return f"The business maintains a healthy profit margin of {profit_margin:.1f}%, indicating strong profitability."
            elif profit_margin > 10:
                return f"The profit margin stands at {profit_margin:.1f}%, showing moderate profitability with room for improvement."
            else:
                return f"The profit margin is {profit_margin:.1f}%, suggesting the need for cost optimization strategies."
        except:
            return None
    
    def _get_category_insight(self):
        category_col = self.config.get('category')
        sales_col = self.config.get('sales')
        
        if not category_col or category_col not in self.df.columns:
            return None
        if not sales_col or sales_col not in self.df.columns:
            return None
        
        try:
            category_sales = self.df.groupby(category_col)[sales_col].sum().sort_values(ascending=False)
            
            if len(category_sales) < 2:
                return None
            
            top_category = category_sales.index[0]
            second_category = category_sales.index[1]
            
            top_sales = category_sales.iloc[0]
            second_sales = category_sales.iloc[1]
            
            difference = ((top_sales - second_sales) / second_sales) * 100
            
            return f"The '{top_category}' category outperforms '{second_category}' by {difference:.1f}%, indicating strong customer preference."
        except:
            return None

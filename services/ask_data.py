"""
Ask Your Data - Conversational Analytics Agent
Natural language interface for dataset queries
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class AskDataAgent:
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
    
    def answer_question(self, question):
        """Answer natural language questions about the data"""
        if self.openai_client:
            try:
                return self._answer_with_ai(question)
            except Exception as e:
                print(f"OpenAI error: {e}. Falling back to rule-based answers.")
                return self._answer_with_rules(question)
        else:
            return self._answer_with_rules(question)
    
    def _answer_with_ai(self, question):
        """Use AI to answer questions"""
        # Get data context
        context = self._get_data_context()
        
        prompt = f"""You are a data analyst. Answer the following question about the dataset using the provided context.

Dataset Context:
{context}

Question: {question}

Provide a clear, specific answer using numbers and insights from the data. Be concise and professional."""

        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional data analyst providing insights from business data."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        answer_text = response.choices[0].message.content.strip()
        
        # Try to generate supporting visualization
        chart = self._generate_chart_for_question(question)
        supporting_data = self._get_supporting_data(question)
        
        return {
            'answer': answer_text,
            'data': supporting_data,
            'chart': chart
        }
    
    def _answer_with_rules(self, question):
        """Answer using rule-based pattern matching"""
        question_lower = question.lower()
        
        # Top performers
        if any(word in question_lower for word in ['top', 'best', 'highest', 'leading']):
            return self._answer_top_performers(question_lower)
        
        # Averages
        elif any(word in question_lower for word in ['average', 'mean', 'avg']):
            return self._answer_average(question_lower)
        
        # Totals
        elif any(word in question_lower for word in ['total', 'sum', 'overall']):
            return self._answer_total(question_lower)
        
        # Trends
        elif any(word in question_lower for word in ['trend', 'over time', 'growth', 'decline']):
            return self._answer_trend(question_lower)
        
        # Comparison
        elif any(word in question_lower for word in ['compare', 'difference', 'vs', 'versus']):
            return self._answer_comparison(question_lower)
        
        # Correlation
        elif any(word in question_lower for word in ['correlate', 'relationship', 'connection']):
            return self._answer_correlation(question_lower)
        
        # Percentage/Share
        elif any(word in question_lower for word in ['percentage', 'percent', 'share', '%']):
            return self._answer_percentage(question_lower)
        
        # Anomalies
        elif any(word in question_lower for word in ['anomaly', 'outlier', 'unusual', 'strange']):
            return self._answer_anomalies(question_lower)
        
        else:
            return self._answer_general(question_lower)
    
    def _answer_top_performers(self, question):
        """Answer questions about top performers"""
        sales_col = self.config.get('sales')
        product_col = self.config.get('product')
        region_col = self.config.get('region')
        category_col = self.config.get('category')
        
        # Determine what to analyze
        if 'region' in question:
            if region_col and region_col in self.df.columns and sales_col and sales_col in self.df.columns:
                try:
                    grouped = self.df.groupby(region_col)[sales_col].sum()
                    if len(grouped) > 0:
                        top_region = grouped.idxmax()
                        top_sales = grouped.max()
                        total = self.df[sales_col].sum()
                        pct = (top_sales / total * 100) if total > 0 else 0
                        
                        # Create chart
                        region_data = grouped.reset_index()
                        region_data.columns = ['Region', 'Sales']
                        fig = px.bar(region_data, x='Region', y='Sales', title='Sales by Region')
                        
                        return {
                            'answer': f"The '{top_region}' region generated the highest revenue of ${top_sales:,.2f}, accounting for {pct:.1f}% of total sales.",
                            'data': region_data,
                            'chart': fig
                        }
                except:
                    pass
        
        elif 'product' in question:
            if product_col and product_col in self.df.columns and sales_col and sales_col in self.df.columns:
                top_products = self.df.groupby(product_col)[sales_col].sum().nlargest(5).reset_index()
                top_products.columns = ['Product', 'Sales']
                top_product = top_products.iloc[0]['Product']
                top_sales = top_products.iloc[0]['Sales']
                
                fig = px.bar(top_products, x='Sales', y='Product', orientation='h',
                           title='Top 5 Products by Sales')
                
                return {
                    'answer': f"The top performing product is '{top_product}' with ${top_sales:,.2f} in sales. The top 5 products are shown in the data table below.",
                    'data': top_products,
                    'chart': fig
                }
        
        elif 'category' in question:
            if category_col and category_col in self.df.columns and sales_col and sales_col in self.df.columns:
                try:
                    grouped = self.df.groupby(category_col)[sales_col].sum()
                    if len(grouped) > 0:
                        top_category = grouped.idxmax()
                        top_sales = grouped.max()
                        
                        category_data = grouped.reset_index()
                        category_data.columns = ['Category', 'Sales']
                        fig = px.pie(category_data, values='Sales', names='Category', 
                                   title='Sales Distribution by Category')
                        
                        return {
                            'answer': f"The '{top_category}' category leads with ${top_sales:,.2f} in sales.",
                            'data': category_data,
                            'chart': fig
                        }
                except:
                    pass
        
        # Default to product
        if product_col and product_col in self.df.columns and sales_col and sales_col in self.df.columns:
            try:
                grouped = self.df.groupby(product_col)[sales_col].sum()
                if len(grouped) > 0:
                    top_product = grouped.idxmax()
                    top_sales = grouped.max()
                    
                    return {
                        'answer': f"The top performer is '{top_product}' with ${top_sales:,.2f} in sales.",
                        'data': None,
                        'chart': None
                    }
            except:
                pass
        
        return {
            'answer': "Unable to determine top performers with the available data columns.",
            'data': None,
            'chart': None
        }
    
    def _answer_average(self, question):
        """Answer questions about averages"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_cols:
            return {
                'answer': "No numeric columns found to calculate averages.",
                'data': None,
                'chart': None
            }
        
        # Find relevant column
        for col in numeric_cols:
            if col.lower() in question:
                avg = self.df[col].mean()
                median = self.df[col].median()
                std = self.df[col].std()
                
                return {
                    'answer': f"The average {col} is ${avg:,.2f}. The median is ${median:,.2f}, with a standard deviation of ${std:,.2f}.",
                    'data': pd.DataFrame({
                        'Metric': ['Mean', 'Median', 'Std Dev', 'Min', 'Max'],
                        'Value': [avg, median, std, self.df[col].min(), self.df[col].max()]
                    }),
                    'chart': None
                }
        
        # Default to first numeric column
        col = numeric_cols[0]
        avg = self.df[col].mean()
        return {
            'answer': f"The average {col} is ${avg:,.2f}.",
            'data': None,
            'chart': None
        }
    
    def _answer_total(self, question):
        """Answer questions about totals"""
        sales_col = self.config.get('sales')
        profit_col = self.config.get('profit')
        
        if sales_col and sales_col in self.df.columns:
            total_sales = self.df[sales_col].sum()
            answer = f"Total {sales_col} is ${total_sales:,.2f} across {len(self.df):,} records."
            
            if profit_col and profit_col in self.df.columns:
                total_profit = self.df[profit_col].sum()
                margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
                answer += f" Total {profit_col} is ${total_profit:,.2f}, representing a {margin:.1f}% profit margin."
            
            return {
                'answer': answer,
                'data': None,
                'chart': None
            }
        
        return {
            'answer': f"The dataset contains {len(self.df):,} total records across {len(self.df.columns)} columns.",
            'data': None,
            'chart': None
        }
    
    def _answer_trend(self, question):
        """Answer questions about trends"""
        date_col = self.config.get('date')
        sales_col = self.config.get('sales')
        
        if not date_col or date_col not in self.df.columns:
            return {
                'answer': "No date column found to analyze trends over time.",
                'data': None,
                'chart': None
            }
        
        if not sales_col or sales_col not in self.df.columns:
            return {
                'answer': "No numeric column found to analyze trends.",
                'data': None,
                'chart': None
            }
        
        try:
            df_sorted = self.df.copy()
            df_sorted[date_col] = pd.to_datetime(df_sorted[date_col])
            df_sorted['Period'] = df_sorted[date_col].dt.to_period('M')
            
            trend_data = df_sorted.groupby('Period')[sales_col].sum().reset_index()
            trend_data['Period'] = trend_data['Period'].astype(str)
            trend_data.columns = ['Period', 'Sales']
            
            # Calculate trend
            if len(trend_data) >= 2:
                first_half = trend_data['Sales'].iloc[:len(trend_data)//2].mean()
                second_half = trend_data['Sales'].iloc[len(trend_data)//2:].mean()
                change = ((second_half - first_half) / first_half * 100) if first_half > 0 else 0
                
                if change > 5:
                    trend_desc = f"showing a positive growth trend of {change:.1f}%"
                elif change < -5:
                    trend_desc = f"showing a declining trend of {abs(change):.1f}%"
                else:
                    trend_desc = "remaining relatively stable"
                
                fig = px.line(trend_data, x='Period', y='Sales', 
                            title=f'{sales_col} Trend Over Time',
                            markers=True)
                
                return {
                    'answer': f"The {sales_col} trend over time is {trend_desc}. The average {sales_col} increased from ${first_half:,.2f} in the first half to ${second_half:,.2f} in the second half of the period.",
                    'data': trend_data,
                    'chart': fig
                }
        except:
            pass
        
        return {
            'answer': "Unable to analyze trend with the available data.",
            'data': None,
            'chart': None
        }
    
    def _answer_comparison(self, question):
        """Answer comparison questions"""
        region_col = self.config.get('region')
        category_col = self.config.get('category')
        sales_col = self.config.get('sales')
        
        if region_col and region_col in self.df.columns and sales_col and sales_col in self.df.columns:
            region_data = self.df.groupby(region_col)[sales_col].sum().reset_index()
            region_data.columns = ['Region', 'Sales']
            region_data = region_data.sort_values('Sales', ascending=False)
            
            if len(region_data) >= 2:
                top = region_data.iloc[0]
                bottom = region_data.iloc[-1]
                diff = top['Sales'] - bottom['Sales']
                diff_pct = (diff / bottom['Sales'] * 100) if bottom['Sales'] > 0 else 0
                
                fig = px.bar(region_data, x='Region', y='Sales', 
                           title='Regional Sales Comparison')
                
                return {
                    'answer': f"Comparing regions: '{top['Region']}' leads with ${top['Sales']:,.2f}, while '{bottom['Region']}' has ${bottom['Sales']:,.2f}. That's a difference of ${diff:,.2f} ({diff_pct:.1f}%).",
                    'data': region_data,
                    'chart': fig
                }
        
        return {
            'answer': "Not enough categorical data to make comparisons.",
            'data': None,
            'chart': None
        }
    
    def _answer_correlation(self, question):
        """Answer correlation questions"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) < 2:
            return {
                'answer': "Need at least 2 numeric columns to analyze correlations.",
                'data': None,
                'chart': None
            }
        
        corr_matrix = self.df[numeric_cols].corr()
        
        # Find strongest correlations
        correlations = []
        for i in range(len(numeric_cols)):
            for j in range(i+1, len(numeric_cols)):
                correlations.append({
                    'Variable 1': numeric_cols[i],
                    'Variable 2': numeric_cols[j],
                    'Correlation': corr_matrix.iloc[i, j]
                })
        
        corr_df = pd.DataFrame(correlations).sort_values('Correlation', key=abs, ascending=False)
        
        if len(corr_df) > 0:
            strongest = corr_df.iloc[0]
            corr_val = strongest['Correlation']
            
            if abs(corr_val) > 0.7:
                strength = "strong"
            elif abs(corr_val) > 0.4:
                strength = "moderate"
            else:
                strength = "weak"
            
            direction = "positive" if corr_val > 0 else "negative"
            
            return {
                'answer': f"There is a {strength} {direction} correlation ({corr_val:.2f}) between {strongest['Variable 1']} and {strongest['Variable 2']}.",
                'data': corr_df.head(5),
                'chart': None
            }
        
        return {
            'answer': "Unable to calculate correlations with available data.",
            'data': None,
            'chart': None
        }
    
    def _answer_percentage(self, question):
        """Answer percentage questions"""
        sales_col = self.config.get('sales')
        category_col = self.config.get('category')
        product_col = self.config.get('product')
        region_col = self.config.get('region')
        
        if category_col and category_col in self.df.columns and sales_col and sales_col in self.df.columns:
            try:
                category_sales = self.df.groupby(category_col)[sales_col].sum()
                total = category_sales.sum()
                
                if total > 0 and len(category_sales) > 0:
                    top_category = category_sales.idxmax()
                    top_pct = (category_sales.max() / total * 100)
                    
                    pct_data = pd.DataFrame({
                        'Category': category_sales.index,
                        'Sales': category_sales.values,
                        'Percentage': (category_sales.values / total * 100).round(2)
                    })
                    
                    fig = px.pie(pct_data, values='Sales', names='Category',
                               title='Sales Distribution by Category')
                    
                    return {
                        'answer': f"The '{top_category}' category accounts for {top_pct:.1f}% of total sales.",
                        'data': pct_data,
                        'chart': fig
                    }
            except:
                pass
        
        return {
            'answer': "Unable to calculate percentages with available data.",
            'data': None,
            'chart': None
        }
    
    def _answer_anomalies(self, question):
        """Answer questions about anomalies"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_cols:
            return {
                'answer': "No numeric columns found to detect anomalies.",
                'data': None,
                'chart': None
            }
        
        col = numeric_cols[0]
        Q1 = self.df[col].quantile(0.25)
        Q3 = self.df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
        
        if len(outliers) > 0:
            outlier_pct = (len(outliers) / len(self.df)) * 100
            return {
                'answer': f"Found {len(outliers)} anomalies ({outlier_pct:.1f}% of data) in {col}. Values outside the range ${lower_bound:,.2f} to ${upper_bound:,.2f} are considered outliers.",
                'data': outliers.head(10),
                'chart': None
            }
        
        return {
            'answer': f"No significant anomalies detected in {col}. All values fall within expected ranges.",
            'data': None,
            'chart': None
        }
    
    def _answer_general(self, question):
        """General fallback answer"""
        return {
            'answer': f"Based on the dataset of {len(self.df):,} records with {len(self.df.columns)} columns, I can provide insights about sales, products, regions, trends, and more. Try asking about top performers, averages, totals, or trends.",
            'data': None,
            'chart': None
        }
    
    def _get_data_context(self):
        """Get data context for AI"""
        context_parts = []
        
        context_parts.append(f"Dataset: {len(self.df):,} records, {len(self.df.columns)} columns")
        context_parts.append(f"Columns: {', '.join(self.df.columns.tolist())}")
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            context_parts.append(f"\nNumeric columns: {', '.join(numeric_cols)}")
            for col in numeric_cols[:3]:
                context_parts.append(f"{col}: Total=${self.df[col].sum():,.2f}, Avg=${self.df[col].mean():,.2f}")
        
        return '\n'.join(context_parts)
    
    def _get_supporting_data(self, question):
        """Get supporting data for question"""
        # This is a placeholder - would need more sophisticated logic
        return None
    
    def _generate_chart_for_question(self, question):
        """Generate relevant chart for question"""
        # This is a placeholder - would need more sophisticated logic
        return None

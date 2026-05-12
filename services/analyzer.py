import pandas as pd
import numpy as np

class DataAnalyzer:
    def __init__(self, df, config=None):
        self.df = df.copy()
        self.config = config or self._auto_detect_columns()
        
        if self.config.get('date') and self.config['date'] in self.df.columns:
            try:
                self.df[self.config['date']] = pd.to_datetime(self.df[self.config['date']])
            except:
                pass
    
    def _auto_detect_columns(self):
        """Auto-detect column mappings"""
        config = {}
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) >= 1:
            config['sales'] = numeric_cols[0]
        if len(numeric_cols) >= 2:
            config['profit'] = numeric_cols[1]
        if len(numeric_cols) >= 3:
            config['quantity'] = numeric_cols[2]
        
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
    
    def get_summary_stats(self):
        sales_col = self.config.get('sales')
        profit_col = self.config.get('profit')
        quantity_col = self.config.get('quantity')
        
        if not sales_col:
            return self._get_basic_stats()
        
        total_sales = self.df[sales_col].sum() if sales_col in self.df.columns else 0
        total_profit = self.df[profit_col].sum() if profit_col and profit_col in self.df.columns else 0
        avg_sales = self.df[sales_col].mean() if sales_col in self.df.columns else 0
        total_orders = len(self.df)
        total_quantity = self.df[quantity_col].sum() if quantity_col and quantity_col in self.df.columns else 0
        
        profit_margin = (total_profit / total_sales * 100) if total_sales > 0 and total_profit else 0
        growth_rate = self._calculate_growth_rate()
        
        return {
            'total_sales': total_sales,
            'total_profit': total_profit,
            'avg_sales': avg_sales,
            'total_orders': total_orders,
            'total_quantity': total_quantity,
            'profit_margin': profit_margin,
            'growth_rate': growth_rate
        }
    
    def _get_basic_stats(self):
        """Get basic stats when standard columns not available"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return {
                'total_sales': 0,
                'total_profit': 0,
                'avg_sales': 0,
                'total_orders': len(self.df),
                'total_quantity': 0,
                'profit_margin': 0,
                'growth_rate': 0
            }
        
        first_col = numeric_cols[0]
        return {
            'total_sales': self.df[first_col].sum(),
            'total_profit': 0,
            'avg_sales': self.df[first_col].mean(),
            'total_orders': len(self.df),
            'total_quantity': 0,
            'profit_margin': 0,
            'growth_rate': 0
        }
    
    def _calculate_growth_rate(self):
        date_col = self.config.get('date')
        sales_col = self.config.get('sales')
        
        if not date_col or date_col not in self.df.columns:
            return 0
        if not sales_col or sales_col not in self.df.columns:
            return 0
        
        try:
            df_sorted = self.df.sort_values(date_col)
            df_sorted['YearMonth'] = pd.to_datetime(df_sorted[date_col]).dt.to_period('M')
            monthly_sales = df_sorted.groupby('YearMonth')[sales_col].sum()
            
            if len(monthly_sales) < 2:
                return 0
            
            first_month = monthly_sales.iloc[0]
            last_month = monthly_sales.iloc[-1]
            
            if first_month == 0:
                return 0
            
            growth = ((last_month - first_month) / first_month) * 100
            return growth
        except:
            return 0
    
    def get_top_products(self, n=5):
        product_col = self.config.get('product')
        sales_col = self.config.get('sales')
        profit_col = self.config.get('profit')
        
        if not product_col or product_col not in self.df.columns:
            return pd.DataFrame()
        if not sales_col or sales_col not in self.df.columns:
            return pd.DataFrame()
        
        agg_dict = {sales_col: 'sum'}
        if profit_col and profit_col in self.df.columns:
            agg_dict[profit_col] = 'sum'
        
        product_sales = self.df.groupby(product_col).agg(agg_dict).reset_index()
        product_sales.columns = ['Product', 'Sales'] + (['Profit'] if profit_col else [])
        product_sales = product_sales.sort_values('Sales', ascending=False).head(n)
        
        return product_sales
    
    def get_top_product(self):
        product_col = self.config.get('product')
        sales_col = self.config.get('sales')
        
        if not product_col or product_col not in self.df.columns:
            return "N/A"
        if not sales_col or sales_col not in self.df.columns:
            return "N/A"
        
        try:
            top = self.df.groupby(product_col)[sales_col].sum().idxmax()
            return top
        except:
            return "N/A"
    
    def get_region_performance(self):
        region_col = self.config.get('region')
        sales_col = self.config.get('sales')
        profit_col = self.config.get('profit')
        
        if not region_col or region_col not in self.df.columns:
            return pd.DataFrame()
        if not sales_col or sales_col not in self.df.columns:
            return pd.DataFrame()
        
        agg_dict = {sales_col: 'sum'}
        if profit_col and profit_col in self.df.columns:
            agg_dict[profit_col] = 'sum'
        
        region_stats = self.df.groupby(region_col).agg(agg_dict).reset_index()
        region_stats.columns = ['Region', 'Sales'] + (['Profit'] if profit_col else [])
        
        return region_stats
    
    def get_top_region(self):
        region_col = self.config.get('region')
        sales_col = self.config.get('sales')
        
        if not region_col or region_col not in self.df.columns:
            return "N/A"
        if not sales_col or sales_col not in self.df.columns:
            return "N/A"
        
        try:
            top = self.df.groupby(region_col)[sales_col].sum().idxmax()
            return top
        except:
            return "N/A"
    
    def get_monthly_trend(self):
        date_col = self.config.get('date')
        sales_col = self.config.get('sales')
        profit_col = self.config.get('profit')
        quantity_col = self.config.get('quantity')
        
        if not date_col or date_col not in self.df.columns:
            return pd.DataFrame()
        if not sales_col or sales_col not in self.df.columns:
            return pd.DataFrame()
        
        try:
            df_copy = self.df.copy()
            df_copy['Month'] = pd.to_datetime(df_copy[date_col]).dt.to_period('M').astype(str)
            
            agg_dict = {sales_col: 'sum'}
            if profit_col and profit_col in self.df.columns:
                agg_dict[profit_col] = 'sum'
            if quantity_col and quantity_col in self.df.columns:
                agg_dict[quantity_col] = 'sum'
            
            monthly = df_copy.groupby('Month').agg(agg_dict).reset_index()
            monthly.columns = ['Month', 'Sales'] + (['Profit'] if profit_col else []) + (['Quantity'] if quantity_col else [])
            
            return monthly
        except:
            return pd.DataFrame()
    
    def get_category_performance(self):
        category_col = self.config.get('category')
        sales_col = self.config.get('sales')
        profit_col = self.config.get('profit')
        
        if not category_col or category_col not in self.df.columns:
            return pd.DataFrame()
        if not sales_col or sales_col not in self.df.columns:
            return pd.DataFrame()
        
        agg_dict = {sales_col: 'sum'}
        if profit_col and profit_col in self.df.columns:
            agg_dict[profit_col] = 'sum'
        
        category_stats = self.df.groupby(category_col).agg(agg_dict).reset_index()
        category_stats.columns = ['Category', 'Sales'] + (['Profit'] if profit_col else [])
        category_stats = category_stats.sort_values('Sales', ascending=False)
        
        return category_stats
    
    def get_top_category(self):
        category_col = self.config.get('category')
        sales_col = self.config.get('sales')
        
        if not category_col or category_col not in self.df.columns:
            return "N/A"
        if not sales_col or sales_col not in self.df.columns:
            return "N/A"
        
        try:
            top = self.df.groupby(category_col)[sales_col].sum().idxmax()
            return top
        except:
            return "N/A"
    
    def get_profit_margin_by_product(self):
        product_col = self.config.get('product')
        sales_col = self.config.get('sales')
        profit_col = self.config.get('profit')
        
        if not product_col or product_col not in self.df.columns:
            return pd.DataFrame()
        if not sales_col or sales_col not in self.df.columns:
            return pd.DataFrame()
        
        agg_dict = {sales_col: 'sum'}
        if profit_col and profit_col in self.df.columns:
            agg_dict[profit_col] = 'sum'
        
        product_stats = self.df.groupby(product_col).agg(agg_dict).reset_index()
        product_stats.columns = ['Product', 'Sales'] + (['Profit'] if profit_col else [])
        
        if profit_col:
            product_stats['Profit_Margin'] = (product_stats['Profit'] / product_stats['Sales'] * 100).round(2)
        
        product_stats = product_stats.sort_values('Sales', ascending=False)
        
        return product_stats

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import plotly.graph_objects as go

class SalesForecaster:
    def __init__(self, df, config=None):
        self.df = df.copy()
        self.config = config or self._auto_detect_columns()
        
        date_col = self.config.get('date')
        if date_col and date_col in self.df.columns:
            try:
                self.df[date_col] = pd.to_datetime(self.df[date_col])
            except:
                pass
    
    def _auto_detect_columns(self):
        """Auto-detect column mappings"""
        config = {}
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) >= 1:
            config['sales'] = numeric_cols[0]
        
        for col in self.df.columns:
            col_lower = col.lower()
            if 'date' in col_lower or 'time' in col_lower:
                config['date'] = col
                break
        
        return config
    
    def forecast_sales(self, periods=6):
        date_col = self.config.get('date')
        sales_col = self.config.get('sales')
        
        if not date_col or date_col not in self.df.columns:
            raise ValueError("Date column is required for forecasting. Please ensure your dataset has a date/time column.")
        
        if not sales_col or sales_col not in self.df.columns:
            raise ValueError("Numeric column is required for forecasting.")
        
        df_sorted = self.df.sort_values(date_col)
        df_sorted['YearMonth'] = pd.to_datetime(df_sorted[date_col]).dt.to_period('M')
        
        monthly_sales = df_sorted.groupby('YearMonth')[sales_col].sum().reset_index()
        monthly_sales['Month_Num'] = range(len(monthly_sales))
        
        X = monthly_sales['Month_Num'].values.reshape(-1, 1)
        y = monthly_sales[sales_col].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        y_pred = model.predict(X)
        score = r2_score(y, y_pred)
        
        future_months = np.arange(len(monthly_sales), len(monthly_sales) + periods).reshape(-1, 1)
        future_sales = model.predict(future_months)
        
        last_date = df_sorted[date_col].max()
        try:
            future_dates = pd.date_range(start=last_date, periods=periods+1, freq='ME')[1:]
        except:
            future_dates = pd.date_range(start=last_date, periods=periods+1, freq='M')[1:]
        
        forecast_df = pd.DataFrame({
            'Date': future_dates,
            'Forecasted_Sales': future_sales
        })
        
        fig = self._create_forecast_plot(monthly_sales, forecast_df, y_pred, sales_col)
        
        return forecast_df, score, fig
    
    def _create_forecast_plot(self, historical, forecast, fitted_values, sales_col):
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=historical['YearMonth'].astype(str),
            y=historical[sales_col],
            mode='lines+markers',
            name='Actual Sales',
            line=dict(color='blue', width=2),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=historical['YearMonth'].astype(str),
            y=fitted_values,
            mode='lines',
            name='Fitted Values',
            line=dict(color='green', width=2, dash='dash')
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast['Date'].dt.to_period('M').astype(str),
            y=forecast['Forecasted_Sales'],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='red', width=2),
            marker=dict(size=10, symbol='diamond')
        ))
        
        fig.update_layout(
            title='Sales Forecast using Linear Regression',
            xaxis_title='Month',
            yaxis_title='Sales',
            hovermode='x unified',
            height=500,
            showlegend=True
        )
        
        return fig

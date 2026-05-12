import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self, df):
        self.df = df.copy()
    
    def get_missing_summary(self):
        missing_data = self.df.isnull().sum()
        missing_percent = (missing_data / len(self.df)) * 100
        
        summary = pd.DataFrame({
            'Column': missing_data.index,
            'Missing Count': missing_data.values,
            'Percentage': missing_percent.values
        })
        
        summary = summary[summary['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
        return summary
    
    def clean_data(self, remove_duplicates=True, missing_strategy="Keep as is"):
        df_cleaned = self.df.copy()
        
        if remove_duplicates:
            df_cleaned = df_cleaned.drop_duplicates()
        
        if missing_strategy == "Drop rows":
            df_cleaned = df_cleaned.dropna()
        
        elif missing_strategy == "Fill with mean":
            numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if df_cleaned[col].isnull().any():
                    df_cleaned[col].fillna(df_cleaned[col].mean(), inplace=True)
        
        elif missing_strategy == "Fill with median":
            numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if df_cleaned[col].isnull().any():
                    df_cleaned[col].fillna(df_cleaned[col].median(), inplace=True)
        
        df_cleaned = self._clean_column_names(df_cleaned)
        df_cleaned = self._convert_data_types(df_cleaned)
        
        return df_cleaned
    
    def _clean_column_names(self, df):
        df.columns = df.columns.str.strip()
        return df
    
    def _convert_data_types(self, df):
        if 'Date' in df.columns:
            try:
                df['Date'] = pd.to_datetime(df['Date'])
            except:
                pass
        
        numeric_candidates = ['Sales', 'Profit', 'Quantity', 'Price', 'Cost', 'Revenue']
        for col in numeric_candidates:
            if col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                except:
                    pass
        
        return df
    
    def detect_outliers(self, column):
        if column not in self.df.columns:
            return None
        
        Q1 = self.df[column].quantile(0.25)
        Q3 = self.df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]
        return outliers

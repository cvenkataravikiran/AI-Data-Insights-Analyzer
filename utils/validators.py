import pandas as pd
import numpy as np

def validate_file(uploaded_file):
    if uploaded_file is None:
        return False, "No file uploaded"
    
    max_size = 50 * 1024 * 1024
    if uploaded_file.size > max_size:
        return False, "File size exceeds 50MB limit"
    
    allowed_extensions = ['csv', 'xlsx', 'xls']
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension not in allowed_extensions:
        return False, f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
    
    return True, "File is valid"

def detect_column_types(df):
    """Automatically detect column types in the dataset"""
    column_mapping = {
        'numeric': [],
        'date': [],
        'categorical': []
    }
    
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            column_mapping['numeric'].append(col)
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            column_mapping['date'].append(col)
        else:
            try:
                pd.to_datetime(df[col])
                column_mapping['date'].append(col)
            except:
                column_mapping['categorical'].append(col)
    
    return column_mapping

def get_suggested_columns(df):
    """Suggest which columns to use for analysis"""
    suggestions = {
        'sales': None,
        'profit': None,
        'quantity': None,
        'date': None,
        'product': None,
        'category': None,
        'region': None
    }
    
    for col in df.columns:
        col_lower = col.lower()
        
        if 'sale' in col_lower or 'revenue' in col_lower or 'amount' in col_lower:
            if suggestions['sales'] is None:
                suggestions['sales'] = col
        
        if 'profit' in col_lower or 'margin' in col_lower:
            if suggestions['profit'] is None:
                suggestions['profit'] = col
        
        if 'quantity' in col_lower or 'qty' in col_lower or 'units' in col_lower:
            if suggestions['quantity'] is None:
                suggestions['quantity'] = col
        
        if 'date' in col_lower or 'time' in col_lower or 'day' in col_lower:
            if suggestions['date'] is None:
                suggestions['date'] = col
        
        if 'product' in col_lower or 'item' in col_lower:
            if suggestions['product'] is None:
                suggestions['product'] = col
        
        if 'category' in col_lower or 'type' in col_lower or 'class' in col_lower:
            if suggestions['category'] is None:
                suggestions['category'] = col
        
        if 'region' in col_lower or 'location' in col_lower or 'area' in col_lower or 'city' in col_lower:
            if suggestions['region'] is None:
                suggestions['region'] = col
    
    return suggestions

def check_required_columns(df):
    """Check if dataset has minimum required columns for analysis"""
    column_types = detect_column_types(df)
    
    has_numeric = len(column_types['numeric']) >= 1
    has_categorical = len(column_types['categorical']) >= 1
    
    if not has_numeric:
        return False, ['At least one numeric column required']
    
    return True, []

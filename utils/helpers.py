import pandas as pd
from pathlib import Path

def save_to_excel(df, filename):
    exports_dir = Path("exports")
    exports_dir.mkdir(exist_ok=True)
    
    filepath = exports_dir / filename
    df.to_excel(filepath, index=False)
    
    return filepath

def save_to_csv(df, filename):
    exports_dir = Path("exports")
    exports_dir.mkdir(exist_ok=True)
    
    filepath = exports_dir / filename
    df.to_csv(filepath, index=False)
    
    return filepath

def create_export_folder():
    exports_dir = Path("exports")
    exports_dir.mkdir(exist_ok=True)
    
    datasets_dir = Path("datasets")
    datasets_dir.mkdir(exist_ok=True)
    
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)

def format_currency(value):
    return f"${value:,.2f}"

def format_percentage(value):
    return f"{value:.2f}%"

def format_number(value):
    return f"{value:,}"

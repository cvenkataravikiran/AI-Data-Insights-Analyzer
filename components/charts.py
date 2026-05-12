import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def render_visualizations(df, config=None):
    st.subheader("Interactive Visualizations")
    
    if config is None:
        config = _auto_detect_columns(df)
    
    viz_type = st.selectbox(
        "Select Visualization Type",
        ["Sales Trends", "Distribution Analysis", "Correlation Heatmap", "Regional Performance", "Product Analysis"]
    )
    
    if viz_type == "Sales Trends":
        render_sales_trends(df, config)
    elif viz_type == "Distribution Analysis":
        render_distribution_analysis(df, config)
    elif viz_type == "Correlation Heatmap":
        render_correlation_heatmap(df)
    elif viz_type == "Regional Performance":
        render_regional_performance(df, config)
    elif viz_type == "Product Analysis":
        render_product_analysis(df, config)

def _auto_detect_columns(df):
    """Auto-detect column mappings"""
    config = {}
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) >= 1:
        config['sales'] = numeric_cols[0]
    if len(numeric_cols) >= 2:
        config['profit'] = numeric_cols[1]
    if len(numeric_cols) >= 3:
        config['quantity'] = numeric_cols[2]
    
    for col in df.columns:
        col_lower = col.lower()
        if 'date' in col_lower or 'time' in col_lower:
            config['date'] = col
            break
    
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    if len(categorical_cols) >= 1:
        config['product'] = categorical_cols[0]
    if len(categorical_cols) >= 2:
        config['category'] = categorical_cols[1]
    if len(categorical_cols) >= 3:
        config['region'] = categorical_cols[2]
    
    return config

def render_sales_trends(df, config):
    st.markdown("### 📈 Sales Trends Over Time")
    
    date_col = config.get('date')
    sales_col = config.get('sales')
    profit_col = config.get('profit')
    quantity_col = config.get('quantity')
    
    if not date_col or date_col not in df.columns:
        st.warning("Date column not found. Cannot display trends.")
        return
    
    if not sales_col or sales_col not in df.columns:
        st.warning("Numeric column not found for trend analysis.")
        return
    
    df_copy = df.copy()
    df_copy[date_col] = pd.to_datetime(df_copy[date_col])
    df_copy['YearMonth'] = df_copy[date_col].dt.to_period('M').astype(str)
    
    agg_dict = {sales_col: 'sum'}
    if profit_col and profit_col in df.columns:
        agg_dict[profit_col] = 'sum'
    if quantity_col and quantity_col in df.columns:
        agg_dict[quantity_col] = 'sum'
    
    monthly_sales = df_copy.groupby('YearMonth').agg(agg_dict).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=monthly_sales['YearMonth'],
        y=monthly_sales[sales_col],
        mode='lines+markers',
        name='Sales',
        line=dict(color='royalblue', width=3),
        fill='tonexty'
    ))
    
    fig.update_layout(
        title='Monthly Sales Trend',
        xaxis_title='Month',
        yaxis_title='Sales Amount',
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if profit_col and profit_col in monthly_sales.columns:
            fig = px.line(
                monthly_sales,
                x='YearMonth',
                y=profit_col,
                title='Monthly Profit Trend',
                markers=True
            )
            fig.update_traces(line_color='green')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if quantity_col and quantity_col in monthly_sales.columns:
            fig = px.bar(
                monthly_sales,
                x='YearMonth',
                y=quantity_col,
                title='Monthly Quantity Sold',
                color=quantity_col,
                color_continuous_scale='Oranges'
            )
            st.plotly_chart(fig, use_container_width=True)

def render_distribution_analysis(df, config):
    st.markdown("### 📊 Distribution Analysis")
    
    sales_col = config.get('sales')
    profit_col = config.get('profit')
    region_col = config.get('region')
    
    if not sales_col or sales_col not in df.columns:
        st.warning("Numeric column not found for distribution analysis.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.histogram(
            df,
            x=sales_col,
            nbins=30,
            title=f'{sales_col} Distribution',
            color_discrete_sequence=['steelblue']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if profit_col and profit_col in df.columns:
            fig = px.histogram(
                df,
                x=profit_col,
                nbins=30,
                title=f'{profit_col} Distribution',
                color_discrete_sequence=['seagreen']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.box(
            df,
            y=sales_col,
            title=f'{sales_col} Box Plot',
            color_discrete_sequence=['#636EFA']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if region_col and region_col in df.columns:
            fig = px.box(
                df,
                x=region_col,
                y=sales_col,
                title=f'{sales_col} Distribution by {region_col}',
                color=region_col
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

def render_correlation_heatmap(df):
    st.markdown("### 🔥 Correlation Heatmap")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) < 2:
        st.warning("Not enough numeric columns for correlation analysis")
        return
    
    corr_matrix = df[numeric_cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title='Correlation Matrix',
        height=600,
        width=800
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("#### Key Correlations")
    
    corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_pairs.append({
                'Variable 1': corr_matrix.columns[i],
                'Variable 2': corr_matrix.columns[j],
                'Correlation': corr_matrix.iloc[i, j]
            })
    
    corr_df = pd.DataFrame(corr_pairs).sort_values('Correlation', ascending=False)
    st.dataframe(corr_df.head(10), use_container_width=True)

def render_regional_performance(df, config):
    st.markdown("### 🌍 Regional Performance Analysis")
    
    region_col = config.get('region')
    sales_col = config.get('sales')
    profit_col = config.get('profit')
    quantity_col = config.get('quantity')
    
    if not region_col or region_col not in df.columns:
        st.warning("Regional column not found in dataset.")
        return
    
    if not sales_col or sales_col not in df.columns:
        st.warning("Numeric column not found for analysis.")
        return
    
    agg_dict = {sales_col: 'sum'}
    if profit_col and profit_col in df.columns:
        agg_dict[profit_col] = 'sum'
    if quantity_col and quantity_col in df.columns:
        agg_dict[quantity_col] = 'sum'
    
    region_stats = df.groupby(region_col).agg(agg_dict).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            region_stats,
            x=region_col,
            y=sales_col,
            title=f'Total {sales_col} by {region_col}',
            color=sales_col,
            color_continuous_scale='Blues',
            text=sales_col
        )
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if profit_col and profit_col in region_stats.columns:
            fig = px.pie(
                region_stats,
                values=profit_col,
                names=region_col,
                title=f'{profit_col} Share by {region_col}',
                hole=0.4
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    if profit_col and profit_col in region_stats.columns:
        # Use absolute values for size to avoid negative values
        region_stats_plot = region_stats.copy()
        size_col = quantity_col if quantity_col and quantity_col in region_stats.columns else sales_col
        region_stats_plot['Size'] = region_stats_plot[size_col].abs()
        
        fig = px.scatter(
            region_stats_plot,
            x=sales_col,
            y=profit_col,
            size='Size',
            color=region_col,
            title=f'{sales_col} vs {profit_col} by {region_col}',
            text=region_col,
            size_max=60
        )
        fig.update_traces(textposition='top center')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

def render_product_analysis(df, config):
    st.markdown("### 🛍️ Product Performance Analysis")
    
    product_col = config.get('product')
    sales_col = config.get('sales')
    profit_col = config.get('profit')
    quantity_col = config.get('quantity')
    
    if not product_col or product_col not in df.columns:
        st.warning("Product column not found in dataset.")
        return
    
    if not sales_col or sales_col not in df.columns:
        st.warning("Numeric column not found for analysis.")
        return
    
    top_n = st.slider("Select number of top products", 5, 20, 10)
    
    agg_dict = {sales_col: 'sum'}
    if profit_col and profit_col in df.columns:
        agg_dict[profit_col] = 'sum'
    if quantity_col and quantity_col in df.columns:
        agg_dict[quantity_col] = 'sum'
    
    product_stats = df.groupby(product_col).agg(agg_dict).reset_index()
    product_stats = product_stats.sort_values(sales_col, ascending=False).head(top_n)
    
    fig = px.bar(
        product_stats,
        y=product_col,
        x=sales_col,
        orientation='h',
        title=f'Top {top_n} Products by {sales_col}',
        color=profit_col if profit_col and profit_col in product_stats.columns else sales_col,
        color_continuous_scale='Viridis',
        text=sales_col
    )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.treemap(
            product_stats,
            path=[product_col],
            values=sales_col,
            title=f'Product {sales_col} Treemap',
            color=profit_col if profit_col and profit_col in product_stats.columns else sales_col,
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if profit_col and profit_col in product_stats.columns:
            product_stats['Profit_Margin'] = (product_stats[profit_col] / product_stats[sales_col] * 100).round(2)
            size_col = quantity_col if quantity_col and quantity_col in product_stats.columns else profit_col
            
            # Use absolute values for size to avoid negative values
            product_stats['Size'] = product_stats[size_col].abs()
            
            fig = px.scatter(
                product_stats,
                x=sales_col,
                y='Profit_Margin',
                size='Size',
                color=product_col,
                title=f'{sales_col} vs Profit Margin',
                hover_data=[product_col]
            )
            fig.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

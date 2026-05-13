import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render_dashboard(analyzer):
    st.markdown("### 📊 Performance Overview")
    st.markdown("")
    
    config = analyzer.config
    product_label = config.get('product', 'Item')
    region_label = config.get('region', 'Group')
    category_label = config.get('category', 'Category')
    sales_label = config.get('sales', 'Value')
    profit_label = config.get('profit', 'Metric')
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        top_products = analyzer.get_top_products(5)
        if not top_products.empty and 'Product' in top_products.columns and 'Sales' in top_products.columns:
            with st.container():
                # Rename columns for display
                display_df = top_products.copy()
                display_df.columns = [product_label if col == 'Product' else sales_label if col == 'Sales' else col for col in display_df.columns]
                
                fig = px.bar(
                    display_df,
                    x=sales_label,
                    y=product_label,
                    orientation='h',
                    title=f'Top 5 {product_label}s by {sales_label}',
                    color=sales_label,
                    color_continuous_scale='Blues'
                )
                fig.update_layout(
                    height=400,
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"📦 {product_label} data not available for visualization")
    
    with col2:
        region_performance = analyzer.get_region_performance()
        if not region_performance.empty and 'Region' in region_performance.columns and 'Sales' in region_performance.columns:
            with st.container():
                # Rename columns for display
                display_df = region_performance.copy()
                display_df.columns = [region_label if col == 'Region' else sales_label if col == 'Sales' else col for col in display_df.columns]
                
                fig = px.pie(
                    display_df,
                    values=sales_label,
                    names=region_label,
                    title=f'{sales_label} Distribution by {region_label}',
                    hole=0.4,
                    color_discrete_sequence=px.colors.sequential.Blues_r
                )
                fig.update_layout(
                    height=400,
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"🌍 {region_label} data not available for visualization")
    
    st.markdown("")
    st.markdown("### 📈 Trend Analysis")
    st.markdown("")
    
    monthly_trend = analyzer.get_monthly_trend()
    
    if not monthly_trend.empty:
        with st.container():
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=monthly_trend['Month'],
                y=monthly_trend['Sales'],
                mode='lines+markers',
                name=sales_label,
                line=dict(color='#3b82f6', width=3),
                marker=dict(size=8),
                fill='tonexty',
                fillcolor='rgba(59, 130, 246, 0.1)'
            ))
            if 'Profit' in monthly_trend.columns:
                fig.add_trace(go.Scatter(
                    x=monthly_trend['Month'],
                    y=monthly_trend['Profit'],
                    mode='lines+markers',
                    name=profit_label,
                    line=dict(color='#10b981', width=3),
                    marker=dict(size=8)
                ))
            
            fig.update_layout(
                title=f'Monthly {sales_label} and {profit_label} Trend',
                xaxis_title='Month',
                yaxis_title='Amount',
                hovermode='x unified',
                height=450,
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📅 Date column required for trend analysis")
    
    st.markdown("")
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        category_sales = analyzer.get_category_performance()
        if not category_sales.empty:
            with st.container():
                # Rename columns for display
                display_df = category_sales.copy()
                display_df.columns = [category_label if col == 'Category' else sales_label if col == 'Sales' else col for col in display_df.columns]
                
                fig = px.bar(
                    display_df,
                    x=category_label,
                    y=sales_label,
                    title=f'{sales_label} by {category_label}',
                    color=profit_label if profit_label in display_df.columns else sales_label,
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(
                    height=400,
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"📂 {category_label} data not available")
    
    with col2:
        profit_margin = analyzer.get_profit_margin_by_product()
        if not profit_margin.empty and len(profit_margin) > 0:
            with st.container():
                # Use absolute values for size to avoid negative values
                plot_data = profit_margin.head(20).copy()
                if 'Profit' in plot_data.columns:
                    plot_data['Size'] = plot_data['Profit'].abs()
                    size_col = 'Size'
                    y_col = 'Profit'
                else:
                    plot_data['Size'] = plot_data['Sales'].abs()
                    size_col = 'Size'
                    y_col = 'Sales'
                
                # Rename for display
                plot_data.columns = [product_label if col == 'Product' else sales_label if col == 'Sales' else profit_label if col == 'Profit' else col for col in plot_data.columns]
                
                fig = px.scatter(
                    plot_data,
                    x=sales_label,
                    y=profit_label if profit_label in plot_data.columns else sales_label,
                    size=size_col,
                    color=product_label,
                    title=f'{sales_label} vs {profit_label} Analysis',
                    hover_data=[product_label]
                )
                fig.update_layout(
                    height=400,
                    showlegend=False,
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"📊 {product_label} data not available")

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render_dashboard(analyzer):
    st.markdown("### 📊 Performance Overview")
    st.markdown("")
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        top_products = analyzer.get_top_products(5)
        if not top_products.empty and 'Product' in top_products.columns and 'Sales' in top_products.columns:
            with st.container():
                fig = px.bar(
                    top_products,
                    x='Sales',
                    y='Product',
                    orientation='h',
                    title='Top 5 Products by Sales',
                    color='Sales',
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
            st.info("📦 Product data not available for visualization")
    
    with col2:
        region_performance = analyzer.get_region_performance()
        if not region_performance.empty and 'Region' in region_performance.columns and 'Sales' in region_performance.columns:
            with st.container():
                fig = px.pie(
                    region_performance,
                    values='Sales',
                    names='Region',
                    title='Sales Distribution by Region',
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
            st.info("🌍 Regional data not available for visualization")
    
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
                name='Sales',
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
                    name='Profit',
                    line=dict(color='#10b981', width=3),
                    marker=dict(size=8)
                ))
            
            fig.update_layout(
                title='Monthly Sales and Profit Trend',
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
                fig = px.bar(
                    category_sales,
                    x='Category',
                    y='Sales',
                    title='Sales by Category',
                    color='Profit' if 'Profit' in category_sales.columns else 'Sales',
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
            st.info("📂 Category data not available")
    
    with col2:
        profit_margin = analyzer.get_profit_margin_by_product()
        if not profit_margin.empty and len(profit_margin) > 0:
            with st.container():
                # Use absolute values for size to avoid negative values
                plot_data = profit_margin.head(20).copy()
                if 'Profit' in plot_data.columns:
                    plot_data['Size'] = plot_data['Profit'].abs()
                    size_col = 'Size'
                else:
                    plot_data['Size'] = plot_data['Sales'].abs()
                    size_col = 'Size'
                
                fig = px.scatter(
                    plot_data,
                    x='Sales',
                    y='Profit' if 'Profit' in plot_data.columns else 'Sales',
                    size=size_col,
                    color='Product',
                    title='Sales vs Profit Analysis',
                    hover_data=['Product']
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
            st.info("📊 Product data not available")

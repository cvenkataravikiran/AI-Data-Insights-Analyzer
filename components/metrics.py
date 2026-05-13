import streamlit as st

def display_kpi_cards(analyzer):
    st.markdown("### 📊 Key Performance Indicators")
    st.markdown("")
    
    summary = analyzer.get_summary_stats()
    config = analyzer.config
    
    # Get actual column names for labels
    sales_label = config.get('sales', 'Value 1')
    profit_label = config.get('profit', 'Value 2')
    product_label = config.get('product', 'Item')
    region_label = config.get('region', 'Group')
    category_label = config.get('category', 'Category')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label=f"💰 Total {sales_label}",
            value=f"${summary['total_sales']:,.0f}",
            delta=f"{summary['growth_rate']:.1f}% growth" if summary['growth_rate'] != 0 else None
        )
    
    with col2:
        if summary['total_profit'] > 0:
            st.metric(
                label=f"📈 Total {profit_label}",
                value=f"${summary['total_profit']:,.0f}",
                delta=f"{summary['profit_margin']:.1f}% margin" if summary['profit_margin'] != 0 else None
            )
        else:
            st.metric(
                label="📈 Records",
                value=f"{summary['total_orders']:,}",
                delta="total count"
            )
    
    with col3:
        st.metric(
            label=f"📊 Avg {sales_label}",
            value=f"${summary['avg_sales']:,.0f}",
            delta="per record"
        )
    
    with col4:
        st.metric(
            label="🎯 Total Records",
            value=f"{summary['total_orders']:,}",
            delta=f"{summary['total_quantity']:,} units" if summary['total_quantity'] > 0 else None
        )
    
    st.markdown("")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        top_product = analyzer.get_top_product()
        if top_product != "N/A":
            st.info(f"🏆 **Top {product_label}:** {top_product}")
    
    with col2:
        top_region = analyzer.get_top_region()
        if top_region != "N/A":
            st.info(f"🌟 **Best {region_label}:** {top_region}")
    
    with col3:
        top_category = analyzer.get_top_category()
        if top_category != "N/A":
            st.info(f"📦 **Top {category_label}:** {top_category}")

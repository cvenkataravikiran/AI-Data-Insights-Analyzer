import streamlit as st

def display_kpi_cards(analyzer):
    st.markdown("### 📊 Key Performance Indicators")
    st.markdown("")
    
    summary = analyzer.get_summary_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Sales",
            value=f"${summary['total_sales']:,.0f}",
            delta=f"{summary['growth_rate']:.1f}% growth" if summary['growth_rate'] != 0 else None
        )
    
    with col2:
        st.metric(
            label="📈 Total Profit",
            value=f"${summary['total_profit']:,.0f}",
            delta=f"{summary['profit_margin']:.1f}% margin" if summary['profit_margin'] != 0 else None
        )
    
    with col3:
        st.metric(
            label="📊 Avg Revenue",
            value=f"${summary['avg_sales']:,.0f}",
            delta="per transaction"
        )
    
    with col4:
        st.metric(
            label="🎯 Total Orders",
            value=f"{summary['total_orders']:,}",
            delta=f"{summary['total_quantity']:,} items" if summary['total_quantity'] > 0 else None
        )
    
    st.markdown("")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        top_product = analyzer.get_top_product()
        if top_product != "N/A":
            st.info(f"🏆 **Top Product:** {top_product}")
    
    with col2:
        top_region = analyzer.get_top_region()
        if top_region != "N/A":
            st.info(f"🌟 **Best Region:** {top_region}")
    
    with col3:
        top_category = analyzer.get_top_category()
        if top_category != "N/A":
            st.info(f"📦 **Top Category:** {top_category}")

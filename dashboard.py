import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show_dashboard():
    # --- Custom CSS ---
    st.markdown("""
    <style>
        .dashboard-header {
            background: linear-gradient(135deg, #155799 0%, #159957 100%);
            color: white; padding: 2rem; border-radius: 10px; text-align: center; margin-bottom: 2rem;
        }
        .metric-card {
            background: #f8f9fa; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #159957;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        }
        .edu-section {
            background: #e9f5ee; padding: 1.5rem; border-radius: 10px; margin-top: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

    if st.button("⬅️ Back to Home"):
        st.session_state.view = 'landing'
        st.rerun()

    st.markdown('<div class="dashboard-header"><h1>📊 Comprehensive Carbon Dashboard</h1><p>Integrated Analytics & Educational Hub</p></div>', unsafe_allow_html=True)

    # --- Data Retrieval (from Session State) ---
    registry_data = st.session_state.get('registry_data', [])
    pers_total = st.session_state.get('pers_total', 0)
    ind_total = st.session_state.get('ind_total', 0)
    
    df_reg = pd.DataFrame(registry_data)

    # --- Section 1: Executive Overview ---
    st.header("🏢 Operational Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    total_credits = df_reg['Issued'].sum() if not df_reg.empty else 0
    retired_credits = df_reg['Retired'].sum() if not df_reg.empty else 0
    active_projects = len(df_reg[df_reg['Status'] != 'Completed']) if not df_reg.empty else 0
    verified_projects = len(df_reg[df_reg['Status'] == 'Verified']) if not df_reg.empty else 0

    with col1:
        st.markdown(f'<div class="metric-card"><h3>Total Credits</h3><h2>{total_credits:,}</h2><p>tCO2e Issued</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card" style="border-left-color: #f39c12"><h3>Active Projects</h3><h2>{active_projects}</h2><p>Currently Monitoring</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card" style="border-left-color: #3498db"><h3>Personal Footprint</h3><h2>{pers_total:.2f}</h2><p>kg CO2 / month</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card" style="border-left-color: #9b59b6"><h3>Industrial Footprint</h3><h2>{ind_total/1000:.2f}</h2><p>t CO2 / month</p></div>', unsafe_allow_html=True)

    st.divider()

    # --- Section 2: Analytics Row ---
    st.header("📈 Data Analytics")
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Registry Composition")
        if not df_reg.empty:
            fig_pie = px.sunburst(df_reg, path=['Authority', 'Type'], values='Issued', color='Issued', color_continuous_scale='Greens')
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No registry data available yet.")

    with c2:
        st.subheader("Emission Comparison")
        comp_df = pd.DataFrame({
            'Category': ['Personal (Annualized)', 'Industrial (Annualized)'],
            'Metric Tons CO2': [pers_total * 12 / 1000, ind_total * 12 / 1000]
        })
        fig_bar = px.bar(comp_df, x='Category', y='Metric Tons CO2', color='Category', color_discrete_sequence=['#2ecc71', '#e74c3c'])
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # --- Section 3: Marketplace & Activity ---
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.subheader("🛒 Carbon Marketplace Preview")
        st.write("Browse available credits for offsetting your footprint.")
        if not df_reg.empty:
            st.dataframe(df_reg[['Project Name', 'Type', 'Location', 'Issued', 'Status']], use_container_width=True, hide_index=True)
        else:
            st.info("Marketplace is empty.")

    with col_b:
        st.subheader("🔔 Recent Activity")
        st.markdown("""
        - **New Project**: 'Amazon Conservation' verified (2h ago)
        - **Calculated**: Personal footprint updated for User (5h ago)
        - **Marketplace**: 5,000 credits retired by 'EcoCorp' (Yesterday)
        - **Registry**: New documentation uploaded for 'Wind India' (Yesterday)
        """)

    st.divider()

    # --- Section 4: Educational Hub & Definitions ---
    st.header("🎓 Carbon Educational Hub")
    
    tab1, tab2, tab3 = st.tabs(["Definitions & Concepts", "Resources & Videos", "External Links"])
    
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 🔍 Key Concepts")
            st.write("**Carbon Registry:** A system for tracking carbon credits to prevent double counting.")
            st.write("**Carbon Marketplace:** A platform where carbon credits are bought and sold.")
            st.write("**Carbon Offsetting:** Compensating for emissions by funding carbon reduction projects elsewhere.")
        with c2:
            st.markdown("### 🌍 Impact Factors")
            st.write("**Carbon Footprint:** The total GHG emissions caused by an individual, event, or organization.")
            st.write("**Net Zero:** Achieving a balance between emitted and removed greenhouse gases.")

    with tab2:
        st.markdown("### 🎥 Learning Materials")
        st.video("https://www.youtube.com/watch?v=S7jpMG5DS4Q") # Example carbon cycle video
        st.markdown("""
        #### Recommended Reading
        - Understanding the Carbon Cycle
        - How Carbon Credits Work
        - The Science of Global Warming
        """)

    with tab3:
        st.markdown("### 🔗 Government & Authority Links")
        st.markdown("- [United Nations Climate Change (UNFCCC)](https://unfccc.int/)")
        st.markdown("- [EPA: Greenhouse Gas Emissions](https://www.epa.gov/ghgemissions)")
        st.markdown("- [Verra Registry](https://registry.verra.org/)")
        st.markdown("- [Gold Standard Impact Registry](https://registry.goldstandard.org/)")
        st.markdown("- [World Bank Carbon Pricing Dashboard](https://carbonpricingdashboard.worldbank.org/)")

    st.divider()
    st.markdown("<p style='text-align: center;'>Carbon Dashboard v1.0 | Empowering Sustainable Decisions</p>", unsafe_allow_html=True)

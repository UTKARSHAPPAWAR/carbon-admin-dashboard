import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# All 15 GHG Protocol Scope 3 categories
SCOPE3_CATEGORIES = {
    "Upstream": {
        "1. Purchased Goods & Services (tonnes)": 0.85,
        "2. Capital Goods (tonnes)": 0.72,
        "3. Fuel & Energy Related (MWh)": 0.18,
        "4. Upstream Transportation (tonne-km)": 0.062,
        "5. Waste in Operations (tonnes)": 0.52,
        "6. Business Travel (km)": 0.18,
        "7. Employee Commuting (km/employee)": 0.14,
        "8. Upstream Leased Assets (m² space)": 0.05,
    },
    "Downstream": {
        "9. Downstream Transportation (tonne-km)": 0.062,
        "10. Processing of Sold Products (tonnes)": 0.44,
        "11. Use of Sold Products (kWh/unit lifetime)": 0.45,
        "12. End-of-Life Treatment of Sold Products (tonnes)": 0.52,
        "13. Downstream Leased Assets (m² space)": 0.05,
        "14. Franchises (locations)": 20.5,
        "15. Investments ($M invested)": 0.075,
    }
}

def show_scope3_calculator():
    if st.button("⬅️ Back to Home"):
        st.session_state.view = 'landing'
        st.rerun()

    st.title("🏭 Full Scope 3 Industrial Tracker")
    st.markdown("Track all **15 GHG Protocol Scope 3 categories** across your upstream and downstream value chain.")

    category_results = {}
    upstream_total = 0
    downstream_total = 0

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⬆️ Upstream Emissions")
        for cat, factor in SCOPE3_CATEGORIES["Upstream"].items():
            val = st.number_input(cat, min_value=0.0, value=0.0, step=1.0, key=f"up_{cat}")
            emission = val * factor
            upstream_total += emission
            category_results[cat.split(".")[1].strip().split("(")[0].strip()] = emission

    with col2:
        st.subheader("⬇️ Downstream Emissions")
        for cat, factor in SCOPE3_CATEGORIES["Downstream"].items():
            val = st.number_input(cat, min_value=0.0, value=0.0, step=1.0, key=f"dn_{cat}")
            emission = val * factor
            downstream_total += emission
            category_results[cat.split(".")[1].strip().split("(")[0].strip()] = emission

    if st.button("Calculate Full Scope 3", type="primary"):
        total = upstream_total + downstream_total

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Scope 3 (kg CO2e)", f"{total:,.2f}")
        m2.metric("Upstream (kg CO2e)", f"{upstream_total:,.2f}")
        m3.metric("Downstream (kg CO2e)", f"{downstream_total:,.2f}")

        st.divider()
        # Filter out zero categories
        non_zero = {k: v for k, v in category_results.items() if v > 0}
        if non_zero:
            c1, c2 = st.columns(2)
            fig_pie = px.pie(names=list(non_zero.keys()), values=list(non_zero.values()),
                             title="Scope 3 Breakdown by Category", hole=0.3)
            c1.plotly_chart(fig_pie, use_container_width=True)

            fig_bar = go.Figure(go.Bar(
                x=list(non_zero.values()),
                y=list(non_zero.keys()),
                orientation='h',
                marker_color='#2ecc71'
            ))
            fig_bar.update_layout(title="Category-wise Impact (kg CO2e)", height=500)
            c2.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Enter values above to see the breakdown chart.")

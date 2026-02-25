import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(layout="wide", page_title="Industrial Carbon Calculator")

st.title("🏭 Industrial Carbon Emission Calculator")
if st.button("⬅️ Back to Home"):
    st.switch_page("app.py")

st.markdown("""
Track and analyze your organization's carbon footprint across Scope 1, 2, and 3 emissions.
""")

# Standard Industrial Emission Factors (kg CO2 per unit)
IND_FACTORS = {
    "Natural Gas (m3)": 2.02,
    "Diesel (Liters)": 2.68,
    "Fuel Oil (Liters)": 2.97,
    "Grid Electricity (kWh)": 0.45,
    "Renewable Energy (kWh)": 0.02,
    "Business Travel (km)": 0.18,
    "Waste Generated (kg)": 0.52,
    "Water Usage (m3)": 0.34
}

with st.sidebar:
    st.header("🏢 Company Information")
    industry_type = st.selectbox("Industry Type", [
        "Manufacturing", "Technology", "Retail", "Healthcare", 
        "Construction", "Logistics", "Energy", "Other"
    ])
    company_size = st.selectbox("Company Size", ["Small (<50)", "Medium (50-250)", "Large (250+)"])
    annual_revenue = st.number_input("Annual Revenue ($)", min_value=0, value=1000000)

tabs = st.tabs(["Scope 1: Direct", "Scope 2: Energy", "Scope 3: Value Chain"])

with tabs[0]:
    st.subheader("🔥 Scope 1: Direct Emissions")
    st.info("Direct emissions from owned or controlled sources.")
    col1, col2, col3 = st.columns(3)
    with col1:
        natural_gas = st.number_input("Natural Gas (m3/month)", min_value=0.0, value=0.0)
    with col2:
        diesel = st.number_input("Diesel (Liters/month)", min_value=0.0, value=0.0)
    with col3:
        fuel = st.number_input("Other Fuel (Liters/month)", min_value=0.0, value=0.0)

with tabs[1]:
    st.subheader("⚡ Scope 2: Energy Consumption")
    st.info("Indirect emissions from the generation of purchased energy.")
    col1, col2 = st.columns(2)
    with col1:
        grid_electricity = st.number_input("Grid Electricity (kWh/month)", min_value=0.0, value=0.0)
    with col2:
        renewable_energy = st.number_input("Renewable Energy (kWh/month)", min_value=0.0, value=0.0)

with tabs[2]:
    st.subheader("🌐 Scope 3: Value Chain")
    st.info("All indirect emissions (not included in scope 2) that occur in the value chain.")
    col1, col2, col3 = st.columns(3)
    with col1:
        business_travel = st.number_input("Business Travel (km/month)", min_value=0.0, value=0.0)
    with col2:
        waste_generated = st.number_input("Waste Generated (kg/month)", min_value=0.0, value=0.0)
    with col3:
        water_usage = st.number_input("Water Usage (m3/month)", min_value=0.0, value=0.0)

if st.button("Calculate Industrial Footprint", type="primary"):
    # Scope 1
    s1_gas = natural_gas * IND_FACTORS["Natural Gas (m3)"]
    s1_diesel = diesel * IND_FACTORS["Diesel (Liters)"]
    s1_fuel = fuel * IND_FACTORS["Fuel Oil (Liters)"]
    total_s1 = s1_gas + s1_diesel + s1_fuel
    
    # Scope 2
    s2_grid = grid_electricity * IND_FACTORS["Grid Electricity (kWh)"]
    s2_renew = renewable_energy * IND_FACTORS["Renewable Energy (kWh)"]
    total_s2 = s2_grid + s2_renew
    
    # Scope 3
    s3_travel = business_travel * IND_FACTORS["Business Travel (km)"]
    s3_waste = waste_generated * IND_FACTORS["Waste Generated (kg)"]
    s3_water = water_usage * IND_FACTORS["Water Usage (m3)"]
    total_s3 = s3_travel + s3_waste + s3_water
    
    total_emissions = total_s1 + total_s2 + total_s3
    
    st.divider()
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Emissions", f"{total_emissions/1000:.2f} tCO2e")
    m2.metric("Scope 1", f"{total_s1/1000:.2f} tCO2e")
    m3.metric("Scope 2", f"{total_s2/1000:.2f} tCO2e")
    m4.metric("Scope 3", f"{total_s3/1000:.2f} tCO2e")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Pie chart for scope distribution
        labels = ['Scope 1', 'Scope 2', 'Scope 3']
        values = [total_s1, total_s2, total_s3]
        fig_pie = px.pie(names=labels, values=values, title="Emissions Distribution by Scope",
                         color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_right:
        # Bar chart for category breakdown
        categories = {
            "Nat. Gas": s1_gas, "Diesel": s1_diesel, "Fuel": s1_fuel,
            "Grid Elec": s2_grid, "Renewable": s2_renew,
            "Travel": s3_travel, "Waste": s3_waste, "Water": s3_water
        }
        fig_bar = px.bar(x=list(categories.keys()), y=list(categories.values()), 
                         title="Detailed Category Breakdown (kg CO2e)",
                         labels={'x': 'Category', 'y': 'kg CO2e'},
                         color=list(categories.values()), color_continuous_scale='Viridis')
        st.plotly_chart(fig_bar, use_container_width=True)

    st.success(f"Calculation complete for {industry_type} sector ({company_size} size).")
else:
    st.info("Enter your operational data and click 'Calculate' to see results.")

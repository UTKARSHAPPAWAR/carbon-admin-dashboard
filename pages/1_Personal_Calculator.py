import streamlit as st
import plotly.express as px
import pandas as pd

# Expanded emission factors for many countries (example values, replace with accurate data)
EMISSION_FACTORS = {
    # Africa (54 countries)
    "Africa": {
        "South Africa": {"Transportation": 0.28, "Electricity": 0.75, "Diet": 1.35, "Waste": 0.18},
        "Nigeria": {"Transportation": 0.28, "Electricity": 0.75, "Diet": 1.35, "Waste": 0.18},
        "Egypt": {"Transportation": 0.22, "Electricity": 0.55, "Diet": 1.1, "Waste": 0.16},
        "Kenya": {"Transportation": 0.22, "Electricity": 0.55, "Diet": 1.1, "Waste": 0.16},
        "Algeria": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Angola": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Benin": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Botswana": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Burkina Faso": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Burundi": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Cabo Verde": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Cameroon": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Central African Republic": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Chad": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Comoros": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Congo (Brazzaville)": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Congo (Kinshasa)": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Djibouti": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Equatorial Guinea": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Eritrea": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Eswatini": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Ethiopia": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Gabon": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Gambia": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Ghana": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Guinea": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Guinea-Bissau": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Ivory Coast": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Lesotho": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Liberia": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Libya": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Madagascar": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Malawi": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Mali": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Mauritania": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Mauritius": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Mozambique": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Namibia": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Niger": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Rwanda": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Sao Tome and Principe": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Senegal": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Seychelles": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Sierra Leone": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Somalia": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "South Sudan": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Sudan": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Tanzania": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Togo": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Uganda": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Zambia": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17},
        "Zimbabwe": {"Transportation": 0.25, "Electricity": 0.65, "Diet": 1.25, "Waste": 0.17}
    },
    
    
    "Antarctica": {
        "Antarctica": {"Transportation": 0.1, "Electricity": 0.3, "Diet": 1.0, "Waste": 0.05}
    },
    # Asia (49 countries)
    "Asia": {
        "India": {"Transportation": 0.17, "Electricity": 0.67, "Diet": 1.72, "Waste": 0.14},
        "China": {"Transportation": 0.17, "Electricity": 0.67, "Diet": 1.72, "Waste": 0.14},
        "Japan": {"Transportation": 0.17, "Electricity": 0.67, "Diet": 1.72, "Waste": 0.14},
        "Pakistan": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Bangladesh": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Indonesia": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Vietnam": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Philippines": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Iran": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Thailand": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Malaysia": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Singapore": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Myanmar": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Nepal": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Sri Lanka": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Afghanistan": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Maldives": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Kazakhstan": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Uzbekistan": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Turkmenistan": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Kyrgyzstan": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Tajikistan": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Georgia": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Armenia": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Azerbaijan": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Russia": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "South Korea": {"Transportation": 0.17, "Electricity": 0.67, "Diet": 1.72, "Waste": 0.14},
        "Mongolia": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Brunei": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Bhutan": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Laos": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Cambodia": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Timor-Leste": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Palestine": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Syria": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Lebanon": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Iraq": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Jordan": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Kuwait": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Qatar": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "United Arab Emirates": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Oman": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Bahrain": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
        "Yemen": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15}
    },

    # Europe (44 countries)
    "Europe": {
        "Germany": {"Transportation": 0.15, "Electricity": 0.33, "Diet": 1.97, "Waste": 0.17},
        "United Kingdom": {"Transportation": 0.15, "Electricity": 0.33, "Diet": 1.97, "Waste": 0.17},
        "France": {"Transportation": 0.15, "Electricity": 0.33, "Diet": 1.97, "Waste": 0.17},
        "Italy": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Spain": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Greece": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Poland": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Ukraine": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Netherlands": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Belgium": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Sweden": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Norway": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Denmark": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Finland": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Austria": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Switzerland": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Czech Republic": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Hungary": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Portugal": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Ireland": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Romania": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Bulgaria": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Slovakia": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Slovenia": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Lithuania": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Latvia": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Estonia": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Cyprus": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Malta": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16},
        "Iceland": {"Transportation": 0.14, "Electricity": 0.4, "Diet": 1.9, "Waste": 0.16}
    },

    # North America (23 countries)
    "North America": {
        "USA": {"Transportation": 0.22, "Electricity": 0.32, "Diet": 2.1, "Waste": 0.18},
        "Canada": {"Transportation": 0.22, "Electricity": 0.32, "Diet": 2.1, "Waste": 0.18},
        "Mexico": {"Transportation": 0.18, "Electricity": 0.2, "Diet": 1.9, "Waste": 0.15},
        "Cuba": {"Transportation": 0.2, "Electricity": 0.3, "Diet": 2.0, "Waste": 0.17},
        "Panama": {"Transportation": 0.2, "Electricity": 0.3, "Diet": 2.0, "Waste": 0.17},
        "Haiti": {"Transportation": 0.2, "Electricity": 0.3, "Diet": 2.0, "Waste": 0.17},
        "Guatemala": {"Transportation": 0.2, "Electricity": 0.3, "Diet": 2.0, "Waste": 0.17},
        "Dominican Republic": {"Transportation": 0.2, "Electricity": 0.3, "Diet": 2.0, "Waste": 0.17},
        "Nicaragua": {"Transportation": 0.2, "Electricity": 0.3, "Diet": 2.0, "Waste": 0.17},
        "Costa Rica": {"Transportation": 0.2, "Electricity": 0.3, "Diet": 2.0, "Waste": 0.17},
        "El Salvador": {"Transportation": 0.2, "Electricity": 0.3, "Diet": 2.0, "Waste": 0.17},
        "Jamaica": {"Transportation": 0.2, "Electricity": 0.3, "Diet": 2.0, "Waste": 0.17},
        "Trinidad and Tobago": {"Transportation": 0.2, "Electricity": 0.3, "Diet": 2.0, "Waste": 0.17},
        "Barbados": {"Transportation": 0.2, "Electricity": 0.3, "Diet": 2.0, "Waste": 0.17},
        "Bahamas": {"Transportation": 0.2, "Electricity": 0.3, "Diet": 2.0, "Waste": 0.17},
        "Saint Lucia": {"Transportation": 0.2, "Electricity": 0.3, "Diet": 2.0, "Waste": 0.17},
        "Grenada": {"Transportation": 0.2, "Electricity": 0.3, "Diet": 2.0, "Waste": 0.17},
        "Saint Vincent and the Grenadines": {"Transportation": 0.2, "Electricity": 0.3, "Diet": 2.0, "Waste": 0.17},
        "Antigua and Barbuda": {"Transportation": 0.2, "Electricity": 0.3, "Diet": 2.0, "Waste": 0.17},
        "Saint Kitts and Nevis": {"Transportation": 0.2, "Electricity": 0.3, "Diet": 2.0, "Waste": 0.17}
    },

    # South America (12 countries)
    "South America": {
        "Brazil": {"Transportation": 0.18, "Electricity": 0.19, "Diet": 1.55, "Waste": 0.13},
        "Argentina": {"Transportation": 0.18, "Electricity": 0.19, "Diet": 1.55, "Waste": 0.13},
        "Chile": {"Transportation": 0.19, "Electricity": 0.2, "Diet": 1.6, "Waste": 0.14},
        "Peru": {"Transportation": 0.19, "Electricity": 0.2, "Diet": 1.6, "Waste": 0.14},
        "Colombia": {"Transportation": 0.19, "Electricity": 0.2, "Diet": 1.6, "Waste": 0.14},
        "Venezuela": {"Transportation": 0.19, "Electricity": 0.2, "Diet": 1.6, "Waste": 0.14},
        "Ecuador": {"Transportation": 0.19, "Electricity": 0.2, "Diet": 1.6, "Waste": 0.14},
        "Uruguay": {"Transportation": 0.19, "Electricity": 0.2, "Diet": 1.6, "Waste": 0.14},
        "Paraguay": {"Transportation": 0.19, "Electricity": 0.2, "Diet": 1.6, "Waste": 0.14},
        "Bolivia": {"Transportation": 0.19, "Electricity": 0.2, "Diet": 1.6, "Waste": 0.14},
        "Guyana": {"Transportation": 0.19, "Electricity": 0.2, "Diet": 1.6, "Waste": 0.14},
        "Suriname": {"Transportation": 0.19, "Electricity": 0.2, "Diet": 1.6, "Waste": 0.14}
    },

    # Oceania (16 countries)
    "Oceania": {
        "Australia": {"Transportation": 0.2, "Electricity": 0.52, "Diet": 1.7, "Waste": 0.21},
        "New Zealand": {"Transportation": 0.2, "Electricity": 0.52, "Diet": 1.7, "Waste": 0.21},
        "Fiji": {"Transportation": 0.21, "Electricity": 0.5, "Diet": 1.65, "Waste": 0.2},
        "Papua New Guinea": {"Transportation": 0.21, "Electricity": 0.5, "Diet": 1.65, "Waste": 0.2},
        "Samoa": {"Transportation": 0.21, "Electricity": 0.5, "Diet": 1.65, "Waste": 0.2},
        "Solomon Islands": {"Transportation": 0.21, "Electricity": 0.5, "Diet": 1.65, "Waste": 0.2},
        "Vanuatu": {"Transportation": 0.21, "Electricity": 0.5, "Diet": 1.65, "Waste": 0.2},
        "Kiribati": {"Transportation": 0.21, "Electricity": 0.5, "Diet": 1.65, "Waste": 0.2},
        "Tonga": {"Transportation": 0.21, "Electricity": 0.5, "Diet": 1.65, "Waste": 0.2},
        "Tuvalu": {"Transportation": 0.21, "Electricity": 0.5, "Diet": 1.65, "Waste": 0.2},
        "Micronesia": {"Transportation": 0.21, "Electricity": 0.5, "Diet": 1.65, "Waste": 0.2},
        "Marshall Islands": {"Transportation": 0.21, "Electricity": 0.5, "Diet": 1.65, "Waste": 0.2},
        "Palau": {"Transportation": 0.21, "Electricity": 0.5, "Diet": 1.65, "Waste": 0.2}
    },
}

st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")

# Sidebar for input fields and region/country selection
with st.sidebar:
    st.header("Input Your Details")
    region = st.selectbox("Select Region", list(EMISSION_FACTORS.keys()))
    
    if region:
        country = st.selectbox("Select Country", list(EMISSION_FACTORS[region].keys()))
        
    transportation = st.number_input("Transportation (km per person, per month)", min_value=0, value=100)
    electricity = st.number_input("Electricity usage (kWh per person, per month)", min_value=0, value=200)
    diet = st.number_input("Diet (kg per person, per month)", min_value=0, value=50)
    waste = st.number_input("Waste (kg per person, per month)", min_value=0, value=20)

    # Button to trigger calculation inside the sidebar
    calculate = st.button("Calculate Emission")

# Calculation based on user input
def calculate_emission(country_factors, transportation, electricity, diet, waste):
    transport_emission = transportation * country_factors.get('Transportation', 0)
    electricity_emission = electricity * country_factors.get('Electricity', 0)
    diet_emission = diet * country_factors.get('Diet', 0)
    waste_emission = waste * country_factors.get('Waste', 0)
    
    total_emission = transport_emission + electricity_emission + diet_emission + waste_emission
    return total_emission, transport_emission, electricity_emission, diet_emission, waste_emission

# Streamlit app layout
st.title("Personal Carbon Emission Calculator")

# Ensure country is selected before calculating
if calculate:
    if 'country' in locals() and country in EMISSION_FACTORS[region]:
        country_factors = EMISSION_FACTORS[region][country]

        # Perform emission calculation
        total_emission, transportation_emissions, electricity_emissions, diet_emissions, waste_emissions = calculate_emission(
            country_factors, transportation, electricity, diet, waste)
        
        # Two columns: left for map, right for results (responsive)
        col1, col2 = st.columns([2, 1])  # You can change the proportions as needed
        
        # Column 1: Choropleth map
        with col1:
            st.subheader("Choropleth Map of Carbon Emissions")

            # Calculate emissions for all countries for the global emissions map
            country_emissions = {c: sum(factor for factor in EMISSION_FACTORS[region].get(c, {}).values()) 
                                for c in EMISSION_FACTORS[region].keys()}

            # Update selected country with user's total emissions
            country_emissions[country] = total_emission  # in kgCO2

            # Create the choropleth map
            fig = px.choropleth(
                locations=list(country_emissions.keys()),
                locationmode="country names",
                color=list(country_emissions.values()),
                hover_name=list(country_emissions.keys()),
                color_continuous_scale=px.colors.sequential.Plasma,  # A more colorful scale
                labels={'color': 'Total Emissions (kgCO2)'},
                template='plotly_white'
            )
            fig.update_layout(coloraxis_colorbar_title='Total Emissions (kgCO2)', height=700, width=1200)  # Increased size
            st.plotly_chart(fig, use_container_width=True)  # Makes the plot responsive
        
        # Column 2: Display detailed results
        with col2:
            st.subheader("CO2 Emissions by Category")
            st.info(f"🚗 Transportation: {transportation_emissions:.2f} tonnes CO2 per person, per year")
            st.info(f"💡 Electricity: {electricity_emissions:.2f} tonnes CO2 per person, per year")
            st.info(f"🍽️ Diet: {diet_emissions:.2f} tonnes CO2 per person, per year")
            st.info(f"🗑️ Waste: {waste_emissions:.2f} tonnes CO2 per person, per year")

            st.subheader("Total Carbon Footprint")
            st.success(f"🌍 Your total carbon footprint is: {total_emission:.2f} kg CO2 per person, per year")

    else:
        st.write("Please select a valid region and country to calculate emissions.")
else:
    st.write("Select your details in the sidebar and click 'Calculate Emission' to see your footprint.")

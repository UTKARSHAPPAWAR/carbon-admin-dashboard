import streamlit as st
import pandas as pd
import database

def show_marketplace():
    if st.button("⬅️ Back to Home"):
        st.session_state.view = 'landing'
        st.rerun()

    st.title("🛒 Carbon Credit Marketplace")
    st.markdown("Browse available carbon offset projects and simulate purchasing credits to compensate for your footprint.")

    # Initialize user wallet in session state
    if 'wallet_credits' not in st.session_state:
        st.session_state.wallet_credits = 500  # Start with 500 free credits
    if 'purchased_offsets' not in st.session_state:
        st.session_state.purchased_offsets = 0

    # Get user's current footprint
    pers_total = st.session_state.get('pers_total', 0)
    ind_total = st.session_state.get('ind_total', 0)
    combined_kg = pers_total + ind_total
    combined_tonnes = combined_kg / 1000

    # Wallet / Status bar
    col1, col2, col3 = st.columns(3)
    col1.metric("💳 Available Credits", f"{st.session_state.wallet_credits:,}")
    col2.metric("🌍 Your Footprint (tCO2)", f"{combined_tonnes:.3f}")
    col3.metric("✅ Offsets Purchased (tCO2)", f"{st.session_state.purchased_offsets:.3f}")

    remaining = max(0, combined_tonnes - st.session_state.purchased_offsets)
    if remaining == 0 and combined_tonnes > 0:
        st.success("🎉 Your footprint is fully offset! You have achieved Net Zero.")
    elif combined_tonnes > 0:
        st.warning(f"⚠️ You still need to offset **{remaining:.3f} tCO2** to reach Net Zero.")
        if st.button("🤖 AI One-Click Net Zero (Auto-Offset)", type="primary"):
            # Automation: AI-Driven Offset Automation
            # Find the best project (simulated as the first one)
            if projects:
                best_proj = projects[0]
                available = best_proj.get('Issued', 0) - best_proj.get('Retired', 0)
                amount_to_buy = min(remaining, float(available))
                cost = amount_to_buy * 10
                
                if st.session_state.wallet_credits >= cost:
                    st.session_state.wallet_credits -= int(cost)
                    st.session_state.purchased_offsets += amount_to_buy
                    
                    # Record the purchase in the database
                    username = st.session_state.get('username', 'Guest')
                    database.add_purchase(username, best_proj['ID'], amount_to_buy)
                    
                    best_proj['Retired'] = best_proj.get('Retired', 0) + int(amount_to_buy * 1000)
                    
                    username = st.session_state.get('username', 'Guest')
                    database.log_activity(username, "Automation", f"AI Auto-Offset: Purchased {amount_to_buy:.3f} tCO2 from {best_proj['Project Name']}")
                    st.success(f"✅ AI Automation: Successfully offset {amount_to_buy:.3f} tCO2 using {best_proj['Project Name']}!")
                    st.rerun()
                else:
                    st.error("Insufficient credits for AI Auto-Offset.")

    st.divider()

    # Marketplace listings
    projects = st.session_state.get('registry_data', [
        {"ID": "VCS-001", "Project Name": "Amazon Rainforest Conservation", "Type": "Nature-based/REDD+", "Location": "Brazil", "Issued": 500000, "Retired": 120000},
        {"ID": "GS-442", "Project Name": "Community Wind Power India", "Type": "Renewable Energy", "Location": "India", "Issued": 250000, "Retired": 210000},
    ])

    st.subheader("📋 Available Offset Projects")
    for proj in projects:
        available = proj.get('Issued', 0) - proj.get('Retired', 0)
        price_per_tonne = 10  # Simulated price in credits

        with st.expander(f"**{proj['Project Name']}** — {proj['Type']} | {proj.get('Location', 'N/A')} | {available:,} tCO2 available"):
            pc1, pc2, pc3 = st.columns(3)
            pc1.write(f"**Project ID**: {proj['ID']}")
            pc2.write(f"**Available Credits**: {available:,} tCO2")
            pc3.write(f"**Price**: {price_per_tonne} credits / tCO2")

            qty = st.number_input(
                f"Tonnes to buy from '{proj['Project Name']}'",
                min_value=0.0, max_value=float(available), step=0.5,
                key=f"buy_{proj['ID']}"
            )
            cost = qty * price_per_tonne
            st.write(f"💰 Total Cost: **{cost:.0f} credits**")

            if st.button(f"Purchase from {proj['ID']}", key=f"btn_{proj['ID']}"):
                if qty <= 0:
                    st.error("Please enter a quantity greater than 0.")
                elif cost > st.session_state.wallet_credits:
                    st.error(f"Insufficient credits! You have {st.session_state.wallet_credits}, need {cost:.0f}.")
                else:
                    st.session_state.wallet_credits -= int(cost)
                    st.session_state.purchased_offsets += qty
                    
                    # Record the purchase in the database
                    username = st.session_state.get('username', 'Guest')
                    database.add_purchase(username, proj['ID'], qty)
                    
                    # Update the project's retired count
                    proj['Retired'] = proj.get('Retired', 0) + int(qty * 1000)
                    
                    username = st.session_state.get('username', 'Guest')
                    database.log_activity(username, "Marketplace Purchase", f"Purchased {qty} tCO2 from {proj['Project Name']}")
                    
                    st.success(f"✅ Successfully purchased {qty} tCO2 from {proj['Project Name']}!")
                    st.rerun()

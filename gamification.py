import streamlit as st
from datetime import datetime

def show_gamification():
    if st.button("⬅️ Back to Home"):
        st.session_state.view = 'landing'
        st.rerun()

    st.title("🏆 Achievements & Leaderboard")
    st.markdown("Earn badges by reducing your footprint and compete on the anonymous leaderboard.")

    # Initialize gamification state
    if 'badges' not in st.session_state:
        st.session_state.badges = []
    if 'streak' not in st.session_state:
        st.session_state.streak = 1
    if 'calc_count' not in st.session_state:
        st.session_state.calc_count = 0

    pers_total = st.session_state.get('pers_total', 0)
    purchased_offsets = st.session_state.get('purchased_offsets', 0)

    # Award badges based on state
    all_badges = [
        {"name": "🌱 First Step", "desc": "Completed your first carbon calculation", "earned": st.session_state.calc_count >= 1},
        {"name": "⚡ Energy Saver", "desc": "Personal electricity footprint below 20 kg CO2", "earned": st.session_state.get('pers_breakdown', {}).get('electricity', 999) < 20},
        {"name": "🌿 Eco Warrior", "desc": "Total personal footprint below 100 kg CO2/month", "earned": 0 < pers_total < 100},
        {"name": "♻️ Net Zero Hero", "desc": "Offset your full footprint via the Marketplace", "earned": purchased_offsets > 0 and purchased_offsets * 1000 >= pers_total},
        {"name": "🔬 Scope Master", "desc": "Used the Full Scope 3 Industrial Tracker", "earned": st.session_state.get('scope3_used', False)},
        {"name": "📜 Registry Pioneer", "desc": "Registered a project in the Carbon Offset Registry", "earned": len(st.session_state.get('registry_data', [])) > 2},
    ]

    # Badges Display
    st.subheader("🎖️ Your Badges")
    b_cols = st.columns(3)
    for i, badge in enumerate(all_badges):
        with b_cols[i % 3]:
            if badge['earned']:
                st.success(f"**{badge['name']}**\n\n{badge['desc']}")
            else:
                st.info(f"🔒 *{badge['name']}*\n\n_{badge['desc']}_")

    st.divider()

    # Streak
    st.subheader(f"🔥 Current Streak: {st.session_state.streak} days")
    st.progress(min(st.session_state.streak / 30, 1.0), text=f"{st.session_state.streak}/30 days to 'Month Warrior' badge")

    st.divider()

    # Anonymous Leaderboard (Simulated)
    st.subheader("🏅 Anonymous Leaderboard (Monthly Lowest Footprint)")
    leaderboard_data = [
        {"Rank": "🥇 1st", "User": "User_A7X", "Footprint (kg CO2)": 48.2, "Offsets Purchased": 0.12},
        {"Rank": "🥈 2nd", "User": "User_B2Q", "Footprint (kg CO2)": 63.5, "Offsets Purchased": 0.05},
        {"Rank": "🥉 3rd", "User": "User_C9K", "Footprint (kg CO2)": 79.1, "Offsets Purchased": 0.00},
        {"Rank": "4th", "User": "User_D4M", "Footprint (kg CO2)": 95.4, "Offsets Purchased": 0.20},
        {"Rank": "5th", "User": "User_E1P", "Footprint (kg CO2)": 112.7, "Offsets Purchased": 0.00},
        {"Rank": "—", "User": "You", "Footprint (kg CO2)": round(pers_total, 2) if pers_total > 0 else "Run calc first", "Offsets Purchased": round(purchased_offsets, 3)},
    ]
    import pandas as pd
    df = pd.DataFrame(leaderboard_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

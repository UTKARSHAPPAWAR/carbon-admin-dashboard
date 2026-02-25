import streamlit as st

def get_tips(t_e, e_e, d_e, w_e):
    tips = []

    # Transport tips
    if t_e > 50:
        saving = round(t_e * 0.4, 1)
        tips.append(("🚗 Transportation", f"You could save ~{saving} kg CO2/month by switching to public transport or carpooling at least 3 days a week."))
    if t_e > 100:
        tips.append(("✈️ Air Travel", f"Consider replacing one flight per year with a train/video call – saves up to 200 kg CO2 per trip."))

    # Electricity tips
    if e_e > 40:
        saving = round(e_e * 0.35, 1)
        tips.append(("💡 Electricity", f"Installing rooftop solar panels could cut your electricity emissions by ~{saving} kg CO2/month."))
    if e_e > 60:
        tips.append(("🌬️ Energy Efficiency", "Switching to LED bulbs and a smart thermostat could reduce energy consumption by up to 20%."))

    # Diet tips
    if d_e > 80:
        saving = round(d_e * 0.3, 1)
        tips.append(("🥗 Diet", f"Reducing meat consumption by 3 days/week could save ~{saving} kg CO2/month."))
    if d_e > 150:
        tips.append(("🌱 Plant-Based Switch", "A full switch to a plant-based diet could reduce your diet emissions by up to 60%."))

    # Waste tips
    if w_e > 10:
        saving = round(w_e * 0.5, 1)
        tips.append(("♻️ Waste", f"Composting organic waste and recycling could halve your waste emissions – saving ~{saving} kg CO2/month."))

    if not tips:
        tips.append(("🏆 Great Job!", "Your footprint is already low! Keep it up and consider offsetting the remaining emissions."))

    return tips


def show_ai_assistant():
    if st.button("⬅️ Back to Home"):
        st.session_state.view = 'landing'
        st.rerun()

    st.title("🤖 AI Carbon Reduction Assistant")
    st.markdown("Get personalized recommendations to reduce your carbon footprint based on your last calculated results.")

    t_e = st.session_state.get('pers_breakdown', {}).get('transport', 0)
    e_e = st.session_state.get('pers_breakdown', {}).get('electricity', 0)
    d_e = st.session_state.get('pers_breakdown', {}).get('diet', 0)
    w_e = st.session_state.get('pers_breakdown', {}).get('waste', 0)

    if t_e == 0 and e_e == 0 and d_e == 0 and w_e == 0:
        st.info("⚠️ Please run your **Personal Calculator** first, then come back here for personalized tips.")
        return

    total = t_e + e_e + d_e + w_e
    st.metric("Your Monthly Footprint (kg CO2)", f"{total:.2f}")
    st.divider()

    tips = get_tips(t_e, e_e, d_e, w_e)
    st.subheader("💡 Personalized Recommendations")
    for category, tip in tips:
        with st.expander(f"**{category}**"):
            st.write(tip)

    st.divider()
    st.subheader("🌍 Your Potential Impact")
    max_saving = round(total * 0.45, 2)
    st.success(f"By following all recommendations, you could reduce your footprint by up to **{max_saving} kg CO2/month** – that's **{round(max_saving*12/1000, 2)} tonnes/year**!")

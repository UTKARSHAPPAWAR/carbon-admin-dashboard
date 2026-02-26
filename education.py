import streamlit as st
import random
import database

QUIZ_QUESTIONS = [
    {
        "question": "What percentage of global greenhouse gas emissions come from energy production?",
        "options": ["15%", "25%", "34%", "50%"],
        "answer": "34%",
        "explanation": "Energy production (electricity & heat) accounts for ~34% of global GHG emissions."
    },
    {
        "question": "Which greenhouse gas has the highest global warming potential (over 100 years)?",
        "options": ["CO2", "Methane (CH4)", "Nitrous Oxide (N2O)", "Sulphur Hexafluoride (SF6)"],
        "answer": "Sulphur Hexafluoride (SF6)",
        "explanation": "SF6 has a GWP of 22,800 over 100 years – the highest of any measured greenhouse gas."
    },
    {
        "question": "What does 'Scope 2' emissions refer to?",
        "options": ["Direct emissions from owned sources", "Indirect emissions from purchased energy", "Value chain emissions", "Transport emissions only"],
        "answer": "Indirect emissions from purchased energy",
        "explanation": "Scope 2 covers indirect GHG emissions from the generation of purchased electricity, steam, heat, or cooling."
    },
    {
        "question": "Approximately how much CO2 does one tree absorb per year?",
        "options": ["2 kg", "22 kg", "100 kg", "500 kg"],
        "answer": "22 kg",
        "explanation": "A mature tree absorbs roughly 22 kg of CO2 per year, though this varies by species and size."
    },
    {
        "question": "Which diet type has the lowest carbon footprint?",
        "options": ["Meat-lover", "Pescatarian", "Vegetarian", "Vegan"],
        "answer": "Vegan",
        "explanation": "A vegan diet typically produces 50–70% less GHG emissions than a high-meat diet."
    },
]

def show_education():
    if st.button("⬅️ Back to Home"):
        st.session_state.view = 'landing'
        st.rerun()

    st.title("🎓 Interactive Educational Hub")
    st.markdown("Learn about climate change, earn certifications, and test your knowledge!")

    tabs = st.tabs(["📚 Learn", "🎥 Videos & Links", "🧠 Take the Quiz", "🏅 Certification"])

    with tabs[0]:
        st.subheader("Core Climate Concepts")
        with st.expander("🌍 What is a Carbon Footprint?"):
            st.write("A carbon footprint is the total greenhouse gas (GHG) emissions caused directly and indirectly by an individual, organization, event, or product, expressed in CO2 equivalents.")
        with st.expander("📊 Scope 1, 2, and 3 Emissions"):
            st.write("**Scope 1**: Direct emissions from owned or controlled sources.\n\n**Scope 2**: Indirect emissions from purchased energy.\n\n**Scope 3**: All other indirect emissions in a company's value chain.")
        with st.expander("💳 Carbon Credits & Offsets"):
            st.write("A carbon credit represents the reduction or removal of one metric tonne of CO2. Organizations can purchase credits to offset their own emissions.")
        with st.expander("🏦 Carbon Registry"):
            st.write("A carbon registry tracks the issuance, transfer, and retirement of carbon credits to ensure they are not counted twice (double-counting prevention).")
        with st.expander("🛒 Carbon Marketplace"):
            st.write("A platform where verified carbon credits (from offset projects like reforestation or renewables) can be bought and sold.")

    with tabs[1]:
        st.subheader("🎥 Recommended Videos")
        st.video("https://www.youtube.com/watch?v=S7jpMG5DS4Q")
        st.caption("The Carbon Cycle – National Geographic")
        st.video("https://www.youtube.com/watch?v=ip-O-3bZwok")
        st.caption("How Carbon Credits Work – Bloomberg")

        st.divider()
        st.subheader("🔗 Government & Official Resources")
        resources = {
            "UNFCCC – UN Climate Change": "https://unfccc.int/",
            "EPA – Greenhouse Gas Emissions": "https://www.epa.gov/ghgemissions",
            "World Bank Carbon Pricing Dashboard": "https://carbonpricingdashboard.worldbank.org/",
            "Verra (VCS) Registry": "https://registry.verra.org/",
            "Gold Standard Registry": "https://registry.goldstandard.org/",
            "IEA – Energy & Climate": "https://www.iea.org/topics/climate-change",
            "India MoEFCC – Climate Portal": "https://moef.gov.in/en/division/environment-divisions/climate-change/",
        }
        for name, url in resources.items():
            st.markdown(f"- [{name}]({url})")

    with tabs[2]:
        st.subheader("🧠 Climate Knowledge Quiz")
        if 'quiz_score' not in st.session_state:
            st.session_state.quiz_score = 0
        if 'quiz_done' not in st.session_state:
            st.session_state.quiz_done = False
        if 'quiz_answers' not in st.session_state:
            st.session_state.quiz_answers = {}

        if not st.session_state.quiz_done:
            score = 0
            with st.form("quiz_form"):
                for i, q in enumerate(QUIZ_QUESTIONS):
                    st.write(f"**Q{i+1}: {q['question']}**")
                    ans = st.radio("Select your answer:", q['options'], key=f"q_{i}", index=None)
                    st.session_state.quiz_answers[i] = ans
                
                if st.form_submit_button("Submit Quiz", type="primary"):
                    for i, q in enumerate(QUIZ_QUESTIONS):
                        if st.session_state.quiz_answers.get(i) == q['answer']:
                            score += 1
                    st.session_state.quiz_score = score
                    st.session_state.quiz_done = True
                    st.session_state.calc_count = st.session_state.get('calc_count', 0) + 1
                    
                    username = st.session_state.get('username', 'Guest')
                    database.log_activity(username, "Educational Quiz", f"Completed climate quiz with score {score}/{len(QUIZ_QUESTIONS)}")
                    
                    st.rerun()
        else:
            score = st.session_state.quiz_score
            st.metric("Your Score", f"{score} / {len(QUIZ_QUESTIONS)}")
            if score == len(QUIZ_QUESTIONS):
                st.balloons()
                st.success("🏆 Perfect Score! You are a Climate Champion!")
            elif score >= 3:
                st.success("👍 Great job! A solid understanding of climate concepts.")
            else:
                st.warning("🌱 Good start! Review the Learn tab and try again.")
            
            st.divider()
            st.subheader("Explanations:")
            for i, q in enumerate(QUIZ_QUESTIONS):
                correct = st.session_state.quiz_answers.get(i) == q['answer']
                icon = "✅" if correct else "❌"
                with st.expander(f"{icon} Q{i+1}: {q['question']}"):
                    st.write(f"**Correct Answer**: {q['answer']}")
                    st.write(f"**Explanation**: {q['explanation']}")

            if st.button("Retake Quiz"):
                st.session_state.quiz_done = False
                st.session_state.quiz_answers = {}
                st.rerun()

    with tabs[3]:
        st.subheader("🏅 Climate Champion Certification")
        score = st.session_state.get('quiz_score', 0)
        pers_total = st.session_state.get('pers_total', 0)
        purchased = st.session_state.get('purchased_offsets', 0)

        requirements = [
            ("✅" if score >= 4 else "❌", f"Score 4+ on Climate Quiz (Your score: {score}/5)"),
            ("✅" if pers_total > 0 else "❌", "Complete Personal Footprint Calculation"),
            ("✅" if purchased > 0 else "❌", "Purchase at least 1 offset from the Marketplace"),
        ]

        st.write("**Requirements to earn your certificate:**")
        all_done = True
        for icon, req in requirements:
            st.write(f"{icon} {req}")
            if icon == "❌":
                all_done = False

        st.divider()
        if all_done:
            st.success("🎉 Congratulations! You have earned the **Climate Champion Certificate**!")
            st.markdown("""
            <div style='border: 3px solid #2ecc71; border-radius: 12px; padding: 2rem; text-align: center; background: #eafaf1;'>
                <h2>🌍 Climate Champion Certificate</h2>
                <p>This certifies that you have demonstrated knowledge and commitment to carbon reduction.</p>
                <p><b>Issued by: Carbon Footprint Navigator</b></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Complete all requirements above to unlock your certificate!")

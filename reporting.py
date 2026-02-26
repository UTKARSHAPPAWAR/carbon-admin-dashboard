import streamlit as st
from datetime import datetime
import io
import database

def show_reporting():
    if st.button("⬅️ Back to Home"):
        st.session_state.view = 'landing'
        st.rerun()

    # Log report generation activity
    username = st.session_state.get('username', 'Guest')
    database.log_activity(username, "Report Generation", "User viewed/generated the sustainability report preview")

    st.title("📄 Professional Sustainability Report")
    st.markdown("Generate a downloadable text-based sustainability report based on all your data.")

    pers_total = st.session_state.get('pers_total', 0)
    ind_total = st.session_state.get('ind_total', 0)
    registry = st.session_state.get('registry_data', [])
    purchased = st.session_state.get('purchased_offsets', 0)
    badges = st.session_state.get('badges', [])

    st.subheader("📝 Report Preview")

    now = datetime.now().strftime("%d %B %Y, %H:%M")
    report_lines = [
        "=" * 60,
        "   CARBON FOOTPRINT NAVIGATOR — SUSTAINABILITY REPORT",
        "=" * 60,
        f"Generated: {now}",
        "",
        "1. PERSONAL CARBON FOOTPRINT",
        "-" * 40,
        f"   Monthly Footprint   : {pers_total:.2f} kg CO2",
        f"   Annual Estimate     : {pers_total * 12 / 1000:.3f} tonnes CO2",
        f"   Daily Average       : {pers_total / 30:.2f} kg CO2",
        "",
        "2. INDUSTRIAL CARBON FOOTPRINT",
        "-" * 40,
        f"   Monthly Footprint   : {ind_total:.2f} kg CO2e",
        f"   Annual Estimate     : {ind_total * 12 / 1000:.3f} tonnes CO2e",
        "",
        "3. CARBON OFFSETS",
        "-" * 40,
        f"   Credits Purchased   : {purchased:.3f} tCO2",
        f"   Net Footprint       : {max(0, (pers_total / 1000) - purchased):.3f} tCO2",
        "",
        "4. REGISTERED OFFSET PROJECTS",
        "-" * 40,
    ]

    if registry:
        for proj in registry:
            report_lines.append(f"   [{proj['ID']}] {proj['Project Name']}")
            report_lines.append(f"         Type: {proj['Type']} | Location: {proj.get('Location', 'N/A')}")
            report_lines.append(f"         Issued: {proj.get('Issued', 0):,} | Retired: {proj.get('Retired', 0):,}")
    else:
        report_lines.append("   No projects registered yet.")

    report_lines += [
        "",
        "5. KEY INSIGHTS",
        "-" * 40,
        f"   Total combined monthly emissions: {(pers_total + ind_total):.2f} kg CO2e",
        f"   Equivalent to planting {int((pers_total + ind_total) / 22)} trees/month to offset.",
        "",
        "=" * 60,
        "   END OF REPORT — Carbon Footprint Navigator v1.0",
        "=" * 60,
    ]

    report_text = "\n".join(report_lines)
    st.code(report_text, language="text")

    # Download Button
    if st.download_button(
        label="⬇️ Download Report (.txt)",
        data=report_text.encode("utf-8"),
        file_name=f"carbon_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        type="primary",
        use_container_width=True
    ):
        database.log_activity(username, "Report Download", "User downloaded the text-based sustainability report")

    st.info("💡 Tip: For a full PDF report, open this file and use your browser's Print → Save as PDF option.")

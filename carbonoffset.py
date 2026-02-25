import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import uuid
import database

def show_registry_page():
    if st.button("⬅️ Back to Home"):
        st.session_state.view = 'landing'
        st.rerun()
    
    st.title("📜 Carbon Offset Registry")
    st.markdown("Browse and manage verified projects dedicated to greenhouse gas reduction.")

    # Registration Form in Expander
    with st.expander("➕ Register a New Project", expanded=False):
        st.subheader("Project Registration Form")
        with st.form("registration_form", clear_on_submit=True):
            p_name = st.text_input("Project Name*")
            p_loc = st.text_input("Location (City, Country)*")
            p_type = st.selectbox("Project Type", ["Nature-based", "Renewable Energy", "Waste Management", "Energy Efficiency", "Other"])
            p_credits = st.number_input("Estimated Carbon Credits (tCO2e)", min_value=0, value=1000)
            p_desc = st.text_area("Project Description")
            p_docs = st.file_uploader("Upload Project Documentation (PDF, Image)", accept_multiple_files=True)
            
            submit_btn = st.form_submit_button("Register Project")
            
            if submit_btn:
                if not p_name or not p_loc:
                    st.error("Please fill in all mandatory fields (*)")
                else:
                    new_project = {
                        "ID": f"REG-{str(uuid.uuid4())[:6].upper()}",
                        "Project Name": p_name,
                        "Developer": "User Registered",
                        "Authority": "Pending Verification",
                        "Type": p_type,
                        "Location": p_loc,
                        "Issued": float(p_credits),
                        "Retired": 0.0,
                        "Description": p_desc,
                        "Status": "Pending"
                    }
                    database.add_project(new_project)
                    st.success(f"Project '{p_name}' has been submitted! It will appear in the registry once verified by an Admin.")
                    st.rerun()

    # Fetch all projects from DB
    all_projects = database.get_projects()
    
    # By default, show only Verified projects in the public registry
    # or show all for admin transparency if they are in this view
    if st.session_state.get('user_role') == 'admin':
        display_projects = all_projects
    else:
        display_projects = [p for p in all_projects if p['status'] == 'Verified']

    if not display_projects:
        st.info("No verified projects are currently available in the registry.")
        return

    df = pd.DataFrame(display_projects)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    type_f = col1.multiselect("Filter Type", options=df["type"].unique(), default=df["type"].unique())
    search_q = col3.text_input("Search Name", "")

    filtered_df = df[df["type"].isin(type_f)]
    if search_q:
        filtered_df = filtered_df[filtered_df["name"].str.contains(search_q, case=False)]

    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    # Visualization
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        fig_pie = px.pie(filtered_df, names="type", values="issued", title="Credits Distribution")
        st.plotly_chart(fig_pie, use_container_width=True)
    with c2:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(x=filtered_df["name"], y=filtered_df["issued"], name="Estimated/Issued"))
        fig_bar.update_layout(title="Project Impact Comparison")
        st.plotly_chart(fig_bar, use_container_width=True)

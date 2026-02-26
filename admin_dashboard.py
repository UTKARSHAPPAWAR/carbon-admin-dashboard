import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import database

def show_admin_dashboard():
    if st.sidebar.button("⬅️ Home / Logout"):
        username = st.session_state.get('username', 'Guest')
        database.log_activity(username, "Logout", "Admin logged out")
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.rerun()

    st.title("🛡️ Admin Control Panel")
    st.markdown("System-wide monitoring, project verification, and sustainability analytics.")

    # Fetch data
    all_projects = database.get_projects()
    pending_projects = [p for p in all_projects if p['status'] == 'Pending' or p['status'] == 'Under Review']
    verified_projects = [p for p in all_projects if p['status'] == 'Verified']
    
    # Overview Metrics
    total_issued = sum(p['issued'] for p in all_projects)
    total_retired = sum(p['retired'] for p in all_projects)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📦 Total Projects", len(all_projects))
    m2.metric("⏳ Pending", len(pending_projects))
    m3.metric("📜 Credits Issued", f"{total_issued:,.0f} tCO2")
    m4.metric("📉 Credits Retired", f"{total_retired:,.0f} tCO2")

    # Purchase metrics
    purchases = database.get_purchases()
    total_purchase_val = sum(p['amount'] for p in purchases)
    st.sidebar.metric("💳 Gross Purchases", f"{total_purchase_val:,.2f} tCO2")

    st.divider()

    # Tabs for Admin Workflow
    tabs = st.tabs(["🚀 Pending Verifications", "📊 System Analytics", "📜 Verified Registry", "🛒 Marketplace", "💳 Purchase History", "🕒 System Activity"])

    with tabs[0]:
        st.subheader("Projects Awaiting Verification")
        if not pending_projects:
            st.info("No projects are currently pending verification.")
        else:
            for p in pending_projects:
                with st.expander(f"**{p['name']}** ({p['type']}) — {p['location']}"):
                    st.write(f"**Description**: {p['description']}")
                    st.write(f"**Estimated Credits**: {p['credits']} tCO2e")
                    st.write(f"**Developer**: {p['developer']}")
                    
                    c1, c2 = st.columns([1, 4])
                    if c1.button("✅ Verify Project", key=f"verify_{p['id']}"):
                        database.update_project_status(p['id'], "Verified")
                        st.success(f"Project '{p['name']}' has been verified and added to the registry!")
                        st.rerun()

    with tabs[1]:
        st.subheader("Sustainability Analytics")
        if all_projects:
            df = pd.DataFrame(all_projects)
            c1, c2 = st.columns(2)
            
            # Credits by Type
            fig_pie = px.pie(df, names="type", values="issued", title="Credits Distribution by Type", hole=0.4)
            c1.plotly_chart(fig_pie, use_container_width=True)
            
            # Status Split
            fig_status = px.bar(df.groupby('status').size().reset_index(name='count'), 
                               x='status', y='count', title="Project Status Overview",
                               color='status', color_discrete_map={'Pending': '#f1c40f', 'Verified': '#2ecc71', 'Under Review': '#e67e22'})
            c2.plotly_chart(fig_status, use_container_width=True)
        else:
            st.info("No data available for analytics yet.")

    with tabs[2]:
        st.subheader("Authenticated Global Registry")
        if verified_projects:
            df_v = pd.DataFrame(verified_projects)
            st.dataframe(df_v[['id', 'name', 'type', 'location', 'issued', 'retired', 'developer']], 
                         use_container_width=True, hide_index=True)
        else:
            st.info("No verified projects found.")

    with tabs[3]:
        st.subheader("Marketplace Monitoring")
        st.markdown("Overview of credit availability and retirement across all projects.")
        if all_projects:
            df_m = pd.DataFrame(all_projects)
            df_m['Available'] = df_m['issued'] - df_m['retired']
            
            fig_m = go.Figure()
            fig_m.add_trace(go.Bar(x=df_m['name'], y=df_m['retired'], name='Retired', marker_color='#e74c3c'))
            fig_m.add_trace(go.Bar(x=df_m['name'], y=df_m['Available'], name='Available', marker_color='#2ecc71'))
            fig_m.update_layout(barmode='stack', title="Credit Inventory by Project")
            st.plotly_chart(fig_m, use_container_width=True)
        else:
            st.info("No marketplace data to display.")

    with tabs[4]:
        st.subheader("Credit Purchase History")
        purchases = database.get_purchases()
        if purchases:
            df_p = pd.DataFrame(purchases)
            st.dataframe(df_p, use_container_width=True, hide_index=True)
        else:
            st.info("No credit purchases recorded in the system yet.")

    with tabs[5]:
        st.subheader("Global System Activity Log")
        all_logs = database.get_all_activity_logs()
        if all_logs:
            log_df = pd.DataFrame(all_logs, columns=["User", "Activity", "Description", "Timestamp"])
            st.dataframe(log_df, use_container_width=True, hide_index=True)
            
            # Analytics on activity
            st.divider()
            st.write("**Activity Distribution**")
            act_counts = log_df['Activity'].value_counts().reset_index()
            act_counts.columns = ['Activity', 'Count']
            fig_act = px.bar(act_counts, x='Activity', y='Count', color='Activity', title="System Usage via Activities")
            st.plotly_chart(fig_act, use_container_width=True)
        else:
            st.info("No activity logs found.")

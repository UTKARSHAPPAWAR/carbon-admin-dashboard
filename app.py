import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import hashlib
from carbonoffset import show_registry_page
from dashboard import show_dashboard
from ai_assistant import show_ai_assistant
from scope3 import show_scope3_calculator
from marketplace import show_marketplace
from reporting import show_reporting
from gamification import show_gamification
from education import show_education
from admin_dashboard import show_admin_dashboard

import database

# --- Initialize Database ---
database.init_db()

# --- Page Configuration ---
st.set_page_config(
    page_title="Carbon Footprint Navigator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed" if 'logged_in' not in st.session_state or not st.session_state.logged_in else "expanded"
)

# --- Session State Initialization ---
if 'view' not in st.session_state:
    st.session_state.view = 'landing'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = 'user'
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'login'
if 'pers_total' not in st.session_state:
    st.session_state.pers_total = 0
if 'ind_total' not in st.session_state:
    st.session_state.ind_total = 0
if 'otp_verified' not in st.session_state:
    st.session_state.otp_verified = False
if 'pending_user' not in st.session_state:
    st.session_state.pending_user = None
if 'generated_otp' not in st.session_state:
    st.session_state.generated_otp = None

# --- Helpers ---
def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def send_otp_email(username, email, otp):
    # Mocking email delivery
    st.info(f"📩 OTP sent to {email} for user {username}")
    print(f"DEBUG: OTP for {username} ({email}) is {otp}")
    return True

# --- Data: Personal Emission Factors ---
EMISSION_FACTORS = {
    "Africa": {
        "South Africa": {"Transportation": 0.28, "Electricity": 0.75, "Diet": 1.35, "Waste": 0.18},
        "Nigeria": {"Transportation": 0.28, "Electricity": 0.75, "Diet": 1.35, "Waste": 0.18},
        "Egypt": {"Transportation": 0.22, "Electricity": 0.55, "Diet": 1.1, "Waste": 0.16},
        "Kenya": {"Transportation": 0.22, "Electricity": 0.55, "Diet": 1.1, "Waste": 0.16},
    },
    "Asia": {
        "India": {"Transportation": 0.17, "Electricity": 0.67, "Diet": 1.72, "Waste": 0.14},
        "China": {"Transportation": 0.17, "Electricity": 0.67, "Diet": 1.72, "Waste": 0.14},
        "Japan": {"Transportation": 0.17, "Electricity": 0.67, "Diet": 1.72, "Waste": 0.14},
        "Pakistan": {"Transportation": 0.18, "Electricity": 0.65, "Diet": 1.7, "Waste": 0.15},
    },
    "Europe": {
        "Germany": {"Transportation": 0.15, "Electricity": 0.33, "Diet": 1.97, "Waste": 0.17},
        "United Kingdom": {"Transportation": 0.15, "Electricity": 0.33, "Diet": 1.97, "Waste": 0.17},
        "France": {"Transportation": 0.15, "Electricity": 0.33, "Diet": 1.97, "Waste": 0.17},
    },
    "North America": {
        "USA": {"Transportation": 0.22, "Electricity": 0.32, "Diet": 2.1, "Waste": 0.18},
        "Canada": {"Transportation": 0.22, "Electricity": 0.32, "Diet": 2.1, "Waste": 0.18},
    },
    "South America": {
        "Brazil": {"Transportation": 0.18, "Electricity": 0.19, "Diet": 1.55, "Waste": 0.13},
        "Argentina": {"Transportation": 0.18, "Electricity": 0.19, "Diet": 1.55, "Waste": 0.13},
    },
    "Oceania": {
        "Australia": {"Transportation": 0.2, "Electricity": 0.52, "Diet": 1.7, "Waste": 0.21},
        "New Zealand": {"Transportation": 0.2, "Electricity": 0.52, "Diet": 1.7, "Waste": 0.21},
    }
}

IND_FACTORS = {
    "Natural Gas (m3)": 2.02, "Diesel (Liters)": 2.68, "Fuel Oil (Liters)": 2.97,
    "Petrol (Liters)": 2.31, "Coal (kg)": 2.42, "LPG (kg)": 2.98,
    "Grid Electricity (kWh)": 0.45, "Renewable Energy (kWh)": 0.02,
    "Business Travel (km)": 0.18, "Waste Generated (kg)": 0.52, "Water Usage (m3)": 0.34
}

# --- UI Components ---
def show_auth():
    st.markdown("""
    <style>
        .auth-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 30px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.auth_mode == 'login':
            if st.session_state.pending_user:
                st.markdown("<h2 style='text-align: center;'>🔑 Two-Step Verification</h2>", unsafe_allow_html=True)
                st.write(f"Enter the 6-digit code sent to your registered email.")
                otp_input = st.text_input("Verification Code", max_chars=6)
                
                if st.button("Verify OTP", use_container_width=True, type="primary"):
                    if otp_input == st.session_state.generated_otp:
                        st.session_state.logged_in = True
                        st.session_state.otp_verified = True
                        role = st.session_state.pending_role
                        st.session_state.username = st.session_state.pending_user
                        st.session_state.user_role = role
                        st.session_state.view = 'admin_dash' if role == 'admin' else 'landing'
                        database.log_activity(st.session_state.username, "Login", "User logged in with 2SV")
                        st.session_state.pending_user = None
                        st.session_state.generated_otp = None
                        st.rerun()
                    else:
                        st.error("Invalid verification code. Please try again.")
                
                if st.button("Cancel", use_container_width=True):
                    st.session_state.pending_user = None
                    st.session_state.generated_otp = None
                    st.rerun()

            else:
                st.markdown("<h2 style='text-align: center;'>🔐 Sign In</h2>", unsafe_allow_html=True)
                
                # Login Type Selection
                login_type = st.radio("Log in as:", ["User", "Admin"], horizontal=True)
                
                username = st.text_input("Username", key="login_user")
                password = st.text_input("Password", type="password", key="login_pass")
                
                if st.button("Log In", use_container_width=True, type="primary"):
                    role = database.verify_user(username, hash_pass(password))
                    if role:
                        if login_type == "Admin" and role != "admin":
                            st.error("Access Denied: You do not have admin privileges.")
                        elif role == "admin":
                            # Admin bypass for OTP in this demo or implement for admin too
                            st.session_state.logged_in = True
                            st.session_state.user_role = role
                            st.session_state.username = username
                            st.session_state.view = 'admin_dash'
                            database.log_activity(username, "Login", "Admin logged in")
                            st.rerun()
                        else:
                            # Trigger 2SV
                            import random
                            st.session_state.generated_otp = str(random.randint(100000, 999999))
                            st.session_state.pending_user = username
                            st.session_state.pending_role = role
                            email = database.get_user_email(username)
                            if not email:
                                # Fallback if no email is set (for old accounts)
                                email = f"{username}@example.com"
                            send_otp_email(username, email, st.session_state.generated_otp)
                            st.rerun()
                    else:
                        st.error("Invalid username or password")
            
            if not st.session_state.pending_user:
                if login_type == "User":
                    c1, c2 = st.columns(2)
                    if c1.button("Create Account", use_container_width=True):
                        st.session_state.auth_mode = 'signup'
                        st.rerun()
                    if c2.button("Forgot Password?", use_container_width=True):
                        st.session_state.auth_mode = 'forgot'
                        st.rerun()
                else:
                    st.info("System Admin Access: Standard credentials required.")

        elif st.session_state.auth_mode == 'signup':
            st.markdown("<h2 style='text-align: center;'>📝 Create Account</h2>", unsafe_allow_html=True)
            new_user = st.text_input("New Username")
            new_email = st.text_input("Email Address (for 2SV)")
            new_pass = st.text_input("New Password", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")
            if st.button("Sign Up", use_container_width=True, type="primary"):
                if not new_email or "@" not in new_email:
                    st.error("Please enter a valid email address")
                elif new_pass != confirm_pass:
                    st.error("Passwords do not match")
                elif len(new_pass) < 6:
                    st.warning("Password should be at least 6 characters")
                else:
                    if database.add_user(new_user, hash_pass(new_pass), email=new_email):
                        st.success("Account created! You can now log in.")
                        st.session_state.auth_mode = 'login'
                        st.rerun()
                    else:
                        st.error("Username already exists")
            if st.button("Back to Login"):
                st.session_state.auth_mode = 'login'
                st.rerun()

        elif st.session_state.auth_mode == 'forgot':
            st.markdown("<h2 style='text-align: center;'>❓ Reset Password</h2>", unsafe_allow_html=True)
            user_to_reset = st.text_input("Enter your username")
            if st.button("Reset (Demo Only)", use_container_width=True, type="primary"):
                # Placeholder for forgot password logic
                st.info(f"Demo Mode: Reset functionality for {user_to_reset} requested.")
            if st.button("Back to Login"):
                st.session_state.auth_mode = 'login'
                st.rerun()

def show_landing_page():
    # Sidebar Info & Logout
    with st.sidebar:
        st.write(f"Logged in as: **{st.session_state.get('username', 'User')}**")
        purchased = st.session_state.get('purchased_offsets', 0)
        st.metric("✅ Total Offsets", f"{purchased:.3f} tCO2")
        
        if st.button("Logout", use_container_width=True):
            username = st.session_state.get('username', 'Guest')
            database.log_activity(username, "Logout", "User logged out")
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("""
    <style>
        .hero-section {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white; padding: 4rem 2rem; border-radius: 15px; text-align: center; margin-bottom: 2rem;
        }
        .info-card {
            background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); height: 100%; transition: transform 0.3s ease;
        }
        .info-card:hover { transform: translateY(-5px); }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-section">
        <h1>🌍 Carbon Footprint Calculator</h1>
        <p style="font-size: 1.5rem; opacity: 0.9;">Welcome back! Monitor and offset your environmental impact.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 🏠 Personal Calculator")
        st.write("Track your individual lifestyle impact.")
        if st.button("Go to Personal", key="goto_p", use_container_width=True, type="primary"):
            st.session_state.view = 'personal'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 🏭 Industrial Calculator")
        st.write("Track organizational Scope 1, 2, and 3 emissions.")
        if st.button("Go to Industrial", key="goto_i", use_container_width=True, type="primary"):
            st.session_state.view = 'industrial'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Analytics Dashboard")
        st.write("Visualize all your results, registry projects, and access the Educational Hub.")
        if st.button("Open Carbon Dashboard", key="goto_dash", use_container_width=True, type="primary"):
            st.session_state.view = 'dashboard'; st.rerun()
        st.link_button("Open Global Stats (External)", "https://ourworldindata.org/co2-and-greenhouse-gas-emissions", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 📜 Carbon Offset Registry")
        st.write("Explore and register authenticated climate projects.")
        if st.button("Open Internal Registry", key="goto_reg", use_container_width=True, type="primary"):
            st.session_state.view = 'registry'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    with col5:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 🤖 AI Reduction Assistant")
        st.write("Get personalized tips to reduce your carbon footprint.")
        if st.button("Open AI Assistant", key="goto_ai", use_container_width=True, type="primary"):
            st.session_state.view = 'ai_assistant'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col6:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 🏭 Full Scope 3 Tracker")
        st.write("All 15 GHG Protocol categories for industrial value chains.")
        if st.button("Open Scope 3 Tracker", key="goto_s3", use_container_width=True, type="primary"):
            st.session_state.view = 'scope3'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col7, col8, col9 = st.columns(3)
    with col7:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 🛒 Carbon Marketplace")
        st.write("Simulate purchasing offsets to achieve Net Zero.")
        if st.button("Open Marketplace", key="goto_mkt", use_container_width=True, type="primary"):
            st.session_state.view = 'marketplace'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col8:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 📄 Reports")
        st.write("Download your professional sustainability report.")
        if st.button("Open Reports", key="goto_rep", use_container_width=True, type="primary"):
            st.session_state.view = 'reporting'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col9:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 🏆 Achievements")
        st.write("Earn badges, track streaks, and explore the Educational Hub.")
        if st.button("Open Achievements", key="goto_game", use_container_width=True, type="primary"):
            st.session_state.view = 'gamification'; st.rerun()
        if st.button("Educational Hub", key="goto_edu", use_container_width=True):
            st.session_state.view = 'education'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def calculate_personal_emission(country_factors, transportation, electricity, diet, waste, petrol=0, diesel=0, lpg=0):
    t_e = transportation * country_factors.get('Transportation', 0)
    e_e = electricity * country_factors.get('Electricity', 0)
    d_e = diet * country_factors.get('Diet', 0)
    w_e = waste * country_factors.get('Waste', 0)
    
    # Fuel emissions
    p_e = petrol * IND_FACTORS.get("Petrol (Liters)", 2.31)
    ds_e = diesel * IND_FACTORS.get("Diesel (Liters)", 2.68)
    l_e = lpg * IND_FACTORS.get("LPG (kg)", 2.98)
    
    total = t_e + e_e + d_e + w_e + p_e + ds_e + l_e
    return total, t_e, e_e, d_e, w_e, p_e, ds_e, l_e

def show_personal_calculator():
    if st.button("⬅️ Back to Home"):
        st.session_state.view = 'landing'; st.rerun()
    st.title("Personal Carbon Emission Calculator")
    
    with st.sidebar:
        st.header("Input Details")
        region = st.selectbox("Select Region", list(EMISSION_FACTORS.keys()))
        country = st.selectbox("Select Country", list(EMISSION_FACTORS[region].keys()))
        t = st.number_input("Transportation (km/month)", value=100)
        e = st.number_input("Electricity (kWh/month)", value=200)
        d = st.number_input("Diet (kg/month)", value=50)
        w = st.number_input("Waste (kg/month)", value=20)
        
        st.divider()
        st.header("📄 Document Verification")
        st.write("Upload supporting documents for a verified footprint.")
        
        with st.expander("👤 Identity & General"):
            v_id = st.file_uploader("Personal Identification (ID/Passport)", type=['pdf', 'jpg', 'png'])
            v_misc = st.file_uploader("Additional Supporting Docs", type=['pdf', 'jpg', 'png'], accept_multiple_files=True)
            
        with st.expander("🚗 Travel & Transport"):
            v_travel = st.file_uploader("Tickets, Fuel Receipts, Mileage Logs", type=['pdf', 'jpg', 'png'], accept_multiple_files=True)
            
        with st.expander("💡 Energy & Utilities"):
            v_elec = st.file_uploader("Electricity & Gas Bills", type=['pdf', 'jpg', 'png'], accept_multiple_files=True)
            
        with st.expander("🍽️ Diet & Lifestyle"):
            v_diet = st.file_uploader("Grocery/Hotel Receipts, Coupons", type=['pdf', 'jpg', 'png'], accept_multiple_files=True)
            
        st.header("⛽ Fuel Usage (Monthly)")
        petrol = st.number_input("Petrol (Liters)", value=0.0)
        diesel = st.number_input("Diesel (Liters)", value=0.0)
        lpg = st.number_input("LPG (kg)", value=0.0)
            
        calc = st.button("Calculate & Verify", type="primary")

    if calc:
        total, t_e, e_e, d_e, w_e, p_e, ds_e, l_e = calculate_personal_emission(EMISSION_FACTORS[region][country], t, e, d, w, petrol, diesel, lpg)
        st.session_state.pers_total = total
        # Save breakdown for AI Assistant
        st.session_state.pers_breakdown = {
            'transport': t_e, 'electricity': e_e, 'diet': d_e, 'waste': w_e,
            'petrol': p_e, 'diesel': ds_e, 'lpg': l_e
        }
        st.session_state.calc_count = st.session_state.get('calc_count', 0) + 1
        
        username = st.session_state.get('username', 'Guest')
        database.log_activity(username, "Footprint Calculation", f"Personal footprint calculated: {total:.2f} kgCO2")

        # Automation: High Emission Alert
        if total > 500:
             st.error(f"🚨 **High Emission Alert!** Your monthly footprint of {total:.2f} kgCO2 is higher than average.")
             database.log_activity(username, "Alert", "High emission alert triggered")

        # Display verification status if files are uploaded
        if any([v_id, v_travel, v_elec, v_diet]):
            st.success("✅ Footprint Verified using uploaded documents")
        else:
            st.warning("⚠️ Footprint Unverified (No documents provided)")
            
        m1, m2, m3 = st.columns(3); m1.metric("Total (kgCO2)", f"{total:.2f}"); m2.metric("Yearly (tCO2)", f"{total*12/1000:.2f}"); m3.metric("Daily (kgCO2)", f"{total/30:.2f}")
        c1, c2 = st.columns(2)
        fig_pie = px.pie(names=['Transport', 'Electricity', 'Diet', 'Waste', 'Fuel'], values=[t_e, e_e, d_e, w_e, p_e+ds_e+l_e], title="Distribution")
        c1.plotly_chart(fig_pie, use_container_width=True)
        fig_bar = px.bar(x=['Transport', 'Electricity', 'Diet', 'Waste', 'Fuel'], y=[t_e, e_e, d_e, w_e, p_e+ds_e+l_e], title="Impact by Category")
        c2.plotly_chart(fig_bar, use_container_width=True)

def show_industrial_calculator():
    if st.button("⬅️ Back to Home"):
        st.session_state.view = 'landing'; st.rerun()
    st.title("🏭 Industrial Calculator")
    with st.sidebar:
        industry = st.selectbox("Industry", ["Manufacturing", "Tech", "Retail", "Energy"])
        rev = st.number_input("Revenue ($)", value=1000000)
    
    tabs = st.tabs(["Scope 1", "Scope 2", "Scope 3"])
    with tabs[0]:
        col1, col2 = st.columns(2)
        gas = col1.number_input("Natural Gas (m3)", value=100.0)
        coal = col2.number_input("Coal (kg)", value=0.0)
        petrol_i = col1.number_input("Petrol (Liters)", value=0.0)
        diesel_i = col2.number_input("Diesel (Liters)", value=0.0)
    with tabs[1]:
        elec = st.number_input("Elec (kWh)", value=500.0)
    with tabs[2]:
        travel = st.number_input("Travel (km)", value=1000.0)

    if st.button("Calculate Industrial", type="primary"):
        s1 = (gas * 2.02) + (coal * 2.42) + (petrol_i * 2.31) + (diesel_i * 2.68)
        s2 = elec * 0.45; s3 = travel * 0.18; total = s1 + s2 + s3
        st.session_state.ind_total = total # Save to session state for dashboard
        
        username = st.session_state.get('username', 'Guest')
        database.log_activity(username, "Industrial Calculation", f"Industrial footprint calculated: {total/1000:.2f} tCO2")

        m1, m2, m3, m4 = st.columns(4); m1.metric("Total (tCO2)", f"{total/1000:.2f}"); m2.metric("S1", f"{s1/1000:.2f}"); m3.metric("S2", f"{s2/1000:.2f}"); m4.metric("S3", f"{s3/1000:.2f}")
        cl, cr = st.columns(2)
        fig_pie = px.pie(names=['S1', 'S2', 'S3'], values=[s1, s2, s3], title="Scope Split")
        cl.plotly_chart(fig_pie, use_container_width=True)
        fig_bar = px.bar(x=['Gas', 'Elec', 'Travel'], y=[s1, s2, s3], title="Source Split")
        cr.plotly_chart(fig_bar, use_container_width=True)

# --- Main Logic ---
if not st.session_state.logged_in:
    show_auth()
else:
    if st.session_state.view == 'landing':
        show_landing_page()
    elif st.session_state.view == 'personal':
        show_personal_calculator()
    elif st.session_state.view == 'industrial':
        show_industrial_calculator()
    elif st.session_state.view == 'registry':
        show_registry_page()
    elif st.session_state.view == 'dashboard':
        show_dashboard()
    elif st.session_state.view == 'ai_assistant':
        show_ai_assistant()
    elif st.session_state.view == 'scope3':
        show_scope3_calculator()
    elif st.session_state.view == 'marketplace':
        show_marketplace()
    elif st.session_state.view == 'reporting':
        show_reporting()
    elif st.session_state.view == 'gamification':
        show_gamification()
    elif st.session_state.view == 'education':
        show_education()
    elif st.session_state.view == 'admin_dash':
        show_admin_dashboard()

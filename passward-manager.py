import streamlit as st
import random
import string
import os
import pandas as pd

# --- UI CONFIG ---
st.set_page_config(page_title="VaultPro Elite", page_icon="🔐", layout="wide")

# --- ADVANCED CUSTOM CSS ---
st.markdown("""
    <style>
    /* Background Gradient */
    .stApp {
        background: radial-gradient(circle at top left, #1e1e2f, #11111d);
        color: #ffffff;
    }

    /* Modern Poppins Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Glassmorphism Cards */
    .bento-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: 0.4s ease;
        text-align: center;
        margin-bottom: 20px;
    }
    .bento-card:hover {
        border: 1px solid #7f5af0;
        transform: translateY(-5px);
        box-shadow: 0 0 20px rgba(127, 90, 240, 0.4);
    }

    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #7f5af0, #2cb67d);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: 700;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        opacity: 0.8;
        box-shadow: 0px 0px 15px #7f5af0;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE LOGIC ---
USER_DB = "users.csv"
VAULT_DB = "vault_data.csv"

def generate_password(length):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def check_strength(password):
    score = 0
    if len(password) >= 8: score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1
    return score

# --- SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'menu_choice' not in st.session_state: st.session_state.menu_choice = "Home"

# --- TOP HEADER ---
st.markdown("<h1 style='text-align: center; color: #7f5af0;'>🛡️ VAULT PRO <span style='color:#2cb67d;'>ELITE</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a1b2;'>The most secure way to manage your digital life.</p>", unsafe_allow_html=True)

# --- BENTO DASHBOARD NAVIGATION ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("<div class='bento-card'><h3>🎲</h3><p>Generator</p></div>", unsafe_allow_html=True)
    if st.button("Open Generator", key="btn_gen"): st.session_state.menu_choice = "Gen"

with col2:
    st.markdown("<div class='bento-card'><h3>⚡</h3><p>Strength</p></div>", unsafe_allow_html=True)
    if st.button("Check Power", key="btn_check"): st.session_state.menu_choice = "Check"

with col3:
    st.markdown("<div class='bento-card'><h3>📥</h3><p>Save</p></div>", unsafe_allow_html=True)
    if st.button("Secure Entry", key="btn_save"): st.session_state.menu_choice = "Save"

with col4:
    st.markdown("<div class='bento-card'><h3>🗝️</h3><p>My Vault</p></div>", unsafe_allow_html=True)
    if st.button("Access Data", key="btn_view"): st.session_state.menu_choice = "View"

st.markdown("---")

# --- FEATURES LOGIC ---
choice = st.session_state.menu_choice

if choice == "Gen":
    st.subheader("🛠️ Smart Password Generator")
    length = st.select_slider("Length of Password", options=range(8, 33), value=16)
    if st.button("Generate Elite Password"):
        p = generate_password(length)
        st.code(p, language="text")
        st.toast("Generated!", icon="✅")

elif choice == "Check":
    st.subheader("📊 Deep Strength Analysis")
    p_input = st.text_input("Enter password to analyze", type="password")
    if p_input:
        s = check_strength(p_input)
        st.progress(s * 25 if s <= 4 else 100)
        st.markdown(f"**Security Score:** {s}/4")

elif choice in ["Save", "View"]:
    if not st.session_state.logged_in:
        st.info("👋 This is a secure zone. Please Log In to continue.")
        # --- LOGIN / SIGNUP UI ---
        t1, t2 = st.tabs(["🔐 Login", "📝 Create Account"])
        with t1:
            email = st.text_input("Email")
            pwd = st.text_input("Password", type="password")
            if st.button("Let Me In"):
                # verify_user function logic here
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.rerun()
    else:
        if choice == "Save":
            st.subheader("📝 Add New Credential")
            with st.container():
                srv = st.text_input("Service Name")
                usr = st.text_input("Username")
                pas = st.text_input("Password", type="password")
                if st.button("Lock It Now"):
                    # save_to_vault logic
                    st.success(f"Encrypted and saved for {srv}!")
        
        elif choice == "View":
            st.subheader("🗄️ Your Encrypted Vault")
            st.warning("Only you can see this data.")
            # Show dataframe logic here
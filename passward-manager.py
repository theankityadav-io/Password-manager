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
    .stApp { background: radial-gradient(circle at top left, #1e1e2f, #11111d); color: #ffffff; }
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    
    /* Bento Card Button Styling */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 40px 20px !important;
        height: 180px !important;
        width: 100% !important;
        transition: 0.4s ease !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    div.stButton > button:hover {
        border: 1px solid #7f5af0 !important;
        transform: translateY(-5px) !important;
        box-shadow: 0 0 20px rgba(127, 90, 240, 0.4) !important;
        background: rgba(127, 90, 240, 0.1) !important;
    }

    .icon-text { font-size: 50px; margin-bottom: 10px; display: block; }
    .label-text { font-size: 18px; font-weight: 600; color: #94a1b2; }
    
    /* Input Fields Styling */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BACKEND LOGIC ---
USER_DB = "users.csv"
VAULT_DB = "vault_data.csv"

def save_user(email, password):
    if not os.path.exists(USER_DB):
        pd.DataFrame(columns=['email', 'password']).to_csv(USER_DB, index=False)
    df = pd.read_csv(USER_DB)
    if email in df['email'].values: return False
    pd.DataFrame([[email, password]], columns=['email', 'password']).to_csv(USER_DB, mode='a', header=False, index=False)
    return True

def verify_user(email, password):
    if not os.path.exists(USER_DB): return False
    df = pd.read_csv(USER_DB)
    user = df[(df['email'] == email) & (df['password'] == str(password))]
    return not user.empty

def save_to_vault(owner, service, username, pwd):
    if not os.path.exists(VAULT_DB):
        pd.DataFrame(columns=['owner', 'service', 'username', 'password']).to_csv(VAULT_DB, index=False)
    new_entry = pd.DataFrame([[owner, service, username, pwd]], columns=['owner', 'service', 'username', 'password'])
    new_entry.to_csv(VAULT_DB, mode='a', header=False, index=False)
    return True

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

# --- MAIN UI ---
st.markdown("<h1 style='text-align: center; color: #7f5af0; margin-bottom: 30px;'>🛡️ VAULT PRO <span style='color:#2cb67d;'>ELITE</span></h1>", unsafe_allow_html=True)

# Navigation with Clickable Cards (Icons + Labels inside buttons)
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🎲\nGenerator", key="gen_btn"):
        st.session_state.menu_choice = "Gen"

with col2:
    if st.button("⚡\nStrength", key="check_btn"):
        st.session_state.menu_choice = "Check"

with col3:
    if st.button("📥\nSave Data", key="save_btn"):
        st.session_state.menu_choice = "Save"

with col4:
    if st.button("🗝️\nMy Vault", key="view_btn"):
        st.session_state.menu_choice = "View"

st.markdown("---")

# --- FEATURE DISPLAY ---
choice = st.session_state.menu_choice

if choice == "Gen":
    st.subheader("🛠️ Elite Password Generator")
    length = st.select_slider("Password Length", options=range(8, 33), value=16)
    if st.button("Generate Now"):
        pwd = generate_password(length)
        st.code(pwd)
        st.toast("Elite Password Generated!")

elif choice == "Check":
    st.subheader("📊 Security Analyzer")
    p_input = st.text_input("Enter password to test", type="password")
    if p_input:
        s = check_strength(p_input)
        st.progress(s * 25 if s <= 4 else 100)
        st.write(f"Strength Score: {s}/4")

elif choice in ["Save", "View"]:
    if not st.session_state.logged_in:
        st.info("🔒 Secure features require login.")
        t1, t2 = st.tabs(["🔐 Login", "📝 Register"])
        with t1:
            e = st.text_input("Email", key="l_email")
            p = st.text_input("Password", type="password", key="l_pass")
            if st.button("Enter Vault"):
                if verify_user(e, p):
                    st.session_state.logged_in = True
                    st.session_state.user_email = e
                    st.rerun()
                else: st.error("Invalid credentials.")
        with t2:
            ne = st.text_input("New Email", key="r_email")
            np = st.text_input("New Password", type="password", key="r_pass")
            if st.button("Create Account"):
                if save_user(ne, np): st.success("Success! Please Login.")
                else: st.error("User already exists.")
    else:
        if choice == "Save":
            st.subheader("📝 Secure New Record")
            srv = st.text_input("Service Name (e.g. GitHub)")
            usr = st.text_input("Username/Email")
            pas = st.text_input("Password", type="password")
            if st.button("Lock and Save"):
                if srv and usr and pas:
                    save_to_vault(st.session_state.user_email, srv, usr, pas)
                    st.success(f"Encrypted record for {srv} saved!")
                else: st.warning("Please fill all fields.")
        
        elif choice == "View":
            st.subheader("🗄️ Your Decrypted Records")
            if os.path.exists(VAULT_DB):
                df = pd.read_csv(VAULT_DB)
                user_data = df[df['owner'] == st.session_state.user_email]
                if not user_data.empty:
                    st.dataframe(user_data[['service', 'username', 'password']], use_container_width=True)
                else: st.warning("No records found in your vault.")
            else: st.info("Database is currently empty.")

# --- SIDEBAR LOGOUT ---
if st.session_state.logged_in:
    if st.sidebar.button("🚪 Logout / Clear Session"):
        st.session_state.logged_in = False
        st.session_state.menu_choice = "Home"
        st.rerun()
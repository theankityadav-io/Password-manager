import streamlit as st
import random
import string
import os
import pandas as pd

# Files
USER_DB = "users.csv"
VAULT_DB = "vault_data.csv"

# --- Functions ---
def check_strength(password):
    score = 0
    if len(password) >= 8: score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1
    return score

def generate_password(length):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def save_user(email, password):
    if not os.path.exists(USER_DB):
        df = pd.DataFrame(columns=['email', 'password'])
        df.to_csv(USER_DB, index=False)
    df = pd.read_csv(USER_DB)
    if email in df['email'].values: return False
    new_user = pd.DataFrame([[email, password]], columns=['email', 'password'])
    new_user.to_csv(USER_DB, mode='a', header=False, index=False)
    return True

def verify_user(email, password):
    if not os.path.exists(USER_DB): return False
    df = pd.read_csv(USER_DB)
    user = df[(df['email'] == email) & (df['password'] == password)]
    return not user.empty

def save_to_vault(owner, service, username, pwd):
    if not os.path.exists(VAULT_DB):
        df = pd.DataFrame(columns=['owner', 'service', 'username', 'password'])
        df.to_csv(VAULT_DB, index=False)
    new_entry = pd.DataFrame([[owner, service, username, pwd]], columns=['owner', 'service', 'username', 'password'])
    new_entry.to_csv(VAULT_DB, mode='a', header=False, index=False)

# --- UI Setup ---
st.set_page_config(page_title="VaultPro", page_icon="🔐")

# Session State Initialization
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'menu_choice' not in st.session_state: st.session_state.menu_choice = "Home"

# --- Authentication Logic ---
if not st.session_state.logged_in:
    st.title("🔐 VaultPro Login")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        e = st.text_input("Email", key="login_email")
        p = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if verify_user(e, p):
                st.session_state.logged_in = True
                st.session_state.user_email = e
                st.success("Login Successful!")
                st.rerun()
            else: st.error("Invalid Credentials")

    with tab2:
        ne = st.text_input("New Email", key="reg_email")
        np = st.text_input("New Password", type="password", key="reg_pass")
        if st.button("Register"):
            if save_user(ne, np): st.success("Account Created! Now Login.")
            else: st.warning("User already exists.")

else:
    # --- LOGGED IN DASHBOARD ---
    st.sidebar.title(f"Welcome, {st.session_state.user_email.split('@')[0]}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("🔐 My Personal Vault")
    
    # Navigation Buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1: 
        if st.button("🎲 Gen"): st.session_state.menu_choice = "Gen"
    with col2: 
        if st.button("➕ Save"): st.session_state.menu_choice = "Save"
    with col3: 
        if st.button("🔍 Check"): st.session_state.menu_choice = "Check"
    with col4: 
        if st.button("🔓 View"): st.session_state.menu_choice = "View"

    st.markdown("---")

    # Feature Logic
    choice = st.session_state.menu_choice

    if choice == "Gen":
        st.subheader("Password Generator")
        l = st.slider("Length", 8, 32, 12)
        if st.button("Generate"): st.code(generate_password(l))

    elif choice == "Save":
        st.subheader("Add to Vault")
        with st.form("save_form"):
            s, u, p = st.text_input("Service"), st.text_input("Username"), st.text_input("Password", type="password")
            if st.form_submit_button("Save"):
                save_to_vault(st.session_state.user_email, s, u, p)
                st.success("Saved!")

    elif choice == "Check":
        st.subheader("Strength Checker")
        cp = st.text_input("Enter Password", type="password")
        if cp:
            score = check_strength(cp)
            st.progress(score * 20)
            st.write(f"Strength: {score}/5")

    elif choice == "View":
        st.subheader("Your Records")
        if os.path.exists(VAULT_DB):
            df = pd.read_csv(VAULT_DB)
            user_data = df[df['owner'] == st.session_state.user_email]
            st.dataframe(user_data[['service', 'username', 'password']], use_container_width=True)
        else: st.info("Empty Vault")

    if st.button("Back to Home"): 
        st.session_state.menu_choice = "Home"
        st.rerun()
import streamlit as st
import hashlib
from database import Database

def init_auth():
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

def login(username: str, password: str) -> bool:
    db = Database()
    user = db.get_user_by_username(username)
    if user and user.password_hash == hashlib.sha256(password.encode()).hexdigest():
        st.session_state.user = user
        st.session_state.authenticated = True
        return True
    return False

def logout():
    st.session_state.user = None
    st.session_state.authenticated = False

def check_auth():
    if not st.session_state.authenticated:
        st.warning("Please log in to access this page")
        st.stop()

def check_role(allowed_roles):
    # Admin has access to all pages
    if st.session_state.user.role == 'admin':
        return True

    if not st.session_state.user or st.session_state.user.role not in allowed_roles:
        st.error("You don't have permission to access this page")
        st.stop()
import streamlit as st
from auth import init_auth, login, logout
from database import Database

st.set_page_config(
    page_title="Làng Hữu Nghị Management System",
    page_icon="🏠",
    layout="wide"
)

def main():
    init_auth()

    st.title("Làng Hữu Nghị Management System")

    if not st.session_state.authenticated:
        with st.form("login_form"):
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                if login(username, password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    else:
        st.sidebar.title(f"Welcome, {st.session_state.user.full_name}")
        st.sidebar.text(f"Role: {st.session_state.user.role}")

        if st.sidebar.button("Logout"):
            logout()
            st.rerun()

        # Display role-specific dashboard
        if st.session_state.user.role == "admin":
            st.header("Admin Dashboard")
            st.write("Welcome to the admin dashboard. Use the sidebar to navigate to different sections.")

        elif st.session_state.user.role == "doctor":
            st.header("Medical Dashboard")
            st.write("Access medical records and patient information through the sidebar menu.")

        elif st.session_state.user.role == "teacher":
            st.header("Teacher Dashboard")
            st.write("View and manage student information using the sidebar menu.")

        elif st.session_state.user.role == "counselor":
            st.header("Counselor Dashboard")
            st.write("Access psychological evaluations and student support information.")

if __name__ == "__main__":
    main()
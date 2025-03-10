import streamlit as st
from auth import init_auth, login, logout
from database import Database
from translations import get_text, set_language, get_current_language

st.set_page_config(
    page_title="Hệ Thống Quản Lý Làng Hữu Nghị",
    page_icon="🏠",
    layout="wide"
)

def main():
    init_auth()

    # Language selector in sidebar
    if st.sidebar.selectbox(
        "Language/Ngôn ngữ",
        ["Tiếng Việt", "English"],
        index=0 if get_current_language() == 'vi' else 1
    ) == "English":
        set_language('en')
    else:
        set_language('vi')

    st.title("Hệ Thống Quản Lý Làng Hữu Nghị - Lang Huu Nghi Management System")

    if not st.session_state.authenticated:
        with st.form("login_form"):
            st.subheader(get_text("login.title"))
            username = st.text_input(get_text("common.username"))
            password = st.text_input(get_text("common.password"), type="password")
            submit = st.form_submit_button(get_text("common.login"))

            if submit:
                if login(username, password):
                    st.success(get_text("login.success"))
                    st.rerun()
                else:
                    st.error(get_text("login.error"))
    else:
        st.sidebar.title(f"{get_text('common.welcome')}, {st.session_state.user.full_name}")
        st.sidebar.text(f"{get_text('common.role')}: {st.session_state.user.role}")

        if st.sidebar.button(get_text("common.logout")):
            logout()
            st.rerun()

        # Display role-specific dashboard
        if st.session_state.user.role == "admin":
            st.header(get_text("dashboard.admin.title"))
            st.write(get_text("dashboard.admin.welcome"))

        elif st.session_state.user.role == "doctor":
            st.header(get_text("dashboard.doctor.title"))
            st.write(get_text("dashboard.doctor.welcome"))

        elif st.session_state.user.role == "teacher":
            st.header(get_text("dashboard.teacher.title"))
            st.write(get_text("dashboard.teacher.welcome"))

        elif st.session_state.user.role == "counselor":
            st.header(get_text("dashboard.counselor.title"))
            st.write(get_text("dashboard.counselor.welcome"))

if __name__ == "__main__":
    main()
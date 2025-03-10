import streamlit as st
from auth import init_auth, login, logout
from database import Database

st.set_page_config(
    page_title="Hệ Thống Quản Lý Làng Hữu Nghị",
    page_icon="🏠",
    layout="wide"
)

def main():
    init_auth()

    st.title("Hệ Thống Quản Lý Làng Hữu Nghị")

    if not st.session_state.authenticated:
        with st.form("login_form"):
            st.subheader("Đăng Nhập")
            username = st.text_input("Tên đăng nhập")
            password = st.text_input("Mật khẩu", type="password")
            submit = st.form_submit_button("Đăng nhập")

            if submit:
                if login(username, password):
                    st.success("Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error("Tên đăng nhập hoặc mật khẩu không đúng")
    else:
        st.sidebar.title(f"Xin chào, {st.session_state.user.full_name}")
        st.sidebar.text(f"Vai trò: {st.session_state.user.role}")

        if st.sidebar.button("Đăng xuất"):
            logout()
            st.rerun()

        # Hiển thị dashboard theo vai trò
        if st.session_state.user.role == "admin":
            st.header("Bảng Điều Khiển Quản Trị")
            st.write("Chào mừng đến với bảng điều khiển quản trị. Sử dụng thanh bên để điều hướng đến các phần khác nhau.")

        elif st.session_state.user.role == "doctor":
            st.header("Bảng Điều Khiển Y Tế")
            st.write("Truy cập hồ sơ y tế và thông tin bệnh nhân thông qua menu bên.")

        elif st.session_state.user.role == "teacher":
            st.header("Bảng Điều Khiển Giáo Viên")
            st.write("Xem và quản lý thông tin sinh viên bằng menu bên.")

        elif st.session_state.user.role == "counselor":
            st.header("Bảng Điều Khiển Tư Vấn")
            st.write("Truy cập đánh giá tâm lý và thông tin hỗ trợ sinh viên.")

if __name__ == "__main__":
    main()
import streamlit as st
from auth import check_auth, check_role
from database import Database
from reports import ReportGenerator
from utils import show_success, show_error

def render():
    check_auth()
    check_role(['admin'])

    st.title("Bảng Điều Khiển Quản Trị")

    db = Database()
    report_gen = ReportGenerator()

    tab1, tab2, tab3 = st.tabs(["Quản Lý Người Dùng", "Báo Cáo", "Thống Kê Hệ Thống"])

    with tab1:
        st.subheader("Thêm Người Dùng Mới")
        with st.form("add_user"):
            username = st.text_input("Tên đăng nhập")
            password = st.text_input("Mật khẩu", type="password")
            role = st.selectbox("Vai trò", [
                "admin", "doctor", "teacher", "counselor",
                "administrative", "nurse"
            ])
            full_name = st.text_input("Họ và tên")

            if st.form_submit_button("Thêm người dùng"):
                if db.add_user(username, password, role, full_name):
                    show_success("Thêm người dùng thành công!")
                else:
                    show_error("Tên đăng nhập đã tồn tại")

    with tab2:
        st.subheader("Tạo Báo Cáo")
        report_type = st.selectbox("Loại báo cáo", ["students", "veterans"])
        if st.button("Tạo báo cáo PDF"):
            pdf_bytes = report_gen.generate_pdf_summary(report_type)
            st.download_button(
                label="Tải xuống báo cáo",
                data=pdf_bytes,
                file_name=f"{report_type}_report.pdf",
                mime="application/pdf"
            )

    with tab3:
        st.subheader("Thống Kê Hệ Thống")

        # Thống kê sinh viên
        student_stats = report_gen.generate_student_statistics()
        st.metric("Tổng số sinh viên", student_stats['total_students'])
        st.plotly_chart(student_stats['health_chart'])
        st.plotly_chart(student_stats['academic_chart'])

        # Thống kê cựu chiến binh
        veteran_stats = report_gen.generate_veteran_statistics()
        st.metric("Tổng số cựu chiến binh", veteran_stats['total_veterans'])
        st.plotly_chart(veteran_stats['health_chart'])

if __name__ == "__main__":
    render()
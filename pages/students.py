import streamlit as st
from streamlit_helpers import translate_sidebar_nav

# Apply sidebar translations
translate_sidebar_nav()
from datetime import datetime
from auth import check_auth, check_role
from database import Database
from utils import show_success, show_error
import io

def render():
    check_auth()
    check_role(['admin', 'teacher'])

    st.title("Quản Lý Sinh Viên")

    db = Database()

    tab1, tab2 = st.tabs(["Danh Sách Sinh Viên", "Thêm Sinh Viên"])

    with tab1:
        students = db.get_students()
        if students:
            for student in students:
                with st.expander(f"Sinh viên: {student.full_name}"):
                    col1, col2 = st.columns([1, 3])

                    with col1:
                        # Hiển thị ảnh hồ sơ nếu có
                        image_data = db.get_student_image(student.id)
                        if image_data:
                            st.image(image_data, caption="Ảnh hồ sơ")
                        else:
                            st.info("Chưa có ảnh hồ sơ")

                        # Tải lên ảnh mới
                        uploaded_file = st.file_uploader(
                            "Cập nhật ảnh hồ sơ",
                            type=['png', 'jpg', 'jpeg'],
                            key=f"student_img_{student.id}"
                        )
                        if uploaded_file:
                            image_bytes = uploaded_file.getvalue()
                            if db.save_student_image(student.id, image_bytes):
                                show_success("Cập nhật ảnh thành công!")
                                st.rerun()
                            else:
                                show_error("Không thể cập nhật ảnh")

                    with col2:
                        st.write(f"Ngày sinh: {student.birth_date}")
                        st.write(f"Địa chỉ: {student.address}")
                        st.write(f"Email: {student.email}")
                        st.write(f"Ngày nhập học: {student.admission_date}")
                        st.write(f"Tình trạng sức khỏe: {student.health_status}")
                        st.write(f"Tình trạng học tập: {student.academic_status}")
        else:
            st.info("Không tìm thấy sinh viên")

    with tab2:
        with st.form("add_student"):
            st.subheader("Thêm Sinh Viên Mới")

            uploaded_file = st.file_uploader(
                "Ảnh hồ sơ",
                type=['png', 'jpg', 'jpeg'],
                key="new_student_img"
            )

            full_name = st.text_input("Họ và tên")
            birth_date = st.date_input("Ngày sinh")
            address = st.text_input("Địa chỉ")
            email = st.text_input("Email")
            admission_date = st.date_input("Ngày nhập học")
            health_status = st.selectbox(
                "Tình trạng sức khỏe", 
                ["Tốt", "Bình thường", "Cần chú ý"]
            )
            academic_status = st.selectbox(
                "Tình trạng học tập",
                ["Xuất sắc", "Tốt", "Trung bình", "Cần cải thiện"]
            )

            if st.form_submit_button("Thêm sinh viên"):
                try:
                    cursor = db.conn.cursor()
                    cursor.execute("""
                        INSERT INTO students (
                            full_name, birth_date, address, email,
                            admission_date, health_status, academic_status
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (full_name, birth_date, address, email,
                          admission_date, health_status, academic_status))

                    student_id = cursor.lastrowid
                    db.conn.commit()

                    if uploaded_file:
                        image_bytes = uploaded_file.getvalue()
                        db.save_student_image(student_id, image_bytes)

                    show_success("Thêm sinh viên thành công!")
                    st.rerun()
                except Exception as e:
                    show_error(f"Lỗi khi thêm sinh viên: {str(e)}")

if __name__ == "__main__":
    render()
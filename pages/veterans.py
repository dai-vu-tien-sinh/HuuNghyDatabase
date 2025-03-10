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
    check_role(['admin', 'doctor'])

    st.title("Quản Lý Cựu Chiến Binh")

    db = Database()

    tab1, tab2 = st.tabs(["Danh Sách Cựu Chiến Binh", "Thêm Cựu Chiến Binh"])

    with tab1:
        veterans = db.get_veterans()
        if veterans:
            for veteran in veterans:
                with st.expander(f"Cựu chiến binh: {veteran.full_name}"):
                    col1, col2 = st.columns([1, 3])

                    with col1:
                        # Hiển thị ảnh hồ sơ nếu có
                        image_data = db.get_veteran_image(veteran.id)
                        if image_data:
                            st.image(image_data, caption="Ảnh hồ sơ")
                        else:
                            st.info("Chưa có ảnh hồ sơ")

                        # Tải lên ảnh mới
                        uploaded_file = st.file_uploader(
                            "Cập nhật ảnh hồ sơ",
                            type=['png', 'jpg', 'jpeg'],
                            key=f"veteran_img_{veteran.id}"
                        )
                        if uploaded_file:
                            image_bytes = uploaded_file.getvalue()
                            if db.save_veteran_image(veteran.id, image_bytes):
                                show_success("Cập nhật ảnh thành công!")
                                st.rerun()
                            else:
                                show_error("Không thể cập nhật ảnh")

                    with col2:
                        st.write(f"Ngày sinh: {veteran.birth_date}")
                        st.write(f"Thời gian phục vụ: {veteran.service_period}")
                        st.write(f"Tình trạng sức khỏe: {veteran.health_condition}")
                        st.write(f"Địa chỉ: {veteran.address}")
                        st.write(f"Email: {veteran.email}")
                        st.write(f"Thông tin liên hệ: {veteran.contact_info}")
        else:
            st.info("Không tìm thấy cựu chiến binh")

    with tab2:
        with st.form("add_veteran"):
            st.subheader("Thêm Cựu Chiến Binh Mới")

            uploaded_file = st.file_uploader(
                "Ảnh hồ sơ",
                type=['png', 'jpg', 'jpeg'],
                key="new_veteran_img"
            )

            full_name = st.text_input("Họ và tên")
            birth_date = st.date_input("Ngày sinh")
            service_period = st.text_input("Thời gian phục vụ")
            health_condition = st.selectbox(
                "Tình trạng sức khỏe",
                ["Tốt", "Bình thường", "Cần chú ý"]
            )
            address = st.text_input("Địa chỉ")
            email = st.text_input("Email")
            contact_info = st.text_input("Thông tin liên hệ")

            if st.form_submit_button("Thêm cựu chiến binh"):
                try:
                    cursor = db.conn.cursor()
                    cursor.execute("""
                        INSERT INTO veterans (
                            full_name, birth_date, service_period,
                            health_condition, address, email, contact_info
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (full_name, birth_date, service_period,
                          health_condition, address, email, contact_info))

                    veteran_id = cursor.lastrowid
                    db.conn.commit()

                    if uploaded_file:
                        image_bytes = uploaded_file.getvalue()
                        db.save_veteran_image(veteran_id, image_bytes)

                    show_success("Thêm cựu chiến binh thành công!")
                    st.rerun()
                except Exception as e:
                    show_error(f"Lỗi khi thêm cựu chiến binh: {str(e)}")

if __name__ == "__main__":
    render()
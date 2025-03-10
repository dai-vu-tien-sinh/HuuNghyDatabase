import streamlit as st
from datetime import datetime
from auth import check_auth, check_role
from database import Database
from utils import show_success, show_error

def render():
    check_auth()
    check_role(['doctor'])

    st.title("Quản Lý Hồ Sơ Y Tế")

    db = Database()

    tab1, tab2 = st.tabs(["Xem Hồ Sơ", "Thêm Hồ Sơ"])

    with tab1:
        records = db.conn.execute("""
            SELECT mr.*, u.full_name as doctor_name,
            CASE 
                WHEN mr.patient_type = 'student' THEN s.email
                WHEN mr.patient_type = 'veteran' THEN v.email
            END as patient_email
            FROM medical_records mr
            JOIN users u ON mr.doctor_id = u.id
            LEFT JOIN students s ON mr.patient_id = s.id AND mr.patient_type = 'student'
            LEFT JOIN veterans v ON mr.patient_id = v.id AND mr.patient_type = 'veteran'
            ORDER BY mr.date DESC
        """).fetchall()

        if records:
            for record in records:
                with st.expander(f"Hồ sơ #{record[0]} - {record[2]} {record[1]}"):
                    st.write(f"Chẩn đoán: {record[3]}")
                    st.write(f"Điều trị: {record[4]}")
                    st.write(f"Bác sĩ: {record[-2]}")
                    st.write(f"Ngày: {record[6]}")
                    if record[-1]:  # If patient has email
                        if not record[8]:  # If notification not sent
                            if st.button(f"Gửi thông báo email", key=f"notify_{record[0]}"):
                                if db.send_medical_record_notification(record[0]):
                                    show_success("Đã gửi thông báo thành công!")
                                    st.rerun()
                                else:
                                    show_error("Không thể gửi thông báo")
                        else:
                            st.info("Đã gửi thông báo ✓")
                    else:
                        st.warning("Không có email bệnh nhân")
        else:
            st.info("Không tìm thấy hồ sơ y tế")

    with tab2:
        with st.form("add_medical_record"):
            st.subheader("Thêm Hồ Sơ Y Tế Mới")

            patient_type = st.selectbox("Loại bệnh nhân", ["student", "veteran"])
            patient_id = st.number_input("ID Bệnh nhân", min_value=1, step=1)
            diagnosis = st.text_area("Chẩn đoán")
            treatment = st.text_area("Điều trị")
            notes = st.text_area("Ghi chú thêm")

            send_notification = st.checkbox("Gửi thông báo email")

            if st.form_submit_button("Thêm hồ sơ"):
                try:
                    record_id = db.add_medical_record({
                        "patient_id": patient_id,
                        "patient_type": patient_type,
                        "diagnosis": diagnosis,
                        "treatment": treatment,
                        "doctor_id": st.session_state.user.id,
                        "notes": notes
                    })

                    if record_id:
                        show_success("Thêm hồ sơ y tế thành công!")
                        if send_notification:
                            if db.send_medical_record_notification(record_id):
                                show_success("Đã gửi thông báo thành công!")
                            else:
                                show_error("Không thể gửi thông báo")
                        st.rerun()
                except Exception as e:
                    show_error(f"Lỗi khi thêm hồ sơ y tế: {str(e)}")

if __name__ == "__main__":
    render()
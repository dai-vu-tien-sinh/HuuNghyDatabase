
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

    tab1, tab2, tab3 = st.tabs(["Xem Hồ Sơ", "Thêm Hồ Sơ", "Thông Tin Gia Đình"])

    with tab1:
        records = db.conn.execute("""
            SELECT mr.*, u.full_name as doctor_name,
            CASE 
                WHEN mr.patient_type = 'student' THEN s.email
                WHEN mr.patient_type = 'veteran' THEN v.email
            END as patient_email,
            CASE 
                WHEN mr.patient_type = 'student' THEN s.full_name
                WHEN mr.patient_type = 'veteran' THEN v.full_name
            END as patient_name
            FROM medical_records mr
            JOIN users u ON mr.doctor_id = u.id
            LEFT JOIN students s ON mr.patient_id = s.id AND mr.patient_type = 'student'
            LEFT JOIN veterans v ON mr.patient_id = v.id AND mr.patient_type = 'veteran'
            ORDER BY mr.date DESC
        """).fetchall()

        if records:
            for record in records:
                with st.expander(f"Hồ sơ #{record[0]} - {record[-1]} ({record[2]} {record[1]})"):
                    st.write(f"Chẩn đoán: {record[3]}")
                    st.write(f"Điều trị: {record[4]}")
                    st.write(f"Bác sĩ: {record[-3]}")
                    st.write(f"Ngày: {record[6]}")
                    
                    # Check if family info exists
                    family_info = db.get_family_info(record[1], record[2])
                    if family_info:
                        with st.expander("Thông tin gia đình"):
                            st.write(f"Họ tên bố: {family_info['father_name']}")
                            st.write(f"Họ tên mẹ: {family_info['mother_name']}")
                            st.write(f"Số thứ tự con: {family_info['birth_order']}")
                            st.write(f"Nghề nghiệp: {family_info['occupation']}")
                            st.write(f"Thông tin người giám hộ: {family_info['caregiver_info']}")
                    else:
                        st.info("Chưa có thông tin gia đình")
                        
                    if record[-2]:  # If patient has email
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
    
    with tab3:
        st.subheader("Quản lý thông tin gia đình")
        
        patient_type = st.selectbox("Loại bệnh nhân", ["student", "veteran"], key="family_patient_type")
        patient_id = st.number_input("ID Bệnh nhân", min_value=1, step=1, key="family_patient_id")
        
        # Kiểm tra xem bệnh nhân có tồn tại không
        patient_exists = False
        patient_name = ""
        
        if patient_type == "student":
            cursor = db.conn.cursor()
            cursor.execute("SELECT full_name FROM students WHERE id = ?", (patient_id,))
            result = cursor.fetchone()
            if result:
                patient_exists = True
                patient_name = result[0]
        else:
            cursor = db.conn.cursor()
            cursor.execute("SELECT full_name FROM veterans WHERE id = ?", (patient_id,))
            result = cursor.fetchone()
            if result:
                patient_exists = True
                patient_name = result[0]
        
        if patient_exists:
            st.success(f"Bệnh nhân: {patient_name}")
            
            # Kiểm tra xem đã có thông tin gia đình chưa
            family_info = db.get_family_info(patient_id, patient_type)
            
            with st.form("family_info_form"):
                father_name = st.text_input("Họ và tên bố", value=family_info["father_name"] if family_info else "")
                mother_name = st.text_input("Họ và tên mẹ", value=family_info["mother_name"] if family_info else "")
                birth_order = st.number_input("Số thứ tự con", min_value=1, value=family_info["birth_order"] if family_info else 1)
                occupation = st.text_input("Nghề nghiệp", value=family_info["occupation"] if family_info else "")
                caregiver_info = st.text_area("Thông tin về người giám hộ", value=family_info["caregiver_info"] if family_info else "")
                
                if st.form_submit_button("Lưu thông tin"):
                    info_data = {
                        "patient_id": patient_id,
                        "patient_type": patient_type,
                        "father_name": father_name,
                        "mother_name": mother_name,
                        "birth_order": birth_order,
                        "occupation": occupation,
                        "caregiver_info": caregiver_info
                    }
                    
                    if family_info:
                        # Cập nhật thông tin gia đình
                        if db.update_family_info(family_info["id"], info_data):
                            show_success("Cập nhật thông tin gia đình thành công!")
                            st.rerun()
                        else:
                            show_error("Không thể cập nhật thông tin gia đình")
                    else:
                        # Thêm mới thông tin gia đình
                        if db.add_family_info(info_data):
                            show_success("Thêm thông tin gia đình thành công!")
                            st.rerun()
                        else:
                            show_error("Không thể thêm thông tin gia đình")
        else:
            st.error("Không tìm thấy bệnh nhân với ID này")

if __name__ == "__main__":
    render()

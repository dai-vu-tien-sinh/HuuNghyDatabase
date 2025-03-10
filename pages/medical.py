import streamlit as st
from datetime import datetime
from auth import check_auth, check_role
from database import Database
from utils import show_success, show_error

def render():
    check_auth()
    check_role(['doctor'])

    st.title("Medical Records Management")

    db = Database()

    tab1, tab2 = st.tabs(["View Records", "Add Record"])

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
                with st.expander(f"Record #{record[0]} - {record[2]} {record[1]}"):
                    st.write(f"Diagnosis: {record[3]}")
                    st.write(f"Treatment: {record[4]}")
                    st.write(f"Doctor: {record[-2]}")
                    st.write(f"Date: {record[6]}")
                    if record[-1]:  # If patient has email
                        if not record[8]:  # If notification not sent
                            if st.button(f"Send Email Notification", key=f"notify_{record[0]}"):
                                if db.send_medical_record_notification(record[0]):
                                    show_success("Notification sent successfully!")
                                    st.experimental_rerun()
                                else:
                                    show_error("Failed to send notification")
                        else:
                            st.info("Notification sent ✓")
                    else:
                        st.warning("No patient email available")
        else:
            st.info("No medical records found")

    with tab2:
        with st.form("add_medical_record"):
            st.subheader("Add New Medical Record")

            patient_type = st.selectbox("Patient Type", ["student", "veteran"])
            patient_id = st.number_input("Patient ID", min_value=1, step=1)
            diagnosis = st.text_area("Diagnosis")
            treatment = st.text_area("Treatment")
            notes = st.text_area("Additional Notes")

            send_notification = st.checkbox("Send email notification")

            if st.form_submit_button("Add Record"):
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
                        show_success("Medical record added successfully!")
                        if send_notification:
                            if db.send_medical_record_notification(record_id):
                                show_success("Notification sent successfully!")
                            else:
                                show_error("Failed to send notification")
                        st.experimental_rerun()
                except Exception as e:
                    show_error(f"Error adding medical record: {str(e)}")

if __name__ == "__main__":
    render()
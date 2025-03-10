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
            SELECT mr.*, u.full_name as doctor_name 
            FROM medical_records mr
            JOIN users u ON mr.doctor_id = u.id
            ORDER BY mr.date DESC
        """).fetchall()
        
        if records:
            record_data = []
            for record in records:
                record_data.append({
                    "ID": record[0],
                    "Patient ID": record[1],
                    "Patient Type": record[2],
                    "Diagnosis": record[3],
                    "Treatment": record[4],
                    "Doctor": record[-1],
                    "Date": record[6]
                })
            st.dataframe(record_data)
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
            
            if st.form_submit_button("Add Record"):
                try:
                    db.add_medical_record({
                        "patient_id": patient_id,
                        "patient_type": patient_type,
                        "diagnosis": diagnosis,
                        "treatment": treatment,
                        "doctor_id": st.session_state.user.id,
                        "notes": notes
                    })
                    show_success("Medical record added successfully!")
                except Exception as e:
                    show_error(f"Error adding medical record: {str(e)}")

if __name__ == "__main__":
    render()

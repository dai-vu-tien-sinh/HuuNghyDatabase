import streamlit as st
from datetime import datetime
from auth import check_auth, check_role
from database import Database
from utils import show_success, show_error

def render():
    check_auth()
    check_role(['admin', 'teacher'])
    
    st.title("Student Management")
    
    db = Database()
    
    tab1, tab2 = st.tabs(["Student List", "Add Student"])
    
    with tab1:
        students = db.get_students()
        if students:
            student_data = []
            for student in students:
                student_data.append({
                    "ID": student.id,
                    "Name": student.full_name,
                    "Birth Date": student.birth_date,
                    "Academic Status": student.academic_status,
                    "Health Status": student.health_status
                })
            st.dataframe(student_data)
        else:
            st.info("No students found")
    
    with tab2:
        with st.form("add_student"):
            st.subheader("Add New Student")
            full_name = st.text_input("Full Name")
            birth_date = st.date_input("Birth Date")
            address = st.text_input("Address")
            admission_date = st.date_input("Admission Date")
            health_status = st.selectbox("Health Status", 
                ["Good", "Fair", "Needs Attention"])
            academic_status = st.selectbox("Academic Status",
                ["Excellent", "Good", "Average", "Needs Improvement"])
            
            if st.form_submit_button("Add Student"):
                try:
                    cursor = db.conn.cursor()
                    cursor.execute("""
                        INSERT INTO students (
                            full_name, birth_date, address, admission_date,
                            health_status, academic_status
                        ) VALUES (?, ?, ?, ?, ?, ?)
                    """, (full_name, birth_date, address, admission_date,
                          health_status, academic_status))
                    db.conn.commit()
                    show_success("Student added successfully!")
                except Exception as e:
                    show_error(f"Error adding student: {str(e)}")

if __name__ == "__main__":
    render()

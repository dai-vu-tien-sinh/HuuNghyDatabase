import streamlit as st
from datetime import datetime
from auth import check_auth, check_role
from database import Database
from utils import show_success, show_error
import io

def render():
    check_auth()
    check_role(['admin', 'teacher'])

    st.title("Student Management")

    db = Database()

    tab1, tab2 = st.tabs(["Student List", "Add Student"])

    with tab1:
        students = db.get_students()
        if students:
            for student in students:
                with st.expander(f"Student: {student.full_name}"):
                    col1, col2 = st.columns([1, 3])

                    with col1:
                        # Display profile image if exists
                        image_data = db.get_student_image(student.id)
                        if image_data:
                            st.image(image_data, caption="Profile Image")
                        else:
                            st.info("No profile image")

                        # Upload new image
                        uploaded_file = st.file_uploader(
                            "Update profile image",
                            type=['png', 'jpg', 'jpeg'],
                            key=f"student_img_{student.id}"
                        )
                        if uploaded_file:
                            image_bytes = uploaded_file.getvalue()
                            if db.save_student_image(student.id, image_bytes):
                                show_success("Image updated successfully!")
                                st.rerun()
                            else:
                                show_error("Failed to update image")

                    with col2:
                        st.write(f"Birth Date: {student.birth_date}")
                        st.write(f"Address: {student.address}")
                        st.write(f"Email: {student.email}")
                        st.write(f"Admission Date: {student.admission_date}")
                        st.write(f"Health Status: {student.health_status}")
                        st.write(f"Academic Status: {student.academic_status}")
        else:
            st.info("No students found")

    with tab2:
        with st.form("add_student"):
            st.subheader("Add New Student")

            uploaded_file = st.file_uploader(
                "Profile Image",
                type=['png', 'jpg', 'jpeg'],
                key="new_student_img"
            )

            full_name = st.text_input("Full Name")
            birth_date = st.date_input("Birth Date")
            address = st.text_input("Address")
            email = st.text_input("Email")
            admission_date = st.date_input("Admission Date")
            health_status = st.selectbox(
                "Health Status", 
                ["Good", "Fair", "Needs Attention"]
            )
            academic_status = st.selectbox(
                "Academic Status",
                ["Excellent", "Good", "Average", "Needs Improvement"]
            )

            if st.form_submit_button("Add Student"):
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

                    show_success("Student added successfully!")
                    st.rerun()
                except Exception as e:
                    show_error(f"Error adding student: {str(e)}")

if __name__ == "__main__":
    render()
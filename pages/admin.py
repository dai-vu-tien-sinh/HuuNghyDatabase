import streamlit as st
from auth import check_auth, check_role
from database import Database
from reports import ReportGenerator
from utils import show_success, show_error

def render():
    check_auth()
    check_role(['admin'])
    
    st.title("Administrative Dashboard")
    
    db = Database()
    report_gen = ReportGenerator()
    
    tab1, tab2, tab3 = st.tabs(["User Management", "Reports", "System Statistics"])
    
    with tab1:
        st.subheader("Add New User")
        with st.form("add_user"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", [
                "admin", "doctor", "teacher", "counselor",
                "administrative", "nurse"
            ])
            full_name = st.text_input("Full Name")
            
            if st.form_submit_button("Add User"):
                if db.add_user(username, password, role, full_name):
                    show_success("User added successfully!")
                else:
                    show_error("Username already exists")
    
    with tab2:
        st.subheader("Generate Reports")
        report_type = st.selectbox("Report Type", ["students", "veterans"])
        if st.button("Generate PDF Report"):
            pdf_bytes = report_gen.generate_pdf_summary(report_type)
            st.download_button(
                label="Download Report",
                data=pdf_bytes,
                file_name=f"{report_type}_report.pdf",
                mime="application/pdf"
            )
    
    with tab3:
        st.subheader("System Statistics")
        
        # Student Statistics
        student_stats = report_gen.generate_student_statistics()
        st.metric("Total Students", student_stats['total_students'])
        st.plotly_chart(student_stats['health_chart'])
        st.plotly_chart(student_stats['academic_chart'])
        
        # Veteran Statistics
        veteran_stats = report_gen.generate_veteran_statistics()
        st.metric("Total Veterans", veteran_stats['total_veterans'])
        st.plotly_chart(veteran_stats['health_chart'])

if __name__ == "__main__":
    render()

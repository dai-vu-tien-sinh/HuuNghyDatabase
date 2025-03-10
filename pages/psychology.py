import streamlit as st
from datetime import datetime
from auth import check_auth, check_role
from database import Database
from utils import show_success, show_error

def render():
    check_auth()
    check_role(['counselor'])
    
    st.title("Psychological Evaluation Management")
    
    db = Database()
    
    tab1, tab2 = st.tabs(["View Evaluations", "Add Evaluation"])
    
    with tab1:
        evaluations = db.conn.execute("""
            SELECT pe.*, s.full_name as student_name, u.full_name as evaluator_name
            FROM psychological_evaluations pe
            JOIN students s ON pe.student_id = s.id
            JOIN users u ON pe.evaluator_id = u.id
            ORDER BY pe.evaluation_date DESC
        """).fetchall()
        
        if evaluations:
            eval_data = []
            for eval in evaluations:
                eval_data.append({
                    "ID": eval[0],
                    "Student": eval[-2],
                    "Evaluation Date": eval[2],
                    "Evaluator": eval[-1],
                    "Assessment": eval[4][:50] + "..."
                })
            st.dataframe(eval_data)
        else:
            st.info("No psychological evaluations found")
    
    with tab2:
        with st.form("add_psychological_evaluation"):
            st.subheader("Add New Psychological Evaluation")
            
            student_id = st.number_input("Student ID", min_value=1, step=1)
            assessment = st.text_area("Assessment")
            recommendations = st.text_area("Recommendations")
            follow_up_date = st.date_input("Follow-up Date")
            
            if st.form_submit_button("Add Evaluation"):
                try:
                    db.add_psychological_evaluation({
                        "student_id": student_id,
                        "evaluator_id": st.session_state.user.id,
                        "assessment": assessment,
                        "recommendations": recommendations,
                        "follow_up_date": follow_up_date
                    })
                    show_success("Psychological evaluation added successfully!")
                except Exception as e:
                    show_error(f"Error adding evaluation: {str(e)}")

if __name__ == "__main__":
    render()

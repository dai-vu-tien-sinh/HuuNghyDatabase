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
            SELECT pe.*, s.full_name as student_name, u.full_name as evaluator_name,
                   s.email as student_email
            FROM psychological_evaluations pe
            JOIN students s ON pe.student_id = s.id
            JOIN users u ON pe.evaluator_id = u.id
            ORDER BY pe.evaluation_date DESC
        """).fetchall()

        if evaluations:
            for eval in evaluations:
                with st.expander(f"Evaluation #{eval[0]} - {eval[-3]}"):
                    st.write(f"Date: {eval[2]}")
                    st.write(f"Evaluator: {eval[-2]}")
                    st.write(f"Assessment: {eval[4]}")
                    st.write(f"Recommendations: {eval[5]}")
                    if eval[6]:
                        st.write(f"Follow-up Date: {eval[6]}")

                    if eval[-1]:  # If student has email
                        if not eval[7]:  # If notification not sent
                            if st.button(f"Send Email Notification", key=f"notify_{eval[0]}"):
                                if db.send_psychological_evaluation_notification(eval[0]):
                                    show_success("Notification sent successfully!")
                                    st.experimental_rerun()
                                else:
                                    show_error("Failed to send notification")
                        else:
                            st.info("Notification sent ✓")
                    else:
                        st.warning("No student email available")
        else:
            st.info("No psychological evaluations found")

    with tab2:
        with st.form("add_psychological_evaluation"):
            st.subheader("Add New Psychological Evaluation")

            student_id = st.number_input("Student ID", min_value=1, step=1)
            assessment = st.text_area("Assessment")
            recommendations = st.text_area("Recommendations")
            follow_up_date = st.date_input("Follow-up Date")

            send_notification = st.checkbox("Send email notification")

            if st.form_submit_button("Add Evaluation"):
                try:
                    eval_id = db.add_psychological_evaluation({
                        "student_id": student_id,
                        "evaluator_id": st.session_state.user.id,
                        "assessment": assessment,
                        "recommendations": recommendations,
                        "follow_up_date": follow_up_date
                    })

                    if eval_id:
                        show_success("Psychological evaluation added successfully!")
                        if send_notification:
                            if db.send_psychological_evaluation_notification(eval_id):
                                show_success("Notification sent successfully!")
                            else:
                                show_error("Failed to send notification")
                        st.experimental_rerun()
                except Exception as e:
                    show_error(f"Error adding evaluation: {str(e)}")

if __name__ == "__main__":
    render()
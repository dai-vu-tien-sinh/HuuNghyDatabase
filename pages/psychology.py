import streamlit as st
from datetime import datetime
from auth import check_auth, check_role
from database import Database
from utils import show_success, show_error

def render():
    check_auth()
    check_role(['counselor'])

    st.title("Quản Lý Đánh Giá Tâm Lý")

    db = Database()

    tab1, tab2 = st.tabs(["Xem Đánh Giá", "Thêm Đánh Giá"])

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
                with st.expander(f"Đánh giá #{eval[0]} - {eval[-3]}"):
                    st.write(f"Ngày: {eval[2]}")
                    st.write(f"Người đánh giá: {eval[-2]}")
                    st.write(f"Đánh giá: {eval[4]}")
                    st.write(f"Khuyến nghị: {eval[5]}")
                    if eval[6]:
                        st.write(f"Ngày theo dõi tiếp: {eval[6]}")

                    if eval[-1]:  # If student has email
                        if not eval[7]:  # If notification not sent
                            if st.button(f"Gửi thông báo email", key=f"notify_{eval[0]}"):
                                if db.send_psychological_evaluation_notification(eval[0]):
                                    show_success("Đã gửi thông báo thành công!")
                                    st.rerun()
                                else:
                                    show_error("Không thể gửi thông báo")
                        else:
                            st.info("Đã gửi thông báo ✓")
                    else:
                        st.warning("Không có email sinh viên")
        else:
            st.info("Không tìm thấy đánh giá tâm lý")

    with tab2:
        with st.form("add_psychological_evaluation"):
            st.subheader("Thêm Đánh Giá Tâm Lý Mới")

            student_id = st.number_input("ID Sinh viên", min_value=1, step=1)
            assessment = st.text_area("Đánh giá")
            recommendations = st.text_area("Khuyến nghị")
            follow_up_date = st.date_input("Ngày theo dõi tiếp")

            send_notification = st.checkbox("Gửi thông báo email")

            if st.form_submit_button("Thêm đánh giá"):
                try:
                    eval_id = db.add_psychological_evaluation({
                        "student_id": student_id,
                        "evaluator_id": st.session_state.user.id,
                        "assessment": assessment,
                        "recommendations": recommendations,
                        "follow_up_date": follow_up_date
                    })

                    if eval_id:
                        show_success("Thêm đánh giá tâm lý thành công!")
                        if send_notification:
                            if db.send_psychological_evaluation_notification(eval_id):
                                show_success("Đã gửi thông báo thành công!")
                            else:
                                show_error("Không thể gửi thông báo")
                        st.rerun()
                except Exception as e:
                    show_error(f"Lỗi khi thêm đánh giá: {str(e)}")

if __name__ == "__main__":
    render()
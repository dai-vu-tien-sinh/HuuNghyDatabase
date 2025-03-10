import streamlit as st
from datetime import datetime
from auth import check_auth, check_role
from database import Database
from utils import show_success, show_error
import io

def render():
    check_auth()
    check_role(['admin', 'doctor'])

    st.title("Veteran Management")

    db = Database()

    tab1, tab2 = st.tabs(["Veteran List", "Add Veteran"])

    with tab1:
        veterans = db.get_veterans()
        if veterans:
            for veteran in veterans:
                with st.expander(f"Veteran: {veteran.full_name}"):
                    col1, col2 = st.columns([1, 3])

                    with col1:
                        # Display profile image if exists
                        image_data = db.get_veteran_image(veteran.id)
                        if image_data:
                            st.image(image_data, caption="Profile Image")
                        else:
                            st.info("No profile image")

                        # Upload new image
                        uploaded_file = st.file_uploader(
                            "Update profile image",
                            type=['png', 'jpg', 'jpeg'],
                            key=f"veteran_img_{veteran.id}"
                        )
                        if uploaded_file:
                            image_bytes = uploaded_file.getvalue()
                            if db.save_veteran_image(veteran.id, image_bytes):
                                show_success("Image updated successfully!")
                                st.rerun()
                            else:
                                show_error("Failed to update image")

                    with col2:
                        st.write(f"Birth Date: {veteran.birth_date}")
                        st.write(f"Service Period: {veteran.service_period}")
                        st.write(f"Health Condition: {veteran.health_condition}")
                        st.write(f"Address: {veteran.address}")
                        st.write(f"Email: {veteran.email}")
                        st.write(f"Contact Info: {veteran.contact_info}")
        else:
            st.info("No veterans found")

    with tab2:
        with st.form("add_veteran"):
            st.subheader("Add New Veteran")

            uploaded_file = st.file_uploader(
                "Profile Image",
                type=['png', 'jpg', 'jpeg'],
                key="new_veteran_img"
            )

            full_name = st.text_input("Full Name")
            birth_date = st.date_input("Birth Date")
            service_period = st.text_input("Service Period")
            health_condition = st.selectbox(
                "Health Condition",
                ["Good", "Fair", "Needs Attention"]
            )
            address = st.text_input("Address")
            email = st.text_input("Email")
            contact_info = st.text_input("Contact Information")

            if st.form_submit_button("Add Veteran"):
                try:
                    cursor = db.conn.cursor()
                    cursor.execute("""
                        INSERT INTO veterans (
                            full_name, birth_date, service_period,
                            health_condition, address, email, contact_info
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (full_name, birth_date, service_period,
                          health_condition, address, email, contact_info))

                    veteran_id = cursor.lastrowid
                    db.conn.commit()

                    if uploaded_file:
                        image_bytes = uploaded_file.getvalue()
                        db.save_veteran_image(veteran_id, image_bytes)

                    show_success("Veteran added successfully!")
                    st.rerun()
                except Exception as e:
                    show_error(f"Error adding veteran: {str(e)}")

if __name__ == "__main__":
    render()
import streamlit as st
from datetime import datetime
from auth import check_auth, check_role
from database import Database
from utils import show_success, show_error

def render():
    check_auth()
    check_role(['admin', 'doctor'])
    
    st.title("Veteran Management")
    
    db = Database()
    
    tab1, tab2 = st.tabs(["Veteran List", "Add Veteran"])
    
    with tab1:
        veterans = db.get_veterans()
        if veterans:
            veteran_data = []
            for veteran in veterans:
                veteran_data.append({
                    "ID": veteran.id,
                    "Name": veteran.full_name,
                    "Birth Date": veteran.birth_date,
                    "Service Period": veteran.service_period,
                    "Health Condition": veteran.health_condition
                })
            st.dataframe(veteran_data)
        else:
            st.info("No veterans found")
    
    with tab2:
        with st.form("add_veteran"):
            st.subheader("Add New Veteran")
            full_name = st.text_input("Full Name")
            birth_date = st.date_input("Birth Date")
            service_period = st.text_input("Service Period")
            health_condition = st.selectbox("Health Condition",
                ["Good", "Fair", "Needs Attention"])
            address = st.text_input("Address")
            contact_info = st.text_input("Contact Information")
            
            if st.form_submit_button("Add Veteran"):
                try:
                    cursor = db.conn.cursor()
                    cursor.execute("""
                        INSERT INTO veterans (
                            full_name, birth_date, service_period,
                            health_condition, address, contact_info
                        ) VALUES (?, ?, ?, ?, ?, ?)
                    """, (full_name, birth_date, service_period,
                          health_condition, address, contact_info))
                    db.conn.commit()
                    show_success("Veteran added successfully!")
                except Exception as e:
                    show_error(f"Error adding veteran: {str(e)}")

if __name__ == "__main__":
    render()

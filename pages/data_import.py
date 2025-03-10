
import streamlit as st
import pandas as pd
import io
import os
from auth import check_auth, check_role
from database import Database
from utils import show_success, show_error
from translations import get_text

def render():
    check_auth()
    check_role(['admin', 'teacher'])

    st.title("Import Data")
    
    db = Database()
    
    st.info("This page allows you to import student data from Excel files.")
    
    uploaded_file = st.file_uploader("Upload Excel file", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.write("Preview of uploaded data:")
            st.dataframe(df)
            
            # Mapping columns
            st.subheader("Map Columns")
            st.write("Please match the Excel columns with the database fields:")
            
            # Get column names from Excel
            columns = df.columns.tolist()
            
            # Define required fields for students
            required_fields = ['full_name', 'birth_date', 'address', 'email', 'admission_date', 'health_status', 'academic_status']
            
            # Create mapping
            field_mapping = {}
            for field in required_fields:
                field_mapping[field] = st.selectbox(
                    f"Map field '{field}' to column:", 
                    ["-- Ignore --"] + columns,
                    key=f"map_{field}"
                )
            
            if st.button("Import Data"):
                success_count = 0
                error_count = 0
                
                for _, row in df.iterrows():
                    try:
                        # Create a dictionary of values to insert
                        student_data = {}
                        for field, column in field_mapping.items():
                            if column != "-- Ignore --":
                                value = row[column]
                                # Handle date fields correctly
                                if field == 'birth_date' or field == 'admission_date':
                                    if pd.isna(value):
                                        value = None
                                    elif isinstance(value, str):
                                        try:
                                            value = pd.to_datetime(value).strftime('%Y-%m-%d')
                                        except:
                                            value = None
                                    else:
                                        try:
                                            value = pd.Timestamp(value).strftime('%Y-%m-%d')
                                        except:
                                            value = None
                                
                                # Handle NaN values
                                if pd.isna(value):
                                    value = None if field in ['birth_date', 'admission_date'] else ""
                                    
                                student_data[field] = value
                        
                        # Check if we have the required fields with values
                        if 'full_name' in student_data and student_data['full_name']:
                            cursor = db.conn.cursor()
                            # Create placeholders and values for SQL
                            fields = []
                            placeholders = []
                            values = []
                            
                            for field, value in student_data.items():
                                if value is not None:
                                    fields.append(field)
                                    placeholders.append("?")
                                    values.append(value)
                            
                            if fields:
                                # Construct and execute the INSERT query
                                query = f"INSERT INTO students ({','.join(fields)}) VALUES ({','.join(placeholders)})"
                                cursor.execute(query, values)
                                db.conn.commit()
                                success_count += 1
                        else:
                            error_count += 1
                    except Exception as e:
                        st.error(f"Error processing row: {e}")
                        error_count += 1
                
                if success_count > 0:
                    show_success(f"Successfully imported {success_count} students!")
                if error_count > 0:
                    show_error(f"Failed to import {error_count} records")
                
                if success_count > 0:
                    if st.button("View Students"):
                        st.switch_page("pages/students.py")
                    
        except Exception as e:
            show_error(f"Error reading Excel file: {str(e)}")

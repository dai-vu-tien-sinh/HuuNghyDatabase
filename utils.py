from datetime import datetime
import streamlit as st
import plotly.express as px
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def format_date(date: datetime) -> str:
    return date.strftime("%Y-%m-%d")

def create_chart(data: pd.DataFrame, chart_type: str, title: str):
    if chart_type == 'bar':
        fig = px.bar(data, title=title)
    elif chart_type == 'line':
        fig = px.line(data, title=title)
    elif chart_type == 'pie':
        fig = px.pie(data, title=title)
    return fig

def generate_pdf_report(data: dict, title: str) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Add title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, title)
    
    # Add content
    c.setFont("Helvetica", 12)
    y = 700
    for key, value in data.items():
        c.drawString(50, y, f"{key}: {value}")
        y -= 20
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

def show_success(message: str):
    st.success(message)

def show_error(message: str):
    st.error(message)

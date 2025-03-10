import pandas as pd
import streamlit as st
from database import Database
from utils import create_chart, generate_pdf_report

class ReportGenerator:
    def __init__(self):
        self.db = Database()

    def generate_student_statistics(self):
        students = self.db.get_students()
        df = pd.DataFrame(students)
        
        total_students = len(students)
        health_status_counts = df['health_status'].value_counts()
        academic_status_counts = df['academic_status'].value_counts()
        
        # Create charts
        health_chart = create_chart(
            health_status_counts,
            'pie',
            'Student Health Status Distribution'
        )
        academic_chart = create_chart(
            academic_status_counts,
            'bar',
            'Academic Status Distribution'
        )
        
        return {
            'total_students': total_students,
            'health_chart': health_chart,
            'academic_chart': academic_chart
        }

    def generate_veteran_statistics(self):
        veterans = self.db.get_veterans()
        df = pd.DataFrame(veterans)
        
        total_veterans = len(veterans)
        health_condition_counts = df['health_condition'].value_counts()
        
        health_chart = create_chart(
            health_condition_counts,
            'pie',
            'Veteran Health Condition Distribution'
        )
        
        return {
            'total_veterans': total_veterans,
            'health_chart': health_chart
        }

    def generate_pdf_summary(self, report_type: str):
        if report_type == 'students':
            stats = self.generate_student_statistics()
            data = {
                'Total Students': stats['total_students'],
                'Report Generated': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            return generate_pdf_report(data, 'Student Statistics Report')
        
        elif report_type == 'veterans':
            stats = self.generate_veteran_statistics()
            data = {
                'Total Veterans': stats['total_veterans'],
                'Report Generated': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            return generate_pdf_report(data, 'Veteran Statistics Report')

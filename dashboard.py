import streamlit as st
from db_connection import Connect_DB
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np

class Dashboard:
    def __init__(self):
        pass
    
    def display_dashboard(self):
        # Create connection
        connection = Connect_DB.get_connection()
        if not connection:
            st.error("Failed to connect to the database. Please try again later.")
            return
        
        cursor = connection.cursor()

        # Helper functions for database queries
        def get_total_classes(cursor):
            cursor.execute("SELECT COUNT(*) AS total_classes FROM classes")
            result = cursor.fetchone()
            return result['total_classes'] if result else 0

        def get_total_students(cursor):
            cursor.execute("SELECT COUNT(*) AS total_students FROM students")
            result = cursor.fetchone()
            return result['total_students'] if result else 0

        def get_highest_students_in_class(cursor):
            cursor.execute(""" 
                SELECT class_id, COUNT(*) AS student_count
                FROM students
                GROUP BY class_id
                ORDER BY student_count DESC LIMIT 1
            """)
            result = cursor.fetchone()
            return result['student_count'] if result else 0

        # Fetch data
        total_classes = get_total_classes(cursor)
        total_students = get_total_students(cursor)
        highest_students = get_highest_students_in_class(cursor)

        # delta for metrics
        delta_classes = total_classes/2 if total_classes > 0 else 0
        delta_students = total_students/2 if total_students > 0 else 0
        delta_highest_students = highest_students/2 if highest_students > 0 else 0

        # Display Metrics in the Dashboard
        st.title("Dashboard")
        container = st.container()
        block1, block2, block3 = container.columns(3)

        with block1:
            st.metric(label="Total Classes Available", value=total_classes, delta=delta_classes)
        with block2:
            st.metric(label="Total Enrolled Students", value=total_students, delta=delta_students)
        with block3:
            st.metric(label="Class with Most Students", value=highest_students, delta=delta_highest_students)
        st.markdown("---")

        # Analytics Section with Tabs
        st.markdown("<h2 style='text-align: center; margin: 2rem 0;'>Analytics Overview</h2>", unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Class Distribution", "Performance Overview", "Enrollment Trends"])
        
        with tab1:
            self.create_class_distribution_chart(cursor)
        
        with tab2:
            self.create_performance_overview_chart(cursor)
        
        with tab3:
            self.create_enrollment_trends_chart(cursor)

        cursor.close()
        connection.close()
    
    def create_class_distribution_chart(self, cursor):
        """Create a modern bar chart showing student distribution across classes"""
        cursor.execute("""
            SELECT c.class_name, COUNT(s.id) AS student_count
            FROM classes c
            LEFT JOIN students s ON c.id = s.class_id
            GROUP BY c.class_name, c.id
            ORDER BY student_count DESC
        """)
        classes = cursor.fetchall()
        
        if classes:
            class_names = [cls['class_name'] for cls in classes]
            student_counts = [cls['student_count'] for cls in classes]
            
            # Create Plotly bar chart
            fig = px.bar(
                x=class_names, 
                y=student_counts,
                title="Students per Class",
                labels={'x': 'Class', 'y': 'Number of Students'},
                color=student_counts,
                color_continuous_scale="Viridis"
            )
            
            fig.update_layout(
                template="plotly_white",
                title_x=0.5,
                xaxis_tickangle=-45,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No classes available to display distribution.")
    
    def create_performance_overview_chart(self, cursor):
        """Create a chart showing overall performance metrics"""
        cursor.execute("""
            SELECT c.class_name, 
                   AVG(r.marks::float / r.total_marks * 100) as avg_percentage,
                   COUNT(r.id) as total_results
            FROM classes c
            LEFT JOIN students s ON c.id = s.class_id
            LEFT JOIN results r ON s.id = r.student_id
            WHERE r.id IS NOT NULL
            GROUP BY c.class_name, c.id
            HAVING COUNT(r.id) > 0
            ORDER BY avg_percentage DESC
        """)
        performance_data = cursor.fetchall()
        
        if performance_data:
            class_names = [data['class_name'] for data in performance_data]
            avg_percentages = [round(data['avg_percentage'], 1) if data['avg_percentage'] else 0 for data in performance_data]
            
            # Create Plotly line chart
            fig = px.line(
                x=class_names,
                y=avg_percentages,
                title="Average Class Performance",
                labels={'x': 'Class', 'y': 'Average Percentage'},
                markers=True
            )
            
            fig.update_traces(
                line=dict(width=3),
                marker=dict(size=8)
            )
            
            fig.update_layout(
                template="plotly_white",
                title_x=0.5,
                xaxis_tickangle=-45,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show performance summary
            if avg_percentages:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Highest Avg", f"{max(avg_percentages):.1f}%")
                with col2:
                    st.metric("Lowest Avg", f"{min(avg_percentages):.1f}%")
                with col3:
                    st.metric("Overall Avg", f"{sum(avg_percentages)/len(avg_percentages):.1f}%")
        else:
            st.info("No results available to show performance overview. Add some results first.")
    
    def create_enrollment_trends_chart(self, cursor):
        """Create a pie chart showing enrollment distribution"""
        cursor.execute("""
            SELECT c.class_name, c.semester, COUNT(s.id) AS student_count
            FROM classes c
            LEFT JOIN students s ON c.id = s.class_id
            GROUP BY c.class_name, c.semester, c.id
            HAVING COUNT(s.id) > 0
            ORDER BY student_count DESC
        """)
        enrollment_data = cursor.fetchall()
        
        if enrollment_data:
            labels = [f"{data['class_name']} ({data['semester']})" for data in enrollment_data]
            values = [data['student_count'] for data in enrollment_data]
            
            # Create Plotly pie chart
            fig = px.pie(
                values=values,
                names=labels,
                title="Enrollment Distribution by Class",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            
            fig.update_layout(
                template="plotly_white",
                title_x=0.5,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No enrollment data available to display trends.")

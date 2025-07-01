import streamlit as st
from db_connection import Connect_DB
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

        # Fetch classes and the number of students in each class
        cursor.execute("""
            SELECT c.class_name, COUNT(s.id) AS student_count
            FROM classes c
            LEFT JOIN students s ON c.id = s.class_id
            GROUP BY c.class_name
        """)
        classes = cursor.fetchall()

        if classes:
            # Display the bar chart for total students in each class dynamically
            class_names = [cls['class_name'] for cls in classes]
            student_counts = [cls['student_count'] for cls in classes]

            # Set Seaborn dark theme
            sns.set_theme(style="dark", palette="dark")

            fig, ax = plt.subplots(figsize=(12, 6))
                
            # Generate a color palette where each bar has a unique color
            bar_colors = sns.color_palette("viridis", len(class_names))

            # Create a bar plot with different colors for each bar
            sns.barplot(x=class_names, y=student_counts, ax=ax, palette=bar_colors, edgecolor='black')

            ax.set_xlabel('Class', fontsize=14, fontweight='bold', color='white')
            ax.set_ylabel('Number of Students', fontsize=14, fontweight='bold', color='white')
            ax.set_title('Total Students per Class', fontsize=16, fontweight='bold', color='white')
            plt.xticks(rotation=45, ha="right", fontsize=12, color='white')
            plt.yticks(fontsize=12, color='white')

            # Customizing the bars for a better look
            for container in ax.containers:
                ax.bar_label(container, fontsize=10, padding=5, color='white', weight='bold')

            # Set dark background for the plot area
            ax.set_facecolor('#1c1c1c')
            fig.patch.set_facecolor('#1c1c1c')

            st.pyplot(fig)
        else:
            st.info("No classes available to display charts.")

        cursor.close()
        connection.close()

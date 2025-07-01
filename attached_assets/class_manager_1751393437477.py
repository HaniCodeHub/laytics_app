import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector
from mysql.connector import Error
import os

# Database configuration from environment variables
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "class_manager"),
    "port": os.getenv("MYSQL_PORT", 3306)
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        st.warning(f"Database connection error: {e}")
        return None

class ClassManager:
    def __init__(self):
        self.connection = get_db_connection()
        if not self.connection:
            st.error("Failed to connect to the database. Please try again later.")
            return
        
        self.cursor = self.connection.cursor(buffered=True)
        
    def run(self):
        options = st.sidebar.selectbox(
            "Navigation", 
            ["🏠 Home Dashboard", "📚 Add New Class", "📊 Results & Class Management"]
        )
        
        # Header
        col1, col2, col3 = st.columns([1,2,1])
        with col1:
            st.image("attached_assets/img3.png")
        with col2:
            st.markdown("## Class Management System")
        st.markdown("---")

        if options == "🏠 Home Dashboard":
            self.show_dashboard()
        elif options == "📚 Add New Class":
            self.add_new_class()
        elif options == "📊 Results & Class Management":
            self.manage_results()

    def show_dashboard(self):
        # Helper functions for database queries
        def get_total_classes():
            self.cursor.execute("SELECT COUNT(*) FROM classes")
            result = self.cursor.fetchone()
            return result[0] if result else 0

        def get_total_students():
            self.cursor.execute("SELECT COUNT(*) FROM students")
            result = self.cursor.fetchone()
            return result[0] if result else 0

        def get_highest_students_in_class():
            self.cursor.execute(""" 
                SELECT class_id, COUNT(*) AS student_count
                FROM students
                GROUP BY class_id
                ORDER BY student_count DESC LIMIT 1
            """)
            result = self.cursor.fetchone()
            return result[1] if result else 0

        # Fetch metrics
        total_classes = get_total_classes()
        total_students = get_total_students()
        highest_students = get_highest_students_in_class()

        # Display Metrics
        st.title("Dashboard")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Classes", total_classes)
        with col2:
            st.metric("Total Students", total_students)
        with col3:
            st.metric("Largest Class Size", highest_students)
        
        st.markdown("---")

        # Display class distribution chart
        self.cursor.execute("""
            SELECT c.class_name, COUNT(s.id) AS student_count
            FROM classes c
            LEFT JOIN students s ON c.id = s.class_id
            GROUP BY c.class_name
        """)
        classes = self.cursor.fetchall()

        if classes:
            class_names = [cls[0] for cls in classes]
            student_counts = [cls[1] for cls in classes]

            # Create the bar chart
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.barplot(x=class_names, y=student_counts, ax=ax, palette="viridis")
            
            ax.set_xlabel('Class', fontsize=14, fontweight='bold')
            ax.set_ylabel('Number of Students', fontsize=14, fontweight='bold')
            ax.set_title('Students per Class', fontsize=16, fontweight='bold')
            plt.xticks(rotation=45, ha="right")
            
            st.pyplot(fig)
        else:
            st.info("No classes available yet. Add some classes to see the distribution.")

    def add_new_class(self):
        st.subheader("Add a New Class")
        
        # Initialize session state for students list
        if "students" not in st.session_state:
            st.session_state.students = [{"roll_no": "", "name": ""}]

        # Class details form
        with st.form("class_form"):
            class_name = st.text_input("Class Name", placeholder="Enter class name")
            semester = st.text_input("Semester", placeholder="Enter semester")
            
            st.subheader("Add Students")
            students = []
            
            for i, student in enumerate(st.session_state.students):
                col1, col2 = st.columns(2)
                with col1:
                    roll_no = st.text_input(f"Roll No {i+1}", value=student["roll_no"], key=f"roll_{i}")
                with col2:
                    name = st.text_input(f"Name {i+1}", value=student["name"], key=f"name_{i}")
                students.append({"roll_no": roll_no, "name": name})
            
            if st.form_submit_button("Save Class"):
                if not class_name or not semester:
                    st.warning("Please provide both class name and semester.")
                    return
                    
                try:
                    # Insert class
                    self.cursor.execute(
                        "INSERT INTO classes (class_name, semester, total_students) VALUES (%s, %s, %s) RETURNING id",
                        (class_name, semester, len(students))
                    )
                    class_id = self.cursor.fetchone()[0]
                    
                    # Insert students
                    for student in students:
                        if student["roll_no"] and student["name"]:
                            self.cursor.execute(
                                "INSERT INTO students (class_id, roll_no, name) VALUES (%s, %s, %s)",
                                (class_id, student["roll_no"], student["name"])
                            )
                    
                    self.connection.commit()
                    st.success("Class created successfully!")
                    st.session_state.students = [{"roll_no": "", "name": ""}]  # Reset form
                    
                except Error as e:
                    self.connection.rollback()
                    st.error(f"Error creating class: {e}")
        
        if st.button("+ Add More Students"):
            st.session_state.students.append({"roll_no": "", "name": ""})

    def manage_results(self):
        st.subheader("Class Results Management")
        
        # Get list of classes
        self.cursor.execute("SELECT id, class_name, semester FROM classes")
        classes = self.cursor.fetchall()
        
        if not classes:
            st.info("No classes available. Please add a class first.")
            return
            
        class_options = {f"{cls[1]} ({cls[2]})": cls[0] for cls in classes}
        selected_class = st.selectbox("Select Class", list(class_options.keys()))
        
        if selected_class:
            class_id = class_options[selected_class]
            
            # Get students in the selected class
            self.cursor.execute(
                "SELECT id, roll_no, name FROM students WHERE class_id = %s ORDER BY roll_no",
                (class_id,)
            )
            students = self.cursor.fetchall()
            
            if not students:
                st.warning("No students found in this class.")
                return

            # Add Results Section
            st.subheader("Add Results")
            with st.form("add_results_form"):
                student_options = {f"{s[1]} - {s[2]}": s[0] for s in students}
                selected_student = st.selectbox("Select Student", list(student_options.keys()))
                subject = st.text_input("Subject")
                marks = st.number_input("Marks", min_value=0, max_value=100)
                exam_date = st.date_input("Exam Date")

                if st.form_submit_button("Add Result"):
                    if subject and marks is not None and exam_date:
                        try:
                            student_id = student_options[selected_student]
                            self.cursor.execute(
                                """
                                INSERT INTO results (student_id, subject, marks, exam_date)
                                VALUES (%s, %s, %s, %s)
                                """,
                                (student_id, subject, marks, exam_date)
                            )
                            self.connection.commit()
                            st.success("Result added successfully!")
                        except Error as e:
                            self.connection.rollback()
                            if "duplicate key" in str(e).lower():
                                st.error("Result already exists for this student, subject and exam date.")
                            else:
                                st.error(f"Error adding result: {e}")
                    else:
                        st.warning("Please fill in all fields.")

            # View Results Section
            st.subheader("View Results")
            view_options = ["By Student", "By Subject"]
            view_by = st.radio("View Results", view_options)

            if view_by == "By Student":
                selected_student = st.selectbox("Select Student", list(student_options.keys()), key="view_student")
                student_id = student_options[selected_student]
                
                self.cursor.execute(
                    """
                    SELECT subject, marks, exam_date
                    FROM results
                    WHERE student_id = %s
                    ORDER BY exam_date DESC, subject
                    """,
                    (student_id,)
                )
                results = self.cursor.fetchall()
                
                if results:
                    df = pd.DataFrame(results, columns=["Subject", "Marks", "Exam Date"])
                    st.dataframe(df)
                    
                    # Create a bar chart for student's performance
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.barplot(data=df, x="Subject", y="Marks", palette="viridis")
                    plt.xticks(rotation=45, ha="right")
                    plt.title(f"Performance Chart for {selected_student}")
                    st.pyplot(fig)
                else:
                    st.info("No results found for this student.")

            else:  # By Subject
                self.cursor.execute("SELECT DISTINCT subject FROM results WHERE student_id IN (SELECT id FROM students WHERE class_id = %s)", (class_id,))
                subjects = [row[0] for row in self.cursor.fetchall()]
                
                if subjects:
                    selected_subject = st.selectbox("Select Subject", subjects)
                    
                    self.cursor.execute(
                        """
                        SELECT s.roll_no, s.name, r.marks, r.exam_date
                        FROM students s
                        JOIN results r ON s.id = r.student_id
                        WHERE s.class_id = %s AND r.subject = %s
                        ORDER BY r.exam_date DESC, s.roll_no
                        """,
                        (class_id, selected_subject)
                    )
                    results = self.cursor.fetchall()
                    
                    if results:
                        df = pd.DataFrame(results, columns=["Roll No", "Name", "Marks", "Exam Date"])
                        st.dataframe(df)
                        
                        # Calculate and show statistics
                        avg_marks = df["Marks"].mean()
                        max_marks = df["Marks"].max()
                        min_marks = df["Marks"].min()
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Average Marks", f"{avg_marks:.2f}")
                        col2.metric("Highest Marks", max_marks)
                        col3.metric("Lowest Marks", min_marks)
                        
                        # Create a box plot for subject performance distribution
                        fig, ax = plt.subplots(figsize=(10, 6))
                        sns.boxplot(data=df, y="Marks", palette="viridis")
                        plt.title(f"Marks Distribution for {selected_subject}")
                        st.pyplot(fig)
                    else:
                        st.info("No results found for this subject.")
                else:
                    st.info("No results have been added yet.")

    def __del__(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()

if __name__ == "__main__":
    app = ClassManager()
    app.run()

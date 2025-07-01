import streamlit as st
from db_connection import Connect_DB
from dashboard import Dashboard

class ClassManager:
    def __init__(self):
        self.dashboard = Dashboard()
    
    def run(self):
        # Display header
        logo, title, right = st.columns(3)
        with logo:
            # Using a placeholder SVG icon for the logo since we can't use the PNG
            st.markdown("📚", unsafe_allow_html=True)
        with title:
            st.markdown("## Class Manager")
        st.markdown("---")
        
        # Sidebar navigation
        options = st.sidebar.selectbox("Navigation", [
            "🏠 Home Dashboard", 
            "📚 Add New Class", 
            "📊 Results & Class Management"
        ])
        
        if options == "🏠 Home Dashboard":
            self.dashboard.display_dashboard()
        elif options == "📚 Add New Class":
            self.display_add_class()
        elif options == "📊 Results & Class Management":
            self.display_results_management()
    
    def display_add_class(self):
        st.subheader("Add a New Class and Students")
        
        # Initialize session state for students list if not already done
        if "students" not in st.session_state:
            st.session_state.students = [{"roll_no": "", "name": ""}]

        # Function to add a new row of student inputs
        def add_student_row():
            st.session_state.students.append({"roll_no": "", "name": ""})

        # Function to create a class and insert data into the database
        def create_class(class_name, semester, students):
            if not class_name or not semester:
                st.error("Please provide both the class name and semester.")
                return

            if not any(student["roll_no"] and student["name"] for student in students):
                st.error("Add at least one student with a valid roll number and name.")
                return

            try:
                connection = Connect_DB.get_connection()
                if not connection:
                    st.error("Database connection failed.")
                    return
                    
                cursor = connection.cursor()
                
                # Insert class
                cursor.execute(
                    "INSERT INTO classes (class_name, semester, total_students) VALUES (%s, %s, %s) RETURNING id",
                    (class_name, semester, len([s for s in students if s["roll_no"] and s["name"]]))
                )
                class_id = cursor.fetchone()['id']

                # Insert students
                for student in students:
                    if student["roll_no"] and student["name"]:
                        cursor.execute(
                            "INSERT INTO students (class_id, roll_no, name) VALUES (%s, %s, %s)",
                            (class_id, student["roll_no"], student["name"])
                        )
                connection.commit()
                cursor.close()
                connection.close()
                st.success("Class created successfully!")
                st.session_state.students = [{"roll_no": "", "name": ""}]  # Reset form
            except Exception as e:
                st.error(f"An error occurred: {e}")

        st.markdown("---")

        # Section 1: Enter Class Name and Semester
        st.subheader("Step 1: Enter Class Details")
        class_name = st.text_input("Enter Class Name")
        semester = st.text_input("Enter Semester")
        st.markdown("---")

        # Section 2: Add Students (Roll Number and Name)
        st.subheader("Step 2: Add Students to the Class")
        students = []

        # Display existing rows of students and create input fields
        for i, student in enumerate(st.session_state.students):
            cols = st.columns(2)
            with cols[0]:
                roll_no = st.text_input(f"Roll No {i + 1}", value=student["roll_no"], key=f"roll_no_{i}")
            with cols[1]:
                name = st.text_input(f"Name {i + 1}", value=student["name"], key=f"name_{i}")
            students.append({"roll_no": roll_no, "name": name})

        # Update the session state with the latest student data
        st.session_state.students = students

        # Button to add more rows dynamically
        if st.button("+ Add More Rows"):
            add_student_row()
            st.rerun()

        # Button to create the class
        if st.button("Save Class"):
            create_class(class_name, semester, students)

    def display_results_management(self):
        st.subheader("Generate Results for a Class")
        st.write("View available classes, manage their details, and generate results for any subject quickly.")

        # Function to reset session state and go back to the main page
        def reset_class_page():
            st.session_state.selected_class = None

        # Initialize session state for selected class
        if "selected_class" not in st.session_state:
            st.session_state.selected_class = None

        # Show the "Go Back" button only if a class is selected
        if st.session_state.selected_class is not None:
            if st.button("Go Back"):
                reset_class_page()
                st.rerun()

        # Check if a class is selected
        if st.session_state.selected_class is None:
            # Main Page: Display existing classes
            st.markdown("---")

            connection = Connect_DB.get_connection()
            if not connection:
                st.error("Database connection failed.")
                return
                
            cursor = connection.cursor()
            cursor.execute("SELECT id, class_name, semester, total_students FROM classes")
            classes = cursor.fetchall()
            cursor.close()
            connection.close()

            if not classes:
                st.info("No classes available.")
            else:
                max_columns = 3  # Number of columns per row
                rows = [classes[i:i + max_columns] for i in range(0, len(classes), max_columns)]

                for row_index, row in enumerate(rows):
                    cols = st.columns(len(row))
                    for col_index, cls in enumerate(row):
                        with cols[col_index]:
                            class_id = cls["id"]
                            class_name = cls["class_name"]
                            semester = cls["semester"]
                            total_students = cls["total_students"]

                            st.markdown(
                                f"""
                                <div style="text-align: center; padding: 20px; margin: 10px; border: 2px solid #4CAF50; border-radius: 10px; background-color: #333333; color: white;">
                                    <h3 style="color: #00FF00;">{class_name}</h3>
                                    <p><strong>Semester:</strong> {semester}</p>
                                    <p><strong>Total Students:</strong> {total_students}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            if st.button(
                                "Select Class",
                                key=f"class_{class_id}_{row_index}_{col_index}",
                                use_container_width=True,
                                help="Click to select this class",
                            ):
                                st.session_state.selected_class = class_id
                                st.rerun()
        else:
            # Class-Specific Page: Show details and generate result form
            self.display_class_results()

    def display_class_results(self):
        selected_class_id = st.session_state.selected_class

        connection = Connect_DB.get_connection()
        if not connection:
            st.error("Database connection failed.")
            return
            
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM classes WHERE id = %s", (selected_class_id,))
        cls = cursor.fetchone()

        st.title(f"Class: {cls['class_name']} - Semester {cls['semester']}")
        st.write(f"Total Students: {cls['total_students']}")

        st.subheader("Generate Subject Result")
        subject_name = st.text_input("Subject Name")
        total_marks = st.number_input("Total Marks", min_value=0, step=1)

        # Fetch students for the selected class
        cursor.execute("SELECT id, roll_no, name FROM students WHERE class_id = %s", (selected_class_id,))
        students = cursor.fetchall()

        if not students:
            st.warning("No students found for this class.")
        else:
            st.write("Enter Marks for each student:")
            results = []
            all_marks_entered = True

            for student in students:
                col1, col2, col3 = st.columns([1, 2, 2])
                with col1:
                    st.write(student["roll_no"])
                with col2:
                    st.write(student["name"])
                with col3:
                    marks = st.number_input(
                        f"Marks for {student['roll_no']}",
                        min_value=0,
                        max_value=total_marks if total_marks > 0 else 100,
                        key=f"marks_{student['roll_no']}"
                    )
                    results.append({
                        "student_id": student["id"],
                        "marks": marks
                    })

            if st.button("Generate Result"):
                if subject_name and len(subject_name.strip()) > 0 and total_marks > 0:
                    try:
                        from datetime import date
                        today = date.today()
                        
                        for result in results:
                            cursor.execute(
                                """INSERT INTO results (student_id, subject, marks, total_marks, exam_date) 
                                   VALUES (%s, %s, %s, %s, %s)
                                   ON CONFLICT (student_id, subject, exam_date) 
                                   DO UPDATE SET marks = EXCLUDED.marks, total_marks = EXCLUDED.total_marks""",
                                (result["student_id"], subject_name, result["marks"], total_marks, today)
                            )
                        
                        connection.commit()
                        st.success("Results saved successfully!")
                        
                        # Display results summary
                        st.subheader("Results Summary")
                        summary_data = []
                        for i, student in enumerate(students):
                            percentage = (results[i]["marks"] / total_marks) * 100 if total_marks > 0 else 0
                            grade = self.calculate_grade(percentage)
                            summary_data.append({
                                "Roll No": student["roll_no"],
                                "Name": student["name"],
                                "Marks": f"{results[i]['marks']}/{total_marks}",
                                "Percentage": f"{percentage:.1f}%",
                                "Grade": grade
                            })
                        
                        import pandas as pd
                        df = pd.DataFrame(summary_data)
                        st.dataframe(df, use_container_width=True)
                        
                    except Exception as e:
                        st.error(f"Error saving results: {e}")
                else:
                    st.error("Please provide subject name and total marks.")

        cursor.close()
        connection.close()

    def calculate_grade(self, percentage):
        if percentage >= 90:
            return "A+"
        elif percentage >= 80:
            return "A"
        elif percentage >= 70:
            return "B+"
        elif percentage >= 60:
            return "B"
        elif percentage >= 50:
            return "C+"
        elif percentage >= 40:
            return "C"
        else:
            return "F"

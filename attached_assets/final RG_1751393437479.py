import streamlit as st
from db_connection import Connect_DB
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


# Database connection
connection = Connect_DB.get_connection()
cursor = connection.cursor()


options = st.sidebar.selectbox("Navigation",["🏠 Home Dashboard", "📚 Add New Class", "📊 Results & Class Management"])
# Header
logo, title, right = st.container().columns(3)
with logo:
    st.image("img3.png")
with title:
    st.markdown("## File Generator")
st.markdown("---")








# ----------Dashboard starting----------------
if options == "🏠 Home Dashboard":


    # Create connection
    connection = Connect_DB.get_connection()
    if not connection:
        st.error("Failed to connect to the database. Please try again later.")
    else:
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
        delta_classes = total_classes/2  # Replace with actual calculation if historical data is available
        delta_students = total_students/2  # Replace with actual calculation if historical data is available
        delta_highest_students = highest_students/2  # Replace with actual calculation if historical data is available

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
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.class_name, COUNT(s.id) AS student_count
                FROM classes c
                LEFT JOIN students s ON c.id = s.class_id
                GROUP BY c.class_name
            """)
            classes = cursor.fetchall()

        # Display the bar chart for total students in each class dynamically
        class_names = [cls['class_name'] for cls in classes]
        student_counts = [cls['student_count'] for cls in classes]
    

        # Set Seaborn dark theme
        sns.set_theme(style="dark", palette="dark")  
        # Set dark background and grid for the plot

        fig, ax = plt.subplots(figsize=(12, 6))  # Specify the size of the figure
            
        # Generate a color palette where each bar has a unique color
        bar_colors = sns.color_palette("viridis", len(class_names))  # Choose a color palette

        # Create a bar plot with different colors for each bar
        sns.barplot(x=class_names, y=student_counts, ax=ax, palette=bar_colors, edgecolor='black')

        ax.set_xlabel('Class', fontsize=14, fontweight='bold', color='white')
        ax.set_ylabel('Number of Students', fontsize=14, fontweight='bold', color='white')
        ax.set_title('Total Students per Class', fontsize=16, fontweight='bold', color='white')
        plt.xticks(rotation=45, ha="right", fontsize=12, color='white')
        plt.yticks(fontsize=12, color='white')

        # Customizing the bars for a better look
        for container in ax.containers:
            ax.bar_label(container, fontsize=10, padding=5, color='white', weight='bold')  # Add labels on bars

        # Set dark background for the plot area
        ax.set_facecolor('#1c1c1c')  # Dark background color for the plot area
        fig.patch.set_facecolor('#1c1c1c')  # Dark background color for the entire figure

        st.pyplot(fig)

        # ----------Dashboard ending----------------















# ---------Create New Class start-------------
elif options == "📚 Add New Class":
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
            with connection.cursor() as cursor:
                # Insert class
                cursor.execute(
                    "INSERT INTO classes (class_name, semester, total_students) VALUES (%s, %s, %s)",
                    (class_name, semester, len(students))
                )
                class_id = cursor.lastrowid

                # Insert students
                for student in students:
                    if student["roll_no"] and student["name"]:
                        cursor.execute(
                            "INSERT INTO students (class_id, roll_no, name) VALUES (%s, %s, %s)",
                            (class_id, student["roll_no"], student["name"])
                        )
                connection.commit()
                st.success("Class created successfully!")
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

    # Button to create the class
    if st.button("Save Class"):
        create_class(class_name, semester, students)



# ---------Create New Class ends-------------













        # ---------existing Class starts-------------
elif options == "📊 Results & Class Management":
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

    # Check if a class is selected
    if st.session_state.selected_class is None:
        # Main Page: Display existing classes
        st.markdown("---")
        # st.subheader("Existing Classes:")

        cursor.execute("SELECT id, class_name, semester, total_students FROM classes")
        classes = cursor.fetchall()

        if not classes:
            st.info("No classes available.")
        else:
            max_columns = 3  # Number of columns per row
            rows = [classes[i:i + max_columns] for i in range(0, len(classes), max_columns)]  # Group into rows

            for row_index, row in enumerate(rows):
                cols = st.columns(len(row))  # Create the appropriate number of columns for this row
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
                            on_click=lambda id=class_id: st.session_state.update(selected_class=id),
                            use_container_width=True,
                            help="Click to select this class",
                        ):
                            pass
    else:
        # Class-Specific Page: Show details and generate result form
        selected_class_id = st.session_state.selected_class

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
            all_marks_entered = True  # Flag to track if all marks are entered

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
                        max_value=total_marks,
                        key=f"marks_{student['roll_no']}"
                    )
                    if marks is None:  # Check if marks are not entered
                        all_marks_entered = False
                    results.append({"student_id": student["id"], "marks": marks})

            if st.button("Generate Result"):
                if not subject_name.strip():
                    st.error("Subject name cannot be empty.")
                elif not all_marks_entered:
                    st.error("Please enter marks for all students before generating the result.")
                else:
                    try:
                        for result in results:
                            cursor.execute(
                                """
                                INSERT INTO results (student_id, subject_name, total_marks, obtained_marks)
                                VALUES (%s, %s, %s, %s)
                                """,
                                (result["student_id"], subject_name, total_marks, result["marks"])
                            )
                        connection.commit()

                        st.success("Results generated successfully!")

                        # Display Results
                        result_data = []
                        for result in results:
                            student_id = result["student_id"]
                            cursor.execute(
                                "SELECT roll_no, name FROM students WHERE id = %s", (student_id,)
                            )
                            student = cursor.fetchone()
                            result_data.append({
                                "Roll No": student["roll_no"],
                                "Name": student["name"],
                                "Marks": result["marks"]
                            })

                        df = pd.DataFrame(result_data)
                        st.subheader("Generated Results")
                        st.dataframe(df)

                        # Provide option to download as CSV
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="Download Results as CSV",
                            data=csv,
                            file_name=f"results_{selected_class_id}_{subject_name}.csv",
                            mime="text/csv"
                        )
                    except Exception as e:
                        st.error(f"Error generating results: {e}")



                    # ---------Existing Class ends-------------


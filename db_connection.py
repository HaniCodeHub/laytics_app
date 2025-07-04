import psycopg2
from psycopg2.extras import RealDictCursor
import os
import streamlit as st

class Connect_DB:
    @staticmethod
    def get_connection():
        """
        Creates and returns a PostgreSQL database connection using environment variables
        """
        try:
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                st.error("DATABASE_URL is not set. Please add it to your environment or Streamlit secrets.")
                return None

            connection = psycopg2.connect(
                database_url,
                cursor_factory=RealDictCursor
            )


            return connection
        except psycopg2.Error as e:
            st.error(f"Database connection error: {e}")
            return None

    @staticmethod
    def create_tables():
        """
        Creates all necessary tables for the application with proper user associations
        """
        connection = Connect_DB.get_connection()
        if not connection:
            return False
            
        try:
            cursor = connection.cursor()
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create classes table with user association
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS classes (
                    id SERIAL PRIMARY KEY,
                    class_name VARCHAR(100) NOT NULL,
                    semester VARCHAR(50) NOT NULL,
                    total_students INTEGER DEFAULT 0,
                    user_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
            """)
            
            # Create students table with user association
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    class_id INTEGER,
                    roll_no VARCHAR(20) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    user_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(class_id, roll_no),
                    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
            """)
            
            # Create results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id SERIAL PRIMARY KEY,
                    student_id INTEGER,
                    subject VARCHAR(100) NOT NULL,
                    marks INTEGER NOT NULL,
                    total_marks INTEGER NOT NULL,
                    exam_date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(student_id, subject, exam_date),
                    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                    CHECK (marks >= 0)
                );
            """)
            
            # Create indexes for better performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_classes_user_id ON classes(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_user_id ON students(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_class_id ON students(class_id)")
            
            connection.commit()
            cursor.close()
            connection.close()
            return True
            
        except psycopg2.Error as e:
            st.error(f"Error creating tables: {e}")
            if connection:
                connection.close()
            return False

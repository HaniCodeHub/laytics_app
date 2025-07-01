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
            # Use environment variables for database configuration
            connection = psycopg2.connect(
                host=os.getenv("PGHOST", "localhost"),
                database=os.getenv("PGDATABASE", "class_manager"),
                user=os.getenv("PGUSER", "postgres"),
                password=os.getenv("PGPASSWORD", ""),
                port=os.getenv("PGPORT", "5432"),
                cursor_factory=RealDictCursor
            )
            return connection
        except psycopg2.Error as e:
            st.error(f"Database connection error: {e}")
            return None

    @staticmethod
    def create_tables():
        """
        Creates all necessary tables for the application
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
            
            # Create classes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS classes (
                    id SERIAL PRIMARY KEY,
                    class_name VARCHAR(100) NOT NULL,
                    semester VARCHAR(50) NOT NULL,
                    total_students INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create students table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    class_id INTEGER,
                    roll_no VARCHAR(20) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(class_id, roll_no),
                    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE
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
            
            connection.commit()
            cursor.close()
            connection.close()
            return True
            
        except psycopg2.Error as e:
            st.error(f"Error creating tables: {e}")
            if connection:
                connection.close()
            return False

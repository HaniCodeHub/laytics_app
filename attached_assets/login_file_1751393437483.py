import streamlit as st
import mysql.connector
from mysql.connector import Error
import hashlib
import os
import time

# Database Configuration using environment variables
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "class_m    anager"),
    "port": os.getenv("MYSQL_PORT", 3306)
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        st.warning(f"Error connecting to MySQL: {e}")
        return None

def initialize_database():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Create users table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            
            # Create classes table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS classes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    class_name VARCHAR(100) NOT NULL,
                    semester VARCHAR(50) NOT NULL,
                    total_students INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            
            # Create students table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    class_id INT,
                    roll_no VARCHAR(20) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE KEY unique_roll_class (class_id, roll_no),
                    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE
                );
                """
            )
            
            # Create results table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS results (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT,
                    subject VARCHAR(100) NOT NULL,
                    marks INT NOT NULL,
                    exam_date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE KEY unique_result (student_id, subject, exam_date),
                    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                    CHECK (marks >= 0 AND marks <= 100)
                );
                """
            )
            
            connection.commit()
        except Error as e:
            st.warning(f"Error initializing database: {e}")
        finally:
            if cursor:
                cursor.close()
            connection.close()

class Login:
    def __init__(self):
        self.identifier = ""
        self.password = ""

    def display_login_form(self):
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)

        # Back button
        if st.button("← Back", key="back_button"):
            st.session_state.show_login_form = False
            st.rerun()

        # Create tabs
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        # Set active tab based on session state
        active_tab = st.session_state.get("current_tab", "login")
        
        # Display content in the appropriate tab
        if active_tab == "login":
            with tab1:
                self._display_login_tab()
            with tab2:
                signup_page = Signup()
                signup_page.display_signup_form_in_tab()
                
                # Add script to switch to signup tab when needed
                st.markdown(
                    """
                    <script>
                        if (window.location.href.includes('current_tab=login')) {
                            window.dispatchEvent(new Event('streamlit:componentReady'));
                            const tabs = window.parent.document.querySelectorAll('.stTabs button[role="tab"]');
                            if (tabs.length > 0) {
                                tabs[0].click();
                            }
                        }
                    </script>
                    """,
                    unsafe_allow_html=True
                )
        else:  # signup tab
            with tab1:
                self._display_login_tab()
            with tab2:
                signup_page = Signup()
                signup_page.display_signup_form_in_tab()
                
                # Add script to switch to signup tab when needed
                st.markdown(
                    """
                    <script>
                        if (window.location.href.includes('current_tab=signup')) {
                            window.dispatchEvent(new Event('streamlit:componentReady'));
                            const tabs = window.parent.document.querySelectorAll('.stTabs button[role="tab"]');
                            if (tabs.length > 1) {
                                tabs[1].click();
                            }
                        }
                    </script>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown('</div>', unsafe_allow_html=True)

    def _display_login_tab(self):
        st.markdown('<div class="auth-emoji">👋</div>', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; margin-bottom: 2rem;'>Welcome Back!</h3>", unsafe_allow_html=True)

        with st.form(key="login_form"):
            col1, col2 = st.columns([0.15, 0.85])
            with col1:
                st.markdown('<div class="input-emoji">📧</div>', unsafe_allow_html=True)
            with col2:
                self.identifier = st.text_input("Email or Username", 
                                              placeholder="Enter your email or username")

            col1, col2 = st.columns([0.15, 0.85])
            with col1:
                st.markdown('<div class="input-emoji">🔑</div>', unsafe_allow_html=True)
            with col2:
                self.password = st.text_input("Password", 
                                            type="password",
                                            placeholder="Enter your password")

            if st.form_submit_button("Login"):
                if not self.identifier or not self.password:
                    st.warning("Please fill in all fields")
                elif self.authenticate():
                    st.session_state["is_logged_in"] = True
                    st.session_state["identifier"] = self.identifier
                    st.session_state["show_login_form"] = False
                    st.rerun()
                else:
                    st.warning("Invalid credentials")

    def authenticate(self):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT password FROM users WHERE email = %s OR username = %s"
                cursor.execute(query, (self.identifier, self.identifier))
                result = cursor.fetchone()

                if result and result[0] == hash_password(self.password):
                    return True
                return False
            except Error as e:
                st.warning("Authentication error")
                return False
            finally:
                if cursor:
                    cursor.close()
                connection.close()
        return False

class Signup:
    def __init__(self):
        self.email = ""
        self.username = ""
        self.password = ""
        self.confirm_password = ""

    def display_signup_form_in_tab(self):
        st.markdown('<div class="auth-emoji">✨</div>', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; margin-bottom: 2rem;'>Create Account</h3>", unsafe_allow_html=True)

        with st.form(key="signup_form"):
            col1, col2 = st.columns([0.15, 0.85])
            with col1:
                st.markdown('<div class="input-emoji">📧</div>', unsafe_allow_html=True)
            with col2:
                self.email = st.text_input("Email", placeholder="Enter your email")

            col1, col2 = st.columns([0.15, 0.85])
            with col1:
                st.markdown('<div class="input-emoji">👤</div>', unsafe_allow_html=True)
            with col2:
                self.username = st.text_input("Username", placeholder="Choose a username")

            col1, col2 = st.columns([0.15, 0.85])
            with col1:
                st.markdown('<div class="input-emoji">🔒</div>', unsafe_allow_html=True)
            with col2:
                self.password = st.text_input("Password", 
                                            type="password",
                                            placeholder="Choose a password")
                self.confirm_password = st.text_input("Confirm Password",
                                                    type="password",
                                                    placeholder="Confirm your password")

            if st.form_submit_button("Sign Up"):
                if self.validate():
                    if self.register_user():
                        st.success("Account created successfully!")
                        st.session_state.current_tab = "login"  # Switch to login tab
                        st.session_state.show_login_form = True
                        time.sleep(1)  # Give time for success message to show
                        st.rerun()
                    else:
                        st.warning("Email or username already exists")
                else:
                    st.warning("Please fill in all fields and ensure passwords match")

    def validate(self):
        return (
            self.password == self.confirm_password and
            len(self.email) > 0 and
            len(self.username) > 0 and
            len(self.password) > 0
        )

    def register_user(self):
        connection = None
        try:
            connection = create_connection()
            if not connection:
                st.warning("Database connection error")
                return False

            cursor = connection.cursor()

            # Check if email or username exists
            check_query = "SELECT * FROM users WHERE email = %s OR username = %s"
            cursor.execute(check_query, (self.email, self.username))
            if cursor.fetchone():
                return False

            # Insert new user
            query = "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (self.email, self.username, hash_password(self.password)))
            connection.commit()
            return True

        except Error as e:
            st.warning("Registration error")
            return False
        finally:
            if connection:
                connection.close()

class ForgotPassword:
    def __init__(self):
        self.identifier = ""
        self.new_password = ""
        self.confirm_password = ""

    def display_forgot_password_form(self):
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="back-button">', unsafe_allow_html=True)
            if st.button("← Back", key="forgot_password_back"):
                st.session_state["show_forgot_password"] = False
                st.session_state["show_login_form"] = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
            <div class="auth-emoji">🔄</div>
            <div class="welcome-text">
                Forgot your password? No worries! Reset it here.
            </div>
        """, unsafe_allow_html=True)

        with st.form(key="forgot_password_form"):
            col1, col2 = st.columns([0.15, 0.85])
            with col1:
                st.markdown('<div class="input-emoji">📧</div>', unsafe_allow_html=True)
            with col2:
                self.identifier = st.text_input("Enter your Email or Username", key="forgot_password_identifier")

            col1, col2 = st.columns([0.15, 0.85])
            with col1:
                st.markdown('<div class="input-emoji">🔒</div>', unsafe_allow_html=True)
            with col2:
                self.new_password = st.text_input("New Password", type="password", key="new_password")
                self.confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_new_password")

            if st.form_submit_button("Reset Password 🔄"):
                if self.validate():
                    if self.reset_password():
                        st.success("Password reset successful! Please login.")
                        st.session_state["show_forgot_password"] = False
                        st.session_state["show_login_form"] = True
                        st.rerun()
                    else:
                        st.warning("Email/Username not found.")
                else:
                    st.warning("Passwords do not match or fields are empty.")

        st.markdown('</div>', unsafe_allow_html=True)

    def validate(self):
        return self.new_password == self.confirm_password and len(self.identifier) > 0

    def reset_password(self):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "UPDATE users SET password = %s WHERE email = %s OR username = %s"
                cursor.execute(query, (hash_password(self.new_password), self.identifier, self.identifier))
                connection.commit()
                return cursor.rowcount > 0
            except Error as e:
                st.warning("An error occurred during password reset. Please try again.")
                return False
            finally:
                if cursor:
                    cursor.close()
                connection.close()
        return False

def load_custom_css():
    st.markdown(
        """
        <style>
        .auth-container {
            max-width: 400px;
            margin: 2rem auto;
            padding: 2rem;
            border-radius: 10px;
            background: white;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }

        .stTab {
            border: none !important;
            background: none !important;
            color: #666 !important;
            font-weight: 500 !important;
        }

        .stTab[aria-selected="true"] {
            color: #4a90e2 !important;
            border-bottom: 2px solid #4a90e2 !important;
        }

        .stTabs {
            background: none !important;
            border: none !important;
            padding: 0 !important;
        }

        [data-testid="stTabsContent"] {
            padding: 1rem 0 !important;
        }

        .stButton > button {
            background-color: #4a90e2 !important;
            color: white !important;
            padding: 0.75rem !important;
            border-radius: 5px !important;
            font-weight: 500 !important;
            width: 100% !important;
            margin-top: 1rem !important;
            border: none !important;
            box-shadow: none !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(74, 144, 226, 0.2) !important;
        }

        .auth-emoji {
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 1rem;
        }

        .input-emoji {
            font-size: 1.2rem;
            margin-right: 8px;
        }

        .stTextInput > div > div > input {
            border-radius: 5px !important;
            border: 1px solid #e0e0e0 !important;
            padding: 0.75rem !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: #4a90e2 !important;
            box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.1) !important;
        }

        /* Hide error messages */
        .stException, .stError {
            display: none !important;
        }

        footer {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Main execution
if __name__ == "__main__":
    load_custom_css()
    initialize_database()

    # Initialize session state variables
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False
    if "show_login_form" not in st.session_state:
        st.session_state.show_login_form = True
    if "show_signup" not in st.session_state:
        st.session_state.show_signup = False
    if "show_forgot_password" not in st.session_state:
        st.session_state.show_forgot_password = False
    if "current_tab" not in st.session_state:
        st.session_state.current_tab = "login"


    if st.session_state.is_logged_in:
        st.markdown(f"<h2 style='text-align: center;'>🎉 Welcome, {st.session_state.get('identifier', 'User')}! 🎉</h2>", unsafe_allow_html=True)
        st.write("You have successfully logged in. 🚀")

        if st.button("Logout"):
            for key in ['is_logged_in', 'show_login_form', 'show_signup', 'show_forgot_password', 'identifier', 'current_tab']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    elif st.session_state.show_forgot_password:
        forgot_password_page = ForgotPassword()
        forgot_password_page.display_forgot_password_form()

    elif st.session_state.show_signup:
        signup_page = Signup()
        signup_page.display_signup_form_in_tab()

    else:
        login_page = Login()
        login_page.display_login_form()
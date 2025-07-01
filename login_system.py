import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib
import os
import time
from db_connection import Connect_DB

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def initialize_database():
    """Initialize the database tables"""
    Connect_DB.create_tables()

def load_custom_css():
    """Load custom CSS styles for the application"""
    st.markdown(
        """
        <style>
        .stApp {
            background: var(--background-color);
            color: var(--text-color);
        }

        .auth-container {
            max-width: 400px;
            margin: 2rem auto;
            padding: 2rem;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .auth-emoji {
            font-size: 3rem;
            text-align: center;
            margin-bottom: 1rem;
        }

        .input-emoji {
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
        }

        .welcome-text {
            text-align: center;
            margin-bottom: 2rem;
            color: #666;
        }

        .back-button {
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

class Login:
    def __init__(self):
        self.identifier = ""
        self.password = ""

    def display_login_form(self):
        load_custom_css()
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
        else:  # signup tab
            with tab1:
                self._display_login_tab()
            with tab2:
                signup_page = Signup()
                signup_page.display_signup_form_in_tab()

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
        connection = Connect_DB.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT password FROM users WHERE email = %s OR username = %s"
                cursor.execute(query, (self.identifier, self.identifier))
                result = cursor.fetchone()

                if result and result['password'] == hash_password(self.password):
                    return True
                return False
            except psycopg2.Error as e:
                st.warning("Authentication error")
                return False
            finally:
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
            connection = Connect_DB.get_connection()
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

        except psycopg2.Error as e:
            st.warning("Registration error")
            return False
        finally:
            if connection:
                connection.close()

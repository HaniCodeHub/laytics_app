import streamlit as st
from attached_assets.HMPG import ClassManagerApp
from attached_assets.login_file import load_custom_css, initialize_database
from attached_assets.class_manager import ClassManager
import os

# Set page configuration at the very beginning
st.set_page_config(
    page_title="Class Manager",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Configure MySQL connection from environment variables
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "class_manager"),
    "port": os.getenv("MYSQL_PORT", 3306)
}

def main():
    # Initialize database and load CSS
    initialize_database()
    load_custom_css()

    # Initialize session state variables if not present
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False

    if "identifier" not in st.session_state:
        st.session_state.identifier = ""

    if "show_login_form" not in st.session_state:
        st.session_state.show_login_form = False

    if "show_signup" not in st.session_state:
        st.session_state.show_signup = False

    if "show_forgot_password" not in st.session_state:
        st.session_state.show_forgot_password = False

    if "current_tab" not in st.session_state:
        st.session_state.current_tab = "login"

    # Create and run the application
    if st.session_state.is_logged_in:
        class_manager = ClassManager()
        class_manager.run()
    else:
        app = ClassManagerApp()
        app.run()

if __name__ == "__main__":
    main()

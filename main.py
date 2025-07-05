import streamlit as st
import os
from home_page import ClassManagerApp
from login_system import initialize_database
from class_manager import ClassManager

# DEBUG: Test if secrets are accessible
st.title("Secrets Debugging Test ")
st.write("Secrets object:", st.secrets)
st.write("DATABASE_URL:", st.secrets.get("DATABASE_URL", "NOT SET"))


# Set page configuration at the very beginning
st.set_page_config(
    page_title="Educational Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    # Initialize database
    initialize_database()

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

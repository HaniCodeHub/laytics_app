import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
from .login_file import *

# Page configuration is now in main.py

# Initialize session state variables
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

if "show_login_form" not in st.session_state:
    st.session_state.show_login_form = False

if "current_tab" not in st.session_state:
    st.session_state.current_tab = "login"

class ClassManagerApp:
    def __init__(self):
        if "current_image_index" not in st.session_state:
            st.session_state.current_image_index = 0

        self.vector_images = {
            "analytics": "https://cdn-icons-png.flaticon.com/512/3135/3135755.png",
            "dashboard": "https://cdn-icons-png.flaticon.com/512/1534/1534959.png",
            "reports": "https://cdn-icons-png.flaticon.com/512/1534/1534993.png"
        }
        self.load_custom_css()

    def load_custom_css(self):
        st.markdown(
            """
            <style>
            .stApp {
                background: var(--background-color);
                color: var(--text-color);
            }

            .top-nav {
                backdrop-filter: blur(10px);
                background: rgba(255, 255, 255, 0.8) !important;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                padding: 1rem 2rem;
                position: sticky;
                top: 0;
                z-index: 1000;
            }

            .logo {
                color: #4a90e2;
                text-decoration: none;
                transition: transform 0.3s ease;
                cursor: pointer;
            }

            .logo:hover {
                transform: scale(1.05);
            }

            .nav-link {
                text-decoration: none !important;
                color: #333;
                padding: 0.5rem 1rem;
                border-radius: 5px;
                transition: all 0.3s ease;
                cursor: pointer;
            }

            .nav-link:hover {
                background: rgba(74, 144, 226, 0.1);
                color: #4a90e2;
            }

            /* Default button styles as originally provided */
            .nav-buttons button {
                background-color: #4a90e2 !important;
                color: white !important;
                padding: 0.75rem !important;
                border-radius: 5px !important;
                font-weight: 500 !important;
                margin: 0 0.5rem !important;
                border: none !important;
                box-shadow: none !important;
            }

            .nav-buttons button:hover,
            .button-style:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 4px 8px rgba(74, 144, 226, 0.2) !important;
            }
            
            .button-style {
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                display: inline-block;
            }

            .hero-container {
                background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
                background-size: 400% 400%;
                animation: gradient 15s ease infinite;
                border-radius: 20px;
                padding: 4rem 2rem;
                margin: 2rem 0;
                text-align: center;
            }

            @keyframes gradient {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            .feature-card {
                background: white !important;
                border-radius: 15px !important;
                padding: 2rem;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                border: none !important;
                min-height: 300px;
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                margin-bottom: 0 !important;
            }

            .feature-card:hover {
                transform: translateY(-10px);
                box-shadow: 0 0 20px rgba(74, 144, 226, 0.3) !important;
            }

            .feature-icon {
                width: 80px;
                height: 80px;
                object-fit: contain;
                margin: 1rem 0;
                filter: drop-shadow(0 5px 10px rgba(0,0,0,0.1));
            }

            .chart-container {
                background: white;
                border-radius: 15px;
                padding: 2rem;
                margin: 1rem 0;
                box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            }

            /* Hide Streamlit error messages */
            .stException, .stError {
                display: none !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    def display_navigation(self):
        st.markdown(
            """
            <div class="top-nav">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center; gap: 2rem;">
                        <a href="/" class="logo" onclick="window._streamlitapp.setSessionState({'show_login_form': false});">
                            <h2 style="margin:0;">📊 Class Manager</h2>
                        </a>
                        <div style="display: flex; gap: 1.5rem;">
                            <a href="#features" class="nav-link">Features</a>
                            <a href="#analytics" class="nav-link">Analytics</a>
                        </div>
                    </div>
                    <div class="nav-buttons" style="display: flex; gap: 0.5rem;">
                        <a href="/?show_login_form=true&current_tab=login">
                            <div class="button-style" style="width: 80px; cursor:pointer; background-color: #4a90e2; color: white; padding: 0.75rem; border-radius: 5px; font-weight: 500; text-align: center;">Login</div>
                        </a>
                        <a href="/?show_login_form=true&current_tab=signup">
                            <div class="button-style" style="width: 80px; cursor:pointer; background-color: #4a90e2; color: white; padding: 0.75rem; border-radius: 5px; font-weight: 500; text-align: center;">Sign Up</div>
                        </a>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Message below navigation bar
        st.markdown("""
            <div style="text-align: center; margin-top: 1rem; padding: 0.5rem; background-color: #f8f9fa; border-radius: 5px; font-size: 18px;">
                Transforming education through data analytics. Our platform helps educators gain insights into student performance.
            </div>
        """, unsafe_allow_html=True)

    def display_hero(self):
        st.markdown(
            """
            <div class="hero-container">
                <div style="position: relative; z-index: 1; text-align: center; color: white;">
                    <h1 style="font-size: 3.5rem; margin-bottom: 1rem;">Transform Classroom Data into Insights</h1>
                    <p style="font-size: 1.2rem; margin-bottom: 2rem;">Advanced analytics platform for educators</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    def display_features(self):
        st.markdown('<div id="features" class="section">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; margin: 1rem 0;'>Key Features</h2>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f"""
                <div class="feature-card">
                    <img src="{self.vector_images['analytics']}" class="feature-icon">
                    <h3>Advanced Analytics</h3>
                    <p>Deep dive into student performance with interactive visualizations</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f"""
                <div class="feature-card">
                    <img src="{self.vector_images['dashboard']}" class="feature-icon">
                    <h3>Real-time Dashboard</h3>
                    <p>Monitor class progress with customizable widgets and metrics</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                f"""
                <div class="feature-card">
                    <img src="{self.vector_images['reports']}" class="feature-icon">
                    <h3>Smart Reports</h3>
                    <p>Generate comprehensive reports with automatic insights</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    def display_analytics(self):
        st.markdown('<div id="analytics" class="section">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; margin: 3rem 0;'>Analytics Preview</h2>", unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["Student Progress", "Grade Distribution", "Performance Trends"])

        with tab1:
            self.create_bar_chart()

        with tab2:
            self.create_pie_chart()

        with tab3:
            self.create_line_chart()

        st.markdown('</div>', unsafe_allow_html=True)

    def create_line_chart(self):
        data = pd.DataFrame({
            "Week": [f"Week {i}" for i in range(1, 11)],
            "Average Score": np.random.randint(60, 90, 10)
        })
        fig = px.line(data, x="Week", y="Average Score",
                     title="Class Performance Trend",
                     template="plotly_white",
                     markers=True)
        fig.update_traces(line=dict(width=3),
                         marker=dict(size=8))
        st.plotly_chart(fig, use_container_width=True)

    def create_pie_chart(self):
        data = pd.DataFrame({
            "Grade": ["A", "B", "C", "D"],
            "Count": np.random.randint(5, 20, 4)
        })
        fig = px.pie(data, values="Count", names="Grade",
                    title="Grade Distribution",
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)

    def create_bar_chart(self):
        data = pd.DataFrame({
            "Student": [f"Student {i}" for i in range(1, 11)],
            "Progress": np.random.randint(1, 100, 10)
        })
        fig = px.bar(data, x="Student", y="Progress",
                    title="Individual Student Progress",
                    color="Progress",
                    color_continuous_scale="Viridis",
                    hover_data={"Progress": ":.1f"})
        st.plotly_chart(fig, use_container_width=True)

    def run(self):
        # Check URL parameters
        params = st.query_params
        if "show_login_form" in params and params["show_login_form"] == "true":
            st.session_state.show_login_form = True
            if "current_tab" in params:
                st.session_state.current_tab = params["current_tab"]
        
        if st.session_state.get("is_logged_in", False):
            st.markdown(f"<h2 style='text-align: center;'>🎉 Welcome, {st.session_state.get('identifier', 'User')}! 🎉</h2>", unsafe_allow_html=True)
            st.write("You have successfully logged in. 🚀")

            if st.button("Logout"):
                for key in ['is_logged_in', 'show_login_form', 'identifier', 'current_tab']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

        elif st.session_state.get("show_login_form", False):
            login_page = Login()
            login_page.display_login_form()

        else:
            self.display_navigation()
            self.display_hero()
            self.display_features()
            self.display_analytics()

if __name__ == "__main__":
    app = ClassManagerApp()
    app.run()
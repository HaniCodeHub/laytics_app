import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from login_system import Login

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
        st.markdown("""
            <style>
            /* Dark Theme Implementation */
            .stApp {
                background: linear-gradient(135deg, #0d1117 0%, #161b22 100%) !important;
                color: #f0f6fc !important;
            }

            /* Override all Streamlit default backgrounds */
            .main .block-container {
                background: transparent !important;
                padding-top: 1rem !important;
            }

            /* Sidebar styling for dark theme */
            .css-1d391kg, .css-1rs6os, .css-17eq0hr {
                background: linear-gradient(180deg, #161b22 0%, #0d1117 100%) !important;
                border-right: 1px solid #30363d !important;
            }

            /* Navigation styling */
            .top-nav {
                backdrop-filter: blur(10px);
                background: rgba(13, 17, 23, 0.9) !important;
                box-shadow: 0 2px 10px rgba(0,0,0,0.3);
                padding: 1rem 2rem;
                position: sticky;
                top: 0;
                z-index: 1000;
                border-bottom: 1px solid #30363d;
            }

            .logo {
                color: #58a6ff !important;
                text-decoration: none;
                transition: transform 0.3s ease;
                cursor: pointer;
            }
                    
            @media screen and (max-width: 768px) {
                .top-nav {
                    flex-direction: column !important;
                    text-align: center !important;
                }

                .logo {
                    font-size: 1.8rem !important;
                    margin-bottom: 1rem !important;
                }
            }


            .logo:hover {
                transform: scale(1.05);
                color: #79c0ff !important;
            }

            .nav-link {
                text-decoration: none !important;
                color: #f0f6fc !important;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                transition: all 0.3s ease;
                cursor: pointer;
                display: inline-block;
            }

            .nav-link:hover {
                background: rgba(88, 166, 255, 0.15) !important;
                color: #58a6ff !important;
            }

            
            .section {
                scroll-margin-top: 80px;
                padding: 40px 0;
            }

            /* Dark hero section */
            .hero-container {
                background: linear-gradient(-45deg, #7c3aed, #2563eb, #059669, #dc2626);
                background-size: 400% 400%;
                animation: gradient 15s ease infinite;
                border-radius: 20px;
                padding: 4rem 2rem;
                border: 1px solid #30363d;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }

            @keyframes gradient {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            /* Dark feature cards */
            .feature-card {
                background: linear-gradient(135deg, #21262d 0%, #161b22 100%) !important;
                border: 1px solid #30363d !important;
                border-radius: 15px !important;
                padding: 2rem;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                min-height: 300px;
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                margin-bottom: 0 !important;
                color: #f0f6fc !important;
            }

            .feature-card:hover {
                transform: translateY(-10px);
                box-shadow: 0 15px 30px rgba(0,0,0,0.4) !important;
                border-color: #58a6ff !important;
            }

            .feature-card h3 {
                color: #58a6ff !important;
                margin: 1rem 0 !important;
            }

            .feature-icon {
                width: 80px;
                height: 80px;
                object-fit: contain;
                margin: 1rem 0;
                filter: drop-shadow(0 5px 10px rgba(0,0,0,0.3)) brightness(0.9) contrast(1.1);
            }

            /* Chart containers */
            .chart-container {
                background: linear-gradient(135deg, #21262d 0%, #161b22 100%);
                border: 1px solid #30363d;
                border-radius: 15px;
                padding: 2rem;
                margin: 1rem 0;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }

            /* Streamlit specific dark theme overrides */
            .stMarkdown, .stText {
                color: #f0f6fc !important;
            }

            .stSelectbox > div > div {
                background-color: #21262d !important;
                border: 1px solid #30363d !important;
                color: #f0f6fc !important;
            }

            .stTextInput > div > div > input {
                background-color: #21262d !important;
                border: 1px solid #30363d !important;
                color: #f0f6fc !important;
            }

            .stTextArea > div > div > textarea {
                background-color: #21262d !important;
                border: 1px solid #30363d !important;
                color: #f0f6fc !important;
            }

            # /* Tabs styling */
            # .stTabs [data-baseweb="tab-list"] {
            #     background: linear-gradient(135deg, #21262d 0%, #161b22 100%) !important;
            #     border-radius: 10px !important;
            #     border: 1px solid #30363d !important;
            # }

            # .stTabs [data-baseweb="tab"] {
            #     background: transparent !important;
            #     color: #8b949e !important;
            #     border-radius: 8px !important;
            #     padding: 10px 20px !important;
            #     margin: 4px !important;
            # }

            # .stTabs [aria-selected="true"] {
            #     background: linear-gradient(135deg, #58a6ff 0%, #79c0ff 100%) !important;
            #     color: #0d1117 !important;
            # }

            /* Metrics styling */
            [data-testid="metric-container"] {
                background: linear-gradient(135deg, #21262d 0%, #161b22 100%) !important;
                border: 1px solid #30363d !important;
                border-radius: 10px !important;
                padding: 1rem !important;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
            }

            [data-testid="metric-container"] > div {
                color: #f0f6fc !important;
            }

            /* Plotly charts dark theme */
            .js-plotly-plot {
                background: transparent !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    def display_navigation(self):
        col1, col2, col3 = st.columns([4, 0.001, 1])

        with col1:
            st.markdown(
                """
                <div class="top-nav">
                    <div style="display: flex; align-items: center; gap: 2rem;">
                        <h2 class="logo" style="margin:0;">Laytics</h2>
                        <div style="display: flex; gap: 1.5rem;">
                            <a href="#features" class="nav-link">Features</a>
                            <a href="#analytics" class="nav-link">Analytics</a>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            if st.button("Login", key="nav_login", use_container_width=True, type="secondary"):
                st.session_state.show_login_form = True
                st.session_state.show_signup = False
                st.rerun()
            if st.button("Sign Up", key="nav_signup", use_container_width=True, type="primary"):
                st.session_state.show_signup = True
                st.session_state.show_login_form = False
                st.rerun()

        st.markdown("<h2 style='text-align: center;'>🎓 Welcome to edu anaytics</h2>", unsafe_allow_html=True)

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
            "Students": [f"Student {i}" for i in range(1, 11)],
            "Average Score": np.random.randint(60, 90, 10)
        })
        fig = px.line(data, x="Students", y="Average Score",
                     title="Class Performance Trend",
                     template="plotly_dark",
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
                    template="plotly_dark",
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
                    template="plotly_dark",
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
            st.markdown(f"<h2 style='text-align: center;'>Welcome, {st.session_state.get('identifier', 'User')}! </h2>", unsafe_allow_html=True)
            st.write("You have successfully logged in. ")

            if st.button("Logout", type="primary"):
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

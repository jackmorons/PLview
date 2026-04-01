import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(
    page_title="PLview",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to hide the sidebar, style the top navbar, and add a footer
def inject_custom_css():
    st.markdown("""
        <style>
        /* Hide the default Streamlit sidebar and header */
        [data-testid="collapsedControl"] { display: none; }
        section[data-testid="stSidebar"] { display: none; }
        header {visibility: hidden;}
        
        /* Reduce top/bottom padding of main content */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 5rem !important;
        }
        
        /* Powerlifting disk accent bar at the very top of the page */
        .disk-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            z-index: 999999;
            background: linear-gradient(
                90deg,
                #d32f2f 0%,
                #d32f2f 15%,
                #1976d2 25%,
                #1976d2 35%,
                #f9a825 45%,
                #f9a825 55%,
                #388e3c 65%,
                #388e3c 75%,
                #e0e0e0 85%,
                #e0e0e0 100%
            );
        }
        
        /* Logo styling */
        .nav-logo {
            font-size: 1.8rem;
            font-weight: 800;
            color: #f0f0f5;
            letter-spacing: -0.5px;
            margin-top: -5px;
        }
        .nav-logo span {
            color: #d32f2f;
        }

        /* Hero Text Styles (used in home.py) */
        .hero-title {
            font-size: 3.5rem !important;
            font-weight: 800 !important;
            letter-spacing: -1px;
            line-height: 1.15;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #f0f0f5 30%, #d32f2f 65%, #1976d2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
        }
        .hero-subtitle {
            font-size: 1.25rem;
            color: #9a9ab0;
            text-align: center;
            margin-bottom: 2rem;
        }

        /* Fixed Footer */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            text-align: center;
            padding: .8rem;
            background-color: #1a1a24;
            color: #5e5e73;
            font-size: 0.85rem;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            z-index: 999998;
        }
        .disk-bar2 {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 4px;
            z-index: 999999;
            background: linear-gradient(
                90deg,
                #d32f2f 0%,
                #d32f2f 15%,
                #1976d2 25%,
                #1976d2 35%,
                #f9a825 45%,
                #f9a825 55%,
                #388e3c 65%,
                #388e3c 75%,
                #e0e0e0 85%,
                #e0e0e0 100%
            );
        }

        /* --- Header Nav Link Colors --- */
        div[data-testid="stColumn"] a[data-testid="stPageLink-NavLink"] {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }

        /* Targeting each column's page link to apply predetermined colors */
        
        /* Home (RED) */
        div[data-testid="stColumn"]:nth-of-type(2) a[data-testid="stPageLink-NavLink"] {
            background-color: rgba(211, 47, 47, 0.1);
            border: 1px solid #d32f2f;
            border-radius: 8px;
            transition: all 0.2s ease;
        }
        div[data-testid="stColumn"]:nth-of-type(2) a[data-testid="stPageLink-NavLink"] p {
            color: #e57373 !important;
            font-weight: 600;
        }
        div[data-testid="stColumn"]:nth-of-type(2) a[data-testid="stPageLink-NavLink"]:hover {
            background-color: #d32f2f;
            transform: translateY(-2px);
        }
        div[data-testid="stColumn"]:nth-of-type(2) a[data-testid="stPageLink-NavLink"]:hover p {
            color: #ffffff !important;
        }

        /* Athletes (BLUE) */
        div[data-testid="stColumn"]:nth-of-type(3) a[data-testid="stPageLink-NavLink"] {
            background-color: rgba(25, 118, 210, 0.1);
            border: 1px solid #1976d2;
            border-radius: 8px;
            transition: all 0.2s ease;
        }
        div[data-testid="stColumn"]:nth-of-type(3) a[data-testid="stPageLink-NavLink"] p {
            color: #64b5f6 !important;
            font-weight: 600;
        }
        div[data-testid="stColumn"]:nth-of-type(3) a[data-testid="stPageLink-NavLink"]:hover {
            background-color: #1976d2;
            transform: translateY(-2px);
        }
        div[data-testid="stColumn"]:nth-of-type(3) a[data-testid="stPageLink-NavLink"]:hover p {
            color: #ffffff !important;
        }

        /* Records (GOLD) */
        div[data-testid="stColumn"]:nth-of-type(4) a[data-testid="stPageLink-NavLink"] {
            background-color: rgba(249, 168, 37, 0.1);
            border: 1px solid #f9a825;
            border-radius: 8px;
            transition: all 0.2s ease;
        }
        div[data-testid="stColumn"]:nth-of-type(4) a[data-testid="stPageLink-NavLink"] p {
            color: #ffd54f !important;
            font-weight: 600;
        }
        div[data-testid="stColumn"]:nth-of-type(4) a[data-testid="stPageLink-NavLink"]:hover {
            background-color: #f9a825;
            transform: translateY(-2px);
        }
        div[data-testid="stColumn"]:nth-of-type(4) a[data-testid="stPageLink-NavLink"]:hover p {
            color: #ffffff !important;
        }

        /* Raw Data (GREEN) */
        div[data-testid="stColumn"]:nth-of-type(5) a[data-testid="stPageLink-NavLink"] {
            background-color: rgba(56, 142, 60, 0.1);
            border: 1px solid #388e3c;
            border-radius: 8px;
            transition: all 0.2s ease;
        }
        div[data-testid="stColumn"]:nth-of-type(5) a[data-testid="stPageLink-NavLink"] p {
            color: #81c784 !important;
            font-weight: 600;
        }
        div[data-testid="stColumn"]:nth-of-type(5) a[data-testid="stPageLink-NavLink"]:hover {
            background-color: #388e3c;
            transform: translateY(-2px);
        }
        div[data-testid="stColumn"]:nth-of-type(5) a[data-testid="stPageLink-NavLink"]:hover p {
            color: #ffffff !important;
        }

        /* Info (WHITE) */
        div[data-testid="stColumn"]:nth-of-type(6) a[data-testid="stPageLink-NavLink"] {
            background-color: rgba(150, 150, 150, 0.1);
            border: 1px solid #9e9e9e;
            border-radius: 8px;
            transition: all 0.2s ease;
        }
        div[data-testid="stColumn"]:nth-of-type(6) a[data-testid="stPageLink-NavLink"] p {
            color: #e0e0e0 !important;
            font-weight: 600;
        }
        div[data-testid="stColumn"]:nth-of-type(6) a[data-testid="stPageLink-NavLink"]:hover {
            background-color: #757575;
            transform: translateY(-2px);
        }
        div[data-testid="stColumn"]:nth-of-type(6) a[data-testid="stPageLink-NavLink"]:hover p {
            color: #ffffff !important;
        }
        </style>
        
        <div class="disk-bar"></div>
        <div class="disk-bar2"></div>
        <div class="footer">PLview &copy; 2026. Data sourced from OpenPowerlifting.</div>
    """, unsafe_allow_html=True)

inject_custom_css()

# Pages definition
pages = {
    "Home": st.Page("pages/home.py", title="Home", icon="🏠"),
    "Athletes": st.Page("pages/athletes.py", title="Athletes", icon="🏋️"),
    "Records": st.Page("pages/record.py", title="Records", icon="🏆"),
    "Tools": st.Page("pages/tools.py", title="Tools", icon="⚙️"),
    "Info": st.Page("pages/info.py", title="Info", icon="ℹ️")
}

# Render top navigation using native columns
with st.container():
    # Col 0 is the Logo, the rest are nav links
    headerNavLinks = st.columns([5, 1, 1, 1, 1, 1])
    
    with headerNavLinks[0]: 
        st.markdown('<div class="nav-logo">PL<span>view</span></div>', unsafe_allow_html=True)
    with headerNavLinks[1]: st.page_link(pages["Home"], label="Home", icon="🏠", use_container_width=True)
    with headerNavLinks[2]: st.page_link(pages["Athletes"], label="Athletes", icon="🏋️", use_container_width=True)
    with headerNavLinks[3]: st.page_link(pages["Records"], label="Records", icon="🏆", use_container_width=True)
    with headerNavLinks[4]: st.page_link(pages["Tools"], label="Tools", icon="⚙️", use_container_width=True)
    with headerNavLinks[5]: st.page_link(pages["Info"], label="Info", icon="ℹ️", use_container_width=True)

st.markdown("---")

# import data from csv files as dictionaries
males_data = pd.read_csv("datasets/OP_Males.csv")
females_data = pd.read_csv("datasets/OP_Females.csv")

if st.session_state.get("males_data") is None:
    st.session_state["males_data"] = males_data
if st.session_state.get("females_data") is None:
    st.session_state["females_data"] = females_data


# Run navigation engine
pg = st.navigation(list(pages.values()), position="hidden")
pg.run()
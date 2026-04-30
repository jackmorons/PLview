import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
        /* Hide the default Streamlit sidebar and header */
        [data-testid="collapsedControl"] { display: none; }
        section[data-testid="stSidebar"] { display: none; }
        header { visibility: hidden; display: none; }
        [data-testid="stHeader"] { display: none; }
        /* Radial gradient background */
        .stApp {
            background: radial-gradient(circle at 50% 100%, #1e1e2b 0%, #0e0e12 80%, #050505 100%);
            background-attachment: fixed;
        }

        /* Custom horizontal rule for a more elegant look */
        hr {
            border: 0;
            height: 1px;
            background-image: linear-gradient(to right, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0));
            margin-top: 2rem !important;
            margin-bottom: 2rem !important;
        }
        
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
            font-size: clamp(5rem, 8vw, 5.0rem) !important;
            font-weight: 800 !important;
            letter-spacing: -1px;
            line-height: 1.15;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #f0f0f5 30%, #d32f2f 65%, #1976d2);
            /* background: linear-gradient(135deg, #d32f2f 35%, #1976d2 45%, #f9a825 50%, #388e3c 55%, #e0e0e0 65%); */
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

        /* Mobile Responsiveness Overrides */
        @media (max-width: 640px) {
            .hero-title {
                font-size: 4rem !important;
                line-height: 1.2 !important;
                width: 100% !important;
            }
            .block-container {
                padding-left: 0.5rem !important;
                padding-right: 0.5rem !important;
                max-width: 100% !important;
            }
        }

        /* Fixed Footer */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            text-align: center;
            padding: .8rem;
            background: rgba(14, 14, 18, 0.85);
            backdrop-filter: blur(8px);
            color: #5e5e73;
            font-size: 0.85rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
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

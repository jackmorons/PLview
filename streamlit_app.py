import streamlit as st

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
            padding-top: 5rem !important;
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
                #d32f2f 20%,
                #1976d2 20%,
                #1976d2 40%,
                #388e3c 40%,
                #388e3c 60%,
                #f9a825 60%,
                #f9a825 80%,
                #e0e0e0 80%,
                #e0e0e0 100%
            );
        }
        
        /* Logo styling */
        .nav-logo {
            font-size: 1.5rem;
            font-weight: 800;
            color: #f0f0f5;
            letter-spacing: -0.5px;
            margin-top: 5px;
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
            padding: 1rem;
            background-color: #1a1a24;
            color: #5e5e73;
            font-size: 0.85rem;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            z-index: 999998;
        }
        </style>
        
        <div class="disk-bar"></div>
        <div class="footer">PLview &copy; 2026. Data sourced from OpenPowerlifting.</div>
    """, unsafe_allow_html=True)

inject_custom_css()

# Pages definition
pages = {
    "Home": st.Page("pages/home.py", title="Home", icon="🏠"),
    "Athletes": st.Page("pages/athletes.py", title="Athletes", icon="🏋️"),
    "Records": st.Page("pages/record.py", title="Records", icon="🏆"),
    "Raw Data": st.Page("pages/raw.py", title="Raw Data", icon="📊"),
    "Info": st.Page("pages/info.py", title="Info", icon="ℹ️")
}

# Render top navigation using native columns
with st.container():
    # Col 0 is the Logo, the rest are nav links
    cols = st.columns([4, 1, 1, 1, 1, 1])
    
    with cols[0]: 
        st.markdown('<div class="nav-logo">PL<span>view</span></div>', unsafe_allow_html=True)
    with cols[1]: st.page_link(pages["Home"], label="Home", icon="🏠")
    with cols[2]: st.page_link(pages["Athletes"], label="Athletes", icon="🏋️")
    with cols[3]: st.page_link(pages["Records"], label="Records", icon="🏆")
    with cols[4]: st.page_link(pages["Raw Data"], label="Raw", icon="📊")
    with cols[5]: st.page_link(pages["Info"], label="Info", icon="ℹ️")

st.markdown("---")

# Run navigation engine
pg = st.navigation(list(pages.values()), position="hidden")
pg.run()

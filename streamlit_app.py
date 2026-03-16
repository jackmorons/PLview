import streamlit as st

st.set_page_config(
    page_title="PLview",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to hide the sidebar and style the top navbar
def inject_custom_css():
    st.markdown("""
        <style>
        /* Hide the default Streamlit sidebar */
        [data-testid="collapsedControl"] { display: none; }
        section[data-testid="stSidebar"] { display: none; }
        
        /* Hide the default Streamlit header bar */
        header {visibility: hidden;}
        
        /* Reduce top padding of main content to make room for nav */
        .block-container {
            padding-top: 5rem !important;
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
        
        /* Custom Top Navbar Styling Container */
        .custom-navbar {
            position: fixed;
            top: 4px;
            right: 2rem;
            z-index: 999998;
            background-color: rgba(18, 18, 24, 0.9);
            padding: 0.5rem 1rem;
            border-radius: 0 0 12px 12px;
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-top: none;
            display: flex;
            gap: 15px;
        }

        /* Adjust hero text gradient to match the HTML version */
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
        </style>
        
        <div class="disk-bar"></div>
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

# Render top navigation using native columns mapped to HTML
with st.container():
    cols = st.columns([8, 1, 1, 1, 1, 1])
    with cols[1]: st.page_link(pages["Home"], label="Home", icon="🏠")
    with cols[2]: st.page_link(pages["Athletes"], label="Athletes", icon="🏋️")
    with cols[3]: st.page_link(pages["Records"], label="Records", icon="🏆")
    with cols[4]: st.page_link(pages["Raw Data"], label="Raw", icon="📊")
    with cols[5]: st.page_link(pages["Info"], label="Info", icon="ℹ️")

st.markdown("---")

# Run navigation engine
pg = st.navigation(list(pages.values()), position="hidden")
pg.run()

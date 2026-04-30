import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="PLview",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from style_utils import inject_custom_css

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
        st.markdown('<div class="nav-logo">PL<span class="red">v</span><span class="blue">i</span><span class="gold">e</span><span class="green">w</span></div>', unsafe_allow_html=True)
    with headerNavLinks[1]: st.page_link(pages["Home"], label="Home", icon="🏠", use_container_width=True)
    with headerNavLinks[2]: st.page_link(pages["Athletes"], label="Athletes", icon="🏋️", use_container_width=True)
    with headerNavLinks[3]: st.page_link(pages["Records"], label="Records", icon="🏆", use_container_width=True)
    with headerNavLinks[4]: st.page_link(pages["Tools"], label="Tools", icon="⚙️", use_container_width=True)
    with headerNavLinks[5]: st.page_link(pages["Info"], label="Info", icon="ℹ️", use_container_width=True)

st.markdown("---")

# import data from csv files as dictionaries
males_data = pd.read_csv("datasets/OP_Males.csv", sep=";")
females_data = pd.read_csv("datasets/OP_Females.csv", sep=";")

if st.session_state.get("males_data") is None:
    st.session_state["males_data"] = males_data
if st.session_state.get("females_data") is None:
    st.session_state["females_data"] = females_data

# Run navigation engine
pg = st.navigation(list(pages.values()), position="hidden")
pg.run()
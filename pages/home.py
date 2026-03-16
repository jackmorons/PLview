import streamlit as st

st.markdown('<div class="hero-title">Powerlifting,<br>Visualized.</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Explore athletes, records, and data from the world of powerlifting — all in one place.</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.markdown("""
        <style>
        div[data-testid="stElementContainer"]:has(.athlete-btn-marker) + div[data-testid="stElementContainer"] button {
            background-color: rgba(211, 47, 47, 0.1);
            border: 1px solid #d32f2f;
            color: #ef5350;
            transition: all 0.2s ease;
        }
        div[data-testid="stElementContainer"]:has(.athlete-btn-marker) + div[data-testid="stElementContainer"] button:hover {
            background-color: #d32f2f;
            color: #ffffff;
            border: 1px solid #d32f2f;
        }
        </style>
        <div class="athlete-btn-marker"></div>
    """, unsafe_allow_html=True)
    if st.button("Browse Athletes", type="primary", use_container_width=True):
        st.switch_page("pages/athletes.py")

col4, col5, col6 = st.columns([1, 1, 1])
with col5:
    st.markdown("""
        <style>
        div[data-testid="stElementContainer"]:has(.record-btn-marker) + div[data-testid="stElementContainer"] button {
            background-color: rgba(25, 118, 210, 0.1);
            border: 1px solid #1976d2;
            color: #64b5f6;
            transition: all 0.2s ease;
        }
        div[data-testid="stElementContainer"]:has(.record-btn-marker) + div[data-testid="stElementContainer"] button:hover {
            background-color: #1976d2;
            color: #ffffff;
            border: 1px solid #1976d2;
        }
        </style>
        <div class="record-btn-marker"></div>
    """, unsafe_allow_html=True)
    if st.button("Browse Records", type="primary", use_container_width=True):
        st.switch_page("pages/record.py")

st.markdown("---")

# Feature Cards
c1, c2, c3 = st.columns(3)

with c1:
    st.page_link("pages/athletes.py", label="**Athletes**", icon="🏋️", font_size="large")
    st.write("Search and explore athlete profiles, competition history, and personal bests.")

with c2:
    st.page_link("pages/record.py", label="**Records**", icon="🏆", font_size="large")
    st.write("Discover all-time records across weight classes, federations, and events.")

with c3:
    st.page_link("pages/tools.py", label="**Tools**", icon="⚙️", font_size="large")
    st.write("Tools for data analysis and visualization built for coaches and athletes.")

st.markdown("---")
st.markdown("## Gallery")

# Gallery Grid
g1, g2 = st.columns(2)
with g1:
    st.info("📷 Image 1 (Placeholder)")
    st.info("📷 Image 3 (Placeholder)")
with g2:
    st.info("📷 Image 2 (Placeholder)")
    st.info("📷 Image 4 (Placeholder)")

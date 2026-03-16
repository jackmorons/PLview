import streamlit as st

st.markdown('<div class="hero-title">Powerlifting,<br>Visualized.</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Explore athletes, records, and raw data from the world of powerlifting — all in one place.</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Browse Athletes", type="primary", use_container_width=True):
        st.switch_page("pages/athletes.py")

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
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
    st.markdown("### 🏋️ Athletes")
    st.write("Search and explore athlete profiles, competition history, and personal bests.")

with c2:
    st.markdown("### 🏆 Records")
    st.write("Discover all-time records across weight classes, federations, and events.")

with c3:
    st.markdown("### 📊 Raw Data")
    st.write("Dive into the raw dataset and run your own queries and analysis.")

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

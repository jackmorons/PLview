import streamlit as st

st.set_page_config(page_title="Info - PLview", page_icon="ℹ️", layout="wide")

# ── Header Section ───────────────────────────────────────────────────
st.title("ℹ️ Project Information")
st.markdown("""
    Welcome to **PLview**, the ultimate data exploration suite for powerlifting. 
    Whether you're a coach seeking a competitive edge or a curious lifter wondering how 
    you stack up against the global average, we've got the charts for you.
""")

st.markdown("---")

# ── The Engine Room (Sources) ────────────────────────────────────────
st.header("🗄️ The Data Engine")
col1, col2 = st.columns([1, 2])

with col1:
    # Humor: No creatine was used
    st.image("https://www.openpowerlifting.org/static/openpowerlifting.svg", width=200)

with col2:
    st.subheader("Data Source: OpenPowerlifting")
    st.write("""
        At the heart of PLview lies the **OpenPowerlifting** database—the gold standard 
        for strength sports records. This project is possible thanks to the tireless 
        volunteers who archive every single attempt in the sport's history.
        
        *   **Dataset Scope**: Over **120,000+** unique contest results.
        *   **Cleaning Process**: We've removed anomalies (like the 0kg SHW squatters) 
            to ensure that the "Average" truly represents the reality of the platform.
        *   **Disclaimer**: This app is for informational purposes. While our math is 
            precise, it does not guarantee your 3rd deadlift will move. 
    """)

st.markdown("---")

# ── Reading the Charts ───────────────────────────────────────────────
st.header("📊 Chart Reading 101")
st.write("If the colors and lines look confusing, here’s a quick field guide to the analytics:")

with st.expander("🛡️ Radar Charts: The Strength Geometry"):
    st.write("""
        - **Outer Points**: Represent the absolute maximums or best coefficients. 
        - **Area**: The bigger the shape, the more "balanced" the athlete. 
        - **Z-Ordering**: In our 1v1 tool, we always put the smaller shape on top 
          so you can see how much further you need to grow to engulf your competition!
    """)

with st.expander("🗺️ Heatmaps: Searching the Ocean"):
    st.write("""
        - **Brightness (Yellow/Green)**: Areas of high population density. Most people live here.
        - **Darkness (Purple)**: The "Quiet Zones." If you see a star marker here at a high Total, 
          you're looking at a world-class outlier (a 'Freak' in our Sandbox terms).
    """)

with st.expander("📈 Trend Path: The Road to White Lights"):
    st.write("""
        - **The Staircase**: Shows your recommended attempt progression.
        - **The Shaded Aura**: This is the 'Safe Zone'—representing **±1 Standard Deviation** 
          of thousands of successful lifters in your weight class. Straying too far outside 
          it might mean your opener is too heavy or your 2nd is too conservative.
    """)

st.markdown("---")

# ── Humor & Credits ──────────────────────────────────────────────────
st.header("🧠 About the Project")
st.info("""
    **PLview** was born from a passion for both brute force and clean data. 
    It was created as a final project for a **Data Visualization University Course**, 
    proving once and for all that mathematicians can (sometimes) bench press.
""")

st.write("---")

# ── Contacts Row ─────────────────────────────────────────────────────
st.header("✉️ Get in Touch")
st.write("Found a bug? Have a feature request? Or just want to brag about your new PR?")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("#### 📧 Email (Lead)")
    st.code("placeholder.one@example.com")

with c2:
    st.markdown("#### 📧 Email (Dev)")
    st.code("placeholder.two@example.com")

with c3:
    st.markdown("#### 🔗 LinkedIn")
    st.markdown("[Visit Profile One](https://www.linkedin.com/in/placeholder1/)")

with c4:
    st.markdown("#### 🔗 LinkedIn")
    st.markdown("[Visit Profile Two](https://www.linkedin.com/in/placeholder2/)")

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("PLview v1.0.0 | Powered by Python, Streamlit, and 100% Pure Data.")

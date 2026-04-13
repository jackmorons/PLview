import streamlit as st
from style_utils import inject_custom_css

inject_custom_css()


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
    # Humor: No creatine was used (Actually, it was)
    st.image("https://gitlab.com/uploads/-/system/project/avatar/6722790/favicon.png", width=200)

with col2:
    st.subheader("Data Source: OpenPowerlifting")
    st.write("""
        At the heart of PLview lies the **OpenPowerlifting** database—the gold standard 
        for strength sports records. This project is possible thanks to the tireless 
        volunteers who archive every single attempt in the sport's history.
        
        *   **Dataset Scope**: Over **120,000+** unique contest results.
        *   **Cleaning Process**: We've removed anomalies (like the 0kg SHW squatters) 
            to ensure that the "Average" truly represents the reality of the platform,
            we also removed single lifts competition for simplicity.
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

with st.expander("🔴 Dots?"):
    st.write("""
        - **What is the Dots value?**: the Dots (Dynamic Objective Team Scoring) is a unified
        method of evaluating someone's strength, taking in consideration their body weight, age and
        total.
    """)

with st.expander("📉 Pearson coefficient"):
    st.write("""
        - **What is the Pearson coefficient?**: the Pearson coefficient is a measure of the
        linear correlation between two sets of data. It is a value between -1 and 1, where 1
        indicates a perfect positive correlation, -1 indicates a perfect negative correlation,
        and 0 indicates no correlation.
    """)

st.markdown("---")

# ── Humor & Credits ──────────────────────────────────────────────────
st.header("🧠 About the Project")
st.info("""
    **PLview** was born from a passion for both brute force and clean data. 
    It was created as a final project for a **Data Visualization University Course**, 
    proving once and for all that engineers can (sometimes) bench press.
""")

st.write("---")

# ── Contacts Row ─────────────────────────────────────────────────────
st.header("✉️ Get in Touch")
st.write("Found a bug? Have a feature request? Or just want to brag about your new PR?")

c1, c2 = st.columns(2)

with c1:
    st.markdown("#### 📧 Email (Muscles)")
    st.code("niccolo.marino@mail.polimi.it")
    st.markdown("#### 🔗 LinkedIn")
    st.markdown("[Visit Profile One](https://www.linkedin.com/in/niccol%C3%B2-marino-a26190267/)")

with c2:
    st.markdown("#### 📧 Email (Brain)")
    st.code("giacomogiovanni.moroni@mail.polimi.it")
    st.markdown("#### 🔗 LinkedIn")
    st.markdown("[Visit Profile Two](https://www.linkedin.com/in/giacomogiovanni-moroni/)")


st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("PLview v1.0.0 | Powered by Python, Streamlit, Creatine and 100% Pure Data.")

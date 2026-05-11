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
        
        *   **Dataset Scope**: Over **120.000+** unique contest results.
        *   **Cleaning Process**: We've removed anomalies (like the 0kg SHW squatters) 
            to ensure that the "Average" truly represents the reality of the platform,
            we also removed single lifts competition for simplicity.
        *   **Disclaimer**: This app is for informational purposes. While our math is 
            precise, it does not guarantee your 3rd deadlift will move. 
    """)

st.markdown("---")

# ── Reading the Charts ───────────────────────────────────────────────
st.header("📊 Chart Reading 101")
st.write("If the colors and lines look confusing, here’s a quick field guide to the analytics and science behind PLview.")

# --- 1. Visual Geometry ---
st.subheader("📐 Visual Geometry")

with st.expander("🛡️ Radar Charts: The Strength Profile"):
    st.write("""
        Radar charts visualize multi-dimensional data in a single 'web'. We use two types:
        
        - **S/B/D Profile**: Shows the absolute balance between your Squat, Bench, and Deadlift. 
            - *How to read*: A perfectly equilateral triangle means a balanced lifter. A sharp point towards one lift indicates a specialist (e.g., a "Bench Specialist").
        - **Coefficient Battle**: Compares multiple scoring systems (Dots, Wilks, etc.). 
            - *How to read*: Since different systems use different scales, we **normalize** these to a 0-100 scale. A score of 100 on the radar represents a world-class level for that specific coefficient.
        - **Pro Tip**: In 1v1 matchups, the smaller shape is always plotted on top of the larger one, making the performance gap immediately visible.
    """)

with st.expander("🗺️ Density Heatmaps: The Ocean of Lifters"):
    st.write("""
        Heatmaps represent the population density across two variables (usually Bodyweight vs. Total).
        
        - **Colorscale (Viridis)**: 
            - **Yellow/Green**: High density. This is where the majority of lifters sit.
            - **Dark Purple**: Low density. These are the outliers.
        - **Non-Linear Scaling**: We use a power-law transformation ($x^3$) for the colors. This "stretches" the scale at the bottom, making it easier to see the difference between 0 lifters and 1-5 lifters in a specific weight/total region.
        - **Markers**: Star markers represent specific athletes. If a star is in a dark purple region but high on the Y-axis, you are looking at a "Freak"—someone lifting weights very few others can at that bodyweight.
    """)

with st.expander("📉 Histograms: Population Distribution"):
    st.write("""
        Histograms show how often certain values occur in the population.
        
        - **X-Axis**: The metric value (e.g., Total in kg).
        - **Y-Axis (Frequency)**: We use **Relative Frequency (Normalized to 1)**. This means the sum of all bars equals 100% of that population (e.g., all Males in the database).
        - **Why Relative?**: It allows you to compare groups of different sizes (e.g., 50,000 Males vs 15,000 Females) on the same scale without one group dwarfing the other.
    """)

with st.expander("📈 Trend Paths & Shaded Areas"):
    st.write("""
        Used primarily in the **Entry Calculator** and **Fatigue Manager**.
        
        - **The Staircase**: Represents a discrete progression (e.g., 1st → 2nd → 3rd attempts).
        - **The Shaded Aura (Population Norm)**: This represents **±1 Standard Deviation** from the mean of successful performances. 
            - *Example*: In the Entry Calculator, staying within the green shaded area means your jump sizes are statistically aligned with how most successful lifters (who go 3-for-3) manage their energy.
    """)

# --- 2. The Coefficient Lab ---
st.subheader("🧪 The Coefficient Lab")
st.write("How do we compare a 60kg woman to a 120kg man? We use mathematical formulas called coefficients.")

with st.expander("🔴 Dots (Dynamic Objective Team Scoring)"):
    st.write("""
        The current standard for many international federations.
        - **Mechanism**: Uses a complex polynomial curve based on bodyweight and sex.
        - **Advantage**: It is designed to be more "fair" across the entire spectrum of bodyweights, reducing the historical advantage that extremely light or extremely heavy lifters had in older systems.
        - **Scale**: A score above **500** is considered elite/national level; above **600** is world-class.
    """)

with st.expander("⚪ Wilks (The Classic)"):
    st.write("""
        The most famous coefficient in powerlifting history.
        - **Mechanism**: A 5th-degree polynomial formula developed by Robert Wilks.
        - **Context**: While less common in the IPF now, it remains the "lingua franca" for many lifters globally when discussing relative strength.
    """)

with st.expander("🟢 Goodlift (IPF Points)"):
    st.write("""
        The modern official system of the International Powerlifting Federation.
        - **Mechanism**: Unlike Dots or Wilks, it is a **points-based system** derived from the regression of actual world-level competition data.
        - **Scale**: Usually expressed in points (e.g., 100 points). It is specifically tuned to reward lifters who perform well relative to the top of their specific category.
    """)

with st.expander("🔵 Glossbrenner"):
    st.write("""
        A hybrid coefficient often used in geared (equipped) powerlifting or by specific federations like the WPC.
        - **Mechanism**: Combines elements of the Wilks and Oliphant formulas. It is often perceived as being more favorable to mid-heavyweight lifters compared to Dots.
    """)

# --- 3. Scientific Metrics ---
st.subheader("🔬 Scientific Metrics")

with st.expander("🔢 Pearson Correlation Coefficient (r)"):
    st.write("""
        Used in our **Correlation Matrix** to show how two variables are related.
        - **r = 1.0 (Bright Red)**: Perfect Positive Correlation. As X goes up, Y goes up (e.g., Squat vs Total).
        - **r = 0.0 (White)**: No Correlation. The variables are independent (e.g., Age vs Eye Color).
        - **r = -1.0 (Bright Blue)**: Perfect Negative Correlation. As X goes up, Y goes down (e.g., Age vs relative strength in older populations).
    """)

with st.expander("🏆 Percentile Standing"):
    st.write("""
        Found in our **Gauge Charts**.
        - **Meaning**: A percentile tells you what percentage of the population you are **stronger than**.
        - **Example**: A **95th Percentile** standing means if you were in a room with 100 random lifters from the database, you would be stronger than 95 of them. You are in the "Top 5%".
    """)

with st.expander("⚡ Strength Efficiency (Total/BW)"):
    st.write("""
        The simplest measure of relative strength.
        - **Calculation**: Your Total divided by your Bodyweight.
        - **Example**: If you weigh 100kg and lift 700kg, your efficiency is **7.0x**. 
        - **Insight**: Generally, lighter lifters have higher efficiency ratios (e.g., 10x) because of the square-cube law in biology, while heavyweights may have lower ratios (e.g., 5x) but higher absolute totals.
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

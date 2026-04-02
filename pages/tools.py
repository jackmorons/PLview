import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Tools - PLview", page_icon="⚙️", layout="wide")

st.header("Tools")
st.write("Tools for data analysis and visualization built for coaches and athletes.")

# ── Custom CSS for sub-navigation buttons ─────────────────────────────
st.markdown("""
    <style>
    /* Target the buttons inside columns and color the 'primary' (active) one */
    div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"]:nth-of-type(1) button[kind="primary"] {
        background-color: #d32f2f !important; color: white !important; border: none !important;
    }
    div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"]:nth-of-type(2) button[kind="primary"] {
        background-color: #1976d2 !important; color: white !important; border: none !important;
    }
    div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"]:nth-of-type(3) button[kind="primary"] {
        background-color: #f9a825 !important; color: white !important; border: none !important;
    }
    div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"]:nth-of-type(4) button[kind="primary"] {
        background-color: #388e3c !important; color: white !important; border: none !important;
    }
    div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"]:nth-of-type(5) button[kind="primary"] {
        background-color: #f0f0f5 !important; color: #1a1a24 !important; border: none !important;
    }
    div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"]:nth-of-type(6) button[kind="primary"] {
        background-color: #d32f2f !important; color: white !important; border: none !important;
    }
    div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"]:nth-of-type(7) button[kind="primary"] {
        background-color: #1976d2 !important; color: white !important; border: none !important;
    }
    div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"]:nth-of-type(8) button[kind="primary"] {
        background-color: #f9a825 !important; color: white !important; border: none !important;
    }
    div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"]:nth-of-type(9) button[kind="primary"] {
        background-color: #388e3c !important; color: white !important; border: none !important;
    }
    div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"]:nth-of-type(10) button[kind="primary"] {
        background-color: #f0f0f5 !important; color: #1a1a24 !important; border: none !important;
    }
    
    /* Subtle hover effect for inactive buttons */
    div[data-testid="stColumn"] button[kind="secondary"]:hover {
        border-color: #9a9ab0 !important;
        color: #f0f0f5 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("---")

# read data stored at beginning
males_data = st.session_state["males_data"]
females_data = st.session_state["females_data"]
malesdf = pd.DataFrame(males_data)
femalesdf = pd.DataFrame(females_data)

# ── Sub-page definitions ──────────────────────────────────────────────
TOOLS_PAGES = [
    {"key": "lift_distributions", "label": "📊 Statistical Distributions"}, # 1
    {"key": "1v1", "label": "⚔️ 1v1 Strength Comparison"}, # 2
    {"key": "weight_class", "label": "⚖️ Weight Class Evaluator"}, # 3
    {"key": "trend_calculator", "label": "📈 Trend Calculator"}, # 4
    {"key": "pattern_discoverer", "label": "🔍 Pattern Discoverer"}, # 5
    #{"key": "relative_lifts", "label": "💪 Relative Lifts"},
    {"key": "freak_finder", "label": "🤯 Strength Freaks Finder"}, # 6
    {"key": "geo_strength", "label": "🌍 Geographical Strength"}, # 7
    {"key": "twin_finder", "label": "🫂 Find Your PL Twin!"}, # 8
    {"key": "strength_index_calculator", "label": "🧮 Strength Index Calculator"}, # 9
]

# Initialise active sub-page (default to first)
if "tools_active_page" not in st.session_state:
    st.session_state["tools_active_page"] = TOOLS_PAGES[0]["key"]

# ── Sub-page button row ──────────────────────────────────────────────
btn_cols = st.columns(len(TOOLS_PAGES))
for i, page in enumerate(TOOLS_PAGES):
    with btn_cols[i]:
        is_active = st.session_state["tools_active_page"] == page["key"]
        btn_type = "primary" if is_active else "secondary"
        if st.button(page["label"], key=f"tools_btn_{page['key']}", use_container_width=True, type=btn_type):
            st.session_state["tools_active_page"] = page["key"]
            st.rerun()

st.markdown("---")

# ── Sub-page content ─────────────────────────────────────────────────
active = st.session_state["tools_active_page"]



# ---------- 1. Lift Distributions ----------
if active == "lift_distributions":
    lift_cols = {
        "🏋️ Squat": "Best3SquatKg",
        "💪 Bench": "Best3BenchKg",
        "🔥 Deadlift": "Best3DeadliftKg",
        "🏆 Total": "TotalKg",
    }

    for label, col in lift_cols.items():
        st.subheader(label)
        c1, c2 = st.columns(2)
        with c1:
            fig_m = px.histogram(
                malesdf[malesdf[col] > 0], x=col,
                title=f"{label} Distribution (Males)",
                template="plotly_dark",
                color_discrete_sequence=["#42a5f5"],
                histnorm="probability",
            )
            fig_m.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="#9a9ab0", title_font_color="#f0f0f5",
                margin=dict(l=20, r=20, t=50, b=20),
            )
            fig_m.update_yaxes(title_text="Frequency (Relative)")
            st.plotly_chart(fig_m, use_container_width=True)
        with c2:
            fig_f = px.histogram(
                femalesdf[femalesdf[col] > 0], x=col,
                title=f"{label} Distribution (Females)",
                template="plotly_dark",
                color_discrete_sequence=["#ef5350"],
                histnorm="probability",
            )
            fig_f.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="#9a9ab0", title_font_color="#f0f0f5",
                margin=dict(l=20, r=20, t=50, b=20),
            )
            fig_f.update_yaxes(title_text="Frequency (Relative)")
            st.plotly_chart(fig_f, use_container_width=True)

# ---------- 2. 1v1 Strength Comparison ----------
elif active == "1v1":
    st.subheader("⚔️ 1v1 Strength Comparison")
    st.info("🚧 **Coming soon** — Detailed 1v1 strength comparison.")

# ---------- 3. Weight Class Evaluator ----------
elif active == "weight_class":
    st.subheader("⚖️ Weight Class Evaluator")
    st.info("🚧 **Coming soon** — Detailed weight class evaluator.")

# ---------- 4. Trend Calculator ----------
elif active == "trend_calculator":
    st.subheader("📈 Trend Calculator")
    st.info("🚧 **Coming soon** — Detailed trend calculator.")

# ---------- 5. Pattern Discoverer ----------
elif active == "pattern_discoverer":
    st.subheader("🔍 Pattern Discoverer")
    st.info("🚧 **Coming soon** — Detailed pattern discoverer.")

# ---------- 6. Freak Finder ----------
elif active == "freak_finder":
    st.subheader("🤯 Strength Freaks Finder")
    st.info("🚧 **Coming soon** — Detailed freak finder.")

# ---------- 7. Geographical Strength ----------
elif active == "geo_strength":
    st.subheader("🌍 Geographical Strength")
    st.info("🚧 **Coming soon** — Detailed geographical strength.")

# ---------- 8. Find Your PL Twin! ----------
elif active == "twin_finder":
    st.subheader("🫂 Find Your PL Twin!")
    st.info("🚧 **Coming soon** — Detailed twin finder.")

# ---------- 9. Strength Index Calculator ----------
elif active == "strength_index_calculator":
    st.subheader("🧮 Strength Index Calculator")
    # Dots;Wilks;Glossbrenner;Goodlift
    st.info("Insert your athlete data to calculate your strength indexes (Dots, Wilks, etc.).")

    input_cols = st.columns(4)
    
    with input_cols[0]:
        gender = st.selectbox("Gender", ["Male", "Female"], help="Select your gender for coefficient calculation.")
    
    with input_cols[1]:
        # Age range from 5 to 100
        age_options = list(range(5, 101))
        age = st.selectbox("Age", age_options, index=20, help="Your current age.")
    
    with input_cols[2]:
        # Weight from 40 to 250 with delta 0.1
        # Use np.linspace for precise step counts or np.arange with round
        weight_range = np.arange(40.0, 250.1, 0.1)
        weight_options = [round(x, 1) for x in weight_range]
        # Default to a common weight like 80.0
        try:
            default_w_idx = weight_options.index(80.0)
        except ValueError:
            default_w_idx = 0
            
        weight = st.selectbox("Bodyweight (kg)", weight_options, index=default_w_idx)
    
    with input_cols[3]:
        # Total from 0 to 1500 with delta 2.5
        total_range = np.arange(0.0, 1502.5, 2.5)
        total_options = [round(x, 1) for x in total_range]
        # Default to a common total like 400.0
        try:
            default_t_idx = total_options.index(400.0)
        except ValueError:
            default_t_idx = 0
            
        total = st.selectbox("Total (kg)", total_options, index=default_t_idx)

    st.markdown("---")
    
    # ── DOTS Calculation ───────────────────────────────────────────
    # Male: A = -0.000001093, B = 0.0007391293, C = -0.1918759221, D = 24.0900756, E = -307.75076
    # Female: A = -0.0000010706, B = 0.0005158568, C = -0.1126655495, D = 13.6175032, E = -57.96288
    # Based on DOTS standard polynomial: f(x) = Ax^4 + Bx^3 + Cx^2 + Dx + E
    if gender == "Male":
        A, B, C, D, E = -0.000001093, 0.0007391293, -0.1918759221, 24.0900756, -307.75076
    else:
        A, B, C, D, E = -0.0000010706, 0.0005158568, -0.1126655495, 13.6175032, -57.96288

    # Calculate denominator
    denom = (A * weight**4) + (B * weight**3) + (C * weight**2) + (D * weight) + E
    
    # Calculate DOTS
    if denom > 0:
        dots_score = total * (500 / denom)
    else:
        dots_score = 0.0

    # ── Wilks Calculation ───────────────────────────────────────────
    if gender == "Male":
        aw, bw, cw, dw, ew, fw = -216.0475144, 16.2606339, -0.002388645, -0.00113732, 7.01863e-6, -1.291e-8
    else:
        aw, bw, cw, dw, ew, fw = 594.31747775582, -27.23842536447, 0.82112226871, -0.00930733913, 4.731582e-5, -9.054e-8

    wilks_denom = aw + (bw * weight) + (cw * weight**2) + (dw * weight**3) + (ew * weight**4) + (fw * weight**5)
    wilks_score = total * (500 / wilks_denom) if wilks_denom > 0 else 0.0

    # ── Glossbrenner Calculation ──────────────────────────────────
    def get_glossbrenner_coeff(w, g):
        suffix = "M" if g == "Male" else "F"
        path = f"datasets/Glossbrenner_{suffix}.csv"
        try:
            df_gb = pd.read_csv(path)
            # Find closest weight
            idx = (df_gb['Weight'] - w).abs().idxmin()
            return df_gb.loc[idx, 'Coefficient']
        except Exception:
            return 0.0

    gb_coeff = get_glossbrenner_coeff(weight, gender)
    glossbrenner_score = total * gb_coeff

    # ── Goodlift Calculation ──────────────────────────────────────
    # Men: A=1199.72839, B=1025.18162, C=0.00921
    # Women: A=610.32796, B=1045.59282, C=0.03048
    if gender == "Male":
        ag, bg, cg = 1199.72839, 1025.18162, 0.00921
    else:
        ag, bg, cg = 610.32796, 1045.59282, 0.03048
    
    gl_denom = ag - bg * np.exp(-cg * weight)
    goodlift_score = total * (100 / gl_denom) if gl_denom > 0 else 0.0

    # Display Results
    res_c1, res_c2, res_c3, res_c4 = st.columns([1, 1, 1, 1])
    with res_c1:
        st.metric("DOTS Score", f"{dots_score:.2f}")
        if dots_score > 500:
            st.success(f"🔥 **Elite Performance!** Your DOTS score of {dots_score:.2f} is world-class.")
        elif dots_score > 400:
            st.info(f"💪 **Strong Lift!** You're highly competitive.")
        elif dots_score > 0:
            st.write(f"📈 Every kilogram added to your total will boost this score.")
        else:
            st.warning("Please check your bodyweight/total values.")
    with res_c2:
        st.metric("Wilks Score", f"{wilks_score:.2f}")
        if wilks_score > 500:
            st.success(f"🔥 **Elite Performance!** Your Wilks score of {wilks_score:.2f} is world-class.")
        elif wilks_score > 400:
            st.info(f"💪 **Strong Lift!** You're highly competitive.")
        elif wilks_score > 0:
            st.write(f"📈 Every kilogram added to your total will boost this score.")
        else:
            st.warning("Please check your bodyweight/total values.")
    with res_c3:
        st.metric("Glossbrenner Score", f"{glossbrenner_score:.2f}")
        if glossbrenner_score > 500:
            st.success(f"🔥 **Elite Performance!** Your Glossbrenner score of {glossbrenner_score:.2f} is world-class.")
        elif glossbrenner_score > 400:
            st.info(f"💪 **Strong Lift!** You're highly competitive.")
        elif glossbrenner_score > 0:
            st.write(f"📈 Every kilogram added to your total will boost this score.")
        else:
            st.warning("Please check your bodyweight/total values.")
    with res_c4:
        st.metric("Goodlift Score", f"{goodlift_score:.2f}")
        if goodlift_score > 120:
            st.success(f"🔥 **Elite Performance!** Your Goodlift score of {goodlift_score:.2f} is world-class.")
        elif goodlift_score > 90:
            st.info(f"💪 **Strong Lift!** You're highly competitive.")
        elif goodlift_score > 0:
            st.write(f"📈 Every kilogram added to your total will boost this score.")
        else:
            st.warning("Please check your bodyweight/total values.")
        
    
#st.write(f"📊 **Summary:** {gender} • {age} years • {weight} kg BW • {total} kg Total")
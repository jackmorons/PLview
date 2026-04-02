import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import urllib.parse
# import geopandas as gpd

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
    {"key": "entry_calculator", "label": "📈 Competition Entry Calculator"}, # 4
    {"key": "pattern_discoverer", "label": "🔍 Pattern Discoverer"}, # 5
    #{"key": "relative_lifts", "label": "💪 Relative Lifts"},
    {"key": "freak_finder", "label": "🤯 Strength Freaks Finder"}, # 6
    #{"key": "geo_strength", "label": "🌍 Geographical Strength"}, # 7
    {"key": "twin_finder", "label": "🫂 Find Your Powerlifting Twin!"}, # 8
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
elif active == "entry_calculator":
    st.subheader("📈 Competition Entry Calculator")
    st.info("🚧 **Coming soon** — Detailed competition entry calculator.")

# ---------- 5. Pattern Discoverer ----------
elif active == "pattern_discoverer":
    st.subheader("🔍 Pattern Discoverer")
    st.info("🚧 **Coming soon** — Detailed pattern discoverer.")

# ---------- 6. Freak Finder ----------
elif active == "freak_finder":
    st.subheader("🤯 Strength Freaks Finder")
    st.info("🚧 **Coming soon** — Detailed freak finder.")

# # ---------- 7. Geographical Strength ----------
# elif active == "geo_strength":
#     st.subheader("🌍 Geographical Strength")
#     st.info("🚧 **Coming soon** — Detailed geographical strength.")

# ---------- 8. Find Your PL Twin! ----------
elif active == "twin_finder":
    st.subheader("🫂 Find Your PL Twin!")
    st.info("Find the athlete in our database with the most similar performance profile to yours.")

    # 1. Inputs
    input_c1, input_c2, input_c3 = st.columns(3)
    with input_c1:
        u_gender = st.selectbox("Gender", ["Male", "Female"], key="twin_gender")
        u_equip = st.selectbox("Equipment", ["Raw", "Wraps", "Single-ply", "Multi-ply"], key="twin_equip")
    with input_c2:
        u_bw = st.number_input("Bodyweight (kg)", min_value=30.0, max_value=250.0, value=82.5, step=0.5)
        u_squat = st.number_input("Best Squat (kg)", min_value=0.0, max_value=600.0, value=180.0, step=2.5)
    with input_c3:
        u_bench = st.number_input("Best Bench (kg)", min_value=0.0, max_value=400.0, value=120.0, step=2.5)
        u_deadlift = st.number_input("Best Deadlift (kg)", min_value=0.0, max_value=500.0, value=220.0, step=2.5)

    if st.button("🔍 Find My Twin", type="primary", use_container_width=True):
        # 2. Logic
        with st.spinner("Searching the database for your match..."):
            # Select dataset
            ref_df = malesdf if u_gender == "Male" else femalesdf
            
            # Pre-filter for performance: +/- 15kg bodyweight to narrow down
            # If no matches found, we can expand, but for this dataset it's usually fine.
            candidates = ref_df[
                (ref_df["BodyweightKg"] >= u_bw - 15) & 
                (ref_df["BodyweightKg"] <= u_bw + 15) &
                (ref_df["Equipment"] == u_equip)
            ].copy()

            if candidates.empty:
                # Fallback to just Equipment if strictly limited BW fails
                candidates = ref_df[ref_df["Equipment"] == u_equip].copy()

            if not candidates.empty:
                # Calculate Euclidean Distance
                # stats: Squat, Bench, Deadlift
                candidates["dist"] = np.sqrt(
                    (candidates["Best3SquatKg"] - u_squat)**2 +
                    (candidates["Best3BenchKg"] - u_bench)**2 +
                    (candidates["Best3DeadliftKg"] - u_deadlift)**2 +
                    (candidates["BodyweightKg"] - u_bw)**2
                )
                
                # Get the top match
                twin = candidates.sort_values("dist").iloc[0]
                twin_name = twin["Name"]
                
                st.success(f"🎉 **Found your twin!** Your closest match is **{twin_name}**.")
                
                # 3. Visualization (Radar Plot)
                # Following athletes.py style
                categories = ['Squat', 'Bench Press', 'Deadlift']
                
                # Category stats for benchmarks (same as athletes.py)
                cat_wc = twin["WeightClassKg"]
                category_df = ref_df[
                    (ref_df["WeightClassKg"] == cat_wc) & 
                    (ref_df["Equipment"] == u_equip)
                ].copy()

                avg_squat = category_df["Best3SquatKg"].mean()
                avg_bench = category_df["Best3BenchKg"].mean()
                avg_deadlift = category_df["Best3DeadliftKg"].mean()
                rec_squat = category_df["Best3SquatKg"].max()
                rec_bench = category_df["Best3BenchKg"].max()
                rec_deadlift = category_df["Best3DeadliftKg"].max()

                fig_twin = go.Figure()

                # Trace 1: Category Average
                fig_twin.add_trace(go.Scatterpolar(
                    r=[avg_squat, avg_bench, avg_deadlift, avg_squat],
                    theta=categories + [categories[0]],
                    fill='toself',
                    fillcolor='rgba(66, 165, 245, 0.05)',
                    name='Category Avg',
                    line=dict(color='rgba(66, 165, 245, 0.4)', width=1, dash='dash'),
                ))

                # Trace 2: User (You)
                fig_twin.add_trace(go.Scatterpolar(
                    r=[u_squat, u_bench, u_deadlift, u_squat],
                    theta=categories + [categories[0]],
                    fill='toself',
                    fillcolor='rgba(239, 83, 80, 0.2)',
                    name='You',
                    line=dict(color='#ef5350', width=3),
                ))

                # Trace 3: Twin
                fig_twin.add_trace(go.Scatterpolar(
                    r=[twin["Best3SquatKg"], twin["Best3BenchKg"], twin["Best3DeadliftKg"], twin["Best3SquatKg"]],
                    theta=categories + [categories[0]],
                    fill='toself',
                    fillcolor='rgba(255, 213, 79, 0.3)',
                    name=f'Twin: {twin_name}',
                    line=dict(color='#ffd54f', width=4),
                    marker=dict(symbol="star", size=8)
                ))

                fig_twin.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, max(u_squat, u_bench, u_deadlift, twin["Best3DeadliftKg"]) * 1.15], gridcolor="rgba(255,255,255,0.1)"),
                        angularaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
                        bgcolor="rgba(0,0,0,0)"
                    ),
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    legend=dict(orientation="h", yanchor="bottom", y=-0.05, xanchor="center", x=0.5)
                )

                v_c1, v_c2 = st.columns([2, 1])
                with v_c1:
                    st.plotly_chart(fig_twin, use_container_width=True)
                with v_c2:
                    st.markdown("### 🧬 Twin Profile")
                    st.write(f"**Name:** [{twin_name}](athletes?name={urllib.parse.quote_plus(twin_name)})")
                    st.write(f"**Bodyweight:** {twin['BodyweightKg']} kg")
                    st.write(f"**S/B/D:** {twin['Best3SquatKg']}/{twin['Best3BenchKg']}/{twin['Best3DeadliftKg']}")
                    st.write(f"**Total:** {twin['TotalKg']} kg")
                    st.write(f"**Dots:** {twin['Dots']:.2f}")
                # --- 4. Grouped Bar Chart ---
                st.markdown("---")
                st.subheader("📊 Direct Strength Comparison")
                
                bar_data = pd.DataFrame({
                    "Lift": ["Squat", "Bench", "Deadlift", "Total"] * 2,
                    "Weight (kg)": [
                        u_squat, u_bench, u_deadlift, u_squat + u_bench + u_deadlift,
                        twin["Best3SquatKg"], twin["Best3BenchKg"], twin["Best3DeadliftKg"], twin["TotalKg"]
                    ],
                    "Athlete": ["You"] * 4 + [twin_name] * 4
                })

                fig_bar = px.bar(
                    bar_data, x="Lift", y="Weight (kg)", color="Athlete",
                    barmode="group",
                    template="plotly_dark",
                    color_discrete_map={"You": "#ef5350", twin_name: "#ffd54f"},
                    text_auto=".1f"
                )
                fig_bar.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)", 
                    paper_bgcolor="rgba(0,0,0,0)",
                    xaxis_title="",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            else:
                st.warning("No athletes found for this equipment category. Try relaxing your filters.")

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

    # ---------- 10. 1RM Calculator ----------

    st.markdown("---")

    st.subheader("🏋️ 1RM Calculator")
    st.info("Calculate your projected 1Rep Max using the O'Conner formula with RPE adjustment.")
    
    calc_c1, calc_c2, calc_c3 = st.columns(3)
    
    with calc_c1:
        load = st.number_input("Load (kg)", min_value=0.0, max_value=1000.0, value=100.0, step=2.5, help="The weight you lifted.")
    
    with calc_c2:
        reps = st.number_input("Reps", min_value=1, max_value=20, value=5, step=1, help="Number of repetitions performed.")
    
    with calc_c3:
        rpe = st.slider("RPE", min_value=5.0, max_value=10.0, value=8.0, step=0.5, help="Rate of Perceived Exertion (10 = absolute limit, 9 = 1 rep in tank, etc.)")

    st.markdown("---")
    
    # ── Calculation ──────────────────────────────────────────────
    # Adjust reps based on RPE: Effective Reps = Actual Reps + (10 - RPE)
    effective_reps = reps + (10.0 - rpe)
    
    # Formula: 1RM = Load * (1 + (Effective Reps * 0.025))
    one_rm = load * (1 + (effective_reps * 0.025))
    
    # Display Result
    res_main, res_chart = st.columns([1, 2])
    
    with res_main:
        st.metric("Estimated 1RM", f"{one_rm:.2f} kg")
        
        st.markdown("### 📊 Intensity Table")
        pcts = [100, 95, 90, 85, 80, 75, 70]
        rows = []
        for p in pcts:
            rows.append({"Percentage (%)": f"{p}%", "Weight (kg)": f"{one_rm * (p/100):.1f}"})
        st.table(pd.DataFrame(rows))
        
    with res_chart:
        # Mini bar chart for intensities
        p_vals = [p for p in range(50, 105, 5)]
        w_vals = [one_rm * (pv/100) for pv in p_vals]
        
        fig_1rm = px.bar(
            x=[f"{pv}%" for pv in p_vals], y=w_vals,
            title="Projected Max % Breakdown",
            labels={'x': 'Percentage', 'y': 'Load (kg)'},
            template="plotly_dark",
            color=w_vals,
            color_continuous_scale="Viridis"
        )
        fig_1rm.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_1rm, use_container_width=True)


        


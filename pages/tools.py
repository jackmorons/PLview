import streamlit as st
from style_utils import inject_custom_css

inject_custom_css()

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

# --- Load data from session state ---
if "males_data" not in st.session_state:
    st.session_state["males_data"] = pd.read_csv("datasets/OP_Males.csv", sep=";")
if "females_data" not in st.session_state:
    st.session_state["females_data"] = pd.read_csv("datasets/OP_Females.csv", sep=";")

malesdf = st.session_state["males_data"]
femalesdf = st.session_state["females_data"]

# Combine both datasets for a unified athlete search
alldf = pd.concat([malesdf, femalesdf], ignore_index=True)
all_names = sorted(alldf["Name"].dropna().unique().tolist())

# ── Sub-page definitions ──────────────────────────────────────────────
TOOLS_PAGES = [
    {"key": "lift_distributions", "label": "📊 Statistical Distributions"}, # 1
    {"key": "1v1", "label": "⚔️ 1v1 Strength Comparison"}, # 2
    {"key": "weight_class", "label": "⚖️ Weight Class Evaluator"}, # 3
    {"key": "entry_calculator", "label": "📈 Competition Entry Calculator"}, # 4
    {"key": "pattern_discoverer", "label": "🔍 Patterns and Trends Discoverer"}, # 5
    #{"key": "relative_lifts", "label": "💪 Relative Lifts"},
    {"key": "freak_finder", "label": "🤯 Strength Freaks Finder"}, # 6
    #{"key": "geo_strength", "label": "🌍 Geographical Strength"}, # 7
    {"key": "twin_finder", "label": "🫂 Find Your Powerlifting Twin!"}, # 8
    {"key": "strength_index_calculator", "label": "🧮 The All-In-One Calculator"}, # 9
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

    # --- 1. Selection & Global Controls ---
    st.markdown("### 📊 Distribution Explorer")
    ctrl_c1, ctrl_c2 = st.columns([1, 3])
    with ctrl_c1:
        color_choice = st.selectbox(
            "🎨 Color bars by:",
            ["None (Solid)", "Age Class", "Weight Class", "Equipment"],
            index=0,
            help="Segment the histogram by a specific category."
        )

    # Map the choice to actual column names
    color_map = {
        "None (Solid)": None,
        "Age Class": "AgeClass",
        "Weight Class": "WeightClassKg",
        "Equipment": "Equipment"
    }
    color_col = color_map[color_choice]

    # st.markdown("##### 🔦 Highlight & Filter")
    filter_expander = st.expander("🔦 Highlight & Filter", expanded=False)
    with filter_expander:
        f_c1, f_c2, f_c3 = st.columns(3)
        with f_c1:
            all_equip = sorted(alldf["Equipment"].dropna().unique().tolist())
            h_equip = st.multiselect("Highlight Equipment", all_equip, default=all_equip, help="Keep only selected equipment types.")
        with f_c2:
            all_age = sorted(alldf["AgeClass"].dropna().unique().tolist())
            h_age = st.multiselect("Highlight Age Class", all_age, default=all_age, help="Keep only selected age classes.")
        with f_c3:
            h_action = st.radio("Action for Excluded", ["Grey-out", "Remove"], horizontal=True, help="'Grey-out' keeps points visible but desaturated. 'Remove' hides them completely.")

    for label, col in lift_cols.items():
        st.subheader(label)
        c1, c2 = st.columns(2)
        
        # Prepare data copies and handle NaNs
        m_plot_df = malesdf[malesdf[col] > 0].copy()
        f_plot_df = femalesdf[femalesdf[col] > 0].copy()

        # --- Apply Filtering & Categorization ---
        def apply_dist_filter(df, color_c, h_eq, h_ag, h_act):
            if df.empty: return df, color_c
            mask = df["Equipment"].isin(h_eq) & df["AgeClass"].isin(h_ag)
            if h_act == "Remove":
                return df[mask].copy(), color_c
            else:
                # Grey-out logic
                res_df = df.copy()
                if color_c:
                    res_df["display_cat"] = res_df[color_c].astype(str)
                    res_df.loc[~mask, "display_cat"] = " Others"
                else:
                    res_df["display_cat"] = "Selected"
                    res_df.loc[~mask, "display_cat"] = " Others"
                return res_df, "display_cat"

        m_plot_df, m_color_col = apply_dist_filter(m_plot_df, color_col, h_equip, h_age, h_action)
        f_plot_df, f_color_col = apply_dist_filter(f_plot_df, color_col, h_equip, h_age, h_action)

        # --- FIX: Custom Weight Normalization to ensure total probability = 1 ---
        # To normalize across the entire population (including 'Others'), we use weights.
        m_plot_df["weight"] = 1.0 / len(m_plot_df) if not m_plot_df.empty else 1.0
        f_plot_df["weight"] = 1.0 / len(f_plot_df) if not f_plot_df.empty else 1.0

        # --- Color Logic ---
        def get_color_configs(df, c_col, is_male):
            if not c_col:
                return ["#42a5f5" if is_male else "#ef5350"], {}, None
            
            # Handle sorting
            all_cats = sorted([str(c) for c in df[c_col].unique()])
            
            # Special sorting for Equipment if it's the color base
            if c_col == "Equipment" or (c_col == "display_cat" and color_col == "Equipment"):
                equip_order = ["Raw", "Wraps", "Single-ply", "Multi-ply"]
                all_cats = [e for e in equip_order if e in all_cats] + [e for e in sorted(set(all_cats) - set(equip_order))]
            
            # Numeric sorting for Weight Class
            if c_col == "WeightClassKg" or (c_col == "display_cat" and color_col == "WeightClassKg"):
                def wc_sort_key(x):
                    try: return float(x.replace("+", ""))
                    except: return 9999
                pure = [c for c in all_cats if c != " Others"]
                all_cats = sorted(pure, key=wc_sort_key) + ([" Others"] if " Others" in all_cats else [])

            # Numeric sorting for Age Class
            if c_col == "AgeClass" or (c_col == "display_cat" and color_col == "AgeClass"):
                def age_sort_key(x):
                    try: return int(x.split("-")[0].replace("+", ""))
                    except: return 9999
                pure = [c for c in all_cats if c != " Others"]
                all_cats = sorted(pure, key=age_sort_key) + ([" Others"] if " Others" in all_cats else [])
            
            # Ensure " Others" is at the end
            if " Others" in all_cats:
                all_cats.remove(" Others")
                all_cats.append(" Others")
            
            n_cats_real = len([c for c in all_cats if c != " Others"])
            
            # Generate chromatic sequence for real categories
            if n_cats_real > 1:
                base_colors = px.colors.sample_colorscale("Turbo", [i/(n_cats_real-1) for i in range(n_cats_real)])
            else:
                base_colors = ["#42a5f5" if is_male else "#ef5350"]
            
            # Map colors
            c_map = {}
            color_idx = 0
            for cat in all_cats:
                if cat == " Others":
                    c_map[cat] = "rgba(200, 200, 200, 0.2)"
                elif cat == "Selected":
                    c_map[cat] = "#42a5f5" if is_male else "#ef5350"
                else:
                    c_map[cat] = base_colors[color_idx]
                    color_idx += 1
            
            return None, {c_col: all_cats}, c_map

        m_seq, m_cat_orders, m_map = get_color_configs(m_plot_df, m_color_col, True)
        f_seq, f_cat_orders, f_map = get_color_configs(f_plot_df, f_color_col, False)

        with c1:
            fig_m = px.histogram(
                m_plot_df, x=col, y="weight", histfunc="sum",
                color=m_color_col,
                title=f"{label} Distribution (Males)",
                template="plotly_dark",
                color_discrete_sequence=m_seq,
                color_discrete_map=m_map,
                category_orders=m_cat_orders,
                barmode="stack" if m_color_col else "relative"
            )
            fig_m.update_layout(
                height=600,
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="#9a9ab0", title_font_color="#f0f0f5",
                margin=dict(l=20, r=20, t=200, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=1.0) if m_color_col else None,
                title=dict(y=0.95, x=0, xanchor='left')
            )
            fig_m.update_yaxes(title_text="Frequency (Relative)")
            st.plotly_chart(fig_m, use_container_width=True)

        with c2:
            fig_f = px.histogram(
                f_plot_df, x=col, y="weight", histfunc="sum",
                color=f_color_col,
                title=f"{label} Distribution (Females)",
                template="plotly_dark",
                color_discrete_sequence=f_seq,
                color_discrete_map=f_map,
                category_orders=f_cat_orders,
                barmode="stack" if f_color_col else "relative"
            )
            fig_f.update_layout(
                height=600,
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="#9a9ab0", title_font_color="#f0f0f5",
                margin=dict(l=20, r=20, t=200, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=1.0) if f_color_col else None,
                title=dict(y=0.95, x=0, xanchor='left')
            )
            fig_f.update_yaxes(title_text="Frequency (Relative)")
            st.plotly_chart(fig_f, use_container_width=True)

    # ── Scientific Discovery: The Correlation Matrix ─────────────────
    st.markdown("---")
    st.subheader("🔬 The Correlation Matrix: Scientific Insights")
    st.write("Understand the mathematical relationship between different variables.")

    # Selection of variables for correlation
    corr_vars = [
        "BodyweightKg", "Age", "Best3SquatKg", 
        "Best3BenchKg", "Best3DeadliftKg", "TotalKg", "Dots"
    ]
    # Human-readable labels
    corr_labels = [
        "Bodyweight", "Age", "Squat", 
        "Bench", "Deadlift", "Total", "Dots"
    ]
    
    # Calculate the Correlation Matrix (using global alldf for broad sample)
    # We drop NAs and ensure columns are numeric
    corr_df = alldf[corr_vars].dropna()
    corr_matrix = corr_df.corr()

    # Create Heatmap
    fig_corr = px.imshow(
        corr_matrix,
        x=corr_labels,
        y=corr_labels,
        color_continuous_scale="RdBu_r", # Red-Blue diverging scale
        range_color=[-1, 1],
        text_auto=".2f", # Show coefficients in cells
        aspect="auto",
        template="plotly_dark",
        title="Metric Correlation Heatmap"
    )
    
    fig_corr.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=600,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    st.plotly_chart(fig_corr, use_container_width=True)
    
    with st.expander("📚 How to read this 'Scientific' Discovery?"):
        st.write("""
            - **Strong Positive (Red)**: Close to 1.0. This means as one goes up, the other usually goes up (e.g., Squat vs Total).
            - **Weak/No Correlation (White)**: Close to 0.0. This means the variables are independent (e.g., Age has a very weak correlation with Bodyweight).
            - **Negative Correlation (Blue)**: Negatives up to -1.0. This means as one goes up, the other usually goes down (e.g., Age vs Dots).
            - **Insights**: Notice how **Bench Press** often has a lower correlation with **Deadlift** than **Squat** does. This statistically demonstrates that deadlifting depends more on lower-body 'squat' patterns than upper-body 'bench' patterns!
        """)

# ---------- 2. 1v1 Strength Comparison ----------
elif active == "1v1":
    st.subheader("⚔️ 1v1 Strength Comparison")
    st.info("Compare two athletes side-by-side using their personal bests and relative performance metrics.")

    # 1. Athlete Selection Row
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### 🏹 Athlete 1")
        name1 = st.selectbox("Search for Athlete 1", [""] + all_names, key="1v1_athlete_1", index=0, placeholder="Type to search...")
    
    with col_b:
        st.markdown("### 🛡️ Athlete 2")
        name2 = st.selectbox("Search for Athlete 2", [""] + all_names, key="1v1_athlete_2", index=0, placeholder="Type to search...")

    st.markdown("---")

    # 2. Data Preparation Function (Enhanced)
    def get_ath_stats(name):
        if not name: return None
        ath_df = alldf[alldf["Name"] == name].copy()
        
        # PB stats
        best_sq = ath_df["Best3SquatKg"].max()
        best_bn = ath_df["Best3BenchKg"].max()
        best_dl = ath_df["Best3DeadliftKg"].max()
        best_tot = ath_df["TotalKg"].max()
        best_dots = ath_df["Dots"].max()
        best_wilks = ath_df["Wilks"].max()
        best_gloss = ath_df["Glossbrenner"].max()
        best_good = ath_df["Goodlift"].max()
        
        # Latest entries
        latest = ath_df.sort_values("Date", ascending=False).iloc[0]
        wc = latest["WeightClassKg"]
        sex = "Male" if latest["Sex"] == "M" else "Female"
        equip = latest["Equipment"]
        bw = latest["BodyweightKg"]
        
        return {
            "name": name,
            "sq": best_sq if best_sq > 0 else 0, 
            "bn": best_bn if best_bn > 0 else 0, 
            "dl": best_dl if best_dl > 0 else 0, 
            "tot": best_tot if best_tot > 0 else 0, 
            "dots": best_dots if best_dots > 0 else 0,
            "wilks": best_wilks if best_wilks > 0 else 0,
            "glossbrenner": best_gloss if best_gloss > 0 else 0,
            "goodlift": best_good if best_good > 0 else 0,
            "wc": wc, "sex": sex, "equip": equip, "bw": bw
        }

    stats1 = get_ath_stats(name1)
    stats2 = get_ath_stats(name2)

    # 3. Comparison Rendering
    disp_a, disp_b = st.columns(2)

    def render_athlete_col(stats, other_stats, column, is_left=True):
        if not stats:
            column.info("👈 Select an athlete to start comparison." if is_left else "Select an athlete to start comparison. 👉")
            return
        
        with column:
            # Styled Header
            st.markdown(f"""
                <div style="background-color: rgba(255, 255, 255, 0.03); padding: 15px; border-radius: 10px; border-left: 5px solid {'#42a5f5' if is_left else '#ef5350'};">
                    <h2 style="margin-top: 0; margin-bottom: 5px;">{stats['name']}</h2>
                    <p style="color: #9a9ab0; margin-bottom: 0;">🧬 {stats['sex']}  •  ⚖️ {stats['wc']}kg  •  ⚙️ {stats['equip']}</p>
                </div>
            """, unsafe_allow_html=True)
            st.write("")
            
            # Metrics Grid
            m_c1, m_c2 = st.columns(2)
            
            # Deltas (compared to the other athlete if both selected)
            d_sq = stats['sq'] - other_stats['sq'] if other_stats else None
            d_bn = stats['bn'] - other_stats['bn'] if other_stats else None
            d_dl = stats['dl'] - other_stats['dl'] if other_stats else None
            d_tot = stats['tot'] - other_stats['tot'] if other_stats else None
            d_dots = stats['dots'] - other_stats['dots'] if other_stats else None

            m_c1.metric("Best Squat", f"{stats['sq']} kg", delta=f"{d_sq:+.1f} kg" if d_sq is not None else None)
            m_c1.metric("Best Bench", f"{stats['bn']} kg", delta=f"{d_bn:+.1f} kg" if d_bn is not None else None)
            m_c2.metric("Best Deadlift", f"{stats['dl']} kg", delta=f"{d_dl:+.1f} kg" if d_dl is not None else None)
            m_c2.metric("Best Total", f"{stats['tot']} kg", delta=f"{d_tot:+.1f} kg" if d_tot is not None else None)
            
            st.divider()
            st.metric("Best Dots", f"{stats['dots']:.2f}", delta=f"{d_dots:+.2f}" if d_dots is not None else None)

    render_athlete_col(stats1, stats2, disp_a, True)
    render_athlete_col(stats2, stats1, disp_b, False)

    # 4. Multi-Chart Dashboard
    if stats1 and stats2:
        st.markdown("---")
        st.subheader("📊 Performance Matchup Dashboard")
        
        # --- Row 1: The Radars ---
        r1_col1, r1_col2 = st.columns(2)
        
        with r1_col1:
            # Radar 1: S/B/D Profile
            categories_sbd = ['Squat', 'Bench', 'Deadlift']
            
            # Data for both athletes
            r1 = [stats1['sq'], stats1['bn'], stats1['dl'], stats1['sq']]
            r2 = [stats2['sq'], stats2['bn'], stats2['dl'], stats2['sq']]
            
            # Plot the larger one first (so smaller is on top for hover)
            sum1 = sum(r1)
            sum2 = sum(r2)
            
            fig_sbd = go.Figure()
            
            order = [(stats1, r1, '#42a5f5', 'rgba(66, 165, 245, 0.2)'), 
                     (stats2, r2, '#ef5350', 'rgba(239, 83, 80, 0.2)')]
            
            # Sort by sum descending (larger sum comes first in traces)
            order.sort(key=lambda x: sum(x[1]), reverse=True)
            
            for s, r_val, color, f_color in order:
                fig_sbd.add_trace(go.Scatterpolar(
                    r=r_val,
                    theta=categories_sbd + [categories_sbd[0]],
                    fill='toself', name=s['name'],
                    line=dict(color=color, width=3),
                    fillcolor=f_color
                ))

            fig_sbd.update_layout(
                polar=dict(radialaxis=dict(visible=True, gridcolor="rgba(255,255,255,0.1)"), bgcolor="rgba(0,0,0,0)"),
                template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                title=dict(text="S/B/D Strength Profile", x=0.5, xanchor='center'),
                legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5), # Repositioned lower
                height=500
            )
            st.plotly_chart(fig_sbd, use_container_width=True)

        with r1_col2:
            # Radar 2: Coefficients (Normalized to 100 Scale)
            categories_coeff = ['Dots', 'Wilks', 'Glossbrenner', 'Goodlift']
            # Normalization factors for visual scaling (Dots/Wilks ~600, Goodlift ~120)
            norm_map = {'Dots': 600, 'Wilks': 600, 'Glossbrenner': 600, 'Goodlift': 120}
            
            def get_norm_r(s):
                vals = []
                for c in categories_coeff:
                    # Using consistent keys
                    raw = s.get(c.lower(), 0)
                    vals.append((raw / norm_map[c]) * 100)
                return vals + [vals[0]]

            # Normalized data
            nr1 = get_norm_r(stats1)
            nr2 = get_norm_r(stats2)
            
            fig_coeff = go.Figure()
            
            order_coeff = [(stats1, nr1, '#42a5f5', 'rgba(66, 165, 245, 0.2)'), 
                           (stats2, nr2, '#ef5350', 'rgba(239, 83, 80, 0.2)')]
            
            # Plot the larger one first
            order_coeff.sort(key=lambda x: sum(x[1]), reverse=True)
            
            for s, r_val, color, f_color in order_coeff:
                fig_coeff.add_trace(go.Scatterpolar(
                    r=r_val,
                    theta=categories_coeff + [categories_coeff[0]],
                    fill='toself', name=s['name'],
                    line=dict(color=color, width=3),
                    fillcolor=f_color
                ))

            fig_coeff.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.1)"), bgcolor="rgba(0,0,0,0)"),
                template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                title=dict(text="Coefficient Battle (Normalized)", x=0.5, xanchor='center'),
                legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5), # Repositioned lower
                height=500
            )
            st.plotly_chart(fig_coeff, use_container_width=True)

        # --- Row 2: Population Heatmap ---
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🗺️ Population Positioning Map")
        st.write("Where do these two stand relative to the ocean of lifters in our database?")
        
        fig_heat = px.density_heatmap(
            alldf[alldf["TotalKg"] > 0], x="BodyweightKg", y="TotalKg",
            template="plotly_dark",
            color_continuous_scale="Viridis",
            nbinsx=50, nbinsy=50,
            labels={"BodyweightKg": "Bodyweight (kg)", "TotalKg": "Total (kg)"}
        )
        # Add Athlete 1 Marker
        fig_heat.add_trace(go.Scatter(
            x=[stats1['bw']], y=[stats1['tot']],
            mode='markers', name=f"🏹 {stats1['name']}",
            marker=dict(color='#42a5f5', size=16, symbol='star', line=dict(width=2, color='white')),
            hovertemplate=f"<b>{stats1['name']}</b><br>BW: %{{x}}kg<br>Total: %{{y}}kg<extra></extra>"
        ))
        # Add Athlete 2 Marker
        fig_heat.add_trace(go.Scatter(
            x=[stats2['bw']], y=[stats2['tot']],
            mode='markers', name=f"🛡️ {stats2['name']}",
            marker=dict(color='#ef5350', size=16, symbol='star', line=dict(width=2, color='white')),
            hovertemplate=f"<b>{stats2['name']}</b><br>BW: %{{x}}kg<br>Total: %{{y}}kg<extra></extra>"
        ))
        fig_heat.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            height=600, margin=dict(l=20, r=20, t=20, b=20),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_heat, use_container_width=True)

        # --- Row 3: Gauges and Efficiency ---
        r3_col1, r3_col2 = st.columns(2)
        
        with r3_col1:
            st.markdown("<div style='text-align: center; font-weight: bold;'>🏆 Percentile Standing (Dots)</div>", unsafe_allow_html=True)
            g_c1, g_c2 = st.columns(2)
            for i, (s, col, color) in enumerate([(stats1, g_c1, '#42a5f5'), (stats2, g_c2, '#ef5350')]):
                # Calculate percentile
                all_dots = alldf[alldf["Dots"] > 0]["Dots"].sort_values()
                rank = (all_dots < s['dots']).sum()
                percentile = (rank / len(all_dots)) * 100 if not all_dots.empty else 0
                
                fig_g = go.Figure(go.Indicator(
                    mode="gauge+number", value=percentile,
                    number={'suffix': "%", 'font': {'size': 24, 'color': '#f0f0f5'}},
                    title={'text': s['name'], 'font': {'size': 16}},
                    gauge={'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "gray"},
                           'bar': {'color': color},
                           'bgcolor': "rgba(0,0,0,0)",
                           'borderwidth': 2, 'bordercolor': "gray"}
                ))
                fig_g.update_layout(height=250, margin=dict(l=30, r=30, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)")
                col.plotly_chart(fig_g, use_container_width=True)

        with r3_col2:
            st.markdown("<div style='text-align: center; font-weight: bold;'>💪 Strength Efficiency (Total/BW)</div>", unsafe_allow_html=True)
            eff1 = stats1['tot'] / stats1['bw'] if stats1['bw'] > 0 else 0
            eff2 = stats2['tot'] / stats2['bw'] if stats2['bw'] > 0 else 0
            
            eff_data = pd.DataFrame({
                "Athlete": [stats1['name'], stats2['name']],
                "Ratio": [eff1, eff2],
                "Color": ['#42a5f5', '#ef5350']
            })
            fig_eff = px.bar(
                eff_data, x="Ratio", y="Athlete", orientation='h',
                template="plotly_dark", color="Athlete",
                color_discrete_map={stats1['name']: '#42a5f5', stats2['name']: '#ef5350'},
                text_auto=".2f"
            )
            fig_eff.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                height=300, margin=dict(l=20, r=20, t=50, b=50),
                showlegend=False, xaxis_title="Kgs lifted per Kg of bodyweight"
            )
            st.plotly_chart(fig_eff, use_container_width=True)

# ---------- 3. Weight Class Evaluator ----------
elif active == "weight_class":
    st.subheader("⚖️ Weight Class Evaluator")
    st.write("Analyze your competitiveness across different weight categories. Simulate weight cuts and discover where you sit in the global rankings.")

    # 1. Simulation Inputs
    with st.container():
        input_c1, input_c2, input_c3 = st.columns(3)
        
        with input_c1:
            eval_gender = st.selectbox("Gender", ["Male", "Female"], key="eval_gen")
            # Get available classes for this gender
            ref_df = malesdf if eval_gender == "Male" else femalesdf
            all_wc = sorted(ref_df["WeightClassKg"].dropna().unique().tolist())
            
            eval_curr_bw = st.number_input("Current Bodyweight (kg)", min_value=30.0, max_value=250.0, value=90.0, step=0.1)
        
        with input_c2:
            eval_curr_tot = st.number_input("Current Total (kg)", min_value=0.0, max_value=1500.0, value=500.0, step=2.5)
            # Find current class automatically
            curr_class_idx = 0
            for i, wc in enumerate(all_wc):
                if eval_curr_bw <= wc:
                    curr_class_idx = i
                    break
            else: curr_class_idx = len(all_wc) - 1 # SHW
            
            eval_target_wc = st.selectbox("Target Weight Class", all_wc, index=max(0, curr_class_idx-1))

        with input_c3:
            st.write("🔮 **The 'Trust Me Bro' Speculator**")
            eval_retention = st.slider("Expected Strength Retention (%)", 80.0, 100.0, 95.0, step=1.0, help="Speculative guess on how much strength you'll keep after the cut.")
            eval_projected_tot = eval_curr_tot * (eval_retention / 100.0)
            st.caption(f"Projected Total: **{eval_projected_tot:.1f} kg**")

    # 2. Analytical Logic
    # Filter populations
    curr_wc_val = all_wc[curr_class_idx]
    curr_pop = ref_df[ref_df["WeightClassKg"] == curr_wc_val]["TotalKg"].dropna()
    target_pop = ref_df[ref_df["WeightClassKg"] == eval_target_wc]["TotalKg"].dropna()

    def get_percentile(val, pop):
        if pop.empty: return 0.0
        return (pop < val).sum() / len(pop) * 100

    curr_pct = get_percentile(eval_curr_tot, curr_pop)
    target_pct = get_percentile(eval_projected_tot, target_pop)

    def calc_dots(w, t, g):
        if g == "Male": A, B, C, D, E = -0.000001093, 0.0007391293, -0.1918759221, 24.0900756, -307.75076
        else: A, B, C, D, E = -0.0000010706, 0.0005158568, -0.1126655495, 13.6175032, -57.96288
        denom = (A * w**4) + (B * w**3) + (C * w**2) + (D * w) + E
        return t * (500 / denom) if denom > 0 else 0.0

    curr_dots = calc_dots(eval_curr_bw, eval_curr_tot, eval_gender)
    target_dots = calc_dots(eval_target_wc, eval_projected_tot, eval_gender)

    # 3. Standings Comparison Dashboard
    st.markdown("---")
    stand_c1, stand_c2 = st.columns(2)
    
    with stand_c1:
        st.markdown(f"### 📍 Current Standings ({curr_wc_val}kg)")
        st.metric("Percentile Standing", f"{curr_pct:.1f}%", help="Higher is better. 90% means you are stronger than 90% of the class.")
        st.metric("Dots Score", f"{curr_dots:.2f}")
        
    with stand_c2:
        st.markdown(f"### 🎯 Projected Standings ({eval_target_wc}kg)")
        pct_delta = target_pct - curr_pct
        st.metric("Percentile Standing", f"{target_pct:.1f}%", delta=f"{pct_delta:+.1f}%", delta_color="normal")
        dots_delta = target_dots - curr_dots
        st.metric("Dots Score", f"{target_dots:.2f}", delta=f"{dots_delta:+.2f}")

    if target_pct > curr_pct:
        st.success(f"📈 **Strategic Advantage!** Moving to the **{eval_target_wc}kg** class could improve your competitive standing by **{pct_delta:.1f}%**.")
    else:
        st.warning(f"📉 **Diminishing Returns.** Strength loss might outweigh the weight class advantage. Staying at **{curr_wc_val}kg** currently keeps you higher in the rankings.")

    # 4. Visualizations
    st.markdown("---")
    viz_c1, viz_c2 = st.columns([2, 1])
    
    with viz_c1:
        # Population Heatmap
        st.markdown("### 🗺️ The Ocean of Lifters")
        st.write("Where you sit relative to every lifter in the database.")
        fig_map = px.density_heatmap(
            ref_df[ref_df["TotalKg"] > 100], x="BodyweightKg", y="TotalKg",
            template="plotly_dark", color_continuous_scale="Viridis",
            nbinsx=40, nbinsy=40,
            labels={"BodyweightKg": "Bodyweight (kg)", "TotalKg": "Total (kg)"}
        )
        # Add Markers
        fig_map.add_trace(go.Scatter(
            x=[eval_curr_bw, eval_target_wc], 
            y=[eval_curr_tot, eval_projected_tot],
            mode='markers+lines',
            name='The Cut Path',
            marker=dict(color=['#42a5f5', '#ef5350'], size=[16, 20], symbol=['circle', 'star'], line=dict(width=2, color='white')),
            text=["Now", "Projected"],
            hovertemplate="<b>%{text}</b><br>BW: %{x}kg<br>Total: %{y}kg<extra></extra>"
        ))
        fig_map.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            height=600, margin=dict(l=20, r=20, t=20, b=20),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with viz_c2:
        # Category Comparison Chart
        st.markdown("### ⚖️ Category Depth")
        # Comparative Stats Table
        def get_pop_stats(pop):
            if pop.empty: return [0, 0, 0]
            return [pop.quantile(0.99), pop.quantile(0.9), pop.median()]
        
        curr_stats = get_pop_stats(curr_pop)
        target_stats = get_pop_stats(target_pop)
        
        comp_data = pd.DataFrame({
            "Tier": ["Top 1%", "Top 10%", "Median"],
            f"{curr_wc_val}kg": [f"{s:.1f}kg" for s in curr_stats],
            f"{eval_target_wc}kg": [f"{s:.1f}kg" for s in target_stats]
        })
        st.table(comp_data.set_index("Tier"))
        
        # Benchmarks chart
        bar_data = pd.DataFrame({
            "Metric": ["Top 10%", "Median"] * 2,
            "Total (kg)": [curr_stats[1], curr_stats[2], target_stats[1], target_stats[2]],
            "Class": [f"{curr_wc_val}kg"] * 2 + [f"{eval_target_wc}kg"] * 2
        })
        fig_bar = px.bar(
            bar_data, x="Metric", y="Total (kg)", color="Class",
            barmode="group", template="plotly_dark",
            color_discrete_map={f"{curr_wc_val}kg": "#42a5f5", f"{eval_target_wc}kg": "#ef5350"}
        )
        fig_bar.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            height=300, showlegend=False, margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# ---------- 4. Trend Calculator (Entry Calculator) ----------
elif active == "entry_calculator":
    st.subheader("📈 Trend-Based Entry Calculator")
    st.write("Plan your competition attempts based on successful 3-for-3 trends from lifters in your specific category.")

    # 1. Inputs & Filters
    input_c1, input_c2, input_c3 = st.columns(3)
    
    with input_c1:
        calc_gender = st.selectbox("Gender", ["Male", "Female"], key="trend_gen")
        calc_lift = st.selectbox("Lift", ["Squat", "Bench", "Deadlift"], key="trend_lift")
    
    with input_c2:
        ref_df = malesdf if calc_gender == "Male" else femalesdf
        all_wc = sorted(ref_df["WeightClassKg"].dropna().unique().tolist())
        calc_wc = st.selectbox("Weight Class", all_wc, index=min(len(all_wc)-1, 5), key="trend_wc")
        calc_goal = st.number_input("Target 3rd Lift (kg)", min_value=20.0, max_value=600.0, value=200.0, step=2.5)

    with input_c3:
        all_equip = sorted(ref_df["Equipment"].dropna().unique().tolist())
        calc_equip = st.selectbox("Equipment", all_equip, key="trend_equip")
        calc_buffer = st.slider("Aggressiveness", 0.0, 1.0, 0.5, help="Higher = closer attempts, Lower = safer opener.")

    # 2. Logic: Find successful 3/3 trends
    lift_cols = {
        "Squat": ["Squat1Kg", "Squat2Kg", "Squat3Kg"],
        "Bench": ["Bench1Kg", "Bench2Kg", "Bench3Kg"],
        "Deadlift": ["Deadlift1Kg", "Deadlift2Kg", "Deadlift3Kg"]
    }
    c1, c2, c3 = lift_cols[calc_lift]
    
    # Filter for category
    cat_df = ref_df[
        (ref_df["WeightClassKg"] == calc_wc) & 
        (ref_df["Equipment"] == calc_equip)
    ].copy()
    
    # Filter for successful 3/3 (increasing positive attempts)
    trend_df = cat_df[(cat_df[c1] > 0) & (cat_df[c2] > cat_df[c1]) & (cat_df[c3] > cat_df[c2])].copy()
    
    if len(trend_df) < 10:
        st.warning(f"⚠️ **Low sample size ({len(trend_df)} athletes).** Recommendations may be less accurate. Try a broader category if possible.")
    
    if not trend_df.empty:
        # Calculate Ratios
        trend_df["r1"] = trend_df[c1] / trend_df[c3]
        trend_df["r2"] = trend_df[c2] / trend_df[c3]
        
        # Use quantiles based on aggressiveness buffer
        # 0.5 aggressiveness = median. Higher = higher quantile (closer to 3rd).
        q1 = 0.45 + (calc_buffer * 0.1)  # Range 0.45 - 0.55
        q2 = 0.94 + (calc_buffer * 0.04) # Range 0.94 - 0.98 (relative to r1/r2 space)
        
        # Simpler: just use median and allow the slider to shift them slightly
        med1 = trend_df["r1"].median() * (0.98 + (calc_buffer * 0.04))
        med2 = trend_df["r2"].median() * (0.99 + (calc_buffer * 0.02))
        
        rec1 = round((calc_goal * med1) / 2.5) * 2.5
        rec2 = round((calc_goal * med2) / 2.5) * 2.5
        
        # Ensure they are strictly increasing
        if rec2 >= calc_goal: rec2 = calc_goal - 2.5
        if rec1 >= rec2: rec1 = rec2 - 5.0

        # 3. Display Recommendations
        st.markdown("---")
        res_c1, res_c2, res_c3 = st.columns(3)
        res_c1.metric("1st Attempt (Opener)", f"{rec1} kg", help="Safe weight you can do for a double.")
        res_c2.metric("2nd Attempt", f"{rec2} kg", help="A transition catch weight to prepare for the 3rd.")
        res_c3.metric("3rd Attempt (Goal)", f"{calc_goal} kg", delta=f"{calc_goal-rec2:+.1f} kg jump")

        # 4. Visualizations
        st.markdown("---")
        chart_c1, chart_c2 = st.columns([2, 1])
        
        with chart_c1:
            # Attempt Path Chart
            fig_path = go.Figure()
            # The Goal Path
            path_x = ["1st", "2nd", "3rd"]
            path_y = [rec1, rec2, calc_goal]
            
            fig_path.add_trace(go.Scatter(
                x=path_x, y=path_y,
                mode='lines+markers+text',
                text=[f"{v}kg" for v in path_y],
                textposition="top center",
                line=dict(color='#388e3c', width=4, shape='spline'),
                marker=dict(size=12, symbol='hexagon', line=dict(width=2, color='white')),
                name="Your Path"
            ))
            
            # Add shaded area for "Normal Range" based on category std dev
            std1 = trend_df["r1"].std() * calc_goal
            std2 = trend_df["r2"].std() * calc_goal
            
            # SHADED AREA
            fig_path.add_trace(go.Scatter(
                x=path_x + path_x[::-1],
                y=[rec1-std1, rec2-std2, calc_goal] + [calc_goal, rec2+std2, rec1+std1],
                fill='toself',
                fillcolor='rgba(56, 142, 60, 0.25)',
                line=dict(color='rgba(255,255,255,0)'),
                hoverinfo="skip",
                showlegend=True,
                name="Population Norm (±1 SD)"
            ))
            
            fig_path.update_layout(
                title=f"The {calc_lift} Path to Success",
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                yaxis_title="Weight (kg)",
                height=500,
                margin=dict(l=20, r=20, t=60, b=20)
            )
            st.plotly_chart(fig_path, use_container_width=True)

        with chart_c2:
            # Jump Distribution (2nd to 3rd)
            trend_df["jump_2_3"] = trend_df[c3] - trend_df[c2]
            fig_dist = px.histogram(
                trend_df, x="jump_2_3",
                histnorm="probability", # Make it relative
                title="Common 2nd → 3rd Jumps",
                labels={"jump_2_3": "Jump Size (kg)"},
                template="plotly_dark",
                color_discrete_sequence=['#f9a825'],
                nbins=20
            )
            # Highlight user's jump
            user_jump = calc_goal - rec2
            fig_dist.add_vline(x=user_jump, line_dash="dash", line_color="#ef5350", 
                              annotation_text="Your Jump", annotation_position="top right")
            
            fig_dist.update_yaxes(title_text="Probability")
            fig_dist.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                height=500,
                margin=dict(l=20, r=20, t=60, b=20)
            )
            st.plotly_chart(fig_dist, use_container_width=True)
            
        with st.expander("📚 Why these numbers?"):
            st.write(f"""
                Based on **{len(trend_df)}** successful 3-for-3 performances in the **{calc_gender} {calc_wc}kg {calc_equip}** category:
                - The median opener is **{(trend_df['r1'].median()*100):.1f}%** of the 3rd attempt.
                - The median 2nd attempt is **{(trend_df['r2'].median()*100):.1f}%** of the 3rd attempt.
                - Your recommended jumps take into account the typical distribution of successful lifters in your weight class.
            """)
    else:
        st.error("No successful 3-for-3 data found for this specific category. Please try a different Equipment or Weight Class.")

# ---------- 5. Pattern Discoverer (Sandbox) ----------
elif active == "pattern_discoverer":
    st.subheader("🔍 Pattern Discoverer Sandbox")
    st.write("The ultimate playground for curious lifters. Plot and outplot any combination of metrics to discover hidden trends in the sport.")

    # 1. Axis & Metric Definitions
    axes_options = {
        "Bodyweight": "BodyweightKg",
        "Age": "Age",
        "Squat": "Best3SquatKg",
        "Bench": "Best3BenchKg",
        "Deadlift": "Best3DeadliftKg",
        "Total": "TotalKg",
        "Dots": "Dots",
        "Wilks": "Wilks",
        "Glossbrenner": "Glossbrenner",
        "Goodlift": "Goodlift"
    }
    
    # 2. Discovery Presets (Quick Access)
    st.markdown("### 💡 Quick Discoveries")
    p_c1, p_c2, p_c3, p_c4 = st.columns(4)
    
    # Preset initialisation
    if "sandbox_x" not in st.session_state: st.session_state["sandbox_x"] = "Age"
    if "sandbox_y" not in st.session_state: st.session_state["sandbox_y"] = "Total"
    if "sandbox_z" not in st.session_state: st.session_state["sandbox_z"] = "None"
    if "sandbox_color" not in st.session_state: st.session_state["sandbox_color"] = "Equipment"
    if "sandbox_dim" not in st.session_state: st.session_state["sandbox_dim"] = "2D"

    if p_c1.button("📈 The Age Peak", use_container_width=True):
        st.session_state["sandbox_x"], st.session_state["sandbox_y"], st.session_state["sandbox_z"] = "Age", "Total", "None"
        st.session_state["sandbox_color"], st.session_state["sandbox_dim"] = "Equipment", "2D"
        st.rerun()
    if p_c2.button("⚖️ Squat-Deadlift Balance", use_container_width=True):
        st.session_state["sandbox_x"], st.session_state["sandbox_y"], st.session_state["sandbox_z"] = "Squat", "Deadlift", "None"
        st.session_state["sandbox_color"], st.session_state["sandbox_dim"] = "Sex", "2D"
        st.rerun()
    if p_c3.button("📦 3D Strength Cube", use_container_width=True):
        st.session_state["sandbox_x"], st.session_state["sandbox_y"], st.session_state["sandbox_z"] = "Squat", "Bench", "Deadlift"
        st.session_state["sandbox_color"], st.session_state["sandbox_dim"] = "Sex", "3D"
        st.rerun()
    if p_c4.button("🧬 Relative Strength", use_container_width=True):
        st.session_state["sandbox_x"], st.session_state["sandbox_y"], st.session_state["sandbox_z"] = "Bodyweight", "Dots", "None"
        st.session_state["sandbox_color"], st.session_state["sandbox_dim"] = "Equipment", "2D"
        st.rerun()

    st.markdown("---")

    # 3. Sandbox Controls
    with st.expander("🛠️ Customise Your Sandbox", expanded=True):
        ctrl_c1, ctrl_c2, ctrl_c3, ctrl_c4 = st.columns(4)
        
        with ctrl_c1:
            dim_mode = st.radio("Dimensions", ["2D", "3D"], index=["2D", "3D"].index(st.session_state["sandbox_dim"]), horizontal=True)
            st.session_state["sandbox_dim"] = dim_mode # Sync back if manually changed
            x_ax = st.selectbox("X-Axis", list(axes_options.keys()), index=list(axes_options.keys()).index(st.session_state["sandbox_x"]))
        
        with ctrl_c2:
            y_ax = st.selectbox("Y-Axis", list(axes_options.keys()), index=list(axes_options.keys()).index(st.session_state["sandbox_y"]))
        
        with ctrl_c3:
            if dim_mode == "3D":
                z_options = list(axes_options.keys())
                z_idx = z_options.index(st.session_state["sandbox_z"]) if st.session_state["sandbox_z"] in z_options else 2
                z_ax = st.selectbox("Z-Axis", z_options, index=z_idx)
            else:
                z_ax = None
                st.write("") # Spacer
                st.info("Switch to 3D to enable Z-Axis.")
        
        with ctrl_c4:
            color_by = st.selectbox("Color By", ["Sex", "Equipment", "AgeClass", "WeightClassKg"], index=["Sex", "Equipment", "AgeClass", "WeightClassKg"].index(st.session_state["sandbox_color"]))

        st.markdown("---")
        st.markdown("##### 🔦 Highlight & Filter")
        f_c1, f_c2, f_c3 = st.columns([1, 1, 1])
        with f_c1:
            h_sex = st.multiselect("Highlight Sex", ["M", "F"], default=["M", "F"], help="Keep only selected genders.")
        with f_c2:
            all_equip = sorted(alldf["Equipment"].dropna().unique().tolist())
            h_equip = st.multiselect("Highlight Equipment", all_equip, default=all_equip, help="Keep only selected equipment types.")
        with f_c3:
            h_action = st.radio("Action for Excluded", ["Grey-out", "Remove"], horizontal=True, help="'Grey-out' keeps points visible but desaturated. 'Remove' hides them completely.")

    # 3.5 User Manual Entry for Plotting
    with st.expander("📍 Plot Your Performance", expanded=False):
        st.write("Enter your data to see where you stand on the distribution map.")
        u_c1, u_c2, u_c3 = st.columns(3)
        with u_c1:
            u_sex_sel = st.selectbox("Your Sex", ["Male", "Female"], key="u_sandbox_gender")
            u_bw = st.number_input("Your Bodyweight (kg)", 30.0, 250.0, 80.0, 0.1, key="u_sandbox_bw")
            u_age = st.number_input("Your Age", 5, 100, 25, 1, key="u_sandbox_age")
        with u_c2:
            u_sq = st.number_input("Your Best Squat (kg)", 0.0, 600.0, 0.0, 2.5, key="u_sandbox_sq")
            u_bn = st.number_input("Your Best Bench (kg)", 0.0, 500.0, 0.0, 2.5, key="u_sandbox_bn")
        with u_c3:
            u_dl = st.number_input("Your Best Deadlift (kg)", 0.0, 600.0, 0.0, 2.5, key="u_sandbox_dl")
            
            # Local utility for calculation
            def get_sandbox_user_metrics(s, b, d, w, a, g):
                tot = s + b + d
                # Dots
                if g == "Male": A, B, C, D, E = -0.000001093, 0.0007391293, -0.1918759221, 24.0900756, -307.75076
                else: A, B, C, D, E = -0.0000010706, 0.0005158568, -0.1126655495, 13.6175032, -57.96288
                denom = (A * w**4) + (B * w**3) + (C * w**2) + (D * w) + E
                dots = tot * (500 / denom) if denom > 0 else 0.0
                # Wilks
                if g == "Male": aw, bw, cw, dw, ew, fw = -216.0475144, 16.2606339, -0.002388645, -0.00113732, 7.01863e-6, -1.291e-8
                else: aw, bw, cw, dw, ew, fw = 594.31747775582, -27.23842536447, 0.82112226871, -0.00930733913, 4.731582e-5, -9.054e-8
                w_denom = aw + (bw * w) + (cw * w**2) + (dw * w**3) + (ew * w**4) + (fw * w**5)
                wilks = tot * (500 / w_denom) if w_denom > 0 else 0.0
                # Goodlift
                if g == "Male": ag, bg, cg = 1199.72839, 1025.18162, 0.00921
                else: ag, bg, cg = 610.32796, 1045.59282, 0.03048
                gl_denom = ag - bg * np.exp(-cg * w)
                goodlift = tot * (100 / gl_denom) if gl_denom > 0 else 0.0
                
                return {
                    "BodyweightKg": w, "Age": a, "Best3SquatKg": s, "Best3BenchKg": b, "Best3DeadliftKg": d,
                    "TotalKg": tot, "Dots": dots, "Wilks": wilks, "Goodlift": goodlift, "Glossbrenner": 0.0
                }
            
            u_metrics = get_sandbox_user_metrics(u_sq, u_bn, u_dl, u_bw, u_age, u_sex_sel)
            st.write("") # Spacer
            st.write(f"**Total:** {u_sq+u_bn+u_dl:.1f} kg")
            st.write(f"**Dots:** {u_metrics['Dots']:.2f}")

    # Map user coordinates
    u_x = u_metrics.get(axes_options[x_ax], 0)
    u_y = u_metrics.get(axes_options[y_ax], 0)
    u_z = u_metrics.get(axes_options[z_ax], 0) if z_ax else 0

    # 4. Data Preparation & Filtering
    filter_data = alldf.dropna(subset=[axes_options[x_ax], axes_options[y_ax]])
    if z_ax: filter_data = filter_data.dropna(subset=[axes_options[z_ax]])
    
    # Apply Highlight/Filter Logic
    mask = filter_data["Sex"].isin(h_sex) & filter_data["Equipment"].isin(h_equip)
    
    if h_action == "Remove":
        filter_data = filter_data[mask]
        display_col = color_by
    else:
        # Grey-out logic: create a specialized display column
        # We use a leading space to ensure " Others" stays at the end of sorted lists
        filter_data["display_cat"] = filter_data.apply(
            lambda row: str(row[color_by]) if (row["Sex"] in h_sex and row["Equipment"] in h_equip) else " Others", 
            axis=1
        )
        display_col = "display_cat"

    # Performance Sampling
    limit = 5000 if dim_mode == "3D" else 15000
    if len(filter_data) > limit:
        st.warning(f"⚡ **Performance Optimisation**: Plotting a random sample of {limit} athletes from the {len(filter_data)} available.")
        plot_df = filter_data.sample(limit)
    else:
        plot_df = filter_data
    
    # 5. Visualization Logic
    st.markdown("---")
    
    # ── Category Sorting & Chromatic Colors ───────────────────────
    cat_order = sorted(plot_df[display_col].dropna().unique().tolist())
    # Special sorting for Weight Classes if numeric
    if color_by == "WeightClassKg":
        try:
            # Sort everything except " Others"
            pure_cats = [c for c in cat_order if c != " Others"]
            pure_cats = sorted(pure_cats, key=float)
            if " Others" in cat_order:
                cat_order = pure_cats + [" Others"]
            else:
                cat_order = pure_cats
        except: pass
    
    # Sample a sequential color scale
    # If " Others" is present, we handle it separately
    base_cats = [c for c in cat_order if c != " Others"]
    n_base = len(base_cats)
    
    # --- Custom Gender Coloring Sync ---
    if color_by == "Sex":
        # Force sync with the app's main color scheme (Male=Blue, Female=Red)
        color_seq = []
        for cat in cat_order:
            if cat == "M": color_seq.append("#42a5f5")
            elif cat == "F": color_seq.append("#ef5350")
            else: color_seq.append("rgba(200, 200, 200, 0.2)") # Others
    else:
        # Standard dynamic Turbo scale for Equipment, WeightClass, AgeClass
        if n_base > 1:
            color_seq = px.colors.sample_colorscale("Turbo", [i/(n_base-1) for i in range(n_base)])
        elif n_base == 1:
            color_seq = [px.colors.sample_colorscale("Turbo", [0.5])[0]]
        else:
            color_seq = []

        if " Others" in cat_order:
            # Add a desaturated grey for " Others"
            color_seq.append("rgba(200, 200, 200, 0.2)")

    if dim_mode == "2D":
        # Calculate Pearson Correlation
        # Only use highlights for correlation if in Grey-out mode? Or full data? 
        # Typically correlation usually refers to the plotted sample.
        corr_df = plot_df[plot_df[display_col] != " Others"] if " Others" in plot_df.columns else plot_df
        if not corr_df.empty:
            corr = corr_df[axes_options[x_ax]].corr(corr_df[axes_options[y_ax]])
            st.write(f"🔬 **Correlation Analysis**: The relationship between **{x_ax}** and **{y_ax}** (highlighted points) has a Pearson coefficient of **{corr:.2f}**.")
        
        fig_sb = px.scatter(
            plot_df, x=axes_options[x_ax], y=axes_options[y_ax],
            color=display_col,
            category_orders={display_col: cat_order},
            color_discrete_sequence=color_seq,
            template="plotly_dark",
            render_mode='webgl', # Performance high-five
            title=f"{y_ax} vs {x_ax} Discovery",
            labels={axes_options[x_ax]: f"{x_ax} (kg/yrs)", axes_options[y_ax]: f"{y_ax} (kg/pts)"},
            hover_name="Name",
            hover_data=["Age", "BodyweightKg", "TotalKg", "Dots"]
        )
    else:
        fig_sb = px.scatter_3d(
            plot_df, x=axes_options[x_ax], y=axes_options[y_ax], z=axes_options[z_ax],
            color=display_col,
            category_orders={display_col: cat_order},
            color_discrete_sequence=color_seq,
            template="plotly_dark",
            title=f"3D Analysis: {z_ax} | {y_ax} | {x_ax}",
            labels={axes_options[x_ax]: x_ax, axes_options[y_ax]: y_ax, axes_options[z_ax]: z_ax},
            hover_name="Name",
            height=800
        )
        fig_sb.update_layout(margin=dict(l=0, r=0, t=30, b=0))


    fig_sb.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # --- Add User Point (Always on Top) ---
    if u_sq + u_bn + u_dl > 0:
        if dim_mode == "2D":
            # Using Scattergl to match the WebGL engine of the main plot
            fig_sb.add_trace(go.Scattergl(
                x=[u_x], y=[u_y],
                mode='markers',
                name='YOU',
                marker=dict(
                    color='#FF1744',
                    size=14,
                    symbol='star',
                    line=dict(width=1.5, color='white')
                ),
                hovertemplate=f"<b>YOU</b><br>{x_ax}: %{{x}}<br>{y_ax}: %{{y}}<extra></extra>"
            ))
        else:
            if color_by == "Sex":
                # Special color for Sex view
                fig_sb.add_trace(go.Scatter3d(
                    x=[u_x], y=[u_y], z=[u_z],
                    mode='markers',
                    name='YOU',
                    marker=dict(
                        color='#39FF14', # Neon Green
                        size=14,
                        symbol='diamond',
                        line=dict(width=3, color='purple')
                    ),
                    hovertemplate=f"<b>YOU</b><br>{x_ax}: %{{x}}<br>{y_ax}: %{{y}}<br>{z_ax}: %{{z}}<extra></extra>"
                ))
            else:
                # Default for other views
                fig_sb.add_trace(go.Scatter3d(
                    x=[u_x], y=[u_y], z=[u_z],
                    mode='markers',
                    name='YOU',
                    marker=dict(
                        color='#FF1744', # Neon Red
                        size=14,
                        symbol='diamond',
                        line=dict(width=3, color='white')
                    ),
                    hovertemplate=f"<b>YOU</b><br>{x_ax}: %{{x}}<br>{y_ax}: %{{y}}<br>{z_ax}: %{{z}}<extra></extra>"
                ))
    bbb1, bbb2, bbb3 = st.columns([1,8,1])
    with bbb2:
        st.plotly_chart(fig_sb, use_container_width=True)
    
    st.info("💡 **Pro-Tip**: Click and drag to rotate 3D plots. Use the legend to toggle specific groups on and off. **Others** represents points excluded by your filters.")
    st.warning("⚠️ **Can't find yourself?**: If you can't find yourself, you're covered by a cluster of dots, right in the middle of the pack.")

    



# ---------- 6. Freak Finder ----------
elif active == "freak_finder":
    st.subheader("🤯 Strength Freaks Finder")
    st.info("Identify performance outliers. Pair any two metrics to visualize the main distribution (heatmap) and highlight the 'freaks' (scatter) who break the norms.")

    # 1. Selection & Filtering UI
    filter_c1, filter_c2, filter_c3 = st.columns(3)
    
    with filter_c1:
        freak_gender = st.selectbox("Gender Filter", ["Male", "Female"], key="freak_gender_sel")
        metric_x = st.selectbox("X-Axis Metric", ["BodyweightKg", "Age", "TotalKg", "Dots", "Best3SquatKg", "Best3BenchKg", "Best3DeadliftKg"], index=0)
    
    with filter_c2:
        # Dynamic Weight Class based on Gender
        ref_df = malesdf if freak_gender == "Male" else femalesdf
        all_wc = sorted(ref_df["WeightClassKg"].dropna().unique().tolist())
        sel_wc = st.selectbox("Weight Class", ["All"] + all_wc, key="freak_wc_sel")
        metric_y = st.selectbox("Y-Axis Metric", ["TotalKg", "Dots", "Best3SquatKg", "Best3BenchKg", "Best3DeadliftKg"], index=0)

    with filter_c3:
        age_range = st.slider("Age Range", 5, 90, (18, 40), key="freak_age_range")
        freak_threshold = st.slider("Freak Threshold (Top %)", 0.1, 5.0, 1.0, step=0.1, help="Highlight the top X% of performers.")

    # 2. Data Filtering
    # Apply filters
    filtered_df = ref_df[
        (ref_df["Age"] >= age_range[0]) & 
        (ref_df["Age"] <= age_range[1])
    ].copy()
    
    if sel_wc != "All":
        filtered_df = filtered_df[filtered_df["WeightClassKg"] == sel_wc]
    
    # 3.5 User Manual Entry for Plotting
    with st.expander("📍 Plot Your Performance", expanded=False):
        st.write("Enter your data to see where you stand on the distribution map.")
        u_c1, u_c2, u_c3 = st.columns(3)
        with u_c1:
            u_sex_sel = st.selectbox("Your Sex", ["Male", "Female"], key="u_sandbox_gender")
            u_bw = st.number_input("Your Bodyweight (kg)", 30.0, 250.0, 80.0, 0.1, key="u_sandbox_bw")
            u_age = st.number_input("Your Age", 5, 100, 25, 1, key="u_sandbox_age")
        with u_c2:
            u_sq = st.number_input("Your Best Squat (kg)", 0.0, 600.0, 0.0, 2.5, key="u_sandbox_sq")
            u_bn = st.number_input("Your Best Bench (kg)", 0.0, 500.0, 0.0, 2.5, key="u_sandbox_bn")
        with u_c3:
            u_dl = st.number_input("Your Best Deadlift (kg)", 0.0, 600.0, 0.0, 2.5, key="u_sandbox_dl")
            
            # Local utility for calculation
            def get_sandbox_user_metrics(s, b, d, w, a, g):
                tot = s + b + d
                # Dots
                if g == "Male": A, B, C, D, E = -0.000001093, 0.0007391293, -0.1918759221, 24.0900756, -307.75076
                else: A, B, C, D, E = -0.0000010706, 0.0005158568, -0.1126655495, 13.6175032, -57.96288
                denom = (A * w**4) + (B * w**3) + (C * w**2) + (D * w) + E
                dots = tot * (500 / denom) if denom > 0 else 0.0
                # Wilks
                if g == "Male": aw, bw, cw, dw, ew, fw = -216.0475144, 16.2606339, -0.002388645, -0.00113732, 7.01863e-6, -1.291e-8
                else: aw, bw, cw, dw, ew, fw = 594.31747775582, -27.23842536447, 0.82112226871, -0.00930733913, 4.731582e-5, -9.054e-8
                w_denom = aw + (bw * w) + (cw * w**2) + (dw * w**3) + (ew * w**4) + (fw * w**5)
                wilks = tot * (500 / w_denom) if w_denom > 0 else 0.0
                # Goodlift
                if g == "Male": ag, bg, cg = 1199.72839, 1025.18162, 0.00921
                else: ag, bg, cg = 610.32796, 1045.59282, 0.03048
                gl_denom = ag - bg * np.exp(-cg * w)
                goodlift = tot * (100 / gl_denom) if gl_denom > 0 else 0.0
                
                return {
                    "BodyweightKg": w, "Age": a, "Best3SquatKg": s, "Best3BenchKg": b, "Best3DeadliftKg": d,
                    "TotalKg": tot, "Dots": dots, "Wilks": wilks, "Goodlift": goodlift, "Glossbrenner": 0.0
                }
            
            u_metrics = get_sandbox_user_metrics(u_sq, u_bn, u_dl, u_bw, u_age, u_sex_sel)
            st.write("") # Spacer
            st.write(f"**Total:** {u_sq+u_bn+u_dl:.1f} kg")
            st.write(f"**Dots:** {u_metrics['Dots']:.2f}")
    
    # Ensure metrics are valid and numeric
    filtered_df = filtered_df.dropna(subset=[metric_x, metric_y])
    filtered_df = filtered_df[(filtered_df[metric_x] > 0) & (filtered_df[metric_y] > 0)]
    
    # Keep only each athlete's best total to avoid duplicates
    filtered_df = filtered_df.sort_values("TotalKg", ascending=False).drop_duplicates(subset="Name", keep="first")

    if len(filtered_df) < 5:
        st.warning(f"⚠️ **Not enough data.** Only {len(filtered_df)} athletes found for this combination. Try broadening your filters.")
    else:
        # 3. Identify Freaks (Outliers)
        # We define freaks as the top X% by the Y metric (usually the strength metric)
        n_freaks = max(1, int(len(filtered_df) * (freak_threshold / 100)))
        freaks_df = filtered_df.sort_values(metric_y, ascending=False).head(n_freaks)
        main_df = filtered_df.drop(freaks_df.index)

        # 4. Combined Visualization
        # Base: Density Heatmap
        fig_freak = px.density_heatmap(
            filtered_df, x=metric_x, y=metric_y,
            title=f"{metric_y} vs {metric_x} Distribution ({freak_gender})",
            labels={metric_x: f"{metric_x} (kg/yrs)", metric_y: f"{metric_y} (kg/pts)"},
            template="plotly_dark",
            nbinsx=30, nbinsy=30,
            color_continuous_scale="Viridis"
        )
        
        # We add them as a separate trace
        fig_freak.add_trace(go.Scatter(
            x=freaks_df[metric_x],
            y=freaks_df[metric_y],
            mode='markers',
            name='Strength Freaks',
            marker=dict(
                color='#ef5350', 
                size=10, 
                symbol='star',
                line=dict(width=1, color='white')
            ),
            text=freaks_df["Name"],
            hovertemplate="<b>%{text}</b><br>" +
                          f"{metric_x}: %{{x}}<br>" +
                          f"{metric_y}: %{{y}}<br>" +
                          "<extra></extra>"
        ))

        fig_freak.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            height=700,
            margin=dict(l=20, r=20, t=60, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        # --- Add User Point (Always on Top) ---
        if u_sq + u_bn + u_dl > 0:
            u_x = u_metrics.get(metric_x, 0)
            u_y = u_metrics.get(metric_y, 0)
            # Using Scattergl to match the WebGL engine of the main plot
            fig_freak.add_trace(go.Scattergl(
                x=[u_x], y=[u_y],
                mode='markers',
                name='YOU',
                marker=dict(
                    color='#2962FF',
                    size=14,
                    symbol='star',
                    line=dict(width=1.5, color='#00E5FF')
                ),
                hovertemplate=f"<b>YOU</b><br>{metric_x}: %{{x}}<br>{metric_y}: %{{y}}<extra></extra>"
            ))
        
        st.plotly_chart(fig_freak, use_container_width=True)

        
        # 5. List of identified freaks
        with st.expander(f"📋 List of {len(freaks_df)} Identified Freaks"):
            # Prepare display dataframe
            display_df = freaks_df.sort_values(metric_y, ascending=False).copy()
            
            # Create clickable link column
            display_df["Profile"] = display_df["Name"].apply(lambda n: f"/athletes?name={urllib.parse.quote_plus(n)}")
            
            # Select columns to show (including the metrics chosen for X and Y)
            show_cols = ["Profile", "Age", "BodyweightKg", "TotalKg", "Dots", "WeightClassKg", "Date", "Federation"]
            # Add metric_x/y if they aren't already in the list
            for m in [metric_x, metric_y]:
                if m not in show_cols:
                    show_cols.insert(1, m)
            
            st.dataframe(
                display_df[show_cols],
                column_config={
                    "Profile": st.column_config.LinkColumn(
                        "Athlete Name",
                        help="Click to view full athlete profile",
                        display_text=r"/athletes\?name=(.*)" # Simple regex to show name (will still be url-encoded in some views but cleaner)
                    )
                },
                use_container_width=True,
                hide_index=True
            )

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

    input_cols = st.columns(3)
    
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

    input_cols2 = st.columns(3)

    with input_cols2[0]:
        # Total from 0 to 1500 with delta 2.5
        bench_range = np.arange(0.0, 1502.5, 2.5)
        bench_options = [round(x, 1) for x in bench_range]
        # Default to a common total like 400.0
        try:
            default_bench_idx = bench_options.index(100.0)
        except ValueError:
            default_bench_idx = 0
            
        bench = st.selectbox("Bench (kg)", bench_options, index=default_bench_idx)
    
    with input_cols2[1]:
        # Total from 0 to 1500 with delta 2.5
        squat_range = np.arange(0.0, 1502.5, 2.5)
        squat_options = [round(x, 1) for x in squat_range]
        # Default to a common total like 400.0
        try:
            default_squat_idx = squat_options.index(150.0)
        except ValueError:
            default_squat_idx = 0
            
        squat = st.selectbox("Squat (kg)", squat_options, index=default_squat_idx)
    
    with input_cols2[2]:
        # Total from 0 to 1500 with delta 2.5
        deadlift_range = np.arange(0.0, 1502.5, 2.5)
        deadlift_options = [round(x, 1) for x in deadlift_range]
        # Default to a common total like 400.0
        try:
            default_deadlift_idx = deadlift_options.index(150.0)
        except ValueError:
            default_deadlift_idx = 0
            
        deadlift = st.selectbox("Deadlift (kg)", deadlift_options, index=default_deadlift_idx)
    
    total = squat + bench + deadlift;

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

    # ---------- 10. Relative Strength Dashboard ----------

    st.markdown("---")
    st.subheader("📊 Relative Strength Dashboard")
    st.write("Compare your entered lifts against the category (same Gender & closest Weight Class).")

    # --- Determine the user's weight class from the dataset ---
    ref_df_calc = malesdf if gender == "Male" else femalesdf
    all_wc_vals = ref_df_calc["WeightClassKg"].dropna().unique().tolist()

    # Find closest weight class by parsing numeric values
    def parse_wc(wc):
        try: return float(str(wc).replace("+", ""))
        except: return 9999

    closest_wc = min(all_wc_vals, key=lambda wc: abs(parse_wc(wc) - weight))

    # Build category reference
    category_df_calc = ref_df_calc[ref_df_calc["WeightClassKg"] == closest_wc].copy()

    if not category_df_calc.empty and total > 0:
        # Category benchmarks
        avg_squat_c = category_df_calc["Best3SquatKg"].mean()
        avg_bench_c = category_df_calc["Best3BenchKg"].mean()
        avg_deadlift_c = category_df_calc["Best3DeadliftKg"].mean()

        rec_squat_c = category_df_calc["Best3SquatKg"].max()
        rec_bench_c = category_df_calc["Best3BenchKg"].max()
        rec_deadlift_c = category_df_calc["Best3DeadliftKg"].max()

        categories_radar = ['Squat', 'Bench Press', 'Deadlift']

        fig_radar_calc = go.Figure()

        # 1. Category Record (Background)
        fig_radar_calc.add_trace(go.Scatterpolar(
            r=[rec_squat_c, rec_bench_c, rec_deadlift_c, rec_squat_c],
            theta=categories_radar + [categories_radar[0]],
            fill='toself',
            fillcolor='rgba(255, 213, 79, 0.1)',
            name='Category Record',
            line=dict(color='rgba(255, 213, 79, 0.4)', width=2, dash='dot'),
            marker=dict(size=4),
            hovertemplate="Record: %{r} kg<extra></extra>"
        ))

        # 2. Category Average (Middle)
        fig_radar_calc.add_trace(go.Scatterpolar(
            r=[avg_squat_c, avg_bench_c, avg_deadlift_c, avg_squat_c],
            theta=categories_radar + [categories_radar[0]],
            fill='toself',
            fillcolor='rgba(66, 165, 245, 0.1)',
            name='Category Average',
            line=dict(color='rgba(66, 165, 245, 0.6)', width=2, dash='dash'),
            marker=dict(size=4),
            hovertemplate="Average: %{r:.1f} kg<extra></extra>"
        ))

        # 3. You (Foreground)
        fig_radar_calc.add_trace(go.Scatterpolar(
            r=[squat, bench, deadlift, squat],
            theta=categories_radar + [categories_radar[0]],
            fill='toself',
            fillcolor='rgba(239, 83, 80, 0.3)',
            name='You',
            line=dict(color='#ef5350', width=4),
            marker=dict(size=10, symbol='diamond'),
            hovertemplate="You: %{r} kg<extra></extra>"
        ))

        fig_radar_calc.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(rec_squat_c, rec_bench_c, rec_deadlift_c, squat, bench, deadlift) * 1.15],
                    gridcolor="rgba(255,255,255,0.1)",
                    angle=-90,
                    tickangle=0
                ),
                angularaxis=dict(gridcolor="rgba(255,255,255,0.1)", linecolor="rgba(255,255,255,0.2)"),
                bgcolor="rgba(0,0,0,0)"
            ),
            showlegend=True,
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=600,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.05, xanchor="center", x=0.5)
        )

        # --- Columns for side-by-side view ---
        rad_cols_calc = st.columns([2, 1])

        with rad_cols_calc[0]:
            st.plotly_chart(fig_radar_calc, use_container_width=True)

        with rad_cols_calc[1]:
            st.write("")  # Spacer
            comparison_data_calc = {
                "Lift": categories_radar,
                "You": [f"{squat} kg", f"{bench} kg", f"{deadlift} kg"],
                "Average": [f"{round(avg_squat_c, 1)} kg", f"{round(avg_bench_c, 1)} kg", f"{round(avg_deadlift_c, 1)} kg"],
                "Record": [f"{rec_squat_c} kg", f"{rec_bench_c} kg", f"{rec_deadlift_c} kg"]
            }
            st.dataframe(
                pd.DataFrame(comparison_data_calc),
                hide_index=True,
                use_container_width=True,
                column_config={"Lift": "Lift", "You": "You", "Average": "Average", "Record": "Record"}
            )

            # --- Percentile & Progress Gauges ---
            cat_totals_calc = category_df_calc[category_df_calc["TotalKg"] > 0]["TotalKg"].sort_values()

            if not cat_totals_calc.empty:
                rank_calc = (cat_totals_calc < total).sum()
                percentile_calc = (rank_calc / len(cat_totals_calc)) * 100
                top_percent_calc = 100 - percentile_calc
                progress_to_record_calc = (total / cat_totals_calc.max()) * 100 if cat_totals_calc.max() > 0 else 0

                fig_pct_calc = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=percentile_calc,
                    number={'suffix': "%", 'font': {'size': 25}},
                    gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#42a5f5"}, 'bgcolor': "rgba(0,0,0,0)"}
                ))
                fig_rec_calc = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=progress_to_record_calc,
                    number={'suffix': "%", 'font': {'size': 25}},
                    gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#ffd54f"}, 'bgcolor': "rgba(0,0,0,0)"}
                ))

                for f_g in [fig_pct_calc, fig_rec_calc]:
                    f_g.update_layout(
                        height=125,
                        margin=dict(l=10, r=10, t=10, b=10),
                        paper_bgcolor="rgba(0,0,0,0)",
                        font={'color': "#f0f0f5"}
                    )

                st.markdown("<br>", unsafe_allow_html=True)

                st.markdown("<div style='text-align: center; font-weight: bold;'>📊 Percentile Standing (total)</div>", unsafe_allow_html=True)
                st.write("")
                st.plotly_chart(fig_pct_calc, use_container_width=True)

                st.markdown("<div style='text-align: center; font-weight: bold;'>🏆 Progress to Record (total)</div>", unsafe_allow_html=True)
                st.write("")
                st.plotly_chart(fig_rec_calc, use_container_width=True)

                # Standing Summary
                if top_percent_calc <= 1: st.success("⭐ Top 1%!")
                elif top_percent_calc <= 10: st.info(f"💪 Top {int(top_percent_calc)}%!")
                st.caption(f"Based on **{len(category_df_calc)}** athletes in **{closest_wc}kg {gender}**.")
    elif total > 0:
        st.info("Not enough category data for benchmarks.")
    else:
        st.info("Enter your lifts above to see your relative strength dashboard.")

    # ---------- 11. 1RM Calculator ----------

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

    # ---------- 12. Load Estimator (Reverse 1RM) ----------

    st.markdown("---")

    st.subheader("🎯 Load Estimator")
    st.info("Given your 1RM, target reps, and RPE — estimate the load you should use. Based on the reverse O'Conner formula.")

    est_c1, est_c2, est_c3 = st.columns(3)

    with est_c1:
        est_1rm = st.number_input("Your 1RM (kg)", min_value=0.0, max_value=1000.0, value=100.0, step=2.5, help="Your known or estimated 1 Rep Max.", key="est_1rm")

    with est_c2:
        est_reps = st.number_input("Target Reps", min_value=1, max_value=20, value=5, step=1, help="How many reps you plan to do.", key="est_reps")

    with est_c3:
        est_rpe = st.slider("Target RPE", min_value=5.0, max_value=10.0, value=8.0, step=0.5, help="Rate of Perceived Exertion you want to hit.", key="est_rpe")

    st.markdown("---")

    # ── Reverse Calculation ──────────────────────────────────────
    # Original: 1RM = Load * (1 + effective_reps * 0.025)
    # Reversed: Load = 1RM / (1 + effective_reps * 0.025)
    est_effective_reps = est_reps + (10.0 - est_rpe)
    est_load = est_1rm / (1 + (est_effective_reps * 0.025)) if (1 + (est_effective_reps * 0.025)) > 0 else 0

    # Display Result
    est_main, est_chart = st.columns([1, 2])

    with est_main:
        st.metric("Recommended Load", f"{est_load:.1f} kg")
        st.caption(f"Effective reps: {est_effective_reps:.1f} (reps {est_reps} + RIR {10.0 - est_rpe:.0f})")

        st.markdown("### 📋 RPE Reference Table")
        rpe_rows = []
        for r in [6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]:
            eff = est_reps + (10.0 - r)
            ld = est_1rm / (1 + (eff * 0.025)) if (1 + (eff * 0.025)) > 0 else 0
            pct = (ld / est_1rm * 100) if est_1rm > 0 else 0
            rpe_rows.append({"RPE": f"{r}", "Load (kg)": f"{ld:.1f}", "% of 1RM": f"{pct:.1f}%"})
        st.table(pd.DataFrame(rpe_rows))

    with est_chart:
        # Bar chart: load across rep ranges at the chosen RPE
        rep_range = list(range(1, 16))
        loads_by_rep = []
        for r in rep_range:
            eff = r + (10.0 - est_rpe)
            ld = est_1rm / (1 + (eff * 0.025)) if (1 + (eff * 0.025)) > 0 else 0
            loads_by_rep.append(ld)

        fig_est = px.bar(
            x=[f"{r} reps" for r in rep_range], y=loads_by_rep,
            title=f"Estimated Load by Rep Count (@ RPE {est_rpe})",
            labels={'x': 'Reps', 'y': 'Load (kg)'},
            template="plotly_dark",
            color=loads_by_rep,
            color_continuous_scale="Viridis"
        )

        # Highlight the selected rep count
        colors = ["rgba(239, 83, 80, 0.9)" if r == est_reps else "rgba(100, 100, 100, 0.5)" for r in rep_range]
        fig_est.update_traces(marker_color=colors, showlegend=False)

        fig_est.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_est, use_container_width=True)

    # ---------- 13. Fatigue Estimator ----------

    st.markdown("---")

    st.subheader("📉 Fatigue Estimator - An absolutely un-scientific calculator")

    st.write("""
        You know that feeling:
        - Today you train "light" (RPE 8)
        - Next session you feel like garbage and can barely lift
        - What the hell happened?
    """)

    st.write("Whenever a scheme uses precentages or RPEs over different sets, fatigue accumulates, making your 5x5@7 feel like a 5x5@9!")
    st.write("But how much does fatigue actually accumulate?")

    fat_c1, fat_c2, fat_c3 = st.columns(3)

    with fat_c1:
        fat_series = st.number_input(
            "Series (sets)", min_value=1, max_value=20, value=5, step=1,
            help="Number of working sets.", key="fat_series"
        )

    with fat_c2:
        fat_reps = st.number_input(
            "Reps per set", min_value=1, max_value=30, value=5, step=1,
            help="Repetitions per set.", key="fat_reps"
        )

    with fat_c3:
        fat_rpe = st.slider(
            "RPE", min_value=6.0, max_value=10.0, value=8.0, step=0.5,
            help="Rate of Perceived Exertion (6 = very easy, 10 = absolute limit).",
            key="fat_rpe"
        )
    
    # import the sheet
    GOOGLE_SHEET_CSV_URL = (
        "https://docs.google.com/spreadsheets/d/"
        "1eWItYgh2UWjA94bXWqOpRkEUkh3gZVG80O00NeubMo0/export?format=csv"
    )

    @st.cache_data(ttl=300)
    def load_sheet_data(url: str) -> pd.DataFrame:
        # Sheet has no header row — each row is a progression of values
        df = pd.read_csv(url, header=None)
        return df

    raw_df = load_sheet_data(GOOGLE_SHEET_CSV_URL)

    # ── Melt: turn each cell into (column_position, value, row_label) ──
    # Columns become 1-indexed positions; each row is a separate series
    raw_df.columns = [i + 1 for i in range(len(raw_df.columns))]
    raw_df["Progression"] = [f"Row {i + 1}" for i in range(len(raw_df))]

    melted = raw_df.melt(
        id_vars="Progression",
        var_name="Step",
        value_name="Value",
    )

    # ── Build normalized data (each row ÷ its first-set value) ──────────
    norm_df = raw_df.copy()
    value_cols = [c for c in norm_df.columns if c != "Progression"]
    norm_df[value_cols] = norm_df[value_cols].astype(float)
    first_vals = norm_df[value_cols[0]].replace(0, np.nan)
    norm_df[value_cols] = norm_df[value_cols].div(first_vals, axis=0)

    melted_norm = norm_df.melt(
        id_vars="Progression",
        var_name="Step",
        value_name="Value",
    )

    exp = st.expander("🤓 Nerd out →", expanded=False)

    with exp:

        st.markdown("#### 🧪 The Experiment")
        st.write("We asked a number of subjects to perform a benching test: **5 sets, 5 minutes rest, 80% of 1RM, all to absolute failure (RPE 10).** "
                 "Each row is a subject, each column is a set, and the values are the reps achieved.")
        st.write("The left column **normalizes** every subject's reps by their first-set count (set 1 = 1.0), revealing the universal fatigue *shape*. "
                 "The right column shows the raw absolute rep counts.")

        st.markdown("#### 🧮 How the RPE Drift Model Works")
        st.write(
            "From the normalized data we fit a **mean quadratic fatigue curve** — this tells us how fast max reps "
            "decay across sets *when every set is taken to failure*."
        )
        st.write(
            "But in real training you stop **before** failure (e.g. RPE 8 = 2 reps in reserve). "
            "Stopping short generates **less fatigue**, so we scale the decay at each set by an "
            "**effort ratio** = (reps done ÷ max reps possible)²."
        )
        st.write(
            "The squaring reflects that the last reps near failure are disproportionately fatiguing — "
            "skipping them has a bigger recovery benefit than a linear model would suggest."
        )
        st.write(
            "This compounds iteratively: less fatigue → more reps available next set → lower effort → even less fatigue. "
            "At RPE 10 the full experimental curve applies; at RPE 7 only ~33% of the fatigue accumulates per set."
        )
        st.caption("⚠️ Sets beyond 5 are extrapolated from the quadratic fit and may be less accurate.")

        col_norm, col_raw = st.columns(2)

        # ── Helper: build all three charts for a given melted df ──────
        def _render_charts(
            container,
            m_df,
            r_df,
            y_label,
            scatter_title,
            reg_title,
            mean_title,
            table_key,
        ):
            """Render scatter → regression → mean-regression inside *container*."""
            with container:
                # 1) Scatter ──────────────────────────────────────────
                fig = px.scatter(
                    m_df,
                    x="Step",
                    y="Value",
                    color="Progression",
                    template="plotly_dark",
                    title=scatter_title,
                    opacity=0.85,
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter, sans-serif"),
                    title_font_size=16,
                    margin=dict(t=50, b=30),
                    xaxis=dict(dtick=1, title="Series"),
                    yaxis=dict(title=y_label),
                    legend=dict(font=dict(size=9)),
                )
                fig.update_traces(
                    marker=dict(size=8, line=dict(width=1, color="rgba(255,255,255,0.3)"))
                )
                st.plotly_chart(fig, use_container_width=True)

                # Raw data toggle
                if st.checkbox("Show raw data table", key=table_key):
                    st.dataframe(r_df.drop(columns="Progression"), use_container_width=True)

                # 2) Quadratic regression ─────────────────────────────
                fig_reg = go.Figure()
                colors = px.colors.qualitative.Plotly
                n_sets = len(r_df.columns) - 1
                x_smooth = np.linspace(1, n_sets, 100)

                for idx, row_label in enumerate(m_df["Progression"].unique()):
                    subset = m_df[m_df["Progression"] == row_label]
                    x_pts = subset["Step"].values.astype(float)
                    y_pts = subset["Value"].values.astype(float)

                    coeffs = np.polyfit(x_pts, y_pts, 2)
                    y_smooth = np.polyval(coeffs, x_smooth)
                    color = colors[idx % len(colors)]

                    fig_reg.add_trace(go.Scatter(
                        x=x_pts, y=y_pts, mode="markers",
                        marker=dict(size=7, color=color,
                                    line=dict(width=1, color="rgba(255,255,255,0.3)")),
                        name=row_label, legendgroup=row_label, showlegend=True,
                    ))
                    fig_reg.add_trace(go.Scatter(
                        x=x_smooth, y=y_smooth, mode="lines",
                        line=dict(color=color, width=2),
                        name=f"{row_label} fit", legendgroup=row_label, showlegend=False,
                    ))

                fig_reg.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter, sans-serif"),
                    title=reg_title, title_font_size=16,
                    margin=dict(t=50, b=30),
                    xaxis=dict(dtick=1, title="Set"),
                    yaxis=dict(title=y_label),
                    legend=dict(font=dict(size=9)),
                )
                st.plotly_chart(fig_reg, use_container_width=True)

                # 3) Mean regression ──────────────────────────────────
                mean_y = np.zeros(len(x_smooth))
                for row_label in m_df["Progression"].unique():
                    subset = m_df[m_df["Progression"] == row_label]
                    x_pts = subset["Step"].values.astype(float)
                    y_pts = subset["Value"].values.astype(float)
                    coeffs = np.polyfit(x_pts, y_pts, 2)
                    mean_y += np.polyval(coeffs, x_smooth)
                mean_y /= len(m_df["Progression"].unique())

                fig_mean = go.Figure()
                fig_mean.add_trace(go.Scatter(
                    x=m_df["Step"].astype(float), y=m_df["Value"].astype(float),
                    mode="markers",
                    marker=dict(size=5, color="rgba(150,150,255,0.7)",
                                line=dict(width=1, color="white")),
                    name="All subjects",
                ))
                fig_mean.add_trace(go.Scatter(
                    x=x_smooth, y=mean_y, mode="lines",
                    line=dict(color="white", width=3, dash="dash"),
                    name="Mean regression",
                ))
                fig_mean.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter, sans-serif"),
                    title=mean_title, title_font_size=16,
                    margin=dict(t=50, b=30),
                    xaxis=dict(dtick=1, title="Set"),
                    yaxis=dict(title=y_label),
                )
                st.plotly_chart(fig_mean, use_container_width=True)

        # ── Left column: Normalized ──────────────────────────────────
        with col_norm:
            st.markdown("#### Normalized (÷ first set)")
        _render_charts(
            col_norm, melted_norm, norm_df,
            y_label="Fraction of Set 1",
            scatter_title="Normalized — Value vs Step",
            reg_title="Normalized — Fatigue Curves",
            mean_title="Normalized — Mean Fatigue Curve",
            table_key="table_norm",
        )

        # ── Right column: Absolute (current) ─────────────────────────
        with col_raw:
            st.markdown("#### Absolute (raw reps)")
        _render_charts(
            col_raw, melted, raw_df,
            y_label="Repetitions",
            scatter_title="Absolute — Value vs Step",
            reg_title="Absolute — Fatigue Curves",
            mean_title="Absolute — Mean Fatigue Curve",
            table_key="table_raw",
        )

    # 1. Compute mean normalized fatigue coefficients from the data
    all_coeffs = []
    for row_label in melted_norm["Progression"].unique():
        subset = melted_norm[melted_norm["Progression"] == row_label]
        x_pts = subset["Step"].values.astype(float)
        y_pts = subset["Value"].values.astype(float)
        all_coeffs.append(np.polyfit(x_pts, y_pts, 2))
    mean_coeffs = np.mean(all_coeffs, axis=0)

    # 2. Derive per-set values using effort-scaled iterative decay
    #    The experimental curve was built at RPE 10 (all-out). Sub-maximal
    #    sets generate less fatigue, so we scale the decay at each step by
    #    the effort ratio: effort = reps_done / max_reps_possible.
    rir_set1 = 10.0 - fat_rpe
    max_reps_set1 = fat_reps + rir_set1

    sets = np.arange(1, fat_series + 1)

    # Pre-compute the experimental per-step decay ratios from the curve
    exp_vals = np.polyval(mean_coeffs, sets)
    exp_vals = np.clip(exp_vals, 0.01, None)  # safety floor

    # Iterative model: accumulate fatigue proportional to effort
    max_reps_per_set = np.zeros(len(sets))
    max_reps_per_set[0] = max_reps_set1

    for i in range(1, len(sets)):
        # How hard was the previous set? (1.0 = to failure, lower = easier)
        # Squared: the last reps near failure generate disproportionately
        # more fatigue, so stopping short has a bigger dampening effect.
        effort_raw = min(fat_reps / max_reps_per_set[i - 1], 1.0) if max_reps_per_set[i - 1] > 0 else 1.0
        effort = effort_raw ** 2
        # Experimental decay ratio from set i-1 → set i
        exp_decay_rate = exp_vals[i] / exp_vals[i - 1]
        # Scale: less effort → less fatigue → decay closer to 1.0
        adjusted_decay = 1.0 - effort * (1.0 - exp_decay_rate)
        max_reps_per_set[i] = max(max_reps_per_set[i - 1] * adjusted_decay, 0.0)

    eff_rir = max_reps_per_set - fat_reps
    eff_rpe = 10.0 - eff_rir

    # 3. Extrapolation warning
    if fat_series > 5:
        st.warning(
            f"⚠️ The fatigue model is built on **5-set** experimental data. "
            f"Sets 6–{fat_series} are **extrapolated** and may be less accurate."
        )

    # 4. Build dual-axis chart
    fig_drift = make_subplots(specs=[[{"secondary_y": True}]])

    # Color map for RPE bars: green → yellow → red
    def rpe_color(r):
        if r >= 10.0:
            return "rgba(239, 83, 80, 0.95)"   # red — failure
        elif r >= 9.0:
            return "rgba(255, 152, 0, 0.85)"    # orange
        elif r >= 8.0:
            return "rgba(255, 213, 79, 0.80)"   # yellow
        else:
            return "rgba(102, 187, 106, 0.80)"  # green

    bar_colors = [rpe_color(r) for r in eff_rpe]

    # RPE bars (primary Y)
    fig_drift.add_trace(
        go.Bar(
            x=sets, y=eff_rpe,
            name="Effective RPE",
            marker=dict(color=bar_colors, line=dict(width=1, color="rgba(255,255,255,0.3)")),
            text=[f"{r:.1f}" for r in eff_rpe],
            textposition="outside",
            textfont=dict(size=12, color="white"),
        ),
        secondary_y=False,
    )

    # Max reps curve (secondary Y) — interpolate the iterative model points
    x_smooth = np.linspace(1, fat_series, 200)
    max_reps_smooth = np.interp(x_smooth, sets, max_reps_per_set)

    fig_drift.add_trace(
        go.Scatter(
            x=x_smooth, y=max_reps_smooth,
            mode="lines",
            name="Max reps (fatigue curve)",
            line=dict(color="#42a5f5", width=3),
        ),
        secondary_y=True,
    )

    # Prescribed reps threshold line
    fig_drift.add_trace(
        go.Scatter(
            x=[1, fat_series], y=[fat_reps, fat_reps],
            mode="lines",
            name=f"Prescribed reps ({fat_reps})",
            line=dict(color="white", width=2, dash="dash"),
        ),
        secondary_y=True,
    )

    # Failure zone shading
    failure_sets = sets[eff_rir < 0]
    if len(failure_sets) > 0:
        first_fail = int(failure_sets[0])
        fig_drift.add_vrect(
            x0=first_fail - 0.4, x1=fat_series + 0.4,
            fillcolor="rgba(239, 83, 80, 0.12)",
            layer="below", line_width=0,
            annotation_text="FAILURE ZONE",
            annotation_position="top left",
            annotation=dict(font=dict(color="#ef5350", size=12)),
        )

    # Layout
    fig_drift.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
        height=500,
        margin=dict(l=20, r=20, t=40, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        bargap=0.3,
    )
    fig_drift.update_xaxes(title_text="Set", dtick=1)
    fig_drift.update_yaxes(title_text="Effective RPE", range=[5.5, 11], secondary_y=False)
    fig_drift.update_yaxes(title_text="Max Reps Possible", secondary_y=True)

    st.plotly_chart(fig_drift, use_container_width=True)

    # 5. Summary table
    summary_rows = []
    for i, s in enumerate(sets):
        rpe_val = eff_rpe[i]
        rir_val = eff_rir[i]
        mr = max_reps_per_set[i]
        status = "✅" if rir_val >= 0 else "❌ FAILURE"
        summary_rows.append({
            "Set": int(s),
            "Prescribed Reps": fat_reps,
            "Max Reps Possible": f"{mr:.1f}",
            "RIR": f"{rir_val:.1f}" if rir_val >= 0 else "—",
            "Effective RPE": f"{min(rpe_val, 10.0):.1f}" if rir_val >= 0 else "10+",
            "Status": status,
        })
    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

    if len(failure_sets) > 0:
        st.error(
            f"🚨 At this scheme ({fat_series}×{fat_reps} @ RPE {fat_rpe}), "
            f"you're predicted to **fail** starting at **set {int(failure_sets[0])}**. "
            f"Consider reducing reps or starting at a lower RPE."
        )
    else:
        st.success(
            f"✅ Scheme {fat_series}×{fat_reps} @ RPE {fat_rpe} looks sustainable! "
            f"Final set estimated RPE: **{eff_rpe[-1]:.1f}**"
        )

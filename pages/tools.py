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

    for label, col in lift_cols.items():
        st.subheader(label)
        c1, c2 = st.columns(2)
        
        # Prepare data copies and handle NaNs for coloring
        m_plot_df = malesdf[malesdf[col] > 0].copy()
        f_plot_df = femalesdf[femalesdf[col] > 0].copy()
        
        # --- FIX: Custom Weight Normalization to ensure total probability = 1 ---
        # When using 'color' with histnorm='probability', Plotly normalizes per group.
        # To normalize across the *entire* population, we use weights.
        m_plot_df["weight"] = 1.0 / len(m_plot_df) if not m_plot_df.empty else 1.0
        f_plot_df["weight"] = 1.0 / len(f_plot_df) if not f_plot_df.empty else 1.0

        category_orders = {}
        color_seq_m = ["#42a5f5"] 
        color_seq_f = ["#ef5350"]

        if color_col:
            # Handle NaNs
            m_plot_df[color_col] = m_plot_df[color_col].fillna("Unknown")
            f_plot_df[color_col] = f_plot_df[color_col].fillna("Unknown")
            
            # Determine global sorted categories
            all_cats = sorted(list(set(m_plot_df[color_col].unique()) | set(f_plot_df[color_col].unique())))
            
            # Special sorting for Equipment
            if color_col == "Equipment":
                equip_order = ["Raw", "Wraps", "Single-ply", "Multi-ply"]
                all_cats = [e for e in equip_order if e in all_cats] + [e for e in sorted(set(all_cats) - set(equip_order))]
            
            category_orders = {color_col: all_cats}
            
            # Generate chromatic sequence
            n_cats = len(all_cats)
            if n_cats > 1:
                color_seq_m = px.colors.sample_colorscale("Turbo", [i/(n_cats-1) for i in range(n_cats)])
                color_seq_f = color_seq_m
            else:
                color_seq_m = ["#42a5f5"]
                color_seq_f = ["#ef5350"]

        with c1:
            fig_m = px.histogram(
                m_plot_df, x=col,
                y="weight",        
                histfunc="sum",    
                color=color_col,
                title=f"{label} Distribution (Males)",
                template="plotly_dark",
                color_discrete_sequence=color_seq_m,
                category_orders=category_orders,
                barmode="stack" if color_col else "relative"
            )
            fig_m.update_layout(
                height=600,
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="#9a9ab0", title_font_color="#f0f0f5",
                # Increase top margin to give space for title + legend
                margin=dict(l=20, r=20, t=200, b=20),
                # Position legend higher and title lower if needed
                legend=dict(
                    orientation="h", 
                    yanchor="bottom", 
                    y=1.1, # Moved further up from 1.02
                    xanchor="right", 
                    x=1.0
                ) if color_col else None,
                title=dict(
                    y=0.95, # Position title slightly lower relative to top margin
                    x=0.0,
                    xanchor='left'
                )
            )
            fig_m.update_yaxes(title_text="Frequency (Relative)")
            st.plotly_chart(fig_m, use_container_width=True)

        with c2:
            fig_f = px.histogram(
                f_plot_df, x=col,
                y="weight",        
                histfunc="sum",    
                color=color_col,
                title=f"{label} Distribution (Females)",
                template="plotly_dark",
                color_discrete_sequence=color_seq_f,
                category_orders=category_orders,
                barmode="stack" if color_col else "relative"
            )
            fig_f.update_layout(
                height=600,
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="#9a9ab0", title_font_color="#f0f0f5",
                # Increase top margin to give space for title + legend
                margin=dict(l=20, r=20, t=200, b=20),
                legend=dict(
                    orientation="h", 
                    yanchor="bottom", 
                    y=1.1, # Moved further up from 1.02
                    xanchor="right", 
                    x=1.0
                ) if color_col else None,
                title=dict(
                    y=0.95, 
                    x=0.0,
                    xanchor='left'
                )
            )
            fig_f.update_yaxes(title_text="Frequency (Relative)")
            st.plotly_chart(fig_f, use_container_width=True)

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

    # 2. Data Preparation Function
    def get_ath_stats(name):
        if not name: return None
        ath_df = alldf[alldf["Name"] == name].copy()
        
        # PB stats (Best 3 across all historical records)
        best_sq = ath_df["Best3SquatKg"].max()
        best_bn = ath_df["Best3BenchKg"].max()
        best_dl = ath_df["Best3DeadliftKg"].max()
        best_tot = ath_df["TotalKg"].max()
        best_dots = ath_df["Dots"].max()
        
        # Latest Categorical Stats (using their most recent entry)
        latest = ath_df.sort_values("Date", ascending=False).iloc[0]
        wc = latest["WeightClassKg"]
        sex = "Male" if latest["Sex"] == "M" else "Female"
        equip = latest["Equipment"]
        
        return {
            "name": name,
            "sq": best_sq if best_sq > 0 else 0, 
            "bn": best_bn if best_bn > 0 else 0, 
            "dl": best_dl if best_dl > 0 else 0, 
            "tot": best_tot if best_tot > 0 else 0, 
            "dots": best_dots if best_dots > 0 else 0,
            "wc": wc, "sex": sex, "equip": equip
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
    st.subheader("🔍 Patterns and Trends Discoverer")
    st.info("🚧 **Coming soon** — Detailed patterns and trends discoverer.")

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
    
    # Ensure metrics are valid and numeric
    filtered_df = filtered_df.dropna(subset=[metric_x, metric_y])
    filtered_df = filtered_df[(filtered_df[metric_x] > 0) & (filtered_df[metric_y] > 0)]

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
        
        # Superimpose Scatterplot for Freaks
        # We add them as a separate trace
        fig_freak.add_trace(go.Scatter(
            x=freaks_df[metric_x],
            y=freaks_df[metric_y],
            mode='markers',
            name='🔥 Strength Freaks',
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
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0)
        )

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


        


import streamlit as st
from style_utils import inject_custom_css

inject_custom_css()
import pandas as pd
import plotly.express as px
import urllib.parse
import plotly.graph_objects as go

st.header("Athletes")
st.write("Search and explore athlete profiles, competition history, and personal bests.")

st.markdown("---")

# --- Load data from session state ---
if "males_data" not in st.session_state:
    st.session_state["males_data"] = pd.read_csv("datasets/OP_Males.csv", sep=";")
if "females_data" not in st.session_state:
    st.session_state["females_data"] = pd.read_csv("datasets/OP_Females.csv", sep=";")

malesdf = st.session_state["males_data"]
femalesdf = st.session_state["females_data"]

# Combine both datasets for a unified search
alldf = pd.concat([malesdf, femalesdf], ignore_index=True)

def reset():
    st.session_state.athlete_search = ""

# --- Athlete Search ---
at1, at2= st.columns([14,1])
with at1:
    st.subheader("🔍 Athlete Search")
with at2:
    resetbutton = st.button('Reset', on_click=reset)

# Get sorted unique names for the dropdown
all_names = sorted(alldf["Name"].dropna().unique().tolist())

# --- Handle Query Parameters ---
if "name" in st.query_params:
    name_from_url = st.query_params["name"]
    if name_from_url in all_names:
        # Avoid overriding if already set manually in this session (optional choice)
        # But for direct links, we usually want to force it.
        st.session_state["athlete_search"] = name_from_url


selected_name = st.selectbox(
    "Search for an athlete",
    options=[""] + all_names,
    index=0,
    placeholder="Type a name to search...",
    key="athlete_search"
)

if selected_name:
    # Filter all competition entries for this athlete
    athlete_df = alldf[alldf["Name"] == selected_name].copy()
    athlete_df = athlete_df.sort_values("Date", ascending=False)

    # --- Athlete Overview Card ---
    st.markdown("---")
    st.subheader(f"🏋️ {selected_name}")

    # Summary stats
    info_cols = st.columns(4)
    with info_cols[0]:
        st.metric("Competitions", len(athlete_df))
    with info_cols[1]:
        best_total = athlete_df["TotalKg"].max()
        st.metric("Best Total", f"{best_total} kg" if best_total > 0 else "N/A")
    with info_cols[2]:
        best_dots = athlete_df["Dots"].max()
        st.metric("Best Dots", f"{best_dots:.2f}" if best_dots > 0 else "N/A")
    with info_cols[3]:
        sex = athlete_df["Sex"].iloc[0]
        st.metric("Sex", "Male" if sex == "M" else "Female")

    # --- Personal Bests ---
    st.markdown("---")
    st.subheader("🏆 Personal Bests")

    pb_cols = st.columns(3)
    lifts = {
        "Squat": "Best3SquatKg",
        "Bench": "Best3BenchKg",
        "Deadlift": "Best3DeadliftKg",
    }
    for i, (label, col_name) in enumerate(lifts.items()):
        with pb_cols[i]:
            valid = athlete_df[athlete_df[col_name] > 0]
            if valid.empty:
                st.metric(label=label, value="N/A")
            else:
                best_val = valid[col_name].max()
                best_row = valid.loc[valid[col_name].idxmax()]
                st.metric(label=label, value=f"{best_val} kg")
                st.caption(f"📅 {best_row.get('Date', '—')}  •  🏢 {best_row.get('Federation', '—')}")

    # --- Radar Chart & Comparative Metrics ---
    st.markdown("---")
    
    with st.container():
        st.subheader("📊 Relative Strength Dashboard")
        st.write("Compare an athlete's results against the category (same Sex, Weight Class, and Equipment).")

        # Get athlete's category context from their history
        latest_entry = athlete_df.iloc[0]
        athlete_wc = latest_entry["WeightClassKg"]
        athlete_equip = latest_entry["Equipment"]
        athlete_sex_val = latest_entry["Sex"]

        # Reference data for benchmarks
        ref_df = malesdf if athlete_sex_val == "M" else femalesdf
        category_df = ref_df[
            (ref_df["WeightClassKg"] == athlete_wc) & 
            (ref_df["Equipment"] == athlete_equip)
        ].copy()

        if not category_df.empty:
            # Personal Bests for the radar
            val_squat = athlete_df["Best3SquatKg"].max()
            val_bench = athlete_df["Best3BenchKg"].max()
            val_deadlift = athlete_df["Best3DeadliftKg"].max()

            # Category Benchmarks
            avg_squat = category_df["Best3SquatKg"].mean()
            avg_bench = category_df["Best3BenchKg"].mean()
            avg_deadlift = category_df["Best3DeadliftKg"].mean()

            rec_squat = category_df["Best3SquatKg"].max()
            rec_bench = category_df["Best3BenchKg"].max()
            rec_deadlift = category_df["Best3DeadliftKg"].max()

            categories = ['Squat', 'Bench Press', 'Deadlift']

            fig_radar = go.Figure()

            # Add traces in specific order for layering (back to front)
            # 1. Category Record (Background)
            fig_radar.add_trace(go.Scatterpolar(
                r=[rec_squat, rec_bench, rec_deadlift, rec_squat],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor='rgba(255, 213, 79, 0.1)',
                name='Category Record (raw/equipped)',
                line=dict(color='rgba(255, 213, 79, 0.4)', width=2, dash='dot'),
                marker=dict(size=4),
                hovertemplate="Record: %{r} kg<extra></extra>"
            ))
            
            # 2. Category Average (Middle)
            fig_radar.add_trace(go.Scatterpolar(
                r=[avg_squat, avg_bench, avg_deadlift, avg_squat],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor='rgba(66, 165, 245, 0.1)',
                name='Category Average',
                line=dict(color='rgba(66, 165, 245, 0.6)', width=2, dash='dash'),
                marker=dict(size=4),
                hovertemplate="Average: %{r:.1f} kg<extra></extra>"
            ))

            # 3. You (Athlete - Foreground)
            fig_radar.add_trace(go.Scatterpolar(
                r=[val_squat, val_bench, val_deadlift, val_squat],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor='rgba(239, 83, 80, 0.3)',
                name='Athlete',
                line=dict(color='#ef5350', width=4),
                marker=dict(size=10, symbol='diamond'),
                hovertemplate="Athlete: %{r} kg<extra></extra>"
            ))

            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, max(rec_squat, rec_deadlift, rec_bench, val_squat, val_deadlift) * 1.15],
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
            rad_cols = st.columns([2, 1])
            
            with rad_cols[0]:
                st.plotly_chart(fig_radar, use_container_width=True)
            
            with rad_cols[1]:
                # Ensure the table is visible
                st.write("") # Spacer
                comparison_data = {
                    "Lift": categories,
                    "Athlete": [f"{val_squat} kg", f"{val_bench} kg", f"{val_deadlift} kg"],
                    "Average": [f"{round(avg_squat, 1)} kg", f"{round(avg_bench, 1)} kg", f"{round(avg_deadlift, 1)} kg"],
                    "Record": [f"{rec_squat} kg", f"{rec_bench} kg", f"{rec_deadlift} kg"]
                }
                st.dataframe(
                    pd.DataFrame(comparison_data), 
                    hide_index=True, 
                    use_container_width=True,
                    column_config={"Lift": "Lift", "Athlete": "Athlete", "Average": "Average", "Record": "Record"}
                )
                # st.caption(f"Based on **{len(category_df)}** athletes: **{athlete_wc}kg {athlete_equip}**.")
                
                # --- Small Gauges in the sidebar ---
                athlete_best_total = athlete_df["TotalKg"].max()
                cat_totals = category_df[category_df["TotalKg"] > 0]["TotalKg"].sort_values()
                
                if not cat_totals.empty:
                    rank = (cat_totals < athlete_best_total).sum()
                    percentile = (rank / len(cat_totals)) * 100
                    top_percent = 100 - percentile
                    progress_to_record = (athlete_best_total / cat_totals.max()) * 100 if cat_totals.max() > 0 else 0
                    
                    fig_percentile = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=percentile,
                        number={'suffix': "%", 'font': {'size': 25}},
                        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#42a5f5"}, 'bgcolor': "rgba(0,0,0,0)"}
                    ))
                    fig_record = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=progress_to_record,
                        number={'suffix': "%", 'font': {'size': 25}},
                        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#ffd54f"}, 'bgcolor': "rgba(0,0,0,0)"}
                    ))

                    # Adjust height and margins for compact sidebar look
                    for f_g in [fig_percentile, fig_record]:
                        f_g.update_layout(
                            height=125, 
                            margin=dict(l=10, r=10, t=10, b=10), 
                            paper_bgcolor="rgba(0,0,0,0)", 
                            font={'color': "#f0f0f5"}
                        )

                    st.markdown("<br>", unsafe_allow_html=True) # Spacer
                    
                    st.markdown("<div style='text-align: center; font-weight: bold;'>📊 Percentile Standing</div>", unsafe_allow_html=True)
                    st.write("") 
                    st.plotly_chart(fig_percentile, use_container_width=True)

                    st.markdown("<div style='text-align: center; font-weight: bold;'>🏆 Progress to Record</div>", unsafe_allow_html=True)
                    st.write("") 
                    st.plotly_chart(fig_record, use_container_width=True)
                    
                    # Standing Summary
                    if top_percent <= 1: st.success("⭐ Top 1%!")
                    elif top_percent <= 10: st.info(f"💪 Top {int(top_percent)}%!")
                    st.caption(f"Based on **{len(category_df)}** athletes: **{athlete_wc}kg {athlete_equip}**.")
        else:
            st.info("Not enough category data for benchmarks.")
        
                

    st.write("") # Extra spacer to push down next section
    st.write("") 
    
    # --- Progress Chart ---
    st.markdown("---")
    st.subheader("📈 Lifts Over Time")
    st.write("This chart shows all lifts performed by the athlete, including failed attempts (negative values).")

    lift_columns = {
        "Squat 1": "Squat1Kg",
        "Squat 2": "Squat2Kg",
        "Squat 3": "Squat3Kg",
        "Bench 1": "Bench1Kg",
        "Bench 2": "Bench2Kg",
        "Bench 3": "Bench3Kg",
        "Deadlift 1": "Deadlift1Kg",
        "Deadlift 2": "Deadlift2Kg",
        "Deadlift 3": "Deadlift3Kg",
        "Total": "TotalKg",
    }

    # Color families: reds for squat, blues for bench, greens for deadlift, gold for total
    lift_colors = {
        "Squat 1": "#ef5350", "Squat 2": "#e53935", "Squat 3": "#b71c1c",
        "Bench 1": "#42a5f5", "Bench 2": "#1e88e5", "Bench 3": "#0d47a1",
        "Deadlift 1": "#66bb6a", "Deadlift 2": "#43a047", "Deadlift 3": "#1b5e20",
        "Total": "#ffd54f",
    }

    chart_source = athlete_df.copy()
    chart_source["Date"] = pd.to_datetime(chart_source["Date"], errors="coerce")
    chart_source = chart_source.dropna(subset=["Date"]).sort_values("Date")

    if not chart_source.empty:
        fig = go.Figure()
        # --- Identify PRs (Personal Records) ---
        pr_markers = []
        # Main lift columns from the dataframe
        main_lifts = {
            "Squat": "Best3SquatKg",
            "Bench": "Best3BenchKg",
            "Deadlift": "Best3DeadliftKg",
            "Total": "TotalKg"
        }

        for display_name, col in main_lifts.items():
            if col not in chart_source.columns:
                continue
            
            # Cumulative max to identify PR points
            running_max = -1 
            for _, row in chart_source.iterrows():
                val = row[col]
                if val > running_max and val > 0:
                    running_max = val
                    pr_markers.append({
                        "Date": row["Date"],
                        "Value": val,
                        "Type": display_name
                    })
        
        if pr_markers:
            pr_df = pd.DataFrame(pr_markers)
            fig.add_trace(go.Scatter(
                x=pr_df["Date"],
                y=pr_df["Value"],
                mode="markers",
                name="Personal Records",
                marker=dict(
                    symbol="star",
                    size=14,
                    # color="#000000",
                    line=dict(width=1.5, color="white"),
                ),
                hoverlabel=dict(
                    font_color="#000000",
                    bgcolor="rgba(255, 213, 79, 0.9)", # Yellow background
                    bordercolor="#000000"
                ),
                hovertemplate="<b>Personal Record (%{customdata})</b><br>%{y} kg<br>%{x|%Y-%m-%d}<extra></extra>",
                customdata=pr_df["Type"]
            ))

        # --- Plot all individual attempt traces ---
        for label, col in lift_columns.items():
            if col not in chart_source.columns:
                continue
            # Convert to numeric, failed attempts are negative
            series = pd.to_numeric(chart_source[col], errors="coerce")

            fig.add_trace(go.Scatter(
                x=chart_source["Date"],
                y=series,
                mode="lines+markers",
                name=label,
                line=dict(color=lift_colors[label], width=2 if "Total" not in label else 3),
                marker=dict(size=6 if "Total" not in label else 8),
                hovertemplate=f"{label}: %{{y}} kg<br>%{{x|%Y-%m-%d}}<extra></extra>",
                visible=True if label == "Total" else "legendonly",
            ))

        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#9a9ab0",
            title_font_color="#f0f0f5",
            title="All Lifts Over Time (click legend to toggle)",
            yaxis_title="Weight (kg)",
            xaxis_title="Date",
            margin=dict(l=20, r=20, t=50, b=20),
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02,
                font=dict(size=12),
            ),
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Not enough data to show a progress chart.")

    # --- Full Competition History Table ---
    st.markdown("---")
    st.subheader("📋 Competition History")

    display_cols = [
        "Date", "MeetName", "Federation", "Equipment", "AgeClass", "WeightClassKg",
        "BodyweightKg", "Best3SquatKg", "Best3BenchKg", "Best3DeadliftKg",
        "TotalKg", "Dots", "Place"
    ]
    # Only show columns that exist
    display_cols = [c for c in display_cols if c in athlete_df.columns]
    history = athlete_df[display_cols].reset_index(drop=True)
    history.index = history.index + 1
    st.dataframe(history, use_container_width=True)

else:
    st.info("🏋️ Select an athlete from the dropdown above to view their profile and competition history.")

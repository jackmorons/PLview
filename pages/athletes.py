import streamlit as st
import pandas as pd
import plotly.express as px

st.header("Athletes")
st.write("Search and explore athlete profiles, competition history, and personal bests.")

st.markdown("---")

# --- Load data from session state ---
males_data = st.session_state["males_data"]
females_data = st.session_state["females_data"]
malesdf = pd.DataFrame(males_data)
femalesdf = pd.DataFrame(females_data)

# Combine both datasets for a unified search
alldf = pd.concat([malesdf, femalesdf], ignore_index=True)

# --- Athlete Search ---
st.subheader("🔍 Athlete Search")

# Get sorted unique names for the dropdown
all_names = sorted(alldf["Name"].dropna().unique().tolist())

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

    # --- Progress Chart ---
    st.markdown("---")
    st.subheader("📈 Lifts Over Time")

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
        import plotly.graph_objects as go
        fig = go.Figure()

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

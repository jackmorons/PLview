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
    st.subheader("📈 Total Over Time")

    chart_df = athlete_df[athlete_df["TotalKg"] > 0][["Date", "TotalKg", "Equipment", "MeetName"]].copy()
    if not chart_df.empty:
        chart_df["Date"] = pd.to_datetime(chart_df["Date"], errors="coerce")
        chart_df = chart_df.dropna(subset=["Date"]).sort_values("Date")

        fig = px.line(
            chart_df,
            x="Date",
            y="TotalKg",
            markers=True,
            hover_data=["MeetName", "Equipment"],
            title="Competition Total Over Time",
            template="plotly_dark",
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#9a9ab0",
            title_font_color="#f0f0f5",
            margin=dict(l=20, r=20, t=50, b=20),
            yaxis_title="Total (kg)",
            xaxis_title="Date",
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

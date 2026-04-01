import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.header("Records")
st.write("Discover all-time records across weight classes, federations, and events.")

st.markdown("---")

# --- Load data from session state ---
males_data = st.session_state["males_data"]
females_data = st.session_state["females_data"]
malesdf = pd.DataFrame(males_data)
femalesdf = pd.DataFrame(females_data)

# --- Filter Panel ---
st.subheader("🔍 Record Lookup")

filter_cols = st.columns(4)

with filter_cols[0]:
    sex = st.selectbox("Sex", ["Male", "Female"], key="rec_sex")

# IPF age division mapping → AgeClass values
IPF_AGE_DIVISIONS = {
    "Sub-Junior (14-18)": ["13-15", "16-17"],
    "Junior (19-23)":     ["18-19", "20-23"],
    "Open (24-39)":       ["24-34", "35-39"],
    "Masters 1 (40-49)":  ["40-44", "45-49"],
    "Masters 2 (50-59)":  ["50-54", "55-59"],
    "Masters 3 (60-69)":  ["60-64", "65-69"],
    "Masters 4 (70+)":    ["70-74", "75-79", "80-84"],
}

# Pick the right dataframe based on sex selection
df = malesdf if sex == "Male" else femalesdf

with filter_cols[1]:
    ipf_division = st.selectbox("Age Division", list(IPF_AGE_DIVISIONS.keys()), key="rec_age")
    selected_age_classes = IPF_AGE_DIVISIONS[ipf_division]

with filter_cols[2]:
    weight_classes = sorted(df["WeightClassKg"].dropna().unique().tolist())
    weight_class = st.selectbox("Weight Class (kg)", weight_classes, key="rec_wc")

with filter_cols[3]:
    equipment_options = sorted(df["Equipment"].dropna().unique().tolist())
    equipment = st.selectbox("Equipment", equipment_options, key="rec_equip")

# --- Apply filters ---
filtered = df[
    (df["AgeClass"] == age_class) &
    (df["WeightClassKg"] == weight_class) &
    (df["Equipment"] == equipment)
].copy()

st.markdown("---")

if filtered.empty:
    st.warning("No records found for the selected combination.")
else:
    # Find top records for each lift
    lifts = {
        "🏋️ Squat": "Best3SquatKg",
        "💪 Bench Press": "Best3BenchKg",
        "🔥 Deadlift": "Best3DeadliftKg",
    }

    record_cols = st.columns(3)

    for i, (label, col_name) in enumerate(lifts.items()):
        with record_cols[i]:
            valid = filtered[filtered[col_name] > 0]
            if valid.empty:
                st.metric(label=label, value="N/A")
                st.caption("No valid attempts")
            else:
                idx = valid[col_name].idxmax()
                record_row = valid.loc[idx]
                record_val = record_row[col_name]
                athlete_name = record_row["Name"]
                date = record_row.get("Date", "—")
                federation = record_row.get("Federation", "—")
                bodyweight = record_row.get("BodyweightKg", "—")

                st.metric(label=label, value=f"{record_val} kg")
                st.caption(f"**{athlete_name}**")
                st.caption(f"📅 {date}  •  🏢 {federation}")
                st.caption(f"⚖️ BW: {bodyweight} kg")

    # --- Total record ---
    st.markdown("---")
    valid_total = filtered[filtered["TotalKg"] > 0]
    if not valid_total.empty:
        idx_total = valid_total["TotalKg"].idxmax()
        total_row = valid_total.loc[idx_total]
        st.metric(label="🏆 Total", value=f"{total_row['TotalKg']} kg")
        st.caption(
            f"**{total_row['Name']}**  •  "
            f"S: {total_row['Best3SquatKg']} / B: {total_row['Best3BenchKg']} / D: {total_row['Best3DeadliftKg']}  •  "
            f"📅 {total_row.get('Date', '—')}  •  🏢 {total_row.get('Federation', '—')}"
        )

    # --- Top 5 table for context ---
    st.markdown("---")
    st.subheader("📊 Top 5 Totals")
    top5 = (
        filtered[filtered["TotalKg"] > 0]
        .nlargest(5, "TotalKg")[["Name", "Best3SquatKg", "Best3BenchKg", "Best3DeadliftKg", "TotalKg", "Dots", "Date", "Federation"]]
        .reset_index(drop=True)
    )
    top5.index = top5.index + 1  # 1-indexed ranking
    st.dataframe(top5, use_container_width=True)

import streamlit as st
from style_utils import inject_custom_css

inject_custom_css()
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import urllib.parse

st.header("Records")
st.write("Discover all-time records across weight classes, federations, and events.")

st.markdown("---")

# --- Load data from session state ---
if "males_data" not in st.session_state:
    st.session_state["males_data"] = pd.read_csv("datasets/OP_Males.csv", sep=";")
if "females_data" not in st.session_state:
    st.session_state["females_data"] = pd.read_csv("datasets/OP_Females.csv", sep=";")

malesdf = st.session_state["males_data"]
femalesdf = st.session_state["females_data"]

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
    (df["AgeClass"].isin(selected_age_classes)) &
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

                athlete_url = f"/athletes?name={urllib.parse.quote(athlete_name)}"
                st.metric(label=label, value=f"{record_val} kg")
                st.caption(f"[**{athlete_name}**]({athlete_url})")
                st.caption(f"📅 {date}  •  🏢 {federation}")
                st.caption(f"⚖️ BW: {bodyweight} kg")

    # --- Total record ---
    st.markdown("---")
    valid_total = filtered[filtered["TotalKg"] > 0]
    if not valid_total.empty:
        idx_total = valid_total["TotalKg"].idxmax()
        total_row = valid_total.loc[idx_total]
        total_athlete_url = f"/athletes?name={urllib.parse.quote(total_row['Name'])}"
        st.metric(label="🏆 Total", value=f"{total_row['TotalKg']} kg")
        st.caption(
            f"[**{total_row['Name']}**]({total_athlete_url})  •  "
            f"S: {total_row['Best3SquatKg']} / B: {total_row['Best3BenchKg']} / D: {total_row['Best3DeadliftKg']}  •  "
            f"📅 {total_row.get('Date', '—')}  •  🏢 {total_row.get('Federation', '—')}"
        )

    # --- Top 5 table for context ---
    st.markdown("---")
    st.subheader("📊 Top 5 Totals")
    top5 = (
        filtered[filtered["TotalKg"] > 0]
        .sort_values("TotalKg", ascending=False)
        .drop_duplicates(subset="Name")
        .head(5)[["Name", "Best3SquatKg", "Best3BenchKg", "Best3DeadliftKg", "TotalKg", "Dots", "Date", "Federation"]]
        .reset_index(drop=True)
    )
    top5.index = top5.index + 1  # 1-indexed ranking
    
    # Construct Athlete URLs for the table
    # We use a trick: display the name but the link is to the profile
    # LinkColumn will display the cell value unless display_text is set.
    # To keep it clean, we'll construct the full URL.
    top5["Profile"] = top5["Name"].apply(lambda x: f"/athletes?name={urllib.parse.quote(x)}")
    
    # Reorder to put Profile first or replace Name
    cols = ["Profile"] + [c for c in top5.columns if c not in ["Name", "Profile"]]
    top5_display = top5[cols].copy()
    
    st.dataframe(
        top5_display,
        column_config={
            "Profile": st.column_config.LinkColumn(
                "Athlete Name",
                help="Click to view athlete profile",
                validate=r"^/athletes\?name=.*",
                display_text=r"/athletes\?name=(.*)" # Shows the decoded name parts if simple, but might show %20
            )
        },
        use_container_width=True
    )


r1, r2, r3 = st.columns(3)

with r2:
    st.markdown("---")
    st.subheader("📊 Top 5 Benches")
    top5 = (
        filtered[filtered["Best3BenchKg"] > 0]
        .sort_values("Best3BenchKg", ascending=False)
        .drop_duplicates(subset="Name")
        .head(5)[["Name", "Best3BenchKg", "Dots", "Date"]]
        .reset_index(drop=True)
    )
    top5.index = top5.index + 1  # 1-indexed ranking
    
    # Construct Athlete URLs for the table
    # We use a trick: display the name but the link is to the profile
    # LinkColumn will display the cell value unless display_text is set.
    # To keep it clean, we'll construct the full URL.
    top5["Profile"] = top5["Name"].apply(lambda x: f"/athletes?name={urllib.parse.quote(x)}")
    
    # Reorder to put Profile first or replace Name
    cols = ["Profile"] + [c for c in top5.columns if c not in ["Name", "Profile"]]
    top5_display = top5[cols].copy()
    
    st.dataframe(
        top5_display,
        column_config={
            "Profile": st.column_config.LinkColumn(
                "Athlete Name",
                help="Click to view athlete profile",
                validate=r"^/athletes\?name=.*",
                display_text=r"/athletes\?name=(.*)" # Shows the decoded name parts if simple, but might show %20
            )
        },
        use_container_width=True
    )
with r1:
    st.markdown("---")
    st.subheader("📊 Top 5 Squat")
    top5 = (
        filtered[filtered["Best3SquatKg"] > 0]
        .sort_values("Best3SquatKg", ascending=False)
        .drop_duplicates(subset="Name")
        .head(5)[["Name", "Best3SquatKg", "Dots", "Date"]]
        .reset_index(drop=True)
    )
    top5.index = top5.index + 1  # 1-indexed ranking
    
    # Construct Athlete URLs for the table
    # We use a trick: display the name but the link is to the profile
    # LinkColumn will display the cell value unless display_text is set.
    # To keep it clean, we'll construct the full URL.
    top5["Profile"] = top5["Name"].apply(lambda x: f"/athletes?name={urllib.parse.quote(x)}")
    
    # Reorder to put Profile first or replace Name
    cols = ["Profile"] + [c for c in top5.columns if c not in ["Name", "Profile"]]
    top5_display = top5[cols].copy()
    
    st.dataframe(
        top5_display,
        column_config={
            "Profile": st.column_config.LinkColumn(
                "Athlete Name",
                help="Click to view athlete profile",
                validate=r"^/athletes\?name=.*",
                display_text=r"/athletes\?name=(.*)" # Shows the decoded name parts if simple, but might show %20
            )
        },
        use_container_width=True
    )
with r3:
    st.markdown("---")
    st.subheader("📊 Top 5 Deadlifts")
    top5 = (
        filtered[filtered["Best3DeadliftKg"] > 0]
        .sort_values("Best3DeadliftKg", ascending=False)
        .drop_duplicates(subset="Name")
        .head(5)[["Name", "Best3DeadliftKg", "Dots", "Date"]]
        .reset_index(drop=True)
    )
    top5.index = top5.index + 1  # 1-indexed ranking
    
    # Construct Athlete URLs for the table
    # We use a trick: display the name but the link is to the profile
    # LinkColumn will display the cell value unless display_text is set.
    # To keep it clean, we'll construct the full URL.
    top5["Profile"] = top5["Name"].apply(lambda x: f"/athletes?name={urllib.parse.quote(x)}")
    
    # Reorder to put Profile first or replace Name
    cols = ["Profile"] + [c for c in top5.columns if c not in ["Name", "Profile"]]
    top5_display = top5[cols].copy()
    
    st.dataframe(
        top5_display,
        column_config={
            "Profile": st.column_config.LinkColumn(
                "Athlete Name",
                help="Click to view athlete profile",
                validate=r"^/athletes\?name=.*",
                display_text=r"/athletes\?name=(.*)" # Shows the decoded name parts if simple, but might show %20
            )
        },
        use_container_width=True
    )
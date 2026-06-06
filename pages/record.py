import streamlit as st
from style_utils import inject_custom_css, format_decimal

inject_custom_css()
import pandas as pd
import numpy as np
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


# ── Spiral helpers ────────────────────────────────────────────────────

def build_record_spiral(df, col):
    """
    Build a month-by-month running record series for a given lift column.
    Returns a DataFrame with x, y, z coordinates for a 3D spiral, or None
    if there is insufficient data.

    Layout:
      z     = year + (month-1)/12   (vertical time axis)
      angle = (month-1)/12 * 2π     (radial position within the year)
      r     = running record value  (distance from the z-axis)
      x, y  = r * cos(angle), r * sin(angle)
    """
    valid = df[df[col] > 0][["Date", col]].copy()
    valid["Date"] = pd.to_datetime(valid["Date"], errors="coerce")
    valid = valid.dropna(subset=["Date"])

    if len(valid) < 3:
        return None

    # Take the best performance recorded in each calendar month
    valid["YM"] = valid["Date"].dt.to_period("M")
    monthly = (
        valid.groupby("YM")[col]
        .max()
        .reset_index()
        .sort_values("YM")
    )

    # Build a complete, gap-free monthly range
    all_months = pd.period_range(monthly["YM"].min(), monthly["YM"].max(), freq="M")
    full = pd.DataFrame({"YM": all_months}).merge(monthly, on="YM", how="left")

    # Forward-fill: carry the record forward until it is broken
    full[col] = full[col].ffill()
    full = full.dropna(subset=[col])

    # Convert to 3D spiral coordinates
    full["year"]  = full["YM"].dt.year
    full["month"] = full["YM"].dt.month
    full["angle"] = (full["month"] - 1) / 12 * 2 * np.pi
    full["z"]     = full["year"] + (full["month"] - 1) / 12
    full["x"]     = full[col] * np.cos(full["angle"])
    full["y"]     = full[col] * np.sin(full["angle"])
    full["label"] = full["YM"].astype(str)

    return full


def plot_spiral(spiral_df, col, accent_color, title):
    """
    Render a 3D line spiral where:
      - height   = time (year)
      - angle    = month within the year
      - radius   = running record value (kg)

    The line is coloured from dark (oldest) to accent_color (most recent).
    """
    fig = go.Figure(data=[go.Scatter3d(
        x=spiral_df["x"],
        y=spiral_df["y"],
        z=spiral_df["z"],
        mode="lines",
        line=dict(
            color=spiral_df["z"],
            colorscale=[[0, "rgba(25, 25, 40, 0.9)"], [1, accent_color]],
            width=5,
        ),
        customdata=np.stack([spiral_df["label"], spiral_df[col].round(1)], axis=-1),
        hovertemplate="<b>%{customdata[0]}</b><br>Record: %{customdata[1]} kg<extra></extra>",
    )])

    z_min = float(spiral_df["z"].min())
    z_max = float(spiral_df["z"].max())

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        height=550,
        margin=dict(l=0, r=0, t=50, b=0),
        title=dict(text=title, x=0.5, xanchor="center", font=dict(color="#f0f0f5", size=14)),
        scene=dict(
            bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                showticklabels=False, showgrid=False,
                zeroline=False, title="", showspikes=False,
            ),
            yaxis=dict(
                showticklabels=False, showgrid=False,
                zeroline=False, title="", showspikes=False,
            ),
            zaxis=dict(
                title=dict(text="Year", font=dict(color="#9a9ab0")),
                range=[z_min, z_max],
                gridcolor="rgba(255,255,255,0.08)",
                tickfont=dict(color="#9a9ab0", size=11),
            ),
            aspectmode="manual",
            aspectratio=dict(x=1, y=1, z=0.7),
        ),
    )
    return fig


# --- Filter Panel ---
st.subheader("🔍 Record Lookup")

filter_cols = st.columns(4)

with filter_cols[0]:
    sex = st.selectbox("Sex", ["Male", "Female"], key="rec_sex", format_func=format_decimal)

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
    ipf_division = st.selectbox("Age Division", list(IPF_AGE_DIVISIONS.keys()), key="rec_age", format_func=format_decimal)
    selected_age_classes = IPF_AGE_DIVISIONS[ipf_division]

with filter_cols[2]:
    all_wc = sorted(df["WeightClassKg"].dropna().unique().tolist())
    weight_class = st.selectbox("Weight Class (kg)", all_wc, key="rec_wc", format_func=lambda x: format_decimal(x) + " kg")

with filter_cols[3]:
    equipment_options = sorted(df["Equipment"].dropna().unique().tolist())
    equipment = st.selectbox("Equipment", equipment_options, key="rec_equip", format_func=format_decimal)

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
                st.metric(label=label, value=f"{format_decimal(record_val)} kg")
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
        st.metric(label="🏆 Total", value=f"{format_decimal(total_row['TotalKg'])} kg")
        st.caption(
            f"[**{total_row['Name']}**]({total_athlete_url})  •  "
            f"S: {format_decimal(total_row['Best3SquatKg'])} / B: {format_decimal(total_row['Best3BenchKg'])} / D: {format_decimal(total_row['Best3DeadliftKg'])}  •  "
            f"📅 {total_row.get('Date', '—')}  •  🏢 {total_row.get('Federation', '—')}"
        )

    # --- Top 5 Totals table ---
    st.markdown("---")
    st.subheader("📊 Top 5 Totals")
    top5 = (
        filtered[filtered["TotalKg"] > 0]
        .sort_values("TotalKg", ascending=False)
        .drop_duplicates(subset="Name")
        .head(5)[["Name", "Best3SquatKg", "Best3BenchKg", "Best3DeadliftKg", "TotalKg", "Dots", "Date", "Federation"]]
        .reset_index(drop=True)
    )
    top5.index = top5.index + 1
    top5["Profile"] = top5["Name"].apply(lambda x: f"/athletes?name={urllib.parse.quote(x)}")
    cols = ["Profile"] + [c for c in top5.columns if c not in ["Name", "Profile"]]
    top5_display = top5[cols].copy()

    st.dataframe(
        top5_display,
        column_config={
            "Profile": st.column_config.LinkColumn(
                "Athlete Name",
                help="Click to view athlete profile",
                validate=r"^/athletes\?name=.*",
                display_text=r"/athletes\?name=(.*)"
            )
        },
        use_container_width=True
    )

    # --- Total record spiral ---
    total_spiral = build_record_spiral(filtered, "TotalKg")
    if total_spiral is not None:
        st.plotly_chart(
            plot_spiral(total_spiral, "TotalKg", "#ffd54f", "🏆 Total Record — History Spiral"),
            use_container_width=True
        )
    else:
        st.caption("Not enough historical data to build the spiral for this category.")


# --- Per-lift columns ---
r1, r2, r3 = st.columns(3)

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
    top5.index = top5.index + 1
    top5["Profile"] = top5["Name"].apply(lambda x: f"/athletes?name={urllib.parse.quote(x)}")
    cols = ["Profile"] + [c for c in top5.columns if c not in ["Name", "Profile"]]
    top5_display = top5[cols].copy()
    st.dataframe(
        top5_display,
        column_config={
            "Profile": st.column_config.LinkColumn(
                "Athlete Name",
                help="Click to view athlete profile",
                validate=r"^/athletes\?name=.*",
                display_text=r"/athletes\?name=(.*)"
            )
        },
        use_container_width=True
    )
    if not filtered.empty:
        squat_spiral = build_record_spiral(filtered, "Best3SquatKg")
        if squat_spiral is not None:
            st.plotly_chart(
                plot_spiral(squat_spiral, "Best3SquatKg", "#ef5350", "🏋️ Squat Record — History Spiral"),
                use_container_width=True
            )
        else:
            st.caption("Not enough historical data to build the spiral.")

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
    top5.index = top5.index + 1
    top5["Profile"] = top5["Name"].apply(lambda x: f"/athletes?name={urllib.parse.quote(x)}")
    cols = ["Profile"] + [c for c in top5.columns if c not in ["Name", "Profile"]]
    top5_display = top5[cols].copy()
    st.dataframe(
        top5_display,
        column_config={
            "Profile": st.column_config.LinkColumn(
                "Athlete Name",
                help="Click to view athlete profile",
                validate=r"^/athletes\?name=.*",
                display_text=r"/athletes\?name=(.*)"
            )
        },
        use_container_width=True
    )
    if not filtered.empty:
        bench_spiral = build_record_spiral(filtered, "Best3BenchKg")
        if bench_spiral is not None:
            st.plotly_chart(
                plot_spiral(bench_spiral, "Best3BenchKg", "#42a5f5", "💪 Bench Record — History Spiral"),
                use_container_width=True
            )
        else:
            st.caption("Not enough historical data to build the spiral.")

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
    top5.index = top5.index + 1
    top5["Profile"] = top5["Name"].apply(lambda x: f"/athletes?name={urllib.parse.quote(x)}")
    cols = ["Profile"] + [c for c in top5.columns if c not in ["Name", "Profile"]]
    top5_display = top5[cols].copy()
    st.dataframe(
        top5_display,
        column_config={
            "Profile": st.column_config.LinkColumn(
                "Athlete Name",
                help="Click to view athlete profile",
                validate=r"^/athletes\?name=.*",
                display_text=r"/athletes\?name=(.*)"
            )
        },
        use_container_width=True
    )
    if not filtered.empty:
        deadlift_spiral = build_record_spiral(filtered, "Best3DeadliftKg")
        if deadlift_spiral is not None:
            st.plotly_chart(
                plot_spiral(deadlift_spiral, "Best3DeadliftKg", "#66bb6a", "🔥 Deadlift Record — History Spiral"),
                use_container_width=True
            )
        else:
            st.caption("Not enough historical data to build the spiral.")

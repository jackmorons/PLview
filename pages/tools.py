import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Tools - PLview", page_icon="⚙️", layout="wide")

st.header("Tools")
st.write("Tools for data analysis and visualization built for coaches and athletes.")

st.markdown("---")

# read data stored at beginning
males_data = st.session_state["males_data"]
females_data = st.session_state["females_data"]
malesdf = pd.DataFrame(males_data)
femalesdf = pd.DataFrame(females_data)

# ── Sub-page definitions ──────────────────────────────────────────────
TOOLS_PAGES = [
    {"key": "lift_distributions", "label": "📊 Lift Distributions"},
    {"key": "aaaa", "label": "aaaa"},
    {"key": "bbbb", "label": "bbbb"},
    {"key": "cccc", "label": "cccc"},
    {"key": "strength_index_calculator", "label": "🧮 Strength Index Calculator"},
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

# ---------- 1. Lift Distributions (original content) ----------
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
            )
            fig_m.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="#9a9ab0", title_font_color="#f0f0f5",
                margin=dict(l=20, r=20, t=50, b=20),
            )
            st.plotly_chart(fig_m, use_container_width=True)
        with c2:
            fig_f = px.histogram(
                femalesdf[femalesdf[col] > 0], x=col,
                title=f"{label} Distribution (Females)",
                template="plotly_dark",
                color_discrete_sequence=["#ef5350"],
            )
            fig_f.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font_color="#9a9ab0", title_font_color="#f0f0f5",
                margin=dict(l=20, r=20, t=50, b=20),
            )
            st.plotly_chart(fig_f, use_container_width=True)

# ---------- 2. Weight Class Analysis (placeholder) ----------
elif active == "weight_class_analysis":
    st.subheader("⚖️ Weight Class Analysis")
    st.info("🚧 **Coming soon** — Breakdowns and comparisons across weight classes.")

# ---------- 3. Performance Trends (placeholder) ----------
elif active == "performance_trends":
    st.subheader("📈 Performance Trends")
    st.info("🚧 **Coming soon** — Historical trend lines and progression tracking.")

# ---------- 4. Wilks Calculator (placeholder) ----------
elif active == "wilks_calculator":
    st.subheader("🧮 Wilks Calculator")
    st.info("🚧 **Coming soon** — Compute and compare Wilks / DOTS scores.")

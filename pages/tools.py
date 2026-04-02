import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

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
    {"key": "lift_distributions", "label": "📊 Lift Distributions"},
    {"key": "1v1", "label": "⚔️ 1v1 Strength Comparison"},
    {"key": "weight_class", "label": "⚖️ Weight Class Evaluator"},
    {"key": "trend_calculator", "label": "📈 Trend Calculator"},
    {"key": "pattern_discoverer", "label": "🔍 Pattern Discoverer"},
    #{"key": "relative_lifts", "label": "💪 Relative Lifts"},
    {"key": "freak_finder", "label": "🤯 Strength Freaks Finder"},
    {"key": "geo_strength", "label": "🌍 Geographical Strength"},
    {"key": "twin_finder", "label": "🫂 Find Your PL Twin!"},
    {"key": "strength_index_calculator", "label": "🧮 Strength Index"},
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

# ---------- 2. Placeholder aaaa ----------
elif active == "aaaa":
    st.subheader("🔵 Section A")
    st.info("🚧 **Placeholder content** for the second tool.")

# ---------- 3. Placeholder bbbb ----------
elif active == "bbbb":
    st.subheader("🟡 Section B")
    st.info("🚧 **Placeholder content** for the third tool.")

# ---------- 4. Placeholder cccc ----------
elif active == "cccc":
    st.subheader("🟢 Section C")
    st.info("🚧 **Placeholder content** for the fourth tool.")

# ---------- 5. Strength Index Calculator ----------
elif active == "strength_index_calculator":
    st.subheader("🧮 Strength Index Calculator")
    st.info("🚧 **Coming soon** — Detailed strength index and DOTS/Wilks comparisons.")

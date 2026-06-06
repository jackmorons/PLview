import streamlit as st
import plotly.express as px

# ── Shared chart colour constants ─────────────────────────────────────
LIFT_COLORS = {
    "Squat":     "#ef5350",
    "Bench":     "#42a5f5",
    "Deadlift":  "#66bb6a",
}
LIFT_ALPHA = {
    "Squat":     "rgba(239,83,80,0.15)",
    "Bench":     "rgba(66,165,245,0.15)",
    "Deadlift":  "rgba(102,187,106,0.15)",
}

# Shared colorscale for record spirals: white → green → yellow → blue → red
SPIRAL_COLORSCALE = [
    [0.00, "#e0e0e0"],
    [0.25, "#66bb6a"],
    [0.50, "#ffd54f"],
    [0.75, "#42a5f5"],
    [1.00, "#ef5350"],
]

# Density heatmap colorscale (log-stretched Viridis)
_viridis_base = px.colors.sequential.Viridis
DENSITY_COLORSCALE = [
    [(i / (len(_viridis_base) - 1)) ** 3, c]
    for i, c in enumerate(_viridis_base)
]

# Shared Plotly layout defaults — spread with **PLOTLY_LAYOUT_BASE
PLOTLY_LAYOUT_BASE = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#f0f0f5", family="'Barlow Condensed', sans-serif"),
)

# Axis style — spread with **PLOTLY_AXIS_STYLE inside xaxis= / yaxis= dicts
PLOTLY_AXIS_STYLE = dict(
    gridcolor="rgba(255,255,255,0.05)",
    zerolinecolor="rgba(239,83,80,0.35)",
    zerolinewidth=1,
)

# ── CSS injection ─────────────────────────────────────────────────────

def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&display=swap');

        /* Hide the default Streamlit sidebar and header */
        [data-testid="collapsedControl"] { display: none; }
        section[data-testid="stSidebar"] { display: none; }
        header { visibility: hidden; display: none; }
        [data-testid="stHeader"] { display: none; }

        /* ── Background: cooler blue-black radial gradient + dot-grid texture ── */
        .stApp {
            background:
                radial-gradient(circle, rgba(255,255,255,0.03) 1px, transparent 1px),
                radial-gradient(circle at 50% 100%, #131824 0%, #0c1018 45%, #080a0f 100%);
            background-size: 24px 24px, 100% 100%;
            background-attachment: fixed, fixed;
        }

        /* ── Typography ── */
        h1, h2, h3,
        .hero-title, .hero-title2, .nav-logo {
            font-family: 'Barlow Condensed', sans-serif !important;
        }

        /* Tabular monospace numbers for metric values */
        [data-testid="stMetricValue"] {
            font-family: var(--font-mono) !important;
            font-variant-numeric: tabular-nums !important;
            letter-spacing: 0.02em;
        }

        /* ── Custom horizontal rule ── */
        hr {
            border: 0;
            height: 1px;
            background-image: linear-gradient(to right, rgba(255,255,255,0), rgba(255,255,255,0.12), rgba(255,255,255,0));
            margin-top: 2rem !important;
            margin-bottom: 2rem !important;
        }

        /* ── Main content padding ── */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 5rem !important;
        }

        /* ── Disk accent bar — thicker ── */
        .disk-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 6px;
            z-index: 999999;
            background: linear-gradient(
                90deg,
                #d32f2f 0%,   #d32f2f 15%,
                #1976d2 25%,  #1976d2 35%,
                #f9a825 45%,  #f9a825 55%,
                #388e3c 65%,  #388e3c 75%,
                #e0e0e0 85%,  #e0e0e0 100%
            );
        }
        .disk-bar2 {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 6px;
            z-index: 999999;
            background: linear-gradient(
                90deg,
                #d32f2f 0%,   #d32f2f 15%,
                #1976d2 25%,  #1976d2 35%,
                #f9a825 45%,  #f9a825 55%,
                #388e3c 65%,  #388e3c 75%,
                #e0e0e0 85%,  #e0e0e0 100%
            );
        }

        /* ── Logo ── */
        .nav-logo {
            font-size: 1.8rem;
            font-weight: 800;
            color: #f0f0f5;
            letter-spacing: 0.02em;
            margin-top: -5px;
        }
        .nav-logo span.red   { color: #d32f2f; }
        .nav-logo span.blue  { color: #1976d2; }
        .nav-logo span.gold  { color: #f9a825; }
        .nav-logo span.green { color: #388e3c; }
        .nav-logo span.white { color: #e0e0e0; }

        /* ── Hero text ── */
        .hero-title {
            font-size: clamp(5rem, 8vw, 5.0rem) !important;
            font-weight: 800 !important;
            letter-spacing: 0.02em;
            line-height: 1.1;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #f0f0f5 30%, #d32f2f 65%, #1976d2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
        }
        .hero-title2 {
            font-size: clamp(5rem, 8vw, 5.0rem) !important;
            font-weight: 800 !important;
            letter-spacing: 0.02em;
            line-height: 1.1;
            margin-bottom: 1rem;
            text-align: center;
            color: #f0f0f5;
        }
        .hero-title2 span.red   { color: #d32f2f; }
        .hero-title2 span.blue  { color: #1976d2; }
        .hero-title2 span.gold  { color: #f9a825; }
        .hero-title2 span.green { color: #388e3c; }
        .hero-title2 span.white { color: #e0e0e0; }

        .hero-subtitle {
            font-size: 1.25rem;
            color: #9a9ab0;
            text-align: center;
            margin-bottom: 2rem;
        }

        /* ── Sharp corners: buttons, expanders, inputs, selects ── */
        button,
        [data-testid="stExpander"],
        [data-testid="stExpander"] > div:first-child,
        input,
        select,
        textarea,
        .stSelectbox > div > div,
        .stMultiSelect > div > div,
        .stNumberInput > div > div,
        .stTextInput > div > div {
            border-radius: 2px !important;
        }

        /* ── Button hover: solid fill ── */
        button:hover {
            filter: brightness(1.15);
        }

        /* ── Mobile responsiveness ── */
        @media (max-width: 640px) {
            .hero-title, .hero-title2 {
                font-size: 4rem !important;
                line-height: 1.2 !important;
                width: 100% !important;
            }
            .block-container {
                padding-left: 0.5rem !important;
                padding-right: 0.5rem !important;
                max-width: 100% !important;
            }
        }

        /* ── Fixed footer ── */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            text-align: center;
            padding: .8rem;
            background: rgba(8, 10, 15, 0.88);
            backdrop-filter: blur(8px);
            color: #5e5e73;
            font-size: 0.85rem;
            border-top: 1px solid rgba(255,255,255,0.05);
            z-index: 999998;
        }

        /* ── Nav link colours (sharp corners) ── */
        div[data-testid="stColumn"] a[data-testid="stPageLink-NavLink"] {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }

        /* Home (RED) */
        div[data-testid="stColumn"]:nth-of-type(2) a[data-testid="stPageLink-NavLink"] {
            background-color: rgba(211,47,47,0.1);
            border: 1px solid #d32f2f;
            border-radius: 2px;
            transition: all 0.15s ease;
        }
        div[data-testid="stColumn"]:nth-of-type(2) a[data-testid="stPageLink-NavLink"] p {
            color: #e57373 !important; font-weight: 600;
            font-family: 'Barlow Condensed', sans-serif;
            letter-spacing: 0.05em;
        }
        div[data-testid="stColumn"]:nth-of-type(2) a[data-testid="stPageLink-NavLink"]:hover {
            background-color: #d32f2f; transform: translateY(-2px);
        }
        div[data-testid="stColumn"]:nth-of-type(2) a[data-testid="stPageLink-NavLink"]:hover p {
            color: #ffffff !important;
        }

        /* Athletes (BLUE) */
        div[data-testid="stColumn"]:nth-of-type(3) a[data-testid="stPageLink-NavLink"] {
            background-color: rgba(25,118,210,0.1);
            border: 1px solid #1976d2;
            border-radius: 2px;
            transition: all 0.15s ease;
        }
        div[data-testid="stColumn"]:nth-of-type(3) a[data-testid="stPageLink-NavLink"] p {
            color: #64b5f6 !important; font-weight: 600;
            font-family: 'Barlow Condensed', sans-serif;
            letter-spacing: 0.05em;
        }
        div[data-testid="stColumn"]:nth-of-type(3) a[data-testid="stPageLink-NavLink"]:hover {
            background-color: #1976d2; transform: translateY(-2px);
        }
        div[data-testid="stColumn"]:nth-of-type(3) a[data-testid="stPageLink-NavLink"]:hover p {
            color: #ffffff !important;
        }

        /* Records (GOLD) */
        div[data-testid="stColumn"]:nth-of-type(4) a[data-testid="stPageLink-NavLink"] {
            background-color: rgba(249,168,37,0.1);
            border: 1px solid #f9a825;
            border-radius: 2px;
            transition: all 0.15s ease;
        }
        div[data-testid="stColumn"]:nth-of-type(4) a[data-testid="stPageLink-NavLink"] p {
            color: #ffd54f !important; font-weight: 600;
            font-family: 'Barlow Condensed', sans-serif;
            letter-spacing: 0.05em;
        }
        div[data-testid="stColumn"]:nth-of-type(4) a[data-testid="stPageLink-NavLink"]:hover {
            background-color: #f9a825; transform: translateY(-2px);
        }
        div[data-testid="stColumn"]:nth-of-type(4) a[data-testid="stPageLink-NavLink"]:hover p {
            color: #ffffff !important;
        }

        /* Raw Data (GREEN) */
        div[data-testid="stColumn"]:nth-of-type(5) a[data-testid="stPageLink-NavLink"] {
            background-color: rgba(56,142,60,0.1);
            border: 1px solid #388e3c;
            border-radius: 2px;
            transition: all 0.15s ease;
        }
        div[data-testid="stColumn"]:nth-of-type(5) a[data-testid="stPageLink-NavLink"] p {
            color: #81c784 !important; font-weight: 600;
            font-family: 'Barlow Condensed', sans-serif;
            letter-spacing: 0.05em;
        }
        div[data-testid="stColumn"]:nth-of-type(5) a[data-testid="stPageLink-NavLink"]:hover {
            background-color: #388e3c; transform: translateY(-2px);
        }
        div[data-testid="stColumn"]:nth-of-type(5) a[data-testid="stPageLink-NavLink"]:hover p {
            color: #ffffff !important;
        }

        /* Info (WHITE) */
        div[data-testid="stColumn"]:nth-of-type(6) a[data-testid="stPageLink-NavLink"] {
            background-color: rgba(150,150,150,0.1);
            border: 1px solid #9e9e9e;
            border-radius: 2px;
            transition: all 0.15s ease;
        }
        div[data-testid="stColumn"]:nth-of-type(6) a[data-testid="stPageLink-NavLink"] p {
            color: #e0e0e0 !important; font-weight: 600;
            font-family: 'Barlow Condensed', sans-serif;
            letter-spacing: 0.05em;
        }
        div[data-testid="stColumn"]:nth-of-type(6) a[data-testid="stPageLink-NavLink"]:hover {
            background-color: #757575; transform: translateY(-2px);
        }
        div[data-testid="stColumn"]:nth-of-type(6) a[data-testid="stPageLink-NavLink"]:hover p {
            color: #ffffff !important;
        }
        </style>

        <div class="disk-bar"></div>
        <div class="disk-bar2"></div>
        <div class="footer">PLview &copy; 2026. Data sourced from OpenPowerlifting.</div>
    """, unsafe_allow_html=True)


def format_decimal(x):
    """Ensures dots are used as decimal separators in strings."""
    return str(x).replace(',', '.')

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

lift_cols = {
    "🏋️ Squat": "Best3SquatKg",
    "💪 Bench": "Best3BenchKg",
    "🔥 Deadlift": "Best3DeadliftKg",
    "🏆 Total": "TotalKg",
}

for label, col in lift_cols.items():
    st.subheader(label)
    col1, col2 = st.columns(2)
    with col1:
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
    with col2:
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


# # --- Sample Data Generation ---
# # 1. Performance Over Time (Line Chart)
# np.random.seed(42)
# dates = pd.date_range(start="2024-01-01", periods=20, freq="W")
# performance_df = pd.DataFrame({
#     "Date": dates,
#     "Squat": np.linspace(150, 180, 20) + np.random.normal(0, 2, 20),
#     "Bench": np.linspace(100, 115, 20) + np.random.normal(0, 1.5, 20),
#     "Deadlift": np.linspace(180, 210, 20) + np.random.normal(0, 3, 20)
# })
# performance_df_melted = performance_df.melt(id_vars=["Date"], var_name="Exercise", value_name="Weight (kg)")

# # 2. Volume Distribution (Bar Chart)
# volume_df = pd.DataFrame({
#     "Muscle Group": ["Legs", "Chest", "Back", "Shoulders", "Arms"],
#     "Sets": [15, 12, 14, 8, 10]
# })

# # 3. Strength vs. Speed (Scatter Plot)
# scatter_df = pd.DataFrame({
#     "Relative Strength (% 1RM)": np.random.uniform(70, 100, 50),
#     "Velocity (m/s)": 1.2 - (np.random.uniform(70, 100, 50) / 100) + np.random.normal(0, 0.05, 50)
# })

# # --- Plotly Charts ---

# st.subheader("📈 Athlete Performance Progress")
# fig_line = px.line(
#     performance_df_melted, 
#     x="Date", 
#     y="Weight (kg)", 
#     color="Exercise",
#     title="Top Lift Progress (Mockup)",
#     template="plotly_dark",
#     color_discrete_sequence=px.colors.qualitative.Prism
# )
# fig_line.update_layout(
#     plot_bgcolor="rgba(0,0,0,0)",
#     paper_bgcolor="rgba(0,0,0,0)",
#     font_color="#9a9ab0",
#     title_font_color="#f0f0f5",
#     legend_title_font_color="#f0f0f5",
#     margin=dict(l=20, r=20, t=50, b=20)
# )
# st.plotly_chart(fig_line, use_container_width=True)

# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("📊 Training Volume")
#     fig_bar = px.bar(
#         volume_df, 
#         x="Muscle Group", 
#         y="Sets", 
#         title="Weekly Sets by Group",
#         template="plotly_dark",
#         color="Sets",
#         color_continuous_scale="Viridis"
#     )
    
#     fig_bar.update_traces(
#         unselected=dict(marker=dict(opacity=0.3))
#     )
#     fig_bar.update_layout(
#         clickmode="event+select",
#         plot_bgcolor="rgba(0,0,0,0)",
#         paper_bgcolor="rgba(0,0,0,0)",
#         font_color="#9a9ab0",
#         title_font_color="#f0f0f5",
#         margin=dict(l=20, r=20, t=50, b=20)
#     )
    
#     event = st.plotly_chart(
#         fig_bar, 
#         use_container_width=True, 
#         on_select="rerun",
#         selection_mode="points",
#         key="bar_select"
#     )
    
#     selected_muscles = []
#     if event and "selection" in event and event["selection"]["points"]:
#         selected_muscles = [pt["x"] for pt in event["selection"]["points"]]
        
#     if selected_muscles:
#         st.write("📊 Filtered Data:")
#         st.dataframe(volume_df[volume_df["Muscle Group"].isin(selected_muscles)], hide_index=True, use_container_width=True)
#     else:
#         st.write("📊 All Data:")
#         st.dataframe(volume_df, hide_index=True, use_container_width=True)

# with col2:
#     st.subheader("🎯 Strength-Velocity Profile")
#     fig_scatter = px.scatter(
#         scatter_df, 
#         x="Relative Strength (% 1RM)", 
#         y="Velocity (m/s)",
#         title="Load-Velocity Correlation",
#         template="plotly_dark",
#         color="Velocity (m/s)",
#         color_continuous_scale="RdYlGn"
#     )
#     fig_scatter.update_layout(
#         plot_bgcolor="rgba(0,0,0,0)",
#         paper_bgcolor="rgba(0,0,0,0)",
#         font_color="#9a9ab0",
#         title_font_color="#f0f0f5",
#         margin=dict(l=20, r=20, t=50, b=20)
#     )
#     st.plotly_chart(fig_scatter, use_container_width=True)

st.info("⚙️ **More tools coming soon**")

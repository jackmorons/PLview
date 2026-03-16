import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.header("Tools")
st.write("Tools for data analysis and visualization built for coaches and athletes.")

st.markdown("---")

st.info("⚙️ **Coming Soon**\n\n Tools will be added here.")

# --- Empty Plot Setup ---
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_title("Placeholder Plot")
ax.set_xlabel("X-Axis")
ax.set_ylabel("Y-Axis")

# This will just show the empty axes setup
st.pyplot(fig)


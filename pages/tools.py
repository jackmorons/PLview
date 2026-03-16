import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.header("Tools")
st.write("Tools for data analysis and visualization built for coaches and athletes.")

st.markdown("---")

st.info("⚙️ **Coming Soon**\n\n Tools will be added here.")

# --- Slick Dark Mode Plot Setup ---
fig, ax = plt.subplots(figsize=(10, 5), dpi=600)

# Transparent backgrounds to blend perfectly with Streamlit
fig.patch.set_facecolor('none')
ax.set_facecolor('none')

# Style text and labels with colors from the custom CSS
ax.set_title("Graph title (Placeholder)", color='#f0f0f5', pad=15, fontweight='800', fontsize=14)
ax.set_xlabel("X-axis (Placeholder)", color='#9a9ab0', fontsize=11, fontweight='600')
ax.set_ylabel("Y-axis (Placeholder)", color='#9a9ab0', fontsize=11, fontweight='600')

# Clean, slick grid and refined spines
ax.grid(True, linestyle='-', alpha=0.08, color='#ffffff')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#333340')
ax.spines['left'].set_color('#333340')
ax.tick_params(colors='#333340', labelcolor='#9a9ab0', width=1.5)

# Setting limits so the empty plot still shows a good grid area
ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.5)

st.pyplot(fig)


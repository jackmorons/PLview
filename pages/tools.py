import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.header("Tools")
st.write("Tools for data analysis and visualization built for coaches and athletes.")

st.markdown("---")

st.info("⚙️ **Coming Soon**\n\n Tools will be added here.")

# --- Slick Dark Mode Plot Setup ---
fig, ax = plt.subplots(figsize=(8, 4))

# Transparent backgrounds to blend perfectly with Streamlit
fig.patch.set_facecolor('none')
ax.set_facecolor('none')

# Add some dummy data for a "slick" look
x = np.linspace(0, 10, 100)
y = np.sin(x) + np.random.normal(0, 0.1, 100)
y_smooth = np.sin(x)

# Plot a glowing-style line with filled area
ax.plot(x, y_smooth, color='#64b5f6', linewidth=2.5, label='Progress Trend')
ax.scatter(x, y, color='#1976d2', alpha=0.5, s=15, label='Recorded Outputs')
ax.fill_between(x, y_smooth, color='#64b5f6', alpha=0.1)

# Style text and labels with colors from the custom CSS
ax.set_title("Athlete Performance Analytics (Placeholder)", color='#f0f0f5', pad=15, fontweight='800', fontsize=14)
ax.set_xlabel("Time (Months)", color='#9a9ab0', fontsize=11, fontweight='600')
ax.set_ylabel("Relative Volume", color='#9a9ab0', fontsize=11, fontweight='600')

# Clean, slick grid and refined spines
ax.grid(True, linestyle='-', alpha=0.08, color='#ffffff')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#333340')
ax.spines['left'].set_color('#333340')
ax.tick_params(colors='#333340', labelcolor='#9a9ab0', width=1.5)

# Minimalist legend
ax.legend(frameon=False, labelcolor='#f0f0f5', loc='upper right')

st.pyplot(fig)


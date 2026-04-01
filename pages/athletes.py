import streamlit as st

st.header("Athletes")
st.write("Search and explore athlete profiles, competition history, and personal bests.")

st.markdown("---")

# read data stored at beginning
males_data = st.session_state["males_data"]
females_data = st.session_state["females_data"]
malesdf = pd.DataFrame(males_data)
femalesdf = pd.DataFrame(females_data)

st.info("🏋️ **Coming Soon**\n\nAthlete data and search functionality will be added here.")

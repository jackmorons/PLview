import streamlit as st

st.header("Records")
st.write("Discover all-time records across weight classes, federations, and events.")

st.markdown("---")

# read data stored at beginning
males_data = st.session_state["males_data"]
females_data = st.session_state["females_data"]
malesdf = pd.DataFrame(males_data)
femalesdf = pd.DataFrame(females_data)

st.info("🏆 **Coming Soon**\n\nRecord tables and filtering will be added here.")

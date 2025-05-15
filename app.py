import streamlit as st
from modules import transitions

st.set_page_config(page_title="🧠 Transition Generator")
st.sidebar.title("🛠️ Modules")
option = st.sidebar.radio("Choose a feature", ["Transition Generator"])

if option == "Transition Generator":
    transitions.render()

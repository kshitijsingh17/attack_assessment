# app.py (Main Streamlit entry point)
import streamlit as st
from pages.api_key_entry import run as api_key_entry_run
from pages.model_evaluation import run as model_evaluation_run
from pages.live_agent import run as live_agent_run


# Use session state to navigate
if 'page' not in st.session_state:
    st.session_state.page = 'API Key Entry'

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["API Key Entry", "Model Evaluation", "Live Agent"])
st.session_state.page = page

# Page Routing
if page == "API Key Entry":
    api_key_entry_run()
elif page == "Model Evaluation":
    model_evaluation_run()
elif page == "Live Agent":
    live_agent_run()

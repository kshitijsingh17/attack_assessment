import streamlit as st

def run():
    st.title("🔐 Enter Gemini API Key")
    api_key = st.text_input("Enter your Gemini API Key", type="password")
    if api_key:
        st.session_state.api_key = api_key
        st.success("API Key stored in session.")
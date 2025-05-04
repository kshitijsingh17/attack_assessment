import streamlit as st
from utils.gemini_utils import classify_incident

def run():
    st.title("🤖 Live Incident Classifier")
    if 'api_key' not in st.session_state:
        st.warning("Please enter your API key on the 'API Key Entry' page.")
        return

    model_choice = st.selectbox("Choose Gemini Model", ["gemini-1.5-flash", "gemini-2.0-flash"])
    user_input = st.text_area("Enter incident description")

    if st.button("Classify") and user_input:
        preds = classify_incident(user_input, model_choice, st.session_state.api_key)
        st.success("Predicted Categories:")
        st.write(preds)
import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.gemini_utils import classify_batch
from utils.metrics import compute_metrics, generate_class_breakdown
import tempfile
import os

def run():
    st.title("📊 Model Evaluation")
    if 'api_key' not in st.session_state:
        st.warning("Please enter your API key on the 'API Key Entry' page.")
        return

    uploaded_file = st.file_uploader("Upload dataset (JSON with 'incident_text' and 'category flow')", type="json")
    model_choice = st.selectbox("Choose Gemini Model", ["gemini-1.5-flash", "gemini-2.0-flash"])

    if uploaded_file and model_choice:
        data = json.load(uploaded_file)
        results = classify_batch(data, model_choice, st.session_state.api_key)

        # Save results
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        json.dump(results, open(tmp_file.name, "w"), indent=2)
        st.download_button("📥 Download Results JSON", data=open(tmp_file.name).read(), file_name="results.json")

        # Metrics summary
        metrics = compute_metrics(results)
        st.subheader("Evaluation Metrics")
        st.dataframe(pd.DataFrame([metrics]))

        # Per-class visualization
        breakdown = generate_class_breakdown(results)
        df_breakdown = pd.DataFrame(breakdown)
        st.subheader("Per-Class Breakdown")
        st.dataframe(df_breakdown)

        st.subheader("Class Performance Visualization")
        melted = df_breakdown.melt(id_vars="class", var_name="metric", value_name="count")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=melted, x="class", y="count", hue="metric", ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

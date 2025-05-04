
#  Attack Incident Classification App

A Streamlit web app for classifying attack incident reports using Gemini 1.5 or 2.0, designed for security analysts and ML researchers.

##  Features

-  API key input for Gemini models
-  Upload labeled datasets (`.json`/`.csv`)
-  Evaluate predictions vs ground truth (correct, missed, extra)
-  Visualize category performance
-  Test custom incident descriptions live
-  Export results as CSV and PNG

##  App Pages

### 1. API Config
Enter your Gemini API key to enable model access.

### 2. Upload Data
Upload and validate incident classification datasets.

### 3. Evaluation
Run evaluation to compare predictions with true labels. Outputs include:
- Category-wise missed, extra, and correct counts
- Downloadable CSV summary
- Bar chart visualization

### 4. Live Test
Input custom incident text and get real-time category predictions.

##  Design Highlights

- Clean layout with status feedback
- Error handling for API issues and invalid model output
- Session state management for continuity
- Progress bars and alerts for user actions

## 🏁 Run the App

```bash
pip install -r requirements.txt
streamlit run app.py

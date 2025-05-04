#  Gemini-Based Attack Category Classification

This project evaluates Google Gemini models (`gemini-1.5-flash` and `gemini-2.0-flash`) on the task of categorizing incidents into predefined attack categories using multi-label classification.

---

##  Project Structure

- `automated_agent.py`  
  Classifies incidents using Gemini APIs and evaluates prediction accuracy.

- `metrics.py`  
  Calculates precision, recall, F1-score, and Hamming Loss using sklearn.

- `graph.py`  
  Generates per-category summary of missed, extra, and correct predictions. Outputs CSV + bar chart.

---

##  Attack Categories

Each incident is classified using the following codes:

| Code | Category                                |
|------|-----------------------------------------|
| AAT  | Emerging & Advanced Technology Attacks  |
| BPA  | Biological & Pandemic Attacks           |
| DCA  | Digital & Cyber Attacks                 |
| EFA  | Economic & Financial Attacks            |
| NDA  | Natural Disaster Attacks                |
| OIA  | Operational & Industrial Attacks        |
| PSI  | Physical Security & Infrastructure      |
| SPI  | Socio-Political & Influence Attacks     |

---

##  Features

- Supports two Gemini model versions (`1.5-flash` and `2.0-flash`)
- Auto-matches model predictions with true labels
- Calculates:
  - Micro & Macro Precision, Recall, F1
  - Hamming Loss
- Saves results to JSON and CSV
- Generates a bar chart of prediction quality per class

---

##  Sample Evaluation Output

**gemini-2.0-flash**:
- Micro F1 Score: `0.843`
- Macro F1 Score: `0.846`
- Hamming Loss: `0.077`

**gemini-1.5-flash**:
- Micro F1 Score: `0.726`
- Macro F1 Score: `0.718`
- Hamming Loss: `0.13`

**Conclusion**:  
Gemini-2.0 outperforms Gemini-1.5 across all metrics. For instance, incidents involving multi-category flows like ["DCA", "EFA", "SPI"] were more accurately captured by Gemini-2.0.

---

##  Metric Relevance

| Metric         | Description |
|----------------|-------------|
| Micro F1 Score | Measures label-wise accuracy accounting for imbalance |
| Macro F1 Score | Equal weight to each class — good for underrepresented categories |
| Hamming Loss   | Penalizes incorrect labels — lower is better |

>  Limitations: These metrics do not capture semantic proximity of classes (e.g., PSI vs SPI), and are sensitive to slight phrasing differences.

---

##  Visualization

Each class is visualized with:
- Correct Predictions 
- Missed Labels 
- Over-predicted (extra) Labels 

Bar charts are saved as PNGs for easy comparison between models.

---

##  Setup Instructions

1. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt

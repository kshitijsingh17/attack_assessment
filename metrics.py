import json
from sklearn.metrics import precision_recall_fscore_support, hamming_loss

# === Label set from category definitions ===
LABEL_SET = {
    "AAT",  # Emerging & Advanced Technology Attacks
    "BPA",  # Biological & Pandemic Attacks
    "DCA",  # Digital & Cyber Attacks
    "EFA",  # Economic & Financial Attacks
    "NDA",  # Natural Disaster Attacks
    "OIA",  # Operational & Industrial Attacks
    "PSI",  # Physical Security & Infrastructure Attacks
    "SPI",  # Socio-Political & Influence Attacks
}

# === Load data ===
DATA_PATH = "gemini_eval_results_gemini-1.5-flash.json"
with open(DATA_PATH, "r") as f:
    data = json.load(f)

# === Binarize true/predicted labels using the fixed label set ===
label_list = sorted(LABEL_SET)

def binarize_labels(labels, classes):
    return [1 if cls in labels else 0 for cls in classes]

y_true = [binarize_labels(entry["true_labels"], label_list) for entry in data]
y_pred = [binarize_labels(entry["predicted_labels"], label_list) for entry in data]

# === Compute metrics ===
metrics = {}

precision_micro, recall_micro, f1_micro, _ = precision_recall_fscore_support(
    y_true, y_pred, average='micro', zero_division=0)
precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
    y_true, y_pred, average='macro', zero_division=0)
hamming = hamming_loss(y_true, y_pred)

metrics["Micro Precision"] = round(precision_micro, 3)
metrics["Micro Recall"] = round(recall_micro, 3)
metrics["Micro F1 Score"] = round(f1_micro, 3)
metrics["Macro Precision"] = round(precision_macro, 3)
metrics["Macro Recall"] = round(recall_macro, 3)
metrics["Macro F1 Score"] = round(f1_macro, 3)
metrics["Hamming Loss"] = round(hamming, 3)

# === Print summary ===
print(" Multi-Label Classification Evaluation Metrics\n")
for k, v in metrics.items():
    print(f"{k}: {v}")

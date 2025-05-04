from sklearn.metrics import precision_score, recall_score, f1_score, hamming_loss
import numpy as np
from collections import defaultdict

ALL_CLASSES = ["AAT", "BPA", "DCA", "EFA", "NDA", "OIA", "PSI", "SPI"]

def compute_metrics(results):
    y_true, y_pred = [], []
    for r in results:
        true, pred = r["true_labels"], r["predicted_labels"]
        y_true.append([cls in true for cls in ALL_CLASSES])
        y_pred.append([cls in pred for cls in ALL_CLASSES])
    return {
        "Micro Precision": round(precision_score(y_true, y_pred, average="micro"), 3),
        "Micro Recall": round(recall_score(y_true, y_pred, average="micro"), 3),
        "Micro F1 Score": round(f1_score(y_true, y_pred, average="micro"), 3),
        "Macro Precision": round(precision_score(y_true, y_pred, average="macro"), 3),
        "Macro Recall": round(recall_score(y_true, y_pred, average="macro"), 3),
        "Macro F1 Score": round(f1_score(y_true, y_pred, average="macro"), 3),
        "Hamming Loss": round(hamming_loss(y_true, y_pred), 3)
    }

def generate_class_breakdown(results):
    stats = defaultdict(lambda: {"correct": 0, "missed": 0, "extra": 0})
    for r in results:
        for c in r["true_labels"]:
            if c in r["predicted_labels"]:
                stats[c]["correct"] += 1
            else:
                stats[c]["missed"] += 1
        for c in r["predicted_labels"]:
            if c not in r["true_labels"]:
                stats[c]["extra"] += 1
    return [{"class": k, **v} for k, v in stats.items()]
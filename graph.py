import json
import csv
import matplotlib.pyplot as plt

# === Configuration ===
INPUT_JSON = "gemini_eval_results_gemini-1.5-flash.json"
CSV_OUTPUT = "missed_extra_correct_summary_1.5.csv"
PNG_OUTPUT = "missed_extra_correct_bar_chart_1.5.png"

LABEL_SET = {
    "AAT", "BPA", "DCA", "EFA", "NDA", "OIA", "PSI", "SPI"
}
LABELS = sorted(LABEL_SET)

# === Load Data ===
with open(INPUT_JSON, "r") as f:
    data = json.load(f)

# === Initialize Counts ===
missed_counts = {label: 0 for label in LABELS}
extra_counts = {label: 0 for label in LABELS}
correct_counts = {label: 0 for label in LABELS}

# === Compute Counts ===
for entry in data:
    true_labels = set(entry.get("true_labels", []))
    pred_labels = set(entry.get("predicted_labels", []))

    for label in true_labels - pred_labels:
        if label in missed_counts:
            missed_counts[label] += 1
    for label in pred_labels - true_labels:
        if label in extra_counts:
            extra_counts[label] += 1
    for label in true_labels & pred_labels:
        if label in correct_counts:
            correct_counts[label] += 1

# === Save to CSV ===
with open(CSV_OUTPUT, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Category", "Correct", "Missed", "Extra"])
    for label in LABELS:
        writer.writerow([
            label,
            correct_counts[label],
            missed_counts[label],
            extra_counts[label]
        ])

# === Plot and Save Chart ===
x = range(len(LABELS))
width = 0.25
correct_vals = [correct_counts[label] for label in LABELS]
missed_vals = [missed_counts[label] for label in LABELS]
extra_vals = [extra_counts[label] for label in LABELS]

plt.figure(figsize=(12, 6))
plt.bar(x, correct_vals, width=width, label="Correct", color="mediumseagreen")
plt.bar([i + width for i in x], missed_vals, width=width, label="Missed", color="tomato")
plt.bar([i + 2 * width for i in x], extra_vals, width=width, label="Extra", color="skyblue")

plt.xlabel("Category")
plt.ylabel("Count")
plt.title("Correct, Missed, and Extra Predictions by Category")
plt.xticks([i + width for i in x], LABELS)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(PNG_OUTPUT)

print(f"✅ Saved CSV: {CSV_OUTPUT}")
print(f"✅ Saved Chart: {PNG_OUTPUT}")

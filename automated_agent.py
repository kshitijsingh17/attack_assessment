import google.generativeai as genai
import json
import os
import time
from ast import literal_eval

# === Ask user for model version ===
print(" Choose Gemini model version:")
print("1 - gemini-1.5-flash")
print("2 - gemini-2.0-flash")
choice = input("Enter choice (1 or 2): ").strip()

if choice == "2":
    MODEL_VERSION = "gemini-2.0-flash"
else:
    MODEL_VERSION = "gemini-1.5-flash"

# === Load API key ===
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# === File with dataset ===
DATA_PATH = "gemini_outputs_cleaned.json"

# === Prompt with category codes ===
CATEGORY_DEFINITIONS = """
Category Definitions (Use only these abbreviations in output):

1. AAT = Emerging & Advanced Technology Attacks
        Attacks operating through cutting-edge technologies not yet fully
        incorporated into standard security frameworks.

2. BPA = Biological & Pandemic Attacks
        Attacks operating through biological agents or pathogens, whether
        naturally occurring or intentionally deployed.

3. DCA = Digital & Cyber Attacks
        Attacks operating through digital channels, targeting IT networks,
        systems, software, or data.

4. EFA = Economic & Financial Attacks
        Attacks operating through financial mechanisms, markets, or monetary
        instruments.

5. NDA = Natural Disaster Attacks
        Attacks operating through natural environmental forces beyond human
        control.

6. OIA = Operational & Industrial Attacks
        Attacks operating through operational technology (OT) and industrial
        control systems (ICS) that manage critical physical processes.

7. PSI = Physical Security & Infrastructure Attacks
        Attacks operating through physical security measures or tangible
        infrastructure through direct physical means.

8. SPI = Socio-Political & Influence Attacks
        Attacks operating through human perception, beliefs, and social
        dynamics via information manipulation or influence operations.
"""

SYSTEM_PROMPT = f"""
You are a security classification agent. Given an incident description, analyze it and return all applicable categories using only the codes (e.g., AAT, BPA). Respond with a comma seperated line like "DCA", "SPI" only—no explanation.

{CATEGORY_DEFINITIONS}
"""

# === Classification function ===
def classify_incident(text: str, model_version: str) -> list:
    try:
        model = genai.GenerativeModel(
            model_name=model_version,
            system_instruction=SYSTEM_PROMPT
        )

        prompt = f"""
Incident Description:
{text}

Return the applicable attack category codes only, in this format:
["DCA", "OIA"]
"""

        convo = model.start_chat()
        convo.send_message(prompt)
        response = convo.last.text.strip()
        print(response)
        prediction = [category.strip() for category in response.split(",")]
        print(prediction)
        if isinstance(prediction, list):
            return prediction
        else:
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

# === Load dataset ===
with open(DATA_PATH, "r") as f:
    dataset = json.load(f)

# === Process and evaluate ===
correct = 0
results = []

for i, entry in enumerate(dataset, 1):
    print(f" [{i}/{len(dataset)}] Classifying with {MODEL_VERSION}...")

    incident = entry["incident_text"]
    true_labels = set(entry.get("category flow", []))
    pred_labels = set(classify_incident(incident, MODEL_VERSION))

    match = pred_labels == true_labels
    if match:
        correct += 1
    print(correct)

    results.append({
        "incident_text": incident,
        "true_labels": list(true_labels),
        "predicted_labels": list(pred_labels),
        "match": match,
        "missed": list(true_labels - pred_labels),
        "extra": list(pred_labels - true_labels)
    })

    time.sleep(5)  # Respect Gemini API rate limits

# === Accuracy summary ===
accuracy = round((correct / len(dataset)) * 100, 2)
print(f"\nDONE: Accuracy = {accuracy}% ({correct}/{len(dataset)} correct)")

# === Save output ===
output_file = f"gemini_eval_results_{MODEL_VERSION}.json"
with open(output_file, "w") as f:
    json.dump(results, f, indent=2)

print(f"Results saved to {output_file}")


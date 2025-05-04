import google.generativeai as genai
from ast import literal_eval
import time

SYSTEM_PROMPT = """
You are a security classification agent. Given an incident description, analyze it and return all applicable categories using only the codes (e.g., AAT, BPA). Respond with a comma separated values like "DCA", "SPI" only—no explanation.

Category Definitions:
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

def classify_incident(text, model_version, api_key):
    genai.configure(api_key=api_key)
    try:
        model = genai.GenerativeModel(
            model_name=model_version,
            system_instruction=SYSTEM_PROMPT
        )
        prompt = f"""
Incident Description:
{text}

Return only category codes in format:
"DCA", "OIA"
"""
        convo = model.start_chat()
        convo.send_message(prompt)
        response = convo.last.text.strip()
        print(response)
        
        prediction = [category.strip() for category in response.split(",")]
        VALID_LABELS = {"FSI", "AAT", "SPI", "DCA", "ETA", "OIA", "BPA", "NDA"}
        print(prediction)
        if not [label for label in prediction if label in VALID_LABELS]:
            return []
        if isinstance(prediction, list):
            return prediction
        else:
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def classify_batch(data, model_version, api_key):
    results = []
    for entry in data:
        incident = entry["incident_text"]
        true_labels = set(entry.get("category flow", []))
        pred_labels = set(classify_incident(incident, model_version, api_key))
        results.append({
            "incident_text": incident,
            "true_labels": list(true_labels),
            "predicted_labels": list(pred_labels),
            "match": pred_labels == true_labels,
            "missed": list(true_labels - pred_labels),
            "extra": list(pred_labels - true_labels)
        })
        time.sleep(5)  # Respect rate limits
    return results
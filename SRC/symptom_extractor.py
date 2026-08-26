import os
import re
import difflib
import pandas as pd

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "DATA")

# Base common symptoms
COMMON_SYMPTOMS = [
    "fever", "headache", "cough", "fatigue", "itching", "skin rash",
    "stomach pain", "dizziness", "nausea", "joint pain", "chest pain",
    "loss of taste", "loss of smell", "breathlessness", "sore throat",
    "vomiting", "chills", "sweating", "back pain", "neck pain",
    "acidity", "indigestion", "muscle pain", "stiff neck", "swelling joints"
]

def load_all_known_symptoms():
    """Dynamically aggregate unique symptoms from CSV dataset if available."""
    symptoms_set = set(s.lower() for s in COMMON_SYMPTOMS)
    
    csv_clean = os.path.join(DATA_DIR, "symptoms_disease_cleaned.csv")
    csv_raw = os.path.join(DATA_DIR, "symptoms_disease.csv")
    csv_path = csv_clean if os.path.exists(csv_clean) else csv_raw
    
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            symptom_cols = [c for c in df.columns if c.lower() != 'disease']
            for col in symptom_cols:
                for val in df[col].dropna():
                    clean_val = str(val).strip().replace("_", " ").lower()
                    if clean_val and clean_val != 'nan':
                        for sub in clean_val.split(","):
                            s = sub.strip()
                            if s:
                                symptoms_set.add(s)
        except Exception as e:
            print(f"[WARN] Error reading symptoms dataset: {e}")
            
    sorted_symptoms = sorted(list(symptoms_set), key=len, reverse=True)
    return sorted_symptoms

KNOWN_SYMPTOMS = load_all_known_symptoms()

def extract_symptoms(text):
    """
    Extract matching symptoms from input natural language text.
    Supports exact matching and fuzzy typo/misspelling matching.
    """
    if not text:
        return []
        
    text_clean = str(text).lower()
    text_clean = re.sub(r'[^a-z0-9\s]', ' ', text_clean)
    words = text_clean.split()
    text_padded = " " + " ".join(words) + " "
    
    extracted = []
    
    # 1. Exact phrase / keyword matching
    for symptom in KNOWN_SYMPTOMS:
        pattern = r'\b' + re.escape(symptom) + r'\b'
        if re.search(pattern, text_padded):
            if symptom not in extracted:
                extracted.append(symptom)

    # 2. Fuzzy matching for misspelled single-word symptoms
    if not extracted and words:
        single_word_symptoms = [s for s in KNOWN_SYMPTOMS if " " not in s and len(s) >= 4]
        for w in words:
            if len(w) >= 3:
                matches = difflib.get_close_matches(w, single_word_symptoms, n=1, cutoff=0.75)
                if matches and matches[0] not in extracted:
                    extracted.append(matches[0])
                    
    return extracted

if __name__ == "__main__":
    print("Testing extract_symptoms with typos...")
    print("Input: 'fevr and coug'", extract_symptoms("fevr and coug"))

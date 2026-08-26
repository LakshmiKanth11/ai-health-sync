import pandas as pd
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "DATA")

def preprocess_symptoms_data():
    raw_csv_path = os.path.join(DATA_DIR, "symptoms_disease.csv")
    cleaned_csv_path = os.path.join(DATA_DIR, "symptoms_disease_cleaned.csv")
    
    print(f"Loading raw symptoms dataset from: {raw_csv_path}")
    df = pd.read_csv(raw_csv_path)
    print(f"Initial shape: {df.shape}")
    
    # 1. Handle missing / empty rows
    df = df.dropna(how="all")
    
    # 2. Lowercase all string columns
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.lower().str.strip()
    
    # 3. Fill remaining missing values with empty string
    df = df.fillna("")
    
    # 4. Remove duplicate rows
    initial_count = len(df)
    df = df.drop_duplicates()
    final_count = len(df)
    print(f"Removed {initial_count - final_count} duplicate rows.")
    print(f"Cleaned shape: {df.shape}")
    
    # Save clean dataset
    df.to_csv(cleaned_csv_path, index=False)
    print(f"Saved cleaned dataset to: {cleaned_csv_path}\n")
    return df

def verify_all_datasets():
    print("--- Verifying Dataset Load Integrity ---")
    
    # 1. Verify symptoms_disease.csv
    symptoms_path = os.path.join(DATA_DIR, "symptoms_disease.csv")
    df_symptoms = pd.read_csv(symptoms_path)
    print(f"[SUCCESS] symptoms_disease.csv loaded. Rows: {len(df_symptoms)}, Cols: {len(df_symptoms.columns)}")
    
    # 2. Verify symptoms_disease_cleaned.csv
    symptoms_clean_path = os.path.join(DATA_DIR, "symptoms_disease_cleaned.csv")
    df_symptoms_clean = pd.read_csv(symptoms_clean_path)
    print(f"[SUCCESS] symptoms_disease_cleaned.csv loaded. Rows: {len(df_symptoms_clean)}, Cols: {len(df_symptoms_clean.columns)}")
    
    # 3. Verify doctors_db.csv
    doctors_path = os.path.join(DATA_DIR, "doctors_db.csv")
    df_doctors = pd.read_csv(doctors_path)
    print(f"[SUCCESS] doctors_db.csv loaded. Rows: {len(df_doctors)}, Cols: {list(df_doctors.columns)}")
    
    # 4. Verify intents.json
    intents_path = os.path.join(DATA_DIR, "intents.json")
    with open(intents_path, "r", encoding="utf-8") as f:
        intents_data = json.load(f)
    intent_tags = [i['tag'] for i in intents_data.get('intents', [])]
    print(f"[SUCCESS] intents.json loaded. Intent tags: {intent_tags}")
    
    print("\nAll datasets verified successfully!")

if __name__ == "__main__":
    preprocess_symptoms_data()
    verify_all_datasets()

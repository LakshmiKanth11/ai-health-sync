import os
import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "DATA")
MODELS_DIR = os.path.join(BASE_DIR, "MODELS")
os.makedirs(MODELS_DIR, exist_ok=True)

def train_model():
    clean_csv = os.path.join(DATA_DIR, "symptoms_disease_cleaned.csv")
    raw_csv = os.path.join(DATA_DIR, "symptoms_disease.csv")
    
    csv_path = clean_csv if os.path.exists(clean_csv) else raw_csv
    print(f"Loading dataset from: {csv_path}")
    df = pd.read_csv(csv_path)
    
    # 3.1 Combine symptom columns into a single symptom_text column
    symptom_cols = [c for c in df.columns if c.lower() != 'disease']
    print(f"Found symptom columns: {symptom_cols}")
    
    def combine_symptoms(row):
        tokens = []
        for col in symptom_cols:
            val = str(row[col]).strip().replace("_", " ").lower()
            if val and val != 'nan':
                items = [item.strip() for item in val.split(",") if item.strip()]
                tokens.extend(items)
        unique_tokens = list(dict.fromkeys(tokens))
        return " ".join(unique_tokens)

    df['symptom_text'] = df.apply(combine_symptoms, axis=1)
    
    # Clean Disease column
    df['Disease'] = df['Disease'].astype(str).str.strip()
    
    # 3.2 Initialize CountVectorizer and transform symptom text to features (X)
    print("Vectorizing symptom_text using CountVectorizer...")
    vectorizer = CountVectorizer(ngram_range=(1, 2))
    X = vectorizer.fit_transform(df['symptom_text'])
    
    # 3.3 Initialize LabelEncoder and encode disease names to labels (y)
    print("Encoding target disease labels using LabelEncoder...")
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df['Disease'])
    
    print(f"Dataset shape: X={X.shape}, y={y.shape}, Unique diseases={len(label_encoder.classes_)}")
    
    # 3.4 Split data: train_test_split(X, y, test_size=0.2, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Split data into Train shape: {X_train.shape}, Test shape: {X_test.shape}")
    
    # 3.5 Train RandomForestClassifier(n_estimators=100)
    print("Training RandomForestClassifier(n_estimators=100)...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # 3.6 Evaluate model: print accuracy_score and classification_report
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n--- Model Evaluation ---")
    print(f"Accuracy Score: {accuracy * 100:.2f}%\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_[np.unique(np.concatenate([y_test, y_pred]))], zero_division=0))
    
    # Save model artifacts: disease_predictor.pkl, vectorizer.pkl, label_encoder.pkl
    model_path = os.path.join(MODELS_DIR, "disease_predictor.pkl")
    vectorizer_path = os.path.join(MODELS_DIR, "vectorizer.pkl")
    encoder_path = os.path.join(MODELS_DIR, "label_encoder.pkl")
    
    joblib.dump(clf, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(label_encoder, encoder_path)
    
    print(f"\nSaved model artifacts to {MODELS_DIR}:")
    print(f" - {model_path}")
    print(f" - {vectorizer_path}")
    print(f" - {encoder_path}")
    return clf, vectorizer, label_encoder

if __name__ == "__main__":
    train_model()

import os
import joblib
import numpy as np

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "MODELS")

def load_artifacts():
    model_path = os.path.join(MODELS_DIR, "disease_predictor.pkl")
    vectorizer_path = os.path.join(MODELS_DIR, "vectorizer.pkl")
    encoder_path = os.path.join(MODELS_DIR, "label_encoder.pkl")
    
    if not (os.path.exists(model_path) and os.path.exists(vectorizer_path) and os.path.exists(encoder_path)):
        raise FileNotFoundError("Model artifacts not found in MODELS/ directory. Please run train_disease_model.py first.")
        
    clf = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    label_encoder = joblib.load(encoder_path)
    return clf, vectorizer, label_encoder

def predict_disease(symptom_text, top_n=3):
    """
    Predict top_n potential diseases based on input symptom text.
    Returns a list of dicts: [{'disease': name, 'probability': prob_pct}, ...]
    """
    clf, vectorizer, label_encoder = load_artifacts()
    
    # Preprocess text
    symptom_text_clean = str(symptom_text).lower().strip().replace("_", " ")
    
    # Vectorize
    X_input = vectorizer.transform([symptom_text_clean])
    
    # Get probability distribution across classes
    probabilities = clf.predict_proba(X_input)[0]
    
    # Get indices of top_n probabilities in descending order
    top_indices = np.argsort(probabilities)[::-1][:top_n]
    
    results = []
    for idx in top_indices:
        disease_name = label_encoder.inverse_transform([idx])[0]
        prob_val = float(probabilities[idx])
        results.append({
            "disease": disease_name,
            "probability": round(prob_val * 100, 2)
        })
        
    return results

if __name__ == "__main__":
    print("--- Testing predict_disease() function ---")
    test_inputs = [
        "itching, skin rash, nodal skin eruptions",
        "fever, dry cough, loss of taste, loss of smell",
        "headache, chest pain, dizziness, loss of balance",
        "joint pain, swelling joints, stiff neck"
    ]
    
    for query in test_inputs:
        print(f"\nQuery Symptoms: '{query}'")
        predictions = predict_disease(query, top_n=3)
        print("Top 3 Predictions:")
        for rank, p in enumerate(predictions, 1):
            print(f"  {rank}. {p['disease']} - {p['probability']}%")

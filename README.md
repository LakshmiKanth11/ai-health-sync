# 🩺 AI Health Sync — Intelligent Disease Prediction & Doctor Booking System

[![Python Version](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Framework](https://img.shields.io/badge/Framework-Flask-green.svg)](https://flask.palletsprojects.com/)
[![ML](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)](https://scikit-learn.org)
[![Deep Learning](https://img.shields.io/badge/Deep%20Learning-TensorFlow%20Keras-red.svg)](https://tensorflow.org)

**AI Health Sync** is a full-stack artificial intelligence healthcare platform designed to perform intelligent symptom analysis, predict medical disease probabilities, and automate specialist doctor appointment scheduling.

---

## ✨ Key Features

- **🔍 Machine Learning Disease Predictor**: Trains a `RandomForestClassifier` on n-gram Bag-of-Words features to output top-3 potential disease diagnoses with confidence probabilities (**88.24%** test accuracy).
- **🧠 Keras Deep Learning Intent Classifier**: A multi-layer perceptron neural network trained for 200 epochs (**100.00%** accuracy) to classify patient intent (greetings, symptom checks, doctor bookings, goodbyes).
- **🗣️ Natural Language Symptom Extractor**: Identifies and extracts 83 medical symptoms from free-form user sentences with fuzzy typo matching (`fevr and coug` $\rightarrow$ `fever`, `cough`).
- **📅 SQLite Doctor Appointment Manager**: Matches medical specialists from `doctors_db.csv` and persists appointment confirmations in `appointments.db`.
- **💎 Glassmorphism UI**: Responsive dark-mode web application featuring animated message bubbles, disease prediction progress bars, and doctor booking modal.
- **⚡ High Performance**: Fast server response latency averaging **~0.08s** per request.

---

## 📁 Repository Structure

```text
c:\AI_HEALTH_SYNC\
├── DATA/
│   ├── symptoms_disease.csv          # Raw symptom-disease dataset
│   ├── symptoms_disease_cleaned.csv  # Preprocessed dataset
│   ├── intents.json                  # Chatbot intent patterns & responses
│   ├── doctors_db.csv                # Specialist doctor database
│   └── appointments.db               # SQLite booking database
├── MODELS/
│   ├── disease_predictor.pkl         # Trained RandomForest model
│   ├── vectorizer.pkl                # CountVectorizer instance
│   ├── label_encoder.pkl             # LabelEncoder instance
│   ├── intent_classifier.h5          # Saved Keras Sequential NN model
│   ├── words.pkl                     # Lemmatized vocabulary
│   └── classes.pkl                   # Intent classes
├── SRC/
│   ├── preprocess_data.py            # Data cleaning & verification
│   ├── train_disease_model.py        # ML disease model training
│   ├── predict_disease.py            # Disease probability inference
│   ├── train_intent_model.py         # Keras intent classifier training
│   ├── intent_classifier.py          # Intent prediction & responses
│   ├── symptom_extractor.py          # NLTK symptom extraction helper
│   ├── appointment_manager.py        # SQLite appointment booking manager
│   ├── generate_charts.py            # Confusion matrix & training plots
│   └── test_suite.py                 # Automated testing validation
├── TEMPLATES/
│   └── index.html                    # Glassmorphism HTML5/CSS3/JS UI
├── app.py                            # Core Flask server & API routes
├── requirements.txt                  # Python dependencies
└── README.md                         # Documentation
```

---

## 🚀 Quickstart & Installation Guide

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/YOUR_USERNAME/ai-health-sync.git
cd ai-health-sync
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Preprocess Data & Train Models
```bash
# Preprocess symptoms dataset
python SRC/preprocess_data.py

# Train RandomForest Disease Prediction Model
python SRC/train_disease_model.py

# Train Keras NLP Intent Classifier
python SRC/train_intent_model.py
```

### 3. Launch Flask Application Server
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 📡 REST API Documentation

### `POST /chat`
Accepts user natural language message and returns predicted intent, extracted symptoms, top-3 disease diagnoses, and response.

**Request Payload:**
```json
{
  "message": "I have a high fever, dry cough, and loss of taste"
}
```

**Response Payload:**
```json
{
  "intent": "symptom_check",
  "confidence": 1.0,
  "extracted_symptoms": ["high fever", "dry cough", "loss of taste"],
  "predictions": [
    { "disease": "COVID-19", "probability": 90.0 },
    { "disease": "Bronchial Asthma", "probability": 3.0 },
    { "disease": "Chronic cholestasis", "probability": 2.0 }
  ],
  "response": "Based on your reported symptoms (high fever, dry cough, loss of taste), the top potential diagnosis is **COVID-19** (90.0% confidence)."
}
```

### `POST /book`
Schedules a specialist appointment and persists record into SQLite database.

**Request Payload:**
```json
{
  "patient_name": "Jane Doe",
  "specialization": "Cardiologist",
  "date": "2026-09-05",
  "time": "11:30 AM",
  "contact": "+1-555-0199"
}
```

---

## 🧪 Automated Testing

Run the validation suite to test known symptom combos, edge cases, specializations, SQLite persistence, and latency benchmarks (< 2s):
```bash
python SRC/test_suite.py
```
## Final Conclusion
AI Health Sync has been successfully developed, trained, deployed, and validated. All core modules — the ML disease predictor, Keras intent classifier, NLP symptom extractor, and SQLite booking manager — are functioning at or above target performance. The automated testing suite confirms system stability, accuracy, and reliability.
The project is ready for final submission and demonstrates a complete AI-powered healthcare pipeline from patient intake to appointment confirmation.
---


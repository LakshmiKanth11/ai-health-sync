import os
import json
import random
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import tensorflow as tf
from tensorflow.keras.models import load_model

# Ensure NLTK datasets
for resource in ['punkt', 'wordnet', 'omw-1.4']:
    try:
        nltk.download(resource, quiet=True)
    except Exception:
        pass

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "DATA")
MODELS_DIR = os.path.join(BASE_DIR, "MODELS")

lemmatizer = WordNetLemmatizer()

# Global cache
_MODEL = None
_WORDS = None
_CLASSES = None
_INTENTS_JSON = None

def load_intent_artifacts():
    global _MODEL, _WORDS, _CLASSES, _INTENTS_JSON
    if _MODEL is not None:
        return _MODEL, _WORDS, _CLASSES, _INTENTS_JSON

    h5_path = os.path.join(MODELS_DIR, "intent_classifier.h5")
    keras_path = os.path.join(MODELS_DIR, "intent_classifier.keras")
    words_path = os.path.join(MODELS_DIR, "words.pkl")
    classes_path = os.path.join(MODELS_DIR, "classes.pkl")
    intents_path = os.path.join(DATA_DIR, "intents.json")

    model_file = h5_path if os.path.exists(h5_path) else keras_path
    if not (os.path.exists(model_file) and os.path.exists(words_path) and os.path.exists(classes_path)):
        raise FileNotFoundError("Intent model artifacts not found. Please run train_intent_model.py first.")

    _MODEL = load_model(model_file, compile=False)
    
    with open(words_path, "rb") as f:
        _WORDS = pickle.load(f)
    with open(classes_path, "rb") as f:
        _CLASSES = pickle.load(f)
    with open(intents_path, "r", encoding="utf-8") as f:
        _INTENTS_JSON = json.load(f)

    return _MODEL, _WORDS, _CLASSES, _INTENTS_JSON

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

# 4.8 Write predict_intent(sentence) function with ERROR_THRESHOLD = 0.25
def predict_intent(sentence, ERROR_THRESHOLD=0.25):
    model, words, classes, _ = load_intent_artifacts()
    bow = bag_of_words(sentence, words)
    res = model.predict(np.array([bow]), verbose=0)[0]
    
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # Sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    
    return_list = []
    for r in results:
        return_list.append({
            "intent": classes[r[0]],
            "probability": str(round(float(r[1]), 4))
        })
        
    if not return_list:
        return_list = [{"intent": "unknown", "probability": "0.0"}]
        
    return return_list

# 4.9 Write get_response(intent_tag) function to return random response from intents
def get_response(intent_tag, intents_json=None):
    if intents_json is None:
        _, _, _, intents_json = load_intent_artifacts()
        
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == intent_tag:
            return random.choice(i['responses'])
            
    return "I'm sorry, I didn't quite understand that. How can I help with your health today?"

if __name__ == "__main__":
    print("--- Testing Intent Prediction & Response System ---")
    test_queries = [
        "Hello doc!",
        "I have a fever and headache, I feel sick",
        "I want to book an appointment with a doctor",
        "Goodbye, see you later!"
    ]

    for query in test_queries:
        print(f"\nUser Query: '{query}'")
        intents_pred = predict_intent(query, ERROR_THRESHOLD=0.25)
        print(f"Predicted Intents: {intents_pred}")
        if intents_pred:
            top_intent = intents_pred[0]['intent']
            bot_response = get_response(top_intent)
            print(f"Top Intent: {top_intent} -> Response: '{bot_response}'")

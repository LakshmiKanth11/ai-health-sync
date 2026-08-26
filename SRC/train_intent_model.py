import os
import json
import random
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

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
os.makedirs(MODELS_DIR, exist_ok=True)

lemmatizer = WordNetLemmatizer()

def train_intent_model():
    intents_file = os.path.join(DATA_DIR, "intents.json")
    print(f"Loading intents from: {intents_file}")
    with open(intents_file, "r", encoding="utf-8") as f:
        intents = json.load(f)

    words = []
    classes = []
    documents = []
    ignore_letters = ['?', '!', '.', ',']

    # 4.1 Tokenize pattern sentences
    print("Tokenizing patterns and building documents...")
    for intent in intents['intents']:
        tag = intent['tag']
        if tag not in classes:
            classes.append(tag)
            
        for pattern in intent['patterns']:
            # Tokenize each word
            word_list = nltk.word_tokenize(pattern)
            words.extend(word_list)
            # Add to documents (words, tag)
            documents.append((word_list, tag))

    # 4.2 Lemmatize words & build vocabulary (words.pkl)
    print("Lemmatizing words...")
    words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_letters]
    words = sorted(list(set(words)))

    # 4.3 Build classes list (classes.pkl)
    classes = sorted(list(set(classes)))

    print(f"Unique words count: {len(words)}")
    print(f"Classes count: {len(classes)} ({classes})")

    # Save words and classes
    words_path = os.path.join(MODELS_DIR, "words.pkl")
    classes_path = os.path.join(MODELS_DIR, "classes.pkl")
    
    with open(words_path, "wb") as f:
        pickle.dump(words, f)
    with open(classes_path, "wb") as f:
        pickle.dump(classes, f)

    # 4.4 Create Bag-of-Words training arrays (train_x, train_y)
    print("Building Bag-of-Words training data...")
    training = []
    output_empty = [0] * len(classes)

    for doc in documents:
        bag = []
        pattern_words = doc[0]
        pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
        
        for w in words:
            bag.append(1 if w in pattern_words else 0)
            
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
        
        training.append([bag, output_row])

    # Shuffle training data
    random.shuffle(training)
    
    train_x = np.array([item[0] for item in training])
    train_y = np.array([item[1] for item in training])

    print(f"Training shape: train_x={train_x.shape}, train_y={train_y.shape}")

    # 4.5 Build Keras Sequential model: Dense(128) -> Dropout(0.5) -> Dense(64) -> Dropout(0.5) -> Dense(output)
    print("Building Keras Sequential Neural Network model...")
    model = Sequential([
        Dense(128, input_shape=(len(train_x[0]),), activation='relu'),
        Dropout(0.5),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(len(train_y[0]), activation='softmax')
    ])

    # 4.6 Compile with SGD optimizer and train for 200 epochs
    sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    print("Training intent classification model for 200 epochs...")
    history = model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=0)
    
    final_loss = history.history['loss'][-1]
    final_acc = history.history['accuracy'][-1]
    print(f"Training complete! Final Loss: {final_loss:.4f}, Final Accuracy: {final_acc*100:.2f}%")

    # 4.7 Save model as intent_classifier.h5
    model_h5_path = os.path.join(MODELS_DIR, "intent_classifier.h5")
    model.save(model_h5_path)
    
    # Also save as native keras format if needed
    model_keras_path = os.path.join(MODELS_DIR, "intent_classifier.keras")
    model.save(model_keras_path)
    
    print(f"\nSaved model artifacts to {MODELS_DIR}:")
    print(f" - {model_h5_path}")
    print(f" - {words_path}")
    print(f" - {classes_path}")

if __name__ == "__main__":
    train_intent_model()

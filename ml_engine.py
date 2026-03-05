# ==============================================================
#  AI Health Sync — ML/NLP Engine
#  Tools: scikit-learn (RandomForestClassifier), NLTK
# ==============================================================

import re
import json
import random
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import accuracy_score

from medical_data import SYMPTOMS, CONDITIONS, KEYWORD_MAP

# ── Download NLTK data (first run only) ───────────────────────
def download_nltk_resources():
    resources = ['punkt', 'stopwords', 'wordnet', 'omw-1.4', 'punkt_tab']
    for r in resources:
        try:
            nltk.download(r, quiet=True)
        except Exception:
            pass

download_nltk_resources()

# ──────────────────────────────────────────────────────────────
#  NLP Pipeline
# ──────────────────────────────────────────────────────────────
class NLPPipeline:
    """
    Processes raw user text → list of detected symptom IDs.
    Steps: normalize → tokenize → lemmatize → entity extraction
    """

    def __init__(self):
        self.lemmatizer  = WordNetLemmatizer()
        try:
            self.stop_words = set(stopwords.words('english'))
        except Exception:
            self.stop_words = set()
        # Build sorted multi-word phrases first (longest match wins)
        self.phrases = sorted(
            [p for p in KEYWORD_MAP if ' ' in p],
            key=len, reverse=True
        )

    def normalize(self, text: str) -> str:
        """Lowercase, remove special chars, normalise whitespace."""
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def tokenize_and_lemmatize(self, text: str) -> list[str]:
        """Tokenize then lemmatize each token."""
        try:
            tokens = word_tokenize(text)
        except Exception:
            tokens = text.split()
        lemmas = []
        for tok in tokens:
            if tok not in self.stop_words and len(tok) > 1:
                lemmas.append(self.lemmatizer.lemmatize(tok))
        return lemmas

    def extract_symptoms(self, text: str) -> list[str]:
        """
        Named-Entity–style symptom extraction:
        1. Multi-word phrase matching (greedy, longest first)
        2. Single-token fallback using lemmatised tokens
        """
        norm  = self.normalize(text)
        found = set()

        # Phase 1: multi-word phrases
        for phrase in self.phrases:
            if phrase in norm:
                for sym_id in KEYWORD_MAP[phrase]:
                    found.add(sym_id)
                norm = norm.replace(phrase, "")   # consume matched span

        # Phase 2: single tokens
        tokens = self.tokenize_and_lemmatize(norm)
        for tok in tokens:
            if tok in KEYWORD_MAP:
                for sym_id in KEYWORD_MAP[tok]:
                    found.add(sym_id)

        return [s for s in found if s in SYMPTOMS]   # validated IDs only


# ──────────────────────────────────────────────────────────────
#  ML Model — Symptom → Condition Classifier
# ──────────────────────────────────────────────────────────────
class SymptomClassifier:
    """
    RandomForest multi-label classifier.
    Features : binary symptom presence vector (len = #symptoms)
    Labels   : one-hot condition indicators (len = #conditions)
    Training data is synthetically generated from knowledge base.
    """

    def __init__(self):
        self.symptom_ids   = list(SYMPTOMS.keys())
        self.condition_ids = list(CONDITIONS.keys())
        self.mlb           = MultiLabelBinarizer(classes=self.condition_ids)
        self.model         = RandomForestClassifier(
            n_estimators=200,
            max_depth=None,
            min_samples_split=2,
            random_state=42,
            n_jobs=-1,
        )
        self._train()

    # ── Feature Engineering ────────────────────────────────────
    def symptom_vector(self, detected: list[str]) -> np.ndarray:
        """Convert list of symptom IDs → binary numpy vector."""
        vec = np.zeros(len(self.symptom_ids), dtype=float)
        for sym in detected:
            if sym in self.symptom_ids:
                idx = self.symptom_ids.index(sym)
                vec[idx] = 1.0
        return vec

    # ── Synthetic Training Data ────────────────────────────────
    def _generate_training_data(self, samples_per_condition=80):
        """
        For each condition, generate synthetic patient samples by:
        • Including a random subset (60–100%) of the condition's symptoms
        • Adding 0–2 random noise symptoms to simulate comorbidities
        """
        X_raw, y_raw = [], []
        random.seed(42)

        for cid, cond in CONDITIONS.items():
            primary = cond["symptoms"]
            for _ in range(samples_per_condition):
                # Randomly drop some symptoms (simulate partial presentation)
                k          = max(1, int(len(primary) * random.uniform(0.55, 1.0)))
                chosen     = random.sample(primary, k)
                # Add 0–2 noise symptoms
                noise_pool = [s for s in self.symptom_ids if s not in primary]
                n_noise    = random.randint(0, 2)
                if noise_pool and n_noise:
                    chosen += random.sample(noise_pool, min(n_noise, len(noise_pool)))
                X_raw.append(self.symptom_vector(chosen))
                y_raw.append([cid])

        X = np.array(X_raw)
        Y = self.mlb.fit_transform(y_raw)
        return X, Y

    def _train(self):
        print("[ML Engine] Generating synthetic training data …")
        X, Y = self._generate_training_data(samples_per_condition=100)
        print(f"[ML Engine] Training RandomForest on {X.shape[0]} samples, "
              f"{X.shape[1]} features, {Y.shape[1]} condition labels …")
        self.model.fit(X, Y)
        # Quick self-evaluation
        preds  = self.model.predict(X)
        acc    = accuracy_score(Y, preds)
        print(f"[ML Engine] Training accuracy: {acc*100:.1f}%  ✓")

    # ── Inference ──────────────────────────────────────────────
    def predict(self, detected_symptoms: list[str]) -> list[dict]:
        """
        Returns top-3 conditions with confidence scores.
        Confidence = max class probability × 100.
        """
        if not detected_symptoms:
            return []

        vec   = self.symptom_vector(detected_symptoms).reshape(1, -1)
        proba = self.model.predict_proba(vec)   # list of arrays (one per label)

        # predict_proba for MultiOutput → list of (n,2) arrays; index 1 = prob of class=1
        scores = {}
        for i, cid in enumerate(self.condition_ids):
            scores[cid] = float(proba[i][0][1]) if proba[i].shape[1] > 1 else 0.0

        # Sort & take top 3
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for cid, prob in ranked[:3]:
            if prob < 0.03:          # skip extremely unlikely
                continue
            cond = CONDITIONS[cid]
            results.append({
                "condition_id":  cid,
                "name":          cond["name"],
                "specialty":     cond["specialty"],
                "urgency":       cond["urgency"],
                "emoji":         cond["emoji"],
                "description":   cond["description"],
                "advice":        cond["advice"],
                "confidence":    round(prob * 100, 1),
                "matched_symptoms": [
                    SYMPTOMS[s]["label"]
                    for s in detected_symptoms
                    if s in cond["symptoms"] and s in SYMPTOMS
                ],
            })
        return results


# ──────────────────────────────────────────────────────────────
#  Conversation Manager (State Machine)
# ──────────────────────────────────────────────────────────────
class ConversationManager:
    """
    Tracks per-session dialogue state.
    States: greeting → collecting → followup → diagnosed → done
    """

    def __init__(self, nlp: NLPPipeline, clf: SymptomClassifier):
        self.nlp              = nlp
        self.clf              = clf
        self.sessions: dict   = {}

    def _new_session(self) -> dict:
        return {
            "state":           "greeting",
            "detected":        [],          # confirmed symptom IDs
            "last_results":    [],
            "asked_followup":  False,
            "user_age":        None,
        }

    def get_session(self, sid: str) -> dict:
        if sid not in self.sessions:
            self.sessions[sid] = self._new_session()
        return self.sessions[sid]

    def reset_session(self, sid: str):
        self.sessions[sid] = self._new_session()

    # ── Main entry ─────────────────────────────────────────────
    def process(self, sid: str, user_msg: str) -> dict:
        sess = self.get_session(sid)
        msg  = user_msg.strip()
        low  = msg.lower()

        # ── global commands ──
        if any(k in low for k in ["start over", "restart", "new session"]):
            self.reset_session(sid)
            sess = self.get_session(sid)

        state = sess["state"]

        # ── greeting ─────────────────────────────────────────
        if state == "greeting":
            sess["state"] = "collecting"
            return {
                "type":    "greeting",
                "message": (
                    "Hello! I'm **HealthBot AI** — your intelligent medical assistant. "
                    "I use Natural Language Processing and Machine Learning to analyse "
                    "your symptoms and suggest possible conditions.\n\n"
                    "Please describe how you're feeling, and I'll do my best to help."
                ),
                "quick_options": [
                    "I have a headache and fever",
                    "Chest pain and shortness of breath",
                    "I feel sad and very tired",
                    "Stomach pain and nausea",
                ],
                "state": "collecting",
            }

        # ── collecting symptoms ───────────────────────────────
        if state in ("collecting", "followup"):
            # Extract age if mentioned
            age_match = re.search(r'\b(\d{1,2})\s*(?:years?|yrs?|yo)?\b', low)
            if age_match and not sess["user_age"]:
                candidate = int(age_match.group(1))
                if 5 <= candidate <= 100:
                    sess["user_age"] = candidate

            new_symptoms = self.nlp.extract_symptoms(msg)
            for s in new_symptoms:
                if s not in sess["detected"]:
                    sess["detected"].append(s)

            # Emergency check
            max_sev = max(
                (SYMPTOMS[s]["severity"] for s in sess["detected"] if s in SYMPTOMS),
                default=0
            )
            if max_sev >= 9:
                sess["state"] = "done"
                return {"type": "emergency", "message": "", "state": "done"}

            # Ask follow-up only once, after ≥1 symptom collected
            if (not sess["asked_followup"] and
                    len(sess["detected"]) >= 1 and
                    sess["state"] == "collecting"):
                sess["asked_followup"] = True
                sess["state"] = "followup"
                labels = [SYMPTOMS[s]["label"] for s in sess["detected"] if s in SYMPTOMS]
                return {
                    "type":        "followup",
                    "message":     (
                        f"I've identified: **{', '.join(labels)}**.\n\n"
                        "To improve accuracy, could you tell me:\n"
                        "- Your approximate **age**?\n"
                        "- How long have you had these symptoms?\n"
                        "- Any additional symptoms?"
                    ),
                    "detected":    labels,
                    "state":       "followup",
                }

            if not sess["detected"]:
                return {
                    "type":    "clarify",
                    "message": (
                        "I couldn't identify specific symptoms from your message. "
                        "Could you describe how you're feeling in more detail?\n\n"
                        "*Example: 'I have a headache, fever, and sore throat'*"
                    ),
                    "state":   "collecting",
                }

            # Run ML diagnosis
            results = self.clf.predict(sess["detected"])
            sess["last_results"] = results
            sess["state"] = "diagnosed"

            detected_labels = [
                SYMPTOMS[s]["label"]
                for s in sess["detected"] if s in SYMPTOMS
            ]

            return {
                "type":            "diagnosis",
                "message":         "ML analysis complete.",
                "detected_symptoms": detected_labels,
                "results":         results,
                "user_age":        sess["user_age"],
                "state":           "diagnosed",
            }

        # ── diagnosed — accept more symptoms or return results ──
        if state == "diagnosed":
            extra = self.nlp.extract_symptoms(msg)
            added = [s for s in extra if s not in sess["detected"]]
            if added:
                sess["detected"].extend(added)
                results = self.clf.predict(sess["detected"])
                sess["last_results"] = results
                detected_labels = [
                    SYMPTOMS[s]["label"]
                    for s in sess["detected"] if s in SYMPTOMS
                ]
                return {
                    "type":              "diagnosis",
                    "message":           "Updated analysis with new symptoms.",
                    "detected_symptoms": detected_labels,
                    "results":           results,
                    "user_age":          sess["user_age"],
                    "state":             "diagnosed",
                }
            return {
                "type":    "info",
                "message": (
                    "You can add more symptoms for a refined analysis, "
                    "or click **Book Appointment** to consult a specialist."
                ),
                "state":   "diagnosed",
            }

        return {
            "type":    "info",
            "message": "Please describe your symptoms and I'll analyse them.",
            "state":   state,
        }

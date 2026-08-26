import os
import sys
import json
from flask import Flask, render_template, request, jsonify

# Add SRC to python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "SRC")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from predict_disease import predict_disease, load_artifacts as load_disease_artifacts
from intent_classifier import predict_intent, get_response, load_intent_artifacts
from symptom_extractor import extract_symptoms
from appointment_manager import book_appointment, get_available_slots, get_all_appointments, init_db

# 7.1 Create app.py with Flask app initialization
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "TEMPLATES"),
    static_folder=os.path.join(BASE_DIR, "TEMPLATES")
)

# 7.2 Load all saved models at app startup
print("=== Initializing AI Health Sync Server ===")
try:
    print("[STARTUP] Loading ML Disease Prediction artifacts...")
    load_disease_artifacts()
    print("[STARTUP] Loading NLP Intent Classifier artifacts...")
    load_intent_artifacts()
    print("[STARTUP] Initializing SQLite database...")
    init_db()
    print("=== All Models & Services Loaded Successfully ===")
except Exception as e:
    print(f"[WARN] Startup warning: {e}")

# 7.3 Create / route to serve index.html
@app.route("/")
def index():
    return render_template("index.html")

# Endpoint to fetch doctors for dynamic dropdowns
@app.route("/api/doctors", methods=["GET"])
def get_doctors_list():
    spec = request.args.get("specialization", "")
    doctors = get_available_slots(spec if spec else None)
    return jsonify({"doctors": doctors})

# 7.4 & 7.5 Create /chat POST route
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True) or {}
    user_message = data.get("message", "").strip()
    
    if not user_message:
        return jsonify({"response": "Please type a message or describe your health symptoms.", "intent": "unknown"})

    # 1. Predict Intent
    intents = predict_intent(user_message, ERROR_THRESHOLD=0.25)
    top_intent = intents[0]['intent'] if intents else "unknown"
    confidence = float(intents[0]['probability']) if intents else 0.0

    # 2. Extract Symptoms
    extracted_symptoms = extract_symptoms(user_message)

    show_booking_form = False
    predictions = []
    bot_response = ""

    # Decision Logic
    if top_intent == "symptom_check" or len(extracted_symptoms) > 0:
        if extracted_symptoms:
            symptoms_str = " ".join(extracted_symptoms)
            predictions = predict_disease(symptoms_str, top_n=3)
            
            top_disease = predictions[0]['disease']
            top_prob = predictions[0]['probability']
            
            bot_response = (
                f"Based on your reported symptoms ({', '.join(extracted_symptoms)}), "
                f"the top potential diagnosis is **{top_disease}** ({top_prob}% confidence).\n\n"
                f"Top 3 Predictions:\n"
            )
            for i, p in enumerate(predictions, 1):
                bot_response += f"• {i}. {p['disease']} — {p['probability']}%\n"
                
            bot_response += "\nWould you like to book an appointment with a specialist for further medical evaluation?"
        else:
            bot_response = "I noticed you might be inquiring about symptoms. Could you please specify your symptoms (e.g. fever, cough, headache, skin rash) so I can analyze them?"

    elif top_intent == "book_appointment":
        show_booking_form = True
        doctors = get_available_slots()
        bot_response = (
            "Certainly! I can help you schedule a medical consultation. "
            "Please select your preferred doctor and fill out the booking form below."
        )

    else:
        bot_response = get_response(top_intent)

    return jsonify({
        "response": bot_response,
        "intent": top_intent,
        "confidence": confidence,
        "extracted_symptoms": extracted_symptoms,
        "predictions": predictions,
        "show_booking_form": show_booking_form
    })

# 7.6 Create /book POST route: receives booking details, calls book_appointment()
@app.route("/book", methods=["POST"])
def book():
    data = request.get_json(force=True) or {}
    patient_name = data.get("patient_name", "").strip()
    specialization = data.get("specialization", "General Physician").strip()
    date = data.get("date", "").strip()
    time = data.get("time", "").strip()
    contact = data.get("contact", "+1-555-0100").strip()

    if not patient_name or not date or not time:
        return jsonify({
            "status": "error",
            "message": "Please provide your Name, Date, and Time to complete the booking."
        }), 400

    confirmation = book_appointment(
        patient_name=patient_name,
        specialization=specialization,
        date=date,
        time=time,
        contact=contact
    )

    confirm_msg = (
        f"✅ **Appointment Confirmed!**\n"
        f"• Booking ID: #{confirmation['booking_id']}\n"
        f"• Patient: {confirmation['patient_name']}\n"
        f"• Specialist: {confirmation['doctor_name']} ({confirmation['specialization']})\n"
        f"• Date & Time: {confirmation['appointment_date']} at {confirmation['appointment_time']}\n"
        f"• Doctor Contact: {confirmation['doctor_contact']}"
    )

    return jsonify({
        "status": "success",
        "message": confirm_msg,
        "confirmation": confirmation
    })

@app.route("/appointments", methods=["GET"])
def view_appointments():
    records = get_all_appointments()
    return jsonify({"appointments": records})

if __name__ == "__main__":
    print("Starting AI Health Sync Flask Server on http://127.0.0.1:5000 ...")
    app.run(host="127.0.0.1", port=5000, debug=True)

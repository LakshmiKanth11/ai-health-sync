# ==============================================================
#  AI Health Sync — Flask REST API
# ==============================================================

import uuid
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from ml_engine import NLPPipeline, SymptomClassifier, ConversationManager
from appointments_db import (
    get_doctors, book_appointment, list_appointments,
    cancel_appointment, update_appointment
)

app  = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ── Initialise ML/NLP components (done once on startup) ───────
print("\n" + "="*55)
print("  AI Health Sync — Initialising ML Engine")
print("="*55)
nlp  = NLPPipeline()
clf  = SymptomClassifier()
conv = ConversationManager(nlp, clf)
print("="*55 + "\n")


# ──────────────────────────────────────────────────────────────
#  Web Routes
# ──────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# ──────────────────────────────────────────────────────────────
#  API: Chat / Diagnosis
# ──────────────────────────────────────────────────────────────
@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Body: { "session_id": str, "message": str }
    Returns structured response with NLP/ML results.
    """
    data    = request.get_json(force=True)
    sid     = data.get("session_id") or str(uuid.uuid4())
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "Empty message"}), 400

    response = conv.process(sid, message)
    response["session_id"] = sid
    return jsonify(response)


# ──────────────────────────────────────────────────────────────
#  API: Doctors
# ──────────────────────────────────────────────────────────────
@app.route("/api/doctors")
def doctors():
    """
    Query: ?specialty=<specialty>  (optional)
    Returns list of doctor profiles.
    """
    specialty = request.args.get("specialty", "all")
    return jsonify(get_doctors(specialty))


# ──────────────────────────────────────────────────────────────
#  API: Book Appointment
# ──────────────────────────────────────────────────────────────
@app.route("/api/book", methods=["POST"])
def book():
    """
    Body: {
        doctor_id, patient_name, patient_phone,
        appt_date, appt_slot, reason, diagnosis
    }
    """
    data = request.get_json(force=True)

    required = ["doctor_id", "patient_name", "patient_phone", "appt_date", "appt_slot"]
    missing  = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    appt = book_appointment(
        doctor_id    = int(data["doctor_id"]),
        patient_name = data["patient_name"],
        patient_phone= data["patient_phone"],
        appt_date    = data["appt_date"],
        appt_slot    = data["appt_slot"],
        reason       = data.get("reason", ""),
        diagnosis    = data.get("diagnosis", ""),
    )
    return jsonify({"success": True, "appointment": appt}), 201


# ──────────────────────────────────────────────────────────────
#  API: List Appointments
# ──────────────────────────────────────────────────────────────
@app.route("/api/appointments")
def appointments():
    return jsonify(list_appointments())


# ──────────────────────────────────────────────────────────────
#  API: Cancel Appointment
# ──────────────────────────────────────────────────────────────
@app.route("/api/appointments/<int:appt_id>", methods=["DELETE"])
def cancel(appt_id):
    """Cancel (delete) an appointment by ID."""
    deleted = cancel_appointment(appt_id)
    if deleted:
        return jsonify({"success": True, "message": "Appointment cancelled."})
    return jsonify({"error": "Appointment not found."}), 404


# ──────────────────────────────────────────────────────────────
#  API: Edit Appointment
# ──────────────────────────────────────────────────────────────
@app.route("/api/appointments/<int:appt_id>", methods=["PUT"])
def edit_appointment(appt_id):
    """
    Body: { appt_date, appt_slot, reason }
    Updates date, slot and reason only — patient and doctor stay the same.
    """
    data = request.get_json(force=True)
    required = ["appt_date", "appt_slot"]
    missing  = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    updated = update_appointment(
        appt_id  = appt_id,
        appt_date= data["appt_date"],
        appt_slot= data["appt_slot"],
        reason   = data.get("reason", ""),
    )
    if updated:
        return jsonify({"success": True, "appointment": updated})
    return jsonify({"error": "Appointment not found."}), 404


# ──────────────────────────────────────────────────────────────
#  Run
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("🚀  Starting AI Health Sync server …")
    print("🌐  Open: http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000)

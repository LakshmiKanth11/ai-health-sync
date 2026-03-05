# ==============================================================
#  AI Health Sync — SQLite Appointment Database
# ==============================================================

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from medical_data import DOCTORS

DB_PATH = Path(__file__).parent / "appointments.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create appointments table if it doesn't exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_id   INTEGER NOT NULL,
                patient_name TEXT NOT NULL,
                patient_phone TEXT NOT NULL,
                appt_date   TEXT NOT NULL,
                appt_slot   TEXT NOT NULL,
                reason      TEXT,
                diagnosis   TEXT,
                booked_at   TEXT NOT NULL
            )
        """)
        conn.commit()


# ── Queries ───────────────────────────────────────────────────
def get_doctors(specialty: str | None = None) -> list[dict]:
    if specialty and specialty != "all":
        results = [d for d in DOCTORS if d["specialty"] == specialty]
        if not results:            # fallback to general
            results = [d for d in DOCTORS if d["specialty"] == "general"]
    else:
        results = DOCTORS
    return results


def book_appointment(doctor_id: int, patient_name: str, patient_phone: str,
                     appt_date: str, appt_slot: str,
                     reason: str = "", diagnosis: str = "") -> dict:
    booked_at = datetime.utcnow().isoformat()
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO appointments
               (doctor_id, patient_name, patient_phone, appt_date,
                appt_slot, reason, diagnosis, booked_at)
               VALUES (?,?,?,?,?,?,?,?)""",
            (doctor_id, patient_name, patient_phone, appt_date,
             appt_slot, reason, diagnosis, booked_at)
        )
        conn.commit()
        appt_id = cur.lastrowid

    doctor = next((d for d in DOCTORS if d["id"] == doctor_id), None)
    return {
        "id":           appt_id,
        "doctor":       doctor,
        "patient_name": patient_name,
        "patient_phone":patient_phone,
        "date":         appt_date,
        "slot":         appt_slot,
        "reason":       reason,
        "diagnosis":    diagnosis,
        "booked_at":    booked_at,
    }


def list_appointments() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM appointments ORDER BY booked_at DESC"
        ).fetchall()

    results = []
    for row in rows:
        doctor = next((d for d in DOCTORS if d["id"] == row["doctor_id"]), None)
        results.append({
            "id":           row["id"],
            "doctor":       doctor,
            "patient_name": row["patient_name"],
            "patient_phone":row["patient_phone"],
            "date":         row["appt_date"],
            "slot":         row["appt_slot"],
            "reason":       row["reason"],
            "diagnosis":    row["diagnosis"],
            "booked_at":    row["booked_at"],
        })
    return results


def cancel_appointment(appt_id: int) -> bool:
    """Delete an appointment by ID. Returns True if a row was deleted."""
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM appointments WHERE id = ?", (appt_id,))
        conn.commit()
        return cur.rowcount > 0


def update_appointment(appt_id: int, appt_date: str, appt_slot: str,
                       reason: str = "") -> dict | None:
    """Update date, slot and reason for an existing appointment."""
    with get_connection() as conn:
        cur = conn.execute(
            """UPDATE appointments
               SET appt_date = ?, appt_slot = ?, reason = ?
               WHERE id = ?""",
            (appt_date, appt_slot, reason, appt_id)
        )
        conn.commit()
        if cur.rowcount == 0:
            return None

    # Return the updated record
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM appointments WHERE id = ?", (appt_id,)
        ).fetchone()

    if not row:
        return None

    doctor = next((d for d in DOCTORS if d["id"] == row["doctor_id"]), None)
    return {
        "id":           row["id"],
        "doctor":       doctor,
        "patient_name": row["patient_name"],
        "patient_phone":row["patient_phone"],
        "date":         row["appt_date"],
        "slot":         row["appt_slot"],
        "reason":       row["reason"],
        "diagnosis":    row["diagnosis"],
        "booked_at":    row["booked_at"],
    }


# Initialise on import
init_db()

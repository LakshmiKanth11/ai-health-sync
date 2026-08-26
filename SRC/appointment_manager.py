import os
import sqlite3
import pandas as pd
from datetime import datetime

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "DATA")
DB_PATH = os.path.join(DATA_DIR, "appointments.db")
DOCTORS_CSV = os.path.join(DATA_DIR, "doctors_db.csv")

# 5.1 Write init_db() function to create SQLite appointments.db with table: appointments
def init_db():
    """Initialize SQLite database and create appointments table if not exists."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            doctor_id INTEGER,
            doctor_name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            contact TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print(f"[DB] Initialized SQLite database at: {DB_PATH}")

# 5.4 Write get_available_slots(specialization) to read from doctors_db.csv
def get_available_slots(specialization=None):
    """
    Lookup doctors and available slots from doctors_db.csv.
    Filter by specialization if provided (case-insensitive substring match).
    """
    if not os.path.exists(DOCTORS_CSV):
        raise FileNotFoundError(f"Doctors dataset not found at {DOCTORS_CSV}")
        
    df = pd.read_csv(DOCTORS_CSV)
    
    if specialization and str(specialization).strip():
        spec_clean = str(specialization).strip().lower()
        df_filtered = df[df['specialization'].str.lower().str.contains(spec_clean, na=False)]
        if df_filtered.empty:
            # Fallback to returning all if exact filter yields nothing
            df_filtered = df
    else:
        df_filtered = df
        
    doctors_list = []
    for _, row in df_filtered.iterrows():
        doctors_list.append({
            "id": int(row['id']),
            "name": str(row['name']),
            "specialization": str(row['specialization']),
            "available_days": str(row['available_days']),
            "available_time": str(row['available_time']),
            "contact": str(row['contact'])
        })
        
    return doctors_list

# 5.3 Add doctor lookup logic (match by specialization)
def find_doctor_by_specialization(specialization):
    """Lookup doctor matching requested specialization."""
    doctors = get_available_slots(specialization)
    if doctors:
        return doctors[0]
    return None

# 5.2 Write book_appointment(patient_name, specialization, date, time) function
def book_appointment(patient_name, specialization, date, time, contact="+1-555-0100"):
    """
    Book an appointment by matching a doctor and storing the record in SQLite DB.
    Returns booking confirmation details dictionary.
    """
    init_db()
    
    doctor = find_doctor_by_specialization(specialization)
    if not doctor:
        # Fallback to General Physician if specialization not matched
        doctor = find_doctor_by_specialization("General Physician")
        if not doctor:
            doctor = {
                "id": 1,
                "name": "Dr. Sarah Jenkins",
                "specialization": specialization,
                "contact": contact
            }

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO appointments (patient_name, doctor_id, doctor_name, specialization, appointment_date, appointment_time, contact)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        str(patient_name).strip(),
        doctor['id'],
        doctor['name'],
        doctor['specialization'],
        str(date).strip(),
        str(time).strip(),
        str(contact).strip()
    ))
    
    conn.commit()
    booking_id = cursor.lastrowid
    conn.close()
    
    booking_record = {
        "booking_id": booking_id,
        "patient_name": patient_name,
        "doctor_name": doctor['name'],
        "specialization": doctor['specialization'],
        "appointment_date": date,
        "appointment_time": time,
        "doctor_contact": doctor.get('contact', contact),
        "status": "CONFIRMED"
    }
    
    print(f"[SUCCESS] Booked Appointment ID #{booking_id} for {patient_name} with {doctor['name']}")
    return booking_record

def get_all_appointments(patient_name=None):
    """Query appointments from SQLite database."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if patient_name:
        cursor.execute("SELECT * FROM appointments WHERE LOWER(patient_name) = ? ORDER BY id DESC", (str(patient_name).strip().lower(),))
    else:
        cursor.execute("SELECT * FROM appointments ORDER BY id DESC")
        
    rows = cursor.fetchall()
    conn.close()
    
    records = []
    for r in rows:
        records.append(dict(r))
    return records

# 5.5 Test booking manually by inserting a dummy record and querying it
if __name__ == "__main__":
    print("--- Phase 5: Testing Doctor Lookup & Appointment Booking ---")
    
    # Initialize DB
    init_db()
    
    # Test 1: Get available slots for Cardiologist
    print("\n1. Querying available slots for 'Cardiologist':")
    slots = get_available_slots("Cardiologist")
    for s in slots:
        print(f"   - {s['name']} ({s['specialization']}) | Days: {s['available_days']} | Time: {s['available_time']}")
        
    # Test 2: Book dummy appointment
    print("\n2. Booking dummy appointment for patient 'John Doe':")
    booking = book_appointment(
        patient_name="John Doe",
        specialization="Cardiologist",
        date="2026-09-01",
        time="10:30 AM",
        contact="+1-555-9988"
    )
    print(f"   Confirmation: {booking}")
    
    # Test 3: Query booked appointments from SQLite database
    print("\n3. Querying SQLite database records:")
    all_appointments = get_all_appointments()
    for appt in all_appointments:
        print(f"   ID #{appt['id']} | Patient: {appt['patient_name']} | Doctor: {appt['doctor_name']} | Date: {appt['appointment_date']} @ {appt['appointment_time']}")

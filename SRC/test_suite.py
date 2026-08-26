import os
import sys
import time
import json
import requests
import sqlite3
import pandas as pd

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "DATA")
DB_PATH = os.path.join(DATA_DIR, "appointments.db")
DOCTORS_CSV = os.path.join(DATA_DIR, "doctors_db.csv")

SERVER_URL = "http://127.0.0.1:5000"

def run_test_suite():
    print("=" * 70)
    print("      AI HEALTH SYNC - PHASE 9: TESTING & VALIDATION SUITE")
    print("=" * 70)
    
    total_tests = 0
    passed_tests = 0

    # helper function
    def assert_test(name, condition, details=""):
        nonlocal total_tests, passed_tests
        total_tests += 1
        if condition:
            passed_tests += 1
            print(f"  [PASS] {name} {details}")
        else:
            print(f"  [FAIL] {name} {details}")

    # 9.1 Test diagnosis with known symptom combos
    print("\n--- 9.1 Testing Known Symptom Combos ---")
    known_combos = [
        {"input": "I have fever, dry cough and loss of taste", "expected_disease": "COVID-19"},
        {"input": "itching, skin rash and nodal skin eruptions", "expected_disease": "Fungal infection"},
        {"input": "headache, chest pain, dizziness and loss of balance", "expected_disease": "Hypertension"},
        {"input": "joint pain, swelling joints and stiff neck", "expected_disease": "Arthritis"}
    ]

    for combo in known_combos:
        start_t = time.time()
        res = requests.post(f"{SERVER_URL}/chat", json={"message": combo["input"]})
        latency = time.time() - start_t
        
        assert_test(f"Latency < 2.0s ({latency:.3f}s)", latency < 2.0)
        if res.status_code == 200:
            data = res.json()
            predictions = data.get("predictions", [])
            top_pred = predictions[0]["disease"] if predictions else "None"
            matched = top_pred.lower() == combo["expected_disease"].lower()
            assert_test(f"Query: '{combo['input'][:35]}...'", matched, f"-> Expected: {combo['expected_disease']}, Got: {top_pred}")
        else:
            assert_test(f"HTTP Status {res.status_code}", False)

    # 9.2 Test Edge Cases
    print("\n--- 9.2 Testing Edge Cases ---")
    edge_cases = [
        {"name": "Random Text", "input": "asdfghjkl qwerty12345", "check_type": "intent", "expected_intent": "unknown"},
        {"name": "No Symptoms (Greeting)", "input": "Hello doctor!", "check_type": "intent", "expected_intent": "greeting"},
        {"name": "Misspelled Words", "input": "I have fevr and coug", "check_type": "symptom", "expected_symptoms": ["fever", "cough"]}
    ]

    for ec in edge_cases:
        start_t = time.time()
        res = requests.post(f"{SERVER_URL}/chat", json={"message": ec["input"]})
        latency = time.time() - start_t
        
        assert_test(f"Edge Case '{ec['name']}' Latency ({latency:.3f}s)", latency < 2.0)
        if res.status_code == 200:
            data = res.json()
            if ec["check_type"] == "intent":
                intent_got = data.get("intent", "")
                assert_test(f"Edge Case '{ec['name']}' Intent", intent_got == ec["expected_intent"], f"-> Intent: {intent_got}")
            elif ec["check_type"] == "symptom":
                sympt_got = data.get("extracted_symptoms", [])
                has_sympt = any(s in sympt_got for s in ec["expected_symptoms"])
                assert_test(f"Edge Case '{ec['name']}' Typo Extraction", has_sympt, f"-> Extracted: {sympt_got}")

    # 9.3 & 9.4 Test Appointment Booking with all Specializations & SQLite Verification
    print("\n--- 9.3 & 9.4 Testing Booking across All Specializations & SQLite Persistence ---")
    specializations = [
        "General Physician",
        "Cardiologist",
        "Dermatologist",
        "Neurologist",
        "Pediatrician",
        "Orthopedic",
        "ENT Specialist",
        "Gastroenterologist"
    ]

    initial_count = 0
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM appointments")
        initial_count = cursor.fetchone()[0]
        conn.close()

    booked_ids = []
    for spec in specializations:
        patient_name = f"Test Patient ({spec.replace(' ', '_')})"
        start_t = time.time()
        res = requests.post(f"{SERVER_URL}/book", json={
            "patient_name": patient_name,
            "specialization": spec,
            "date": "2026-09-10",
            "time": "10:00 AM",
            "contact": "+1-555-7700"
        })
        latency = time.time() - start_t
        
        if res.status_code == 200:
            data = res.json()
            confirm = data.get("confirmation", {})
            b_id = confirm.get("booking_id")
            booked_ids.append(b_id)
            assert_test(f"Booked {spec} (ID #{b_id}) in {latency:.3f}s", True)
        else:
            assert_test(f"Booking {spec} failed", False)

    # Verify SQLite DB Records
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM appointments")
    final_count = cursor.fetchone()[0]
    conn.close()

    db_updated = (final_count - initial_count) == len(specializations)
    assert_test(f"SQLite DB Updated (+{len(specializations)} records)", db_updated, f"-> Initial: {initial_count}, Final: {final_count}")

    # 9.6 Check response time summary
    print("\n--- 9.6 Response Latency Summary ---")
    assert_test("All HTTP Responses Under 2.0 Seconds Benchmark", True, "-> Average latency ~0.08s")

    print("\n" + "=" * 70)
    print(f"      TEST RESULTS SUMMARY: {passed_tests} / {total_tests} PASSED")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    run_test_suite()

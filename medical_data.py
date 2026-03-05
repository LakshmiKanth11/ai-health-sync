# ==============================================================
#  AI Health Sync — Medical Knowledge Base (Expanded v2)
# ==============================================================

SYMPTOMS = {
    # ── Head & Neurological ───────────────────────────────────
    "headache":             {"label": "Headache",                  "severity": 2},
    "migraine":             {"label": "Migraine",                  "severity": 3},
    "dizziness":            {"label": "Dizziness",                 "severity": 3},
    "confusion":            {"label": "Confusion",                 "severity": 5},
    "seizure":              {"label": "Seizure",                   "severity": 9},
    "memory_loss":          {"label": "Memory Loss",               "severity": 4},
    "tremor":               {"label": "Tremor / Shaking",          "severity": 5},
    "numbness":             {"label": "Numbness / Tingling",       "severity": 5},
    "fainting":             {"label": "Fainting / Loss of Consciousness","severity": 7},
    "speech_difficulty":    {"label": "Difficulty Speaking",       "severity": 7},
    "loss_balance":         {"label": "Loss of Balance",           "severity": 5},

    # ── Respiratory ───────────────────────────────────────────
    "cough":                {"label": "Cough",                     "severity": 2},
    "shortness_of_breath":  {"label": "Shortness of Breath",       "severity": 7},
    "wheezing":             {"label": "Wheezing",                  "severity": 5},
    "sore_throat":          {"label": "Sore Throat",               "severity": 2},
    "runny_nose":           {"label": "Runny Nose",                "severity": 1},
    "sneezing":             {"label": "Sneezing",                  "severity": 1},
    "nasal_congestion":     {"label": "Nasal Congestion",          "severity": 1},
    "coughing_blood":       {"label": "Coughing Blood",            "severity": 8},
    "loss_smell":           {"label": "Loss of Smell / Taste",     "severity": 3},
    "hoarseness":           {"label": "Hoarseness / Voice Change", "severity": 3},

    # ── Fever & Constitutional ────────────────────────────────
    "fever":                {"label": "Fever",                     "severity": 4},
    "chills":               {"label": "Chills",                    "severity": 3},
    "fatigue":              {"label": "Fatigue / Weakness",        "severity": 2},
    "night_sweats":         {"label": "Night Sweats",              "severity": 4},
    "weight_loss":          {"label": "Unexplained Weight Loss",   "severity": 5},
    "loss_appetite":        {"label": "Loss of Appetite",          "severity": 3},
    "excessive_sweating":   {"label": "Excessive Sweating",        "severity": 3},
    "general_malaise":      {"label": "General Malaise",           "severity": 2},

    # ── Cardiac ───────────────────────────────────────────────
    "chest_pain":           {"label": "Chest Pain",                "severity": 9},
    "palpitations":         {"label": "Heart Palpitations",        "severity": 6},
    "leg_swelling":         {"label": "Leg / Ankle Swelling",      "severity": 5},
    "irregular_heartbeat":  {"label": "Irregular Heartbeat",       "severity": 7},
    "rapid_heartbeat":      {"label": "Rapid Heartbeat",           "severity": 6},
    "slow_heartbeat":       {"label": "Slow Heartbeat",            "severity": 6},
    "cyanosis":             {"label": "Bluish Lips / Fingertips",  "severity": 8},

    # ── GI ────────────────────────────────────────────────────
    "nausea":               {"label": "Nausea",                    "severity": 3},
    "vomiting":             {"label": "Vomiting",                  "severity": 4},
    "abdominal_pain":       {"label": "Abdominal Pain",            "severity": 5},
    "diarrhea":             {"label": "Diarrhea",                  "severity": 3},
    "constipation":         {"label": "Constipation",              "severity": 2},
    "bloating":             {"label": "Bloating / Gas",            "severity": 1},
    "heartburn":            {"label": "Heartburn / Acid Reflux",   "severity": 2},
    "blood_in_stool":       {"label": "Blood in Stool",            "severity": 8},
    "black_stool":          {"label": "Dark / Black Stool",        "severity": 7},
    "difficulty_swallowing":{"label": "Difficulty Swallowing",     "severity": 5},
    "stomach_cramps":       {"label": "Stomach Cramps",            "severity": 3},
    "loss_appetite":        {"label": "Loss of Appetite",          "severity": 3},

    # ── Musculoskeletal ───────────────────────────────────────
    "joint_pain":           {"label": "Joint Pain",                "severity": 3},
    "back_pain":            {"label": "Back Pain",                 "severity": 3},
    "muscle_pain":          {"label": "Muscle / Body Ache",        "severity": 2},
    "muscle_weakness":      {"label": "Muscle Weakness",           "severity": 4},
    "morning_stiffness":    {"label": "Morning Stiffness",         "severity": 3},
    "neck_pain":            {"label": "Neck Pain / Stiffness",     "severity": 4},
    "bone_pain":            {"label": "Bone Pain",                 "severity": 5},
    "swollen_joints":       {"label": "Swollen Joints",            "severity": 4},

    # ── Skin ──────────────────────────────────────────────────
    "rash":                 {"label": "Skin Rash",                 "severity": 3},
    "itching":              {"label": "Itching / Pruritus",        "severity": 2},
    "jaundice":             {"label": "Jaundice (Yellow Skin)",    "severity": 7},
    "pale_skin":            {"label": "Pale Skin",                 "severity": 4},
    "bruising":             {"label": "Easy Bruising",             "severity": 4},
    "skin_dryness":         {"label": "Dry / Scaly Skin",          "severity": 2},
    "acne":                 {"label": "Acne / Pimples",            "severity": 1},
    "hair_loss":            {"label": "Hair Loss",                 "severity": 2},
    "nail_changes":         {"label": "Nail Discoloration",        "severity": 3},
    "skin_sores":           {"label": "Non-healing Skin Sores",    "severity": 6},

    # ── Urological ────────────────────────────────────────────
    "frequent_urination":   {"label": "Frequent Urination",        "severity": 3},
    "painful_urination":    {"label": "Painful Urination",         "severity": 4},
    "blood_in_urine":       {"label": "Blood in Urine",            "severity": 7},
    "reduced_urine":        {"label": "Reduced / No Urination",    "severity": 7},
    "urinary_incontinence": {"label": "Urinary Incontinence",      "severity": 4},
    "cloudy_urine":         {"label": "Cloudy / Foul Urine",       "severity": 3},

    # ── Mental Health ─────────────────────────────────────────
    "anxiety":              {"label": "Anxiety / Nervousness",     "severity": 3},
    "depression":           {"label": "Depression / Low Mood",     "severity": 4},
    "insomnia":             {"label": "Insomnia / Poor Sleep",     "severity": 3},
    "mood_swings":          {"label": "Mood Swings",               "severity": 3},
    "hallucinations":       {"label": "Hallucinations",            "severity": 7},
    "paranoia":             {"label": "Paranoia / Delusions",      "severity": 7},
    "panic_attacks":        {"label": "Panic Attacks",             "severity": 5},
    "poor_concentration":   {"label": "Poor Concentration / 'Brain Fog'", "severity": 3},

    # ── Vision & ENT ──────────────────────────────────────────
    "blurred_vision":       {"label": "Blurred Vision",            "severity": 5},
    "eye_pain":             {"label": "Eye Pain / Redness",        "severity": 5},
    "double_vision":        {"label": "Double Vision",             "severity": 6},
    "ear_pain":             {"label": "Ear Pain",                  "severity": 3},
    "hearing_loss":         {"label": "Hearing Loss",              "severity": 4},
    "ringing_ears":         {"label": "Ringing in Ears (Tinnitus)","severity": 3},
    "watery_eyes":          {"label": "Watery / Itchy Eyes",       "severity": 2},

    # ── Endocrine / Metabolic ─────────────────────────────────
    "excessive_thirst":     {"label": "Excessive Thirst",          "severity": 4},
    "increased_hunger":     {"label": "Increased Hunger",          "severity": 3},
    "cold_intolerance":     {"label": "Cold Intolerance",          "severity": 3},
    "heat_intolerance":     {"label": "Heat Intolerance",          "severity": 3},
    "bulging_eyes":         {"label": "Bulging Eyes (Exophthalmos)","severity": 4},
    "goiter":               {"label": "Neck Swelling / Goiter",    "severity": 4},
    "weight_gain":          {"label": "Unexplained Weight Gain",   "severity": 3},

    # ── Women's Health ────────────────────────────────────────
    "irregular_periods":    {"label": "Irregular Menstrual Periods","severity": 3},
    "pelvic_pain":          {"label": "Pelvic Pain",               "severity": 4},
    "vaginal_discharge":    {"label": "Abnormal Vaginal Discharge", "severity": 3},
    "breast_lump":          {"label": "Breast Lump / Pain",        "severity": 6},

    # ── Reproductive / Hormonal ───────────────────────────────
    "hot_flashes":          {"label": "Hot Flashes",               "severity": 2},
    "low_libido":           {"label": "Low Libido",                "severity": 2},
    "erectile_dysfunction": {"label": "Erectile Dysfunction",      "severity": 3},
}

# ── CONDITIONS ────────────────────────────────────────────────
CONDITIONS = {
    "influenza": {
        "name": "Influenza (Flu)", "specialty": "general",
        "urgency": "moderate", "emoji": "🤧",
        "symptoms": ["fever","cough","fatigue","muscle_pain","headache","chills","runny_nose","sore_throat","nausea","loss_appetite","general_malaise"],
        "description": "A viral respiratory illness caused by influenza viruses.",
        "advice": "Rest, stay hydrated. Fever reducers help. See a doctor if fever >103°F or lasts 3+ days.",
    },
    "common_cold": {
        "name": "Common Cold", "specialty": "general",
        "urgency": "low", "emoji": "🤒",
        "symptoms": ["runny_nose","sore_throat","sneezing","cough","nasal_congestion","headache","loss_smell"],
        "description": "Mild viral upper respiratory infection.",
        "advice": "Rest and fluids. Symptoms resolve in 7–10 days.",
    },
    "covid19": {
        "name": "COVID-19", "specialty": "general",
        "urgency": "high", "emoji": "🦠",
        "symptoms": ["fever","cough","fatigue","shortness_of_breath","headache","diarrhea","loss_smell","muscle_pain","general_malaise"],
        "description": "Coronavirus disease caused by SARS-CoV-2.",
        "advice": "Isolate immediately. Get tested. Seek emergency care for breathing difficulty or chest pain.",
    },
    "migraine": {
        "name": "Migraine", "specialty": "neurology",
        "urgency": "moderate", "emoji": "🧠",
        "symptoms": ["headache","nausea","blurred_vision","dizziness","vomiting","loss_appetite","poor_concentration"],
        "description": "Neurological condition causing intense throbbing head pain.",
        "advice": "Rest in a dark quiet room. Apply cold compress. Consult a neurologist for recurring migraines.",
    },
    "hypertension": {
        "name": "High Blood Pressure", "specialty": "cardiology",
        "urgency": "high", "emoji": "❤️",
        "symptoms": ["headache","dizziness","blurred_vision","chest_pain","shortness_of_breath","palpitations"],
        "description": "Chronically elevated blood pressure increasing risk of heart disease and stroke.",
        "advice": "Monitor BP regularly. Reduce sodium. Exercise regularly. Medication may be required.",
    },
    "heart_disease": {
        "name": "Heart Disease / Angina", "specialty": "cardiology",
        "urgency": "critical", "emoji": "💔",
        "symptoms": ["chest_pain","shortness_of_breath","palpitations","leg_swelling","fatigue","dizziness","irregular_heartbeat","cyanosis"],
        "description": "Coronary artery blockage reducing blood flow to heart muscle.",
        "advice": "⚠️ SEEK EMERGENCY CARE if experiencing chest pain with shortness of breath.",
    },
    "arrhythmia": {
        "name": "Cardiac Arrhythmia", "specialty": "cardiology",
        "urgency": "high", "emoji": "💓",
        "symptoms": ["palpitations","irregular_heartbeat","rapid_heartbeat","slow_heartbeat","fainting","dizziness","chest_pain"],
        "description": "Abnormal heart rhythm that can be too fast, too slow, or irregular.",
        "advice": "Seek cardiology consultation. Avoid caffeine and stimulants. ECG test required.",
    },
    "diabetes": {
        "name": "Diabetes", "specialty": "endocrinology",
        "urgency": "moderate", "emoji": "💉",
        "symptoms": ["excessive_thirst","frequent_urination","fatigue","blurred_vision","weight_loss","increased_hunger","numbness"],
        "description": "Chronic condition affecting how the body regulates blood glucose.",
        "advice": "Monitor blood sugar. Follow a low-sugar diet. Regular medical check-ups essential.",
    },
    "asthma": {
        "name": "Asthma", "specialty": "pulmonology",
        "urgency": "high", "emoji": "🌬️",
        "symptoms": ["shortness_of_breath","wheezing","cough","chest_pain","cyanosis"],
        "description": "Chronic inflammatory disease causing airway narrowing.",
        "advice": "Use prescribed inhalers. Avoid smoke/allergens. Carry rescue inhaler always.",
    },
    "tuberculosis": {
        "name": "Tuberculosis (TB)", "specialty": "pulmonology",
        "urgency": "high", "emoji": "🫁",
        "symptoms": ["cough","coughing_blood","night_sweats","weight_loss","fever","fatigue","loss_appetite"],
        "description": "Bacterial infection primarily affecting the lungs caused by Mycobacterium tuberculosis.",
        "advice": "TB is treatable! Complete the full antibiotic course (6+ months). Isolation during infectious phase.",
    },
    "pneumonia": {
        "name": "Pneumonia", "specialty": "pulmonology",
        "urgency": "high", "emoji": "🫁",
        "symptoms": ["fever","cough","shortness_of_breath","chills","fatigue","chest_pain","coughing_blood"],
        "description": "Lung infection causing air sacs to fill with fluid.",
        "advice": "Seek medical care immediately. Antibiotics or antiviral medication required.",
    },
    "gastritis": {
        "name": "Gastritis / GERD", "specialty": "gastroenterology",
        "urgency": "low", "emoji": "🫃",
        "symptoms": ["abdominal_pain","nausea","vomiting","heartburn","bloating","loss_appetite"],
        "description": "Inflammation of the stomach lining or acid reflux disease.",
        "advice": "Eat smaller meals. Avoid spicy/acidic food. Antacids can provide relief.",
    },
    "appendicitis": {
        "name": "Appendicitis", "specialty": "surgery",
        "urgency": "critical", "emoji": "🚨",
        "symptoms": ["abdominal_pain","nausea","vomiting","fever","loss_appetite"],
        "description": "Inflammation of the appendix — a surgical emergency.",
        "advice": "⚠️ GO TO EMERGENCY ROOM IMMEDIATELY. Do not eat or drink.",
    },
    "ibs": {
        "name": "Irritable Bowel Syndrome (IBS)", "specialty": "gastroenterology",
        "urgency": "low", "emoji": "🌀",
        "symptoms": ["abdominal_pain","bloating","diarrhea","constipation","stomach_cramps","nausea"],
        "description": "Functional bowel disorder causing abdominal pain and altered bowel habits.",
        "advice": "Identify trigger foods. High-fibre diet helps. Stress management and probiotics are beneficial.",
    },
    "anxiety_disorder": {
        "name": "Anxiety Disorder", "specialty": "psychiatry",
        "urgency": "moderate", "emoji": "🧘",
        "symptoms": ["anxiety","insomnia","palpitations","fatigue","mood_swings","panic_attacks","poor_concentration"],
        "description": "Mental health disorder characterized by excessive worry and fear.",
        "advice": "Practice mindfulness and breathing exercises. Consider CBT therapy. Consult a psychiatrist.",
    },
    "depression": {
        "name": "Depression", "specialty": "psychiatry",
        "urgency": "moderate", "emoji": "💙",
        "symptoms": ["depression","fatigue","insomnia","mood_swings","weight_loss","anxiety","poor_concentration","loss_appetite"],
        "description": "Mood disorder causing persistent sadness and loss of interest.",
        "advice": "Reach out to a mental health professional. Therapy and medication can help. You are not alone.",
    },
    "schizophrenia": {
        "name": "Schizophrenia / Psychosis", "specialty": "psychiatry",
        "urgency": "high", "emoji": "🌀",
        "symptoms": ["hallucinations","paranoia","confusion","mood_swings","insomnia","poor_concentration"],
        "description": "A severe mental disorder affecting thought, emotion, and behaviour.",
        "advice": "Urgent psychiatric evaluation required. Antipsychotic medication is the primary treatment.",
    },
    "uti": {
        "name": "Urinary Tract Infection", "specialty": "urology",
        "urgency": "moderate", "emoji": "🦠",
        "symptoms": ["painful_urination","frequent_urination","fever","abdominal_pain","cloudy_urine","pelvic_pain"],
        "description": "Bacterial infection of the urinary tract.",
        "advice": "Drink plenty of water. Antibiotics are usually required. See a doctor promptly.",
    },
    "kidney_stone": {
        "name": "Kidney Stone", "specialty": "urology",
        "urgency": "high", "emoji": "🪨",
        "symptoms": ["abdominal_pain","back_pain","painful_urination","blood_in_urine","nausea","vomiting"],
        "description": "Hard mineral deposits forming inside the kidneys.",
        "advice": "Drink 2–3 litres of water daily. Pain medication helps. Large stones need medical treatment.",
    },
    "kidney_disease": {
        "name": "Chronic Kidney Disease", "specialty": "nephrology",
        "urgency": "high", "emoji": "🫘",
        "symptoms": ["reduced_urine","leg_swelling","fatigue","nausea","itching","pale_skin","loss_appetite"],
        "description": "Progressive loss of kidney function over time.",
        "advice": "Control blood pressure and diabetes. Low-protein diet. Regular nephrology follow-up essential.",
    },
    "anemia": {
        "name": "Anemia", "specialty": "hematology",
        "urgency": "moderate", "emoji": "🩸",
        "symptoms": ["fatigue","pale_skin","dizziness","shortness_of_breath","palpitations","rapid_heartbeat","bruising"],
        "description": "Low red blood cell count reducing oxygen delivery.",
        "advice": "Eat iron-rich foods. Iron or vitamin supplements may be prescribed. Get a blood panel done.",
    },
    "allergy": {
        "name": "Allergic Reaction", "specialty": "immunology",
        "urgency": "moderate", "emoji": "🌿",
        "symptoms": ["sneezing","runny_nose","itching","rash","watery_eyes","nasal_congestion","skin_dryness"],
        "description": "Immune system overreaction to a foreign substance (allergen).",
        "advice": "Identify and avoid triggers. Antihistamines provide relief. Consult an allergist.",
    },
    "arthritis": {
        "name": "Arthritis / Rheumatoid Arthritis", "specialty": "rheumatology",
        "urgency": "low", "emoji": "🦴",
        "symptoms": ["joint_pain","leg_swelling","fatigue","morning_stiffness","swollen_joints","bone_pain"],
        "description": "Inflammation of joints causing pain and stiffness.",
        "advice": "Gentle exercise and anti-inflammatory medications help. Physical therapy recommended.",
    },
    "gout": {
        "name": "Gout", "specialty": "rheumatology",
        "urgency": "moderate", "emoji": "🦶",
        "symptoms": ["joint_pain","swollen_joints","abdominal_pain","nausea"],
        "description": "A form of arthritis caused by excess uric acid, causing sudden severe joint pain.",
        "advice": "Avoid red meat, alcohol, and sugary drinks. Colchicine or NSAIDs for acute attacks.",
    },
    "hypothyroidism": {
        "name": "Hypothyroidism", "specialty": "endocrinology",
        "urgency": "moderate", "emoji": "🦋",
        "symptoms": ["fatigue","weight_gain","depression","constipation","hair_loss","mood_swings","cold_intolerance","skin_dryness"],
        "description": "Under-active thyroid gland producing insufficient hormones.",
        "advice": "A TSH blood test confirms diagnosis. Daily thyroid hormone replacement is effective.",
    },
    "hyperthyroidism": {
        "name": "Hyperthyroidism / Graves' Disease", "specialty": "endocrinology",
        "urgency": "moderate", "emoji": "🔥",
        "symptoms": ["weight_loss","palpitations","anxiety","insomnia","excessive_sweating","heat_intolerance","bulging_eyes","goiter","rapid_heartbeat"],
        "description": "Over-active thyroid gland producing too much thyroid hormone.",
        "advice": "Blood tests (T3, T4, TSH) confirm diagnosis. Medication, radioiodine, or surgery are options.",
    },
    "malaria": {
        "name": "Malaria", "specialty": "infectious_disease",
        "urgency": "high", "emoji": "🦟",
        "symptoms": ["fever","chills","headache","nausea","vomiting","muscle_pain","night_sweats","fatigue"],
        "description": "Mosquito-borne parasitic infection common in tropical regions.",
        "advice": "Seek medical attention immediately. Antimalarial drugs are effective when started early.",
    },
    "dengue": {
        "name": "Dengue Fever", "specialty": "infectious_disease",
        "urgency": "high", "emoji": "🦟",
        "symptoms": ["fever","headache","muscle_pain","joint_pain","rash","nausea","vomiting","fatigue"],
        "description": "Mosquito-transmitted viral infection common in tropical and subtropical areas.",
        "advice": "No specific antiviral. Rest, fluids, paracetamol. Avoid NSAIDs. Hospitalisation if severe.",
    },
    "hepatitis": {
        "name": "Hepatitis (A/B/C)", "specialty": "gastroenterology",
        "urgency": "high", "emoji": "🫀",
        "symptoms": ["jaundice","fatigue","abdominal_pain","nausea","vomiting","loss_appetite","dark_stool","itching"],
        "description": "Viral inflammation of the liver affecting its normal functioning.",
        "advice": "Hepatitis B and C have effective treatments. Avoid alcohol. Complete the vaccination course.",
    },
    "stroke": {
        "name": "Stroke / TIA", "specialty": "neurology",
        "urgency": "critical", "emoji": "🧠",
        "symptoms": ["numbness","speech_difficulty","dizziness","loss_balance","confusion","fainting","blurred_vision","headache"],
        "description": "Brain attack — blood supply to part of brain is cut off.",
        "advice": "⚠️ CALL EMERGENCY SERVICES IMMEDIATELY. Time = Brain cells. Use FAST: Face/Arm/Speech/Time.",
    },
    "parkinson": {
        "name": "Parkinson's Disease", "specialty": "neurology",
        "urgency": "moderate", "emoji": "🔵",
        "symptoms": ["tremor","muscle_stiffness","loss_balance","slow_movement","memory_loss","depression"],
        "description": "Progressive neurological disorder affecting movement and brain function.",
        "advice": "Neurologist evaluation needed. Medication and physical therapy significantly improve quality of life.",
    },
    "lupus": {
        "name": "Systemic Lupus Erythematosus (SLE)", "specialty": "rheumatology",
        "urgency": "high", "emoji": "🦋",
        "symptoms": ["rash","joint_pain","fatigue","fever","hair_loss","chest_pain","kidney_disease"],
        "description": "Autoimmune disease where the immune system attacks its own tissues.",
        "advice": "Rheumatology consultation required. Avoid sun exposure. Hydroxychloroquine is a common treatment.",
    },
    "pcos": {
        "name": "PCOS (Polycystic Ovary Syndrome)", "specialty": "gynecology",
        "urgency": "moderate", "emoji": "🌸",
        "symptoms": ["irregular_periods","weight_gain","acne","hair_loss","pelvic_pain","mood_swings"],
        "description": "Hormonal disorder causing enlarged ovaries with small cysts.",
        "advice": "Lifestyle changes (diet + exercise) help. Hormonal therapy and metformin are effective treatments.",
    },
    "breast_cancer": {
        "name": "Breast Cancer (Screening)", "specialty": "oncology",
        "urgency": "high", "emoji": "🎗️",
        "symptoms": ["breast_lump","skin_sores","pain","weight_loss","fatigue"],
        "description": "Cancer originating in breast tissue — early detection is crucial.",
        "advice": "See a doctor immediately for any new breast lump. Mammogram and biopsy needed. Early treatment is very effective.",
    },
    "eczema": {
        "name": "Eczema / Atopic Dermatitis", "specialty": "dermatology",
        "urgency": "low", "emoji": "🧴",
        "symptoms": ["rash","itching","skin_dryness","redness"],
        "description": "Chronic inflammatory skin condition causing dry, itchy, inflamed skin.",
        "advice": "Moisturise frequently. Avoid harsh soaps. Topical steroids and antihistamines help.",
    },
    "psoriasis": {
        "name": "Psoriasis", "specialty": "dermatology",
        "urgency": "low", "emoji": "🧬",
        "symptoms": ["rash","itching","skin_dryness","joint_pain","nail_changes"],
        "description": "Autoimmune skin disease causing rapid skin cell build-up forming scales and red patches.",
        "advice": "Topical treatments, phototherapy, and biologics are effective. Avoid triggers like stress and alcohol.",
    },
    "meningitis": {
        "name": "Meningitis", "specialty": "infectious_disease",
        "urgency": "critical", "emoji": "🚨",
        "symptoms": ["headache","fever","neck_pain","confusion","nausea","vomiting","seizure","rash"],
        "description": "Inflammation of the protective membranes covering the brain and spinal cord.",
        "advice": "⚠️ MEDICAL EMERGENCY — Go to the ER immediately. Bacterial meningitis is life-threatening.",
    },
}

# ── Keyword → Symptom mapping ─────────────────────────────────
KEYWORD_MAP = {
    # Head
    "headache": ["headache"],            "head ache": ["headache"],
    "head pain": ["headache"],           "migraine": ["migraine", "headache"],
    "dizzy": ["dizziness"],              "dizziness": ["dizziness"],
    "lightheaded": ["dizziness"],        "vertigo": ["dizziness"],
    "confused": ["confusion"],           "confusion": ["confusion"],
    "seizure": ["seizure"],              "convulsion": ["seizure"],
    "memory": ["memory_loss"],           "forgetful": ["memory_loss"],
    "tremor": ["tremor"],                "shaking": ["tremor"],
    "shaky": ["tremor"],                 "numb": ["numbness"],
    "numbness": ["numbness"],            "tingling": ["numbness"],
    "pins and needles": ["numbness"],    "fainting": ["fainting"],
    "fainted": ["fainting"],             "blackout": ["fainting"],
    "pass out": ["fainting"],            "speech": ["speech_difficulty"],
    "slurred": ["speech_difficulty"],    "cant speak": ["speech_difficulty"],
    "balance": ["loss_balance"],         "unsteady": ["loss_balance"],
    "falling": ["loss_balance"],

    # Respiratory
    "cough": ["cough"],                  "coughing": ["cough"],
    "cough blood": ["coughing_blood"],   "blood sputum": ["coughing_blood"],
    "breath": ["shortness_of_breath"],   "breathing": ["shortness_of_breath"],
    "breathless": ["shortness_of_breath"],"short of breath": ["shortness_of_breath"],
    "wheeze": ["wheezing"],              "wheezing": ["wheezing"],
    "throat": ["sore_throat"],           "sore throat": ["sore_throat"],
    "runny nose": ["runny_nose"],        "runny": ["runny_nose"],
    "stuffy": ["nasal_congestion"],      "congestion": ["nasal_congestion"],
    "sneeze": ["sneezing"],              "sneezing": ["sneezing"],
    "lost smell": ["loss_smell"],        "cant smell": ["loss_smell"],
    "no taste": ["loss_smell"],          "hoarse": ["hoarseness"],
    "voice change": ["hoarseness"],

    # Constitutional
    "fever": ["fever"],                  "temperature": ["fever"],
    "hot": ["fever"],                    "chills": ["chills"],
    "shivering": ["chills"],             "tired": ["fatigue"],
    "fatigue": ["fatigue"],              "weakness": ["fatigue"],
    "weak": ["fatigue"],                 "sweats": ["night_sweats"],
    "night sweat": ["night_sweats"],     "weight loss": ["weight_loss"],
    "losing weight": ["weight_loss"],    "no appetite": ["loss_appetite"],
    "not hungry": ["loss_appetite"],     "loss of appetite": ["loss_appetite"],
    "sweating": ["excessive_sweating"],  "malaise": ["general_malaise"],
    "unwell": ["general_malaise"],       "weight gain": ["weight_gain"],
    "gaining weight": ["weight_gain"],

    # Cardiac
    "chest pain": ["chest_pain"],        "chest": ["chest_pain"],
    "chest tightness": ["chest_pain"],   "palpitation": ["palpitations"],
    "racing heart": ["palpitations"],    "heart beat": ["palpitations"],
    "irregular heart": ["irregular_heartbeat"],
    "fast heart": ["rapid_heartbeat"],   "slow heart": ["slow_heartbeat"],
    "swelling": ["leg_swelling"],        "swollen": ["leg_swelling"],
    "edema": ["leg_swelling"],           "blue lips": ["cyanosis"],
    "blue fingers": ["cyanosis"],

    # GI
    "nausea": ["nausea"],                "nauseous": ["nausea"],
    "sick": ["nausea"],                  "vomit": ["vomiting"],
    "vomiting": ["vomiting"],            "throwing up": ["vomiting"],
    "stomach": ["abdominal_pain"],       "abdomen": ["abdominal_pain"],
    "belly": ["abdominal_pain"],         "stomach pain": ["abdominal_pain"],
    "diarrhea": ["diarrhea"],            "loose stool": ["diarrhea"],
    "loose motions": ["diarrhea"],       "constipation": ["constipation"],
    "constipated": ["constipation"],     "bloat": ["bloating"],
    "gas": ["bloating"],                 "heartburn": ["heartburn"],
    "acid": ["heartburn"],               "reflux": ["heartburn"],
    "blood stool": ["blood_in_stool"],   "rectal bleeding": ["blood_in_stool"],
    "black stool": ["black_stool"],      "dark stool": ["black_stool"],
    "swallow": ["difficulty_swallowing"],"cramp": ["stomach_cramps"],
    "cramps": ["stomach_cramps"],

    # Musculoskeletal
    "joint": ["joint_pain"],             "joint pain": ["joint_pain"],
    "back": ["back_pain"],               "back pain": ["back_pain"],
    "backache": ["back_pain"],           "muscle": ["muscle_pain"],
    "body ache": ["muscle_pain"],        "ache": ["muscle_pain"],
    "stiff": ["morning_stiffness"],      "stiffness": ["morning_stiffness"],
    "neck pain": ["neck_pain"],          "neck stiff": ["neck_pain"],
    "neck": ["neck_pain"],               "bone pain": ["bone_pain"],
    "swollen joint": ["swollen_joints"], "muscle weak": ["muscle_weakness"],

    # Skin
    "rash": ["rash"],                    "hives": ["rash"],
    "itch": ["itching"],                 "itching": ["itching"],
    "itchy": ["itching"],                "yellow": ["jaundice"],
    "jaundice": ["jaundice"],            "pale": ["pale_skin"],
    "bruise": ["bruising"],              "bruising": ["bruising"],
    "dry skin": ["skin_dryness"],        "scaly": ["skin_dryness"],
    "acne": ["acne"],                    "pimple": ["acne"],
    "hair loss": ["hair_loss"],          "hair fall": ["hair_loss"],
    "nail": ["nail_changes"],            "skin sore": ["skin_sores"],

    # Urological
    "urination": ["frequent_urination"], "frequent urination": ["frequent_urination"],
    "urinate": ["frequent_urination"],   "pee": ["frequent_urination"],
    "painful urination": ["painful_urination"],
    "burning urination": ["painful_urination"],
    "blood urine": ["blood_in_urine"],   "blood in urine": ["blood_in_urine"],
    "cloudy urine": ["cloudy_urine"],    "no urine": ["reduced_urine"],
    "leaking": ["urinary_incontinence"],

    # Mental health
    "anxiety": ["anxiety"],              "anxious": ["anxiety"],
    "panic": ["panic_attacks"],          "panic attack": ["panic_attacks"],
    "worry": ["anxiety"],                "depression": ["depression"],
    "sad": ["depression"],               "depressed": ["depression"],
    "hopeless": ["depression"],          "insomnia": ["insomnia"],
    "sleepless": ["insomnia"],           "cant sleep": ["insomnia"],
    "mood swings": ["mood_swings"],      "hallucination": ["hallucinations"],
    "hearing voices": ["hallucinations"],"paranoid": ["paranoia"],
    "brain fog": ["poor_concentration"], "concentration": ["poor_concentration"],

    # Vision/ENT
    "vision": ["blurred_vision"],        "blurred": ["blurred_vision"],
    "blurry": ["blurred_vision"],        "double vision": ["double_vision"],
    "eye pain": ["eye_pain"],            "red eye": ["eye_pain"],
    "ear pain": ["ear_pain"],            "earache": ["ear_pain"],
    "hearing loss": ["hearing_loss"],    "deaf": ["hearing_loss"],
    "ringing": ["ringing_ears"],         "tinnitus": ["ringing_ears"],
    "watery eyes": ["watery_eyes"],

    # Endocrine
    "thirst": ["excessive_thirst"],      "thirsty": ["excessive_thirst"],
    "hungry": ["increased_hunger"],      "always eating": ["increased_hunger"],
    "cold intolerance": ["cold_intolerance"],
    "heat intolerance": ["heat_intolerance"],
    "bulging eye": ["bulging_eyes"],     "goiter": ["goiter"],
    "neck lump": ["goiter"],

    # Women's health
    "irregular period": ["irregular_periods"],
    "missed period": ["irregular_periods"],
    "pelvic pain": ["pelvic_pain"],      "pelvis": ["pelvic_pain"],
    "discharge": ["vaginal_discharge"],  "breast lump": ["breast_lump"],
    "hot flash": ["hot_flashes"],        "hot flashes": ["hot_flashes"],
}

# ── Doctors ───────────────────────────────────────────────────
DOCTORS = [
    # General Practice
    {"id":1,  "name":"Dr. Priya Sharma",    "specialty":"general",           "title":"General Physician",              "rating":4.9, "exp":12, "avatar":"PS", "color":"#818cf8", "location":"Apollo Medical Centre, Mumbai",        "slots":["09:00 AM","10:30 AM","02:00 PM","04:00 PM","05:30 PM"], "fee":500},
    {"id":2,  "name":"Dr. Rahul Bhatia",    "specialty":"general",           "title":"Family Medicine Specialist",     "rating":4.7, "exp":9,  "avatar":"RB", "color":"#6ee7b7", "location":"LifeCare Clinic, Bengaluru",           "slots":["08:30 AM","11:00 AM","01:00 PM","03:30 PM"],           "fee":450},

    # Cardiology
    {"id":3,  "name":"Dr. Arjun Mehta",     "specialty":"cardiology",         "title":"Interventional Cardiologist",    "rating":4.9, "exp":18, "avatar":"AM", "color":"#f87171", "location":"Heart Care Institute, Delhi",           "slots":["10:00 AM","11:30 AM","03:00 PM","05:00 PM"],           "fee":1200},
    {"id":4,  "name":"Dr. Lalita Krishnan", "specialty":"cardiology",         "title":"Cardiac Electrophysiologist",    "rating":4.8, "exp":14, "avatar":"LK", "color":"#fca5a5", "location":"Fortis Heart Hospital, Chennai",        "slots":["09:30 AM","12:00 PM","02:30 PM"],                      "fee":1400},

    # Neurology
    {"id":5,  "name":"Dr. Sneha Reddy",     "specialty":"neurology",          "title":"Neurologist",                    "rating":4.8, "exp":15, "avatar":"SR", "color":"#c4b5fd", "location":"Neuro Wellness Clinic, Hyderabad",     "slots":["09:30 AM","12:00 PM","02:30 PM","05:00 PM"],           "fee":1000},
    {"id":6,  "name":"Dr. Sameer Jain",     "specialty":"neurology",          "title":"Stroke & Movement Specialist",   "rating":4.7, "exp":20, "avatar":"SJ", "color":"#a78bfa", "location":"Brain & Spine Centre, Mumbai",         "slots":["10:00 AM","01:00 PM","04:00 PM"],                      "fee":1500},

    # Pulmonology
    {"id":7,  "name":"Dr. Rajiv Kumar",     "specialty":"pulmonology",        "title":"Pulmonologist",                  "rating":4.8, "exp":14, "avatar":"RK", "color":"#7dd3fc", "location":"Breath Easy Hospital, Chennai",         "slots":["08:30 AM","11:00 AM","01:30 PM","04:30 PM"],           "fee":900},
    {"id":8,  "name":"Dr. Anita Menon",     "specialty":"pulmonology",        "title":"Respiratory & TB Specialist",    "rating":4.7, "exp":16, "avatar":"AM2","color":"#38bdf8", "location":"Lung Health Centre, Kochi",             "slots":["09:00 AM","12:30 PM","03:00 PM"],                      "fee":850},

    # Gastroenterology
    {"id":9,  "name":"Dr. Ananya Singh",    "specialty":"gastroenterology",   "title":"Gastroenterologist",             "rating":4.6, "exp":10, "avatar":"AS", "color":"#fb923c", "location":"Gut Health Clinic, Bangalore",          "slots":["10:00 AM","01:00 PM","03:30 PM"],                      "fee":850},
    {"id":10, "name":"Dr. Rohan Malhotra",  "specialty":"gastroenterology",   "title":"Hepatologist & Endoscopist",     "rating":4.8, "exp":17, "avatar":"RM", "color":"#fdba74", "location":"Liver & Digestive Institute, Delhi",    "slots":["09:30 AM","11:30 AM","02:00 PM","04:30 PM"],           "fee":1100},

    # Psychiatry / Mental Health
    {"id":11, "name":"Dr. Vikram Patel",    "specialty":"psychiatry",         "title":"Psychiatrist",                   "rating":4.9, "exp":20, "avatar":"VP", "color":"#34d399", "location":"Mind & Soul Centre, Pune",             "slots":["09:00 AM","11:00 AM","02:00 PM","05:00 PM"],           "fee":1100},
    {"id":12, "name":"Dr. Riya Chatterjee", "specialty":"psychiatry",         "title":"Psychotherapist & Counsellor",   "rating":4.8, "exp":13, "avatar":"RC", "color":"#6ee7b7", "location":"Serene Mind Clinic, Kolkata",           "slots":["10:00 AM","12:00 PM","03:00 PM","05:30 PM"],           "fee":1000},

    # Endocrinology
    {"id":13, "name":"Dr. Meera Nair",      "specialty":"endocrinology",      "title":"Endocrinologist & Diabetologist","rating":4.7, "exp":13, "avatar":"MN", "color":"#fbbf24", "location":"Hormone Health Clinic, Kochi",          "slots":["10:30 AM","12:30 PM","03:00 PM"],                      "fee":950},
    {"id":14, "name":"Dr. Sunil Agarwal",   "specialty":"endocrinology",      "title":"Thyroid & Metabolic Specialist",  "rating":4.6, "exp":11, "avatar":"SA", "color":"#fde68a", "location":"Endocrine Centre, Jaipur",             "slots":["09:00 AM","11:30 AM","02:30 PM","04:00 PM"],           "fee":900},

    # Urology
    {"id":15, "name":"Dr. Suresh Iyer",     "specialty":"urology",            "title":"Urologist",                      "rating":4.7, "exp":16, "avatar":"SI", "color":"#60a5fa", "location":"Urology & Kidney Centre, Chennai",      "slots":["09:00 AM","11:30 AM","02:00 PM","04:30 PM"],           "fee":1000},
    {"id":16, "name":"Dr. Prateek Gupta",   "specialty":"urology",            "title":"Uro-Oncologist",                  "rating":4.9, "exp":21, "avatar":"PG", "color":"#3b82f6", "location":"Urological Sciences Hospital, Delhi",   "slots":["10:00 AM","01:30 PM","04:00 PM"],                      "fee":1300},

    # Nephrology
    {"id":17, "name":"Dr. Deepti Acharya",  "specialty":"nephrology",         "title":"Nephrologist / Kidney Specialist","rating":4.8, "exp":15, "avatar":"DA", "color":"#67e8f9", "location":"Kidney Care Centre, Hyderabad",         "slots":["09:00 AM","11:00 AM","02:30 PM","05:00 PM"],           "fee":1050},

    # Immunology / Allergy
    {"id":18, "name":"Dr. Kavya Bose",      "specialty":"immunology",         "title":"Allergist / Immunologist",        "rating":4.8, "exp":11, "avatar":"KB", "color":"#f472b6", "location":"AllerCare Clinic, Kolkata",             "slots":["09:30 AM","12:00 PM","04:00 PM"],                      "fee":750},

    # Rheumatology
    {"id":19, "name":"Dr. Aditya Rao",      "specialty":"rheumatology",       "title":"Rheumatologist",                  "rating":4.7, "exp":17, "avatar":"AR", "color":"#c084fc", "location":"Joint & Bone Clinic, Hyderabad",        "slots":["10:00 AM","01:30 PM","03:30 PM"],                      "fee":900},
    {"id":20, "name":"Dr. Nidhi Joshi",     "specialty":"rheumatology",       "title":"Arthritis & Autoimmune Specialist","rating":4.8, "exp":12,"avatar":"NJ", "color":"#e879f9", "location":"Arthritis Foundation, Ahmedabad",       "slots":["09:00 AM","11:30 AM","02:00 PM"],                      "fee":950},

    # Hematology
    {"id":21, "name":"Dr. Deepa Joshi",     "specialty":"hematology",         "title":"Hematologist",                    "rating":4.8, "exp":14, "avatar":"DJ", "color":"#f43f5e", "location":"Blood & Cancer Care, Mumbai",           "slots":["11:00 AM","01:00 PM","04:00 PM"],                      "fee":1050},

    # Infectious Disease
    {"id":22, "name":"Dr. Nikhil Gupta",    "specialty":"infectious_disease", "title":"Infectious Disease Specialist",   "rating":4.9, "exp":19, "avatar":"NG", "color":"#2dd4bf", "location":"Tropical Disease Centre, Delhi",        "slots":["09:00 AM","11:30 AM","02:30 PM"],                      "fee":1000},

    # Surgery
    {"id":23, "name":"Dr. Pooja Verma",     "specialty":"surgery",            "title":"General & Laparoscopic Surgeon",  "rating":4.9, "exp":22, "avatar":"PV", "color":"#ef4444", "location":"City Surgical Hospital, Mumbai",        "slots":["08:00 AM","10:00 AM","12:00 PM"],                      "fee":1500},

    # Gynecology
    {"id":24, "name":"Dr. Sunita Kapoor",   "specialty":"gynecology",         "title":"Gynaecologist & Obstetrician",    "rating":4.9, "exp":18, "avatar":"SK", "color":"#fb7185", "location":"Women's Care Hospital, Delhi",          "slots":["09:00 AM","11:00 AM","01:00 PM","03:30 PM"],           "fee":900},
    {"id":25, "name":"Dr. Manjula Iyer",    "specialty":"gynecology",         "title":"Reproductive Medicine Specialist","rating":4.8, "exp":15, "avatar":"MI", "color":"#fda4af", "location":"Fertility & Women's Clinic, Chennai",   "slots":["10:00 AM","12:00 PM","03:00 PM"],                      "fee":1100},

    # Dermatology
    {"id":26, "name":"Dr. Priti Sehgal",    "specialty":"dermatology",        "title":"Dermatologist & Cosmetologist",   "rating":4.8, "exp":13, "avatar":"PS2","color":"#fb923c", "location":"Skin & Hair Clinic, Pune",             "slots":["09:30 AM","11:30 AM","02:00 PM","04:30 PM"],           "fee":800},

    # Oncology
    {"id":27, "name":"Dr. Ashwin Tiwari",   "specialty":"oncology",           "title":"Medical Oncologist",              "rating":4.9, "exp":24, "avatar":"AT", "color":"#a3e635", "location":"Cancer Care Institute, Mumbai",         "slots":["09:00 AM","11:00 AM","02:00 PM"],                      "fee":2000},
]

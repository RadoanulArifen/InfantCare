from rapidfuzz import fuzz
import re
from symptom_data import TARGET_DISEASES, chatbot_symptom_keywords, chatbot_negation_phrases

# ================== 2) Text normalize + fuzzy score helper ==================

def normalize_text(text: str) -> str:
    t = str(text).lower()
    t = re.sub(r"\s+", " ", t).strip()
    return t

def match_phrase(text_norm: str, phrase: str, fuzzy_threshold: int = 85) -> bool:
    """
    Returns True if the phrase matches (exact or fuzzy).
    """
    p = phrase.lower().strip()
    
    # Exact match
    if p in text_norm:
        return True
        
    # Fuzzy match - Use token_set_ratio to handle inserted words 
    # e.g. "feels kinda hot" matches "feels hot"
    sim = fuzz.token_set_ratio(text_norm, p)
    return sim >= fuzzy_threshold

def analyze_symptoms_weighted(symptom_text: str):
    """
    For each disease, sum up weighted scores.
    Returns:
      - scores: {disease: float_score}
      - evidence: {disease: [matched_phrases]}
    """
    t = normalize_text(symptom_text)
    scores = {d: 0.0 for d in TARGET_DISEASES}
    evidence = {d: [] for d in TARGET_DISEASES}

    for disease, weighted_phrases in chatbot_symptom_keywords.items():
        # Negation check
        neg_list = chatbot_negation_phrases.get(disease, [])
        if any(neg in t for neg in neg_list):
            continue

        # Weighted matching
        for phrase, weight in weighted_phrases:
            if match_phrase(t, phrase):
                # Avoid double counting if multiple similar phrases match? 
                # For simplicity in this research prototype, we sum them, 
                # but might want to limit to unique hits per concept in future.
                # A simple de-duplication: if we haven't already matched this exact phrase
                if phrase not in evidence[disease]:
                    scores[disease] += weight
                    evidence[disease].append(phrase)

    return scores, evidence


# ================== 3) Age + Temperature rules ==================

def apply_clinical_rules(scores, evidence, age_months, temp_value, unit="F"):
    """
    Adjust scores based on Vitals (Temp) and Safety Rules.
    Input temp_value can be in F or C, specified by unit.
    """
    final_scores = scores.copy()
    
    # Temperature Rule
    tv = None
    if temp_value is not None:
        try:
            tv = float(temp_value)
        except:
            pass

    if tv is not None:
        display_str = f"{tv}°{unit}"
        
        is_high_fever = False
        is_fever = False
        is_normal = False
        
        # User Defined Custom Rules
        if unit == "F":
             # Normal: 97.5°F – 98.6°F
             # Fever: 98.7°F or higher
             # High fever: 102°F+
             if tv >= 102.0:
                 is_high_fever = True
             elif tv >= 98.7:
                 is_fever = True
             elif tv <= 98.6:
                 is_normal = True
        else: # Unit == "C"
             # Normal: 36.4°C – 37.0°C
             # Fever: 37.1°C or higher
             # High fever: 38.9°C+
             if tv >= 38.9:
                 is_high_fever = True
             elif tv >= 37.1:
                 is_fever = True
             elif tv <= 37.0:
                 is_normal = True

        # Apply Scoring based on classification
        # IMPORTANT: If we have a valid temp reading, it overrides subjective text scores.
        # Reset fever score to 0 and rely solely on the thermometer.
        if is_high_fever or is_fever or is_normal:
            final_scores["fever"] = 0.0 

        if is_high_fever:
            # High assurance (+5)
            final_scores["fever"] += 5.0 
            evidence["fever"].append(f"High Fever ({display_str})")
        elif is_fever:
            # Standard assurance (+3) -> Medium Confidence
            final_scores["fever"] += 3.0
            evidence["fever"].append(f"Fever Detected ({display_str})")
        elif is_normal:
            # Penalize subjective fever (Score -3.0)
            final_scores["fever"] -= 3.0
            evidence["fever"].append(f"Normal Temp ({display_str})")

    return final_scores

# ================== 4) Confidence & Priority ==================

def get_confidence_level(score):
    if score >= 4.0:
        return "High"
    elif score >= 2.0:
        return "Medium"
    else:
        return "Low"

def get_final_assessment(symptom_text, age_months, temp_value, unit="F"):
    base_scores, evidence = analyze_symptoms_weighted(symptom_text)
    final_scores = apply_clinical_rules(base_scores, evidence, age_months, temp_value, unit)
    
    # Determine active flags based on thresholds
    # Threshold 1.5 ensures at least one "Standard" symptom or multiple "Weak" ones
    flags = {d: 1 if s >= 1.5 else 0 for d, s in final_scores.items()}
    

    
    # Special strict rule for Fever if no temp is provided: need strong text evidence
    # (already handled by weights: 'fever' is 1.5, 'warm' is only 1.0)

    # Sort by score
    priority = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
    
    return flags, final_scores, priority, evidence


# ================== 5) Response Builder ==================

def build_support_message(symptom_text, flags, scores, priority, evidence, age, temp, unit="F"):
    active = [d for d, v in flags.items() if v == 1]

    name_map = {
        "fever": "Fever / Pyrexia",
        "diarrhea": "Diarrhea / Dehydration Risk",
        "ear infection": "Ear Infection (Otitis Media)",
        "skin infection": "Skin Infection / Dermatitis",
        "ari": "Respiratory Infection (ARI)"
    }

    result_data = {
        "found_issues": False,
        "input_summary": {
            "symptoms": symptom_text.strip(),
            "age": age,
            "temp": f"{temp}°{unit}" if temp else "Not recorded"
        },
        "conditions": [],
        "general_advice": [],
        "emergency_warnings": []
    }

    if not active:
        result_data["found_issues"] = False
        return result_data

    result_data["found_issues"] = True

    # 1. Populate Conditions with Confidence & Evidence
    for d, sc in priority:
        if d not in active:
            continue
        
        confidence = get_confidence_level(sc)
        matched_terms = ", ".join([f"'{e}'" for e in evidence[d][:3]]) # Show top 3
        if len(evidence[d]) > 3:
            matched_terms += ", ..."

        detail_text = f"Detected based on: {matched_terms}"

        result_data["conditions"].append({
            "name": name_map.get(d, d.title()),
            "id": d,
            "detail": detail_text,
            "confidence": confidence,
            "score": round(sc, 1)
        })

    # 2. Populate Advice (Standard)
    if "fever" in active:
        result_data["general_advice"].append("Hydration: Offer plenty of fluids/breast milk.")
        result_data["general_advice"].append("Medication: Consult doctor for Paracetamol dosage if uncomfortable.")
    if "diarrhea" in active:
        result_data["general_advice"].append("Rehydration: Use Oral Rehydration Solution (ORS) after each loose stool.")
        result_data["general_advice"].append("Zinc: Zinc supplements (20mg/day) for 14 days are recommended by WHO.")
    if "ear infection" in active:
        result_data["general_advice"].append("Pain Management: Warm compress may help. Do not insert objects into ear.")
    if "skin infection" in active:
        result_data["general_advice"].append("Hygiene: Keep area clean/dry. Wash hands before touching baby.")
    if "ari" in active:
        result_data["general_advice"].append("Comfort: Keep nose clear with saline drops. Keep baby upright.")

    # 3. Emergency Warnings
    result_data["emergency_warnings"] = [
        "Difficulty Breathing (Fast breathing, chest indrawing, grunting).",
        "Altered Consciousness (Hard to wake, very drowsy).",
        "Severe Dehydration (Sunken eyes, no tears, dry mouth).",
        "High Fever (>104°F) or Fever > 3 days."
    ]

    return result_data

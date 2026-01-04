# ================== CONFIG: disease list ==================
TARGET_DISEASES = ["ari", "diarrhea", "ear infection", "fever", "skin infection"]

# ================== 1) Rich phrase dictionary (Weighted) ==================
# Format: "keyword": [(phrase, weight), ...]
# Weight guide: 3.0 (Strong/Explicit), 1.5 (Standard), 0.8 (Vague/Casual)

chatbot_symptom_keywords = {
    "fever": [
        # direct fever (Strong)
        ("on fire", 2.5),
        ("burning up", 2.5),
        ("glowing hot", 2.0),
        ("high fever", 3.0),
        ("running a fever", 2.0),
        ("has a fever", 2.0),
        ("fever", 1.5),
        
        # hot body (Medium/Strong)
        ("burning up", 2.5),
        ("body is hot", 2.0),
        ("feels hot", 2.0),
        ("very hot to touch", 2.0),
        ("temperature is high", 2.0),
        
        # casual/vague (Low/Medium)
        ("warm to touch", 1.0),
        ("feels very warm", 1.0),
        ("feels hotter than usual", 1.0),
        ("hot head", 1.0),
        ("feverish", 1.0),
        ("warm head", 0.8),
        
        # typos
        ("feaver", 1.5),
        ("feverr", 1.5),
        ("feverishness", 1.5),
        
        # Human-like descriptions
        ("head is burning", 2.0),
        ("forehead is hot", 2.0),
        ("sweating through clothes", 1.5),
        ("feels like an oven", 1.5),
        ("shaking from cold", 1.5),
        ("body is very warm", 1.5),
        ("too hot to touch", 2.0),
    ],

    "diarrhea": [
        # explicit (Strong)
        ("watery stool", 3.0),
        ("liquid stool", 3.0),
        ("loose stool", 2.5),
        ("diarrhea", 3.0),
        ("loose motion", 2.5),
        ("exploded in diaper", 2.5),
        ("exploded in his diaper", 2.5),
        ("exploded in her diaper", 2.5),
        ("messy diaper", 2.0),
        
        # typos
        ("diarea", 2.5),
        ("diarrea", 2.5),
        ("diarhea", 2.5),
        ("poo", 1.0),
        
        # frequency (Medium)
        ("frequent stool", 2.0),
        ("pooping again and again", 2.0),
        ("many times poop", 1.5),
        ("going to toilet a lot", 1.5),
        
        # casual (Medium/Low)
        ("runny poop", 1.5),
        ("water coming instead of stool", 2.0),
        ("poop looks like water", 2.0),
        ("stomach bug", 1.0),
        
        # Human-like descriptions
        ("poop is like juice", 2.5),
        ("yellow water", 2.0),
        ("dirty diaper all the time", 1.5),
        ("pooping every hour", 2.0),
        ("messy poop", 1.5),
        ("loose motions", 2.0),
        ("watery diarrhea", 3.0),
    ],

    "skin infection": [
        # explicit (Strong)
        ("rash", 2.0),
        ("skin rash", 2.5),
        ("red rash", 2.5),
        ("pus filled blister", 3.0),
        ("blister", 2.0),
        
        # descriptive (Medium)
        ("red spots", 1.5),
        ("itchy skin", 1.5),
        ("scratching a lot", 1.5),
        ("red patches", 1.5),
        ("pimples", 1.5),
        
        # casual (Low)
        ("skin looks irritated", 1.0),
        ("red dots", 1.0),
        ("bumpy skin", 1.0),
        ("bumps", 1.5),
        ("red bumps", 2.0),
        
        # Human-like descriptions
        ("skin is peeling", 2.0),
        ("crusty skin", 2.0),
        ("scratched it open", 1.5),
        ("angry red rash", 2.5),
        ("weird marks on skin", 1.5),
        ("skin is dry and flaky", 1.5),
        ("pimply", 1.5),
    ],

    "ear infection": [
        # explicit pain (Strong)
        ("ear pain", 3.0),
        ("pain in ear", 3.0),
        ("discharge from ear", 3.0),
        ("fluid coming from ear", 3.0),
        
        # behavior (Medium)
        ("pulling ear", 2.0),
        ("screaming", 2.0),
        ("screams", 2.0),
        ("tugging ear", 2.0),
        ("holding ear", 1.5),
        ("rubbing ear", 1.5),
        ("cries when ear is touched", 2.5),
        
        # casual (Low)
        ("touching ear", 1.0),
        ("playing with ear", 0.8),
        
        # Human-like descriptions
        ("banging head", 2.0),
        ("cries when lying down", 2.0),
        ("wont let me touch head", 2.0),
        ("ear is red", 1.5),
        ("smelly fluid from ear", 3.0),
        ("bad smell from ear", 2.5),
        ("hitting side of head", 2.0),
    ],

    "ari": [
        # breathing (Critical/Strong)
        ("difficulty breathing", 3.0),
        ("struggling to breathe", 3.0),
        ("shortness of breath", 3.0),
        ("wheezing", 3.0),
        ("fast breathing", 2.5),
        ("ribs moving in", 3.0),
        ("ribs sucking in", 3.0),
        
        # cough/cold (Medium)
        ("cough", 1.5),
        ("bad cough", 2.0),
        ("cold and cough", 2.0),
        ("chest cough", 2.0),
        
        # nose (Low/Medium)
        ("runny nose", 1.0),
        ("blocked nose", 1.0),
        ("snotty nose", 1.0),
        ("nasal congestion", 1.0),
        ("chest is noisy", 1.5),
        
        # Human-like descriptions
        ("whistling breath", 2.5),
        ("chest is tight", 2.5),
        ("barking cough", 2.5),
        ("can't catch breath", 3.0),
        ("heavy breathing", 2.0),
        ("breathing sounds like a whistle", 2.5),
        ("phlegm", 1.5),
        ("lots of mucus", 1.5),
    ]
}


# Optional: phrases that mean a symptom is NOT present
chatbot_negation_phrases = {
    "ari": [
        # cough/cold negation
        "no cough", "not coughing", "does not cough", "never cough",
        "no cold", "not cold", "no runny nose", "nose not runny",
        # breathing negation
        "no breathing problem", "no breathing problems",
        "no breathing issue", "no breathing issues",
        "breathing normal", "breathing is normal",
        "breathing fine", "breathing ok", "breathing okay",
        "not breathing fast", "not fast breathing",
        "no difficulty breathing",
        "no signs of cough or cold",
    ],
    "fever": [
        "no fever", "not feverish", "no high fever",
        "not hot", "body is not hot", "temperature normal"
    ],
    "diarrhea": [
        "no diarrhea", "not diarrhea",
        "no loose stool", "no watery stool",
        "normal poop", "stool is normal"
    ],
    "ear infection": [
        "no ear pain", "ear is fine",
        "not touching ear", "no issue in ear"
    ],
    "skin infection": [
        "no rash", "no skin rash", "no itching", 
        "skin looks fine", "skin normal"
    ]
}

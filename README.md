# Infant Care Chatbot (Research-Grade)

An advanced pediatric symptom assessment AI that uses weighted logic and fuzzy matching to distinguish between subjective descriptions and clinical reality.

## Features
- **Research-Grade Logic**: Differentiates between "warm" (subjective) and "102°F" (clinical fever).
- **Weighted Scoring**: Prioritizes explicit medical terms over vague descriptions.
- **Objective Dominance**: Thermometer readings override subjective panic text.
- **Explainable AI**: Displays "Evidence" for every detected condition.
- **Premium UI**: Glassmorphism, card-based results, and responsive design.

## Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Open browser: `https://infant-care-chatbot.onrender.com/`
  

## Files
- `app.py`: Web server (Flask).
- `core_logic.py`: Scoring algorithms and clinical rules.
- `symptom_data.py`: Medical knowledge base (keywords/weights).

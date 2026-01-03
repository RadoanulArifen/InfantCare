from flask import Flask, render_template, request
from core_logic import get_final_assessment, build_support_message

app = Flask(__name__)

# ================== 6) Flask routes ==================

@app.route("/", methods=["GET"])
def index():
    # Render the splash/demo page
    return render_template("demo.html")


@app.route("/assessment", methods=["GET", "POST"])
def assessment():
    # GET: show the full assessment form (no results yet)
    if request.method == "GET":
        return render_template(
            "index.html",
            result_data=None,
            symptom_value="",
            age_value="",
            temp_value=""
        )

    # POST: process the submitted form and render results in `index.html`
    result_data = None
    symptom = request.form.get("symptom", "")
    age = request.form.get("age", "")
    temp = request.form.get("temp", "")

    if not symptom.strip():
        result_text = "Please describe your child's symptoms."
    else:
        try:
            age_val = float(age) if age.strip() != "" else None
        except:
            age_val = None

        try:
            temp_val = float(temp) if temp.strip() != "" else None
        except:
            temp_val = None

        from core_logic import get_final_assessment

        flags, scores, priority, evidence = get_final_assessment(symptom, age_val, temp_val)
        result_data = build_support_message(symptom, flags, scores, priority, evidence, age_val, temp_val)

    return render_template(
        "index.html",
        result_data=result_data,
        symptom_value=symptom,
        age_value=age,
        temp_value=temp
    )

if __name__ == "__main__":
    app.run(debug=True)

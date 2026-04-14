# -wca-ai-tool--CV-REVIEWER-
 from flask import Flask, render_template, request
import PyPDF2
import pytesseract
from PIL import Image
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# 🔴 SET THIS PATH (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# -------- FILE READING --------
def read_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.lower()


def read_image(file):
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    return text.lower()


def extract_text(file):
    filename = file.filename.lower()
    if filename.endswith(".pdf"):
        return read_pdf(file)
    elif filename.endswith((".png", ".jpg", ".jpeg")):
        return read_image(file)
    return ""


# -------- SCORING --------
def score_cv(text):
    score = 0
    feedback = []

    sections = {
        "education": 15,
        "experience": 20,
        "skills": 15,
        "projects": 10
    }

    for section, pts in sections.items():
        if section in text:
            score += pts
            feedback.append(f"{section} ✔ (+{pts})")
        else:
            feedback.append(f"{section} ❌ (0/{pts})")

    if "@" in text:
        score += 10
        feedback.append("email ✔ (+10)")
    else:
        feedback.append("email ❌")

    if len(text) > 1000:
        score += 10
        feedback.append("good length ✔ (+10)")
    else:
        feedback.append("too short ⚠")

    keywords = ["python", "teamwork", "leadership", "communication"]
    found = sum(1 for k in keywords if k in text)
    score += (found / len(keywords)) * 20

    return int(score), feedback


# -------- AI FEEDBACK --------
def smart_feedback(text):
    tips = []

    if "responsible for" in text:
        tips.append("👉 Replace 'responsible for' with action verbs (e.g. 'developed', 'led')")

    if "i" in text:
        tips.append("👉 Avoid using 'I' in CV")

    if len(text.split()) < 300:
        tips.append("👉 Add more details to your experience")

    if "project" not in text:
        tips.append("👉 Add projects to strengthen your CV")

    return tips


# -------- JOB MATCHING --------
def job_match(cv_text, job_text):
    docs = [cv_text, job_text]

    vectorizer = CountVectorizer().fit_transform(docs)
    vectors = vectorizer.toarray()

    similarity = cosine_similarity(vectors)[0][1]
    return int(similarity * 100)


# -------- ROUTE --------
@app.route("/", methods=["GET", "POST"])
def index():
    result = {}

    if request.method == "POST":
        file = request.files["cv"]
        job_desc = request.form["job"]

        text = extract_text(file)

        score, feedback = score_cv(text)
        tips = smart_feedback(text)
        match = job_match(text, job_desc)

        result = {
            "score": score,
            "feedback": feedback,
            "tips": tips,
            "match": match
        }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)


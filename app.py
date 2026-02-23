from flask import Flask, request, jsonify
from flask_cors import CORS
from pypdf import PdfReader
import requests
import groq

app = Flask(__name__)
CORS(app)

# روابط PDF الخام من GitHub
GITHUB_PDFS = [
    "https://raw.githubusercontent.com/waillydomour-adam/enshaei-backend/main/Prompt_Part_1.pdf",
    "https://raw.githubusercontent.com/waillydomour-adam/enshaei-backend/main/Prompt_Part_2.pdf",
    "https://raw.githubusercontent.com/waillydomour-adam/enshaei-backend/main/Prompt_Part_3.pdf",
    "https://raw.githubusercontent.com/waillydomour-adam/enshaei-backend/main/random-230117164555-17eca030.pdf",
    "https://raw.githubusercontent.com/waillydomour-adam/enshaei-backend/main/%D9%83%D8%AA%D8%A7%D8%A8_%D8%A7%D9%84%D8%AA%D8%B9%D9%84%D9%8A%D9%85%D8%A7%D8%AA_%D8%A7%D9%84%D9%81%D9%86%D9%8A%D8%A9_2025.pdf"
]

# تحميل محتوى PDF
pdf_texts = []
for url in GITHUB_PDFS:
    r = requests.get(url)
    reader = PdfReader(r.content)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    pdf_texts.append(text)

@app.route("/")
def home():
    return "Flask app is running ✅"

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question", "").lower()
    
    # مثال بحث بسيط داخل النصوص
    answer = ""
    for text in pdf_texts:
        if user_question in text.lower():
            answer = text
            break
    
    if not answer:
        answer = "عذرًا، لم أجد إجابة دقيقة. يمكنك البحث عنها، وسنقوم بتحديث البيانات لاحقًا."
    
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
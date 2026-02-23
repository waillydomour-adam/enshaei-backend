import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from pypdf import PdfReader
import groq

app = Flask(__name__)
CORS(app)

# روابط Raw لملفات PDF على GitHub
GITHUB_PDFS = [
    "https://raw.githubusercontent.com/waillydomour-adam/enshaei-backend/main/Prompt_Part_1.pdf",
    "https://raw.githubusercontent.com/waillydomour-adam/enshaei-backend/main/Prompt_Part_2.pdf",
    "https://raw.githubusercontent.com/waillydomour-adam/enshaei-backend/main/Prompt_Part_3.pdf",
    "https://raw.githubusercontent.com/waillydomour-adam/enshaei-backend/main/random-230117164555-17eca030.pdf",
    "https://raw.githubusercontent.com/waillydomour-adam/enshaei-backend/main/%D9%83%D8%AA%D8%A7%D8%A8_%D8%A7%D9%84%D8%AA%D8%B9%D9%84%D9%8A%D9%85%D8%A7%D8%AA_%D8%A7%D9%84%D9%81%D9%86%D9%8A%D8%A9_2025.pdf"
]

# تحميل نصوص PDF مرة واحدة عند تشغيل السيرفر
PDF_TEXTS = []

for url in GITHUB_PDFS:
    try:
        response = requests.get(url)
        response.raise_for_status()
        reader = PdfReader(response.content)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        PDF_TEXTS.append(text)
    except Exception as e:
        print(f"خطأ عند تحميل أو قراءة الملف {url}: {e}")


@app.route("/", methods=["GET"])
def home():
    return "Enshaei Backend is live ✅"


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"answer": "الرجاء إرسال سؤال صحيح."})

    # البحث البسيط داخل PDF_TEXTS
    answer = None
    for doc in PDF_TEXTS:
        if question.lower() in doc.lower():
            answer = f"Found in documents: {question}"
            break

    if not answer:
        # هنا يمكن استدعاء groq أو أي ذكاء صناعي خارجي لاحقًا
        answer = (
            "نعتذر، لا تتوفر إجابة للسؤال الآن. "
            "يمكنك البحث عنها بنفسك، وسنقوم بتحديث البيانات لاحقًا."
        )

    return jsonify({"answer": answer})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
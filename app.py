import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from pypdf import PdfReader
from io import BytesIO

app = Flask(__name__)
CORS(app)

# روابط Raw الخاصة بملفات PDF على GitHub
GITHUB_PDFS = [
    "https://raw.githubusercontent.com/waillydomour-adam/enshaei-backend/main/Prompt_Part_1.pdf",
    "https://raw.githubusercontent.com/waillydomour-adam/enshaei-backend/main/Prompt_Part_2.pdf",
    "https://raw.githubusercontent.com/waillydomour-adam/enshaei-backend/main/Prompt_Part_3.pdf",
    "https://raw.githubusercontent.com/waillydomour-adam/enshaei-backend/main/random-230117164555-17eca030.pdf",
    "https://raw.githubusercontent.com/waillydomour-adam/enshaei-backend/main/%D9%83%D8%AA%D8%A7%D8%A8_%D8%A7%D9%84%D8%AA%D8%B9%D9%84%D9%8A%D9%85%D8%A7%D8%AA_%D8%A7%D9%84%D9%81%D9%86%D9%8A%D8%A9_2025.pdf"
]

pdf_texts = []

# تنزيل وقراءة ملفات PDF عند تشغيل السيرفر
for url in GITHUB_PDFS:
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        reader = PdfReader(BytesIO(resp.content))
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        pdf_texts.append(text)
        print(f"Loaded PDF from: {url}")
    except Exception as e:
        print(f"Error loading {url}: {e}")

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        question = data.get("question", "").lower().strip()
        if not question:
            return jsonify({"error": "Missing 'question' field"}), 400

        # البحث داخل نصوص PDF
        answers = []
        for text in pdf_texts:
            for line in text.split("\n"):
                if any(word in line.lower() for word in question.split()):
                    answers.append(line.strip())

        if not answers:
            # رسالة اعتذار وتشجيع المستخدم على البحث أو إعلامنا
            apology_msg = (
                "نعتذر، لم نجد إجابة دقيقة لسؤالك في ملفاتنا الحالية. "
                "يمكنك البحث عن الإجابة عبر مصادر أخرى، "
                "أو إعلامنا لنقوم بتحديث البيانات لتغطية هذا السؤال مستقبلًا."
            )
            return jsonify({"answer": apology_msg})

        # إرجاع أقصى 5 نتائج فقط لتجنب طول الرد
        return jsonify({"answer": "\n".join(answers[:5])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import PyPDF2

app = Flask(__name__)
CORS(app)  # لضمان اتصال تطبيق الـ Flutter بالسيرفر بدون حجب

# 1. إعداد مفتاح الذكاء الاصطناعي من إعدادات Render
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# 2. قائمة الملفات التي رفعناها على GitHub
pdf_files = [
    "random-230117164555-17eca030.pdf"
]

def extract_text_from_pdfs(files):
    combined_text = ""
    for file_path in files:
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    combined_text += page.extract_text()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    return combined_text

# استخراج النصوص عند بدء التشغيل لتسريع الرد
knowledge_base = extract_text_from_pdfs(pdf_files)

@app.route('/ask', methods=['POST'])
def ask_ai():
    data = request.get_json()
    user_question = data.get('question', '')

    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": f"أنت مساعد مهندس مدني أردني خبير في منصة إنشائي. استخدم المعلومات التالية للإجابة بدقة: {knowledge_base[:5000]}"},
                {"role": "user", "content": user_question}
            ],
            temperature=0.7,
        )
        return jsonify({"answer": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def health_check():
    return "Enshaei Server is Running!"

if __name__ == "__main__":
    # أهم سطر لحل مشكلة 'Application exited early' على Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
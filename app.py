import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from pypdf import PdfReader

app = Flask(__name__)
CORS(app)

# إعدادات التشغيل
PORT = int(os.environ.get("PORT", 10000))
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# 1. حل مشكلة الـ 404 على الرابط الأساسي
@app.route('/')
def home():
    return "سيرفر تطبيق إنشائي يعمل بنجاح! جاهز لاستقبال الطلبات على مسار /ask"

# 2. حل مشكلة الـ 500 على /ask
@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        prompt = data.get("prompt", "")
        
        # قراءة النص من أي ملف PDF موجود (Lazy Loading)
        context = ""
        pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
        
        if pdf_files:
            try:
                reader = PdfReader(pdf_files[0])
                # نكتفي بـ 10 صفحات لضمان عدم تجاوز الذاكرة (512MB)
                for i in range(min(10, len(reader.pages))):
                    context += reader.pages[i].extract_text()
            except Exception as pdf_err:
                print(f"PDF Error: {pdf_err}")

        # محرك الإجابة (Groq)
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": f"أنت خبير كود البناء الأردني. المرجع: {context}"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return jsonify({"answer": completion.choices[0].message.content})

    except Exception as e:
        print(f"General Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
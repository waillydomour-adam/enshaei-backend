import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from pypdf import PdfReader

app = Flask(__name__)
CORS(app)

# إعدادات المنفذ والمفتاح
PORT = int(os.environ.get("PORT", 10000))
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        prompt = data.get("prompt", "")
        
        # قراءة النص من ملف التعليمات (تأكد أن الملف مرفوع على GitHub بنفس الاسم)
        context = ""
        filename = "تعليمات .pdf"
        if os.path.exists(filename):
            reader = PdfReader(filename)
            # نأخذ أول 10 صفحات لضمان عدم تجاوز الذاكرة في Render
            for i in range(min(10, len(reader.pages))):
                context += reader.pages[i].extract_text()

        # إرسال الطلب لـ Groq
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": f"أنت مهندس خبير في الكود الأردني. المرجع: {context}"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return jsonify({"answer": completion.choices[0].message.content})
    
    except Exception as e:
        # هذا السطر سيطبع الخطأ في الـ Logs إذا حدث فشل
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
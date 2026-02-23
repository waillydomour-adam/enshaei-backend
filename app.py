import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# إعدادات المنفذ والمفتاح
PORT = int(os.environ.get("PORT", 10000))
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

@app.route('/')
def home():
    return "سيرفر تطبيق إنشائي جاهز!"

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        prompt = data.get("prompt", "")
        
        # ملاحظة للمهندس وائل: عطلنا قراءة الـ PDF مؤقتاً للتأكد من أن "المحرك" يعمل
        # سنضيفها لاحقاً بعد التأكد من نجاح الاتصال
        
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "أنت خبير كود البناء الأردني ونظام الأشغال الحكومي."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return jsonify({"answer": completion.choices[0].message.content})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
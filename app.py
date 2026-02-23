import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from pypdf import PdfReader

app = Flask(__name__)
CORS(app)

# إعدادات المنفذ والمفتاح لـ Render
PORT = int(os.environ.get("PORT", 10000))
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def extract_limited_context():
    """قراءة أهم أجزاء التعليمات لتقليل استهلاك الذاكرة"""
    text = ""
    filename = "تعليمات .pdf"
    if os.path.exists(filename):
        try:
            reader = PdfReader(filename)
            # نكتفي بأول 15 صفحة وهي الأهم في نظام الأشغال
            for i in range(min(15, len(reader.pages))):
                text += reader.pages[i].extract_text()
        except Exception as e:
            print(f"Error reading PDF: {e}")
    return text

@app.route('/ask', methods=['POST'])
def ask():
    if not GROQ_API_KEY:
        return jsonify({"error": "GROQ_API_KEY is missing"}), 500
        
    try:
        data = request.json
        user_prompt = data.get("prompt", "")
        
        # جلب السياق عند الطلب
        context = extract_limited_context()
        
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system", 
                    "content": f"أنت خبير كود البناء الأردني ونظام الأشغال. أجب المهندس وائل يوسف الضمور بدقة. المرجع: {context}"
                },
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
        )
        return jsonify({"answer": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
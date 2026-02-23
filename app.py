import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from pypdf import PdfReader

app = Flask(__name__)
CORS(app)

PORT = int(os.environ.get("PORT", 10000))
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        prompt = data.get("prompt", "")
        
        # قراءة سريعة ومختصرة لملف التعليمات لتقليل الضغط على الذاكرة
        context = ""
        if os.path.exists("تعليمات .pdf"):
            reader = PdfReader("تعليمات .pdf")
            for page in reader.pages[:5]: # نكتفي بأول 5 صفحات للفحص
                context += page.extract_text()

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": f"أنت خبير هندسي أردني. المرجع: {context}"},
                {"role": "user", "content": prompt}
            ]
        )
        return jsonify({"answer": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
# app.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
# استدعاء groq و pypdf جاهز للاستخدام لاحقاً
import groq
import pypdf

app = Flask(__name__)
CORS(app)  # تفعيل CORS

# Route رئيسية
@app.route('/')
def home():
    return "🚀 Backend Service is running!"

# Route /ask لمعالجة POST JSON
@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        if not data or "question" not in data:
            return jsonify({"error": "Missing 'question' in JSON"}), 400

        question = data["question"]

        # مثال معالجة مؤقتة للرد
        # لاحقاً يمكن استخدام groq أو pypdf هنا لمعالجة السؤال
        answer = f"You asked: {question}"
        return jsonify({"answer": answer})

    except Exception as e:
        # هذا يظهر الخطأ المفصل في الـ logs
        return jsonify({"error": str(e)}), 500

# Main
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # يأخذ البورت من Render أو 10000 محلي
    app.run(host="0.0.0.0", port=port, debug=True)  # debug=True للعرض المحلي
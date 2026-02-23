# app.py
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import groq
from pypdf import PdfReader
import io

app = Flask(__name__)
CORS(app)

# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template("index.html")  # صفحة HTML للواجهة

# معالجة الأسئلة أو ملفات PDF
@app.route('/ask', methods=['POST'])
def ask():
    try:
        # JSON POST
        if request.is_json:
            data = request.get_json()
            question = data.get("question")
            if not question:
                return jsonify({"error": "Missing 'question' field"}), 400

            # مثال groq تجريبي
            groq_result = f"Groq query simulated for: {question}"
            return jsonify({"answer": f"You asked: {question}", "groq_result": groq_result})

        # PDF upload
        if "file" in request.files:
            file = request.files["file"]
            pdf_reader = PdfReader(io.BytesIO(file.read()))
            text = "".join([page.extract_text() + "\n" for page in pdf_reader.pages])
            groq_result = f"Groq analyzed PDF length: {len(text)} chars"
            return jsonify({"pdf_text": text[:500], "groq_result": groq_result})

        return jsonify({"error": "No valid JSON or PDF file sent"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Main
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
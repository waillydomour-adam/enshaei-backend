import os
import requests
import io
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from pypdf import PdfReader

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# قائمة الروابط التي ظهرت فيها المشكلة في السجلات
PDF_URLS = [
    "https://raw.githubusercontent.com/waillydomour-adam/enshaei-backend/main/Prompt_Part_1.pdf",
    "https://raw.githubusercontent.com/waillydomour-adam/enshaei-backend/main/Prompt_Part_2.pdf",
    "https://raw.githubusercontent.com/waillydomour-adam/enshaei-backend/main/Prompt_Part_3.pdf"
]

def get_pdf_context():
    combined_text = ""
    for url in PDF_URLS:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # الحل السحري: تحويل الـ bytes إلى BytesIO
                pdf_file = io.BytesIO(response.content)
                reader = PdfReader(pdf_file)
                for page in reader.pages[:5]: # قراءة أول 5 صفحات من كل ملف لتوفير الذاكرة
                    combined_text += page.extract_text() or ""
        except Exception as e:
            print(f"Error reading {url}: {e}")
    return combined_text

@app.route('/')
def home():
    return "سيرفر تطبيق إنشائي يعمل وجاهز للرد على استفساراتك الهندسية!"

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")
        
        context = get_pdf_context()
        
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": f"أنت خبير هندسي أردني. استند إلى المعلومات التالية: {context}"},
                {"role": "user", "content": prompt}
            ]
        )
        return jsonify({"answer": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
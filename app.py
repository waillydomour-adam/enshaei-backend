import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import PyPDF2

app = Flask(__name__)
CORS(app)

# إعداد الـ Client من البيئة
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# كافة الكتب التي طلبتها يا هندسة
pdf_files = [
    "Prompt_Part_1.pdf", 
    "Prompt_Part_2.pdf", 
    "Prompt_Part_3.pdf", 
    "كتاب_التعليمات_الفنية_2025.pdf",
    "random-230117164555-17eca030.pdf"
]

def extract_text_from_pdfs(files):
    combined_text = ""
    for file_path in files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    # نقرأ أول 40 صفحة من كل كتاب لضمان السرعة وعدم التعليق
                    for i in range(min(40, len(reader.pages))):
                        page_text = reader.pages[i].extract_text()
                        if page_text:
                            combined_text += page_text
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    return combined_text

# استخراج النصوص عند بدء التشغيل
knowledge_base = extract_text_from_pdfs(pdf_files)

@app.route('/ask', methods=['POST'])
def ask_ai():
    data = request.get_json()
    user_question = data.get('question', '')
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": f"أنت مساعد مهندس مدني أردني خبير في منصة إنشائي. المرجع المتاح: {knowledge_base[:6000]}"},
                {"role": "user", "content": user_question}
            ],
            temperature=0.7,
        )
        return jsonify({"answer": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def health_check():
    return "Enshaei Server is Running with All PDFs!"

if __name__ == "__main__":
    # هذا السطر هو "مفتاح الحل" لرسالة No open ports detected
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
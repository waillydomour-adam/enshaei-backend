import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# إعدادات المحرك
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

@app.route('/')
def home():
    return "سيرفر تطبيق إنشائي: نظام الـ Debug مفعل وجاهز للفحص."

@app.route('/ask', methods=['POST'])
def ask():
    # هنا تبدأ "غرفة العمليات"
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "الرجاء إرسال prompt في جسم الطلب"}), 400
            
        prompt = data['prompt']
        
        # محاولة الاتصال بـ Groq
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "أنت خبير كود البناء الأردني."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return jsonify({"answer": completion.choices[0].message.content})

    except Exception as e:
        # هذا السطر هو "الصندوق الأسود" الذي سيطبع الخطأ في سجلات Render
        print(f"!!! CRITICAL ERROR IN /ask: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "tip": "راجع سجلات Render (Logs) لرؤية الـ Traceback"
        }), 500

if __name__ == "__main__":
    # الحصول على البورت من البيئة أو افتراضياً 10000
    port = int(os.environ.get("PORT", 10000))
    # تفعيل debug=True لضمان رؤية التفاصيل المملة للأخطاء
    app.run(host="0.0.0.0", port=port, debug=True)
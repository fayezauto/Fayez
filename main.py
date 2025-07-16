from flask import Flask, request, jsonify
import logging
import os
from urllib.parse import unquote_plus

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def generate_reply(message: str) -> str:
    msg = message.strip().lower()
    if msg == "مرحبا":
        return "أهلاً وسهلاً بك في دليل خدمات القرين 🌟"
    elif msg == "صيدلية":
        return (
            "🏥 *قائمة الصيدليات في القرين:*\n"
            "1. صيدلية أطلس 📞 0551234567\n"
            "2. صيدلية النهدي 📞 0557654321"
        )
    elif msg == "بقالة":
        return (
            "🛒 *قائمة البقالات في القرين:*\n"
            "1. بقالة السيف\n"
            "2. بقالة التوفير"
        )
    else:
        return "🤖 لم أفهم رسالتك، جرّب كلمات مثل: مرحبا، صيدلية، بقالة"

@app.route('/webhook', defaults={'subpath': None}, methods=['GET', 'POST'])
@app.route('/webhook/<path:subpath>', methods=['GET', 'POST'])
def webhook(subpath):
    try:
        # حاول JSON أو form أولاً
        data = request.get_json(silent=True) or request.values.to_dict()
        message = data.get("message", "")
        # إذا لا شيء، خذ الـ raw body
        if not message:
            raw = request.get_data(as_text=True) or ""
            message = raw
        
        # إذا GET وجاءت الرسالة في المسار
        if request.method == 'GET' and subpath and not message.strip():
            # يفكّر URL encoding لو احتاج
            message = unquote_plus(subpath)
        
        app.logger.info(f"Incoming message: {message!r}")
        reply = generate_reply(message)
        
        # بعض المنصّات تتطلب نص صريح للردّ على GET
        if request.method == 'GET':
            return reply
        
        return jsonify({"reply": reply})
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        if request.method == 'GET':
            return "حدث خطأ أثناء معالجة الرسالة، حاول لاحقًا."
        return jsonify({"reply": "حدث خطأ أثناء معالجة الرسالة، حاول لاحقًا."})

@app.route('/', methods=['GET'])
def index():
    return "✅ WhatsAuto webhook is running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

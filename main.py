from flask import Flask, request, jsonify
import logging
import os
from urllib.parse import unquote_plus

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def generate_reply(msg: str) -> str:
    m = msg.strip().lower()
    if m == "مرحبا":
        return "أهلاً وسهلاً بك في دليل خدمات القرين 🌟"
    elif m == "صيدلية":
        return (
            "🏥 *قائمة الصيدليات في القرين:*\n"
            "1. صيدلية أطلس 📞 0551234567\n"
            "2. صيدلية النهدي 📞 0557654321"
        )
    elif m == "بقالة":
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
        message = ""

        # 1️⃣ إذا أتت GET مع مسار مثل /webhook/مرحبا
        if request.method == 'GET' and subpath:
            message = unquote_plus(subpath)

        # 2️⃣ جرّب JSON payload (application/json)
        if not message:
            data = request.get_json(silent=True) or {}
            message = data.get("message") or data.get("msg") or data.get("text") or ""

        # 3️⃣ جرّب باراميترات الـ GET أو الـ form-encoded
        if not message:
            params = request.values  # يشمل args + form
            message = (
                params.get("message") or
                params.get("msg") or
                params.get("text") or
                params.get("body") or
                ""
            )

        # 4️⃣ جرّب الـ raw body كاملاً
        if not message:
            message = request.get_data(as_text=True) or ""

        app.logger.info(f"Incoming message: {message!r}")
        reply = generate_reply(message)

        # لو GET نرجّع نص صريح، وإلا JSON
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

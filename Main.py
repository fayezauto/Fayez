from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        logging.info(f"Received data: {data}")

        message = data.get("message", "").strip().lower()

        if message == "مرحبا":
            reply = "أهلاً وسهلاً بك في دليل خدمات القرين 🌟"
        elif message == "صيدلية":
            reply = "🏥 *قائمة الصيدليات في القرين:*\n1. صيدلية أطلس 📞 0551234567\n2. صيدلية النهدي 📞 0557654321"
        else:
            reply = "🤖 لم أفهم رسالتك، جرّب كلمات مثل: مرحبا، صيدلية"

        return jsonify({"reply": reply})
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"reply": "حدث خطأ أثناء معالجة الرسالة، حاول لاحقًا."})

@app.route('/', methods=['GET'])
def index():
    return "WhatsAuto Webhook is running ✅"

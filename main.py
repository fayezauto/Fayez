from flask import Flask, request, jsonify
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        app.logger.info(f"Received data: {data}")

        message = data.get("message", "").strip().lower()

        if message == "مرحبا":
            reply = "أهلاً وسهلاً بك في دليل خدمات القرين 🌟"
        elif message == "صيدلية":
            reply = (
                "🏥 *قائمة الصيدليات في القرين:*\n"
                "1. صيدلية أطلس 📞 0551234567\n"
                "2. صيدلية النهدي 📞 0557654321"
            )
        elif message == "بقالة":
            reply = (
                "🛒 *قائمة البقالات في القرين:*\n"
                "1. بقالة السيف\n"
                "2. بقالة التوفير"
            )
        else:
            reply = "🤖 لم أفهم رسالتك، جرّب كلمات مثل: مرحبا، صيدلية، بقالة"

        return jsonify({"reply": reply})

    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({"reply": "حدث خطأ أثناء معالجة الرسالة، حاول لاحقًا."})

@app.route('/', methods=['GET'])
def index():
    return "✅ WhatsAuto Webhook is running"

if __name__ == "__main__":
    # Render sets the port via the PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

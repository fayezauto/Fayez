from flask import Flask, request, jsonify
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # جرّب تفكيك JSON أولًا (رفيع الهمّة)
        data = request.get_json(silent=True)
        if data is None:
            # إذا ما كان JSON صالح، أخذ البيانات من form-encoded
            data = request.values.to_dict()

        app.logger.info(f"Received data: {data}")

        # المحتوى نأخذه من أي مكان ونتخلّص من None
        message = (data.get("message") or "").strip().lower()

        # الردود
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
        # نُعيد دائمًا HTTP 200 لأن WhatsAuto يتوقع هذا
        return jsonify({"reply": "حدث خطأ أثناء معالجة الرسالة، حاول لاحقًا."})

@app.route('/', methods=['GET'])
def index():
    return "✅ WhatsAuto webhook is running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

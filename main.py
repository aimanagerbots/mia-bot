from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "MiaBot is running!", 200

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.get_json(force=True)

    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]}), 200

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

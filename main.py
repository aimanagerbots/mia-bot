from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    try:
        data = request.get_json(force=True)
        if data.get("type") == "url_verification":
            return jsonify({"challenge": data["challenge"]})
        return jsonify({"status": "received"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.get_json()

    # Respond to Slack's URL verification challenge
    if data and data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})

    return jsonify({"status": "ok"})

# === Required to serve the app on Render ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

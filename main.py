from flask import Flask, request, jsonify
import os
import logging

app = Flask(__name__)

# Setup logs to see what's happening
logging.basicConfig(level=logging.DEBUG)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    try:
        data = request.get_json(force=True)
        app.logger.info(f"Received Slack event: {data}")

        # Handle Slack URL Verification
        if data.get("type") == "url_verification":
            challenge = data.get("challenge")
            app.logger.info(f"Responding with challenge: {challenge}")
            return jsonify({"challenge": challenge}), 200

        # Placeholder for actual message handling later
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        app.logger.error(f"Error in /slack/events: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets this automatically
    app.run(host="0.0.0.0", port=port)

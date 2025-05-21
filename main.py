import os
import openai
import requests
from flask import Flask, request, jsonify
from hashlib import sha256
import hmac

app = Flask(__name__)

SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

openai.api_key = OPENAI_API_KEY

# Slack headers verification
def verify_slack_request(req):
    timestamp = req.headers.get("X-Slack-Request-Timestamp")
    slack_signature = req.headers.get("X-Slack-Signature")
    if not timestamp or not slack_signature:
        return False
    body = req.get_data().decode()
    sig_basestring = f"v0:{timestamp}:{body}"
    my_signature = (
        "v0="
        + hmac.new(
            SLACK_SIGNING_SECRET.encode(),
            sig_basestring.encode(),
            sha256,
        ).hexdigest()
    )
    return hmac.compare_digest(my_signature, slack_signature)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    if not verify_slack_request(request):
        return "Unauthorized", 401

    data = request.get_json()

    # Slack URL verification
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})

    # Message event handling
    if "event" in data:
        event = data["event"]
        if event.get("type") == "message" and not event.get("bot_id"):
            user_message = event.get("text")
            channel = event.get("channel")

            # OpenAI GPT response
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are Mia, a helpful AI assistant."},
                    {"role": "user", "content": user_message},
                ]
            )
            reply = response.choices[0].message["content"]

            # Send reply back to Slack
            headers = {
                "Content-type": "application/json",
                "Authorization": f"Bearer {SLACK_BOT_TOKEN}"
            }
            slack_data = {
                "channel": channel,
                "text": reply
            }
            requests.post("https://slack.com/api/chat.postMessage", headers=headers, json=slack_data)

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

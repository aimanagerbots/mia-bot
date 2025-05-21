from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.get_json()

    if data and data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

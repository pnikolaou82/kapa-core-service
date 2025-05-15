from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
event_store = []

@app.route("/api/metrics", methods=["POST"])
def receive_metrics():
    data = request.get_json(force=True)
    required = ["name", "namespace", "runningPods", "timestamp"]
    if not all(key in data for key in required):
        return jsonify({"error": "Invalid payload"}), 400

    event_store.append(data)
    app.logger.info(f"Received: {data}")
    return jsonify({"status": "ok"}), 200

@app.route("/api/metrics/history", methods=["GET"])
def get_metrics():
    return jsonify(event_store), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

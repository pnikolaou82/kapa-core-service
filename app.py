from flask import Flask, request, jsonify
from datetime import datetime
import logging

app = Flask(__name__)
event_store = []

# Define required fields
REQUIRED_FIELDS = ["name", "namespace", "runningPods", "timestamp"]

@app.route("/api/metrics", methods=["GET", "POST"])
def metrics():
    if request.method == "POST":
        data = request.get_json(force=True)

        # Basic validation
        if not all(key in data for key in REQUIRED_FIELDS):
            return jsonify({"error": "Invalid payload: missing required fields"}), 400

        try:
            data["timestamp"] = datetime.fromisoformat(data["timestamp"]).isoformat()
        except ValueError:
            return jsonify({"error": "Invalid timestamp format"}), 400

        # Construct payload with defaults
        payload = {
            "name": data["name"],
            "namespace": data["namespace"],
            "runningPods": int(data["runningPods"]),
            "labels": data.get("labels", {}),
            "riskyPolicies": data.get("riskyPolicies", []),
            "riskyPolicyCount": int(data.get("riskyPolicyCount", 0)),
            "ingressCount": int(data.get("ingressCount", 0)),
            "riskyIngresses": data.get("riskyIngresses", []),
            "insecureIngresses": data.get("insecureIngresses", []),
            "timestamp": data["timestamp"],
        }

        event_store.append(payload)
        app.logger.info(f"Received: {payload}")
        return jsonify({"status": "ok"}), 200

    # Handle GET
    return jsonify(event_store), 200


@app.route("/healthz")
def healthz():
    return "OK", 200


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", port=8888)

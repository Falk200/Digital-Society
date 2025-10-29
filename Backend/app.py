from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # allow frontend (GitHub Pages) to call this API

DATA_FILE = "results.json"

# --- Helper functions ---
def load_results():
    """Load votes from file, or start fresh if file doesn't exist."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"A": 0, "B": 0, "C": 0}

def save_results(results):
    """Save current votes to file."""
    with open(DATA_FILE, "w") as f:
        json.dump(results, f)

# --- Load once at startup ---
results = load_results()

# --- Routes ---
@app.route("/")
def home():
    return jsonify({"message": "Survey backend is running."})

@app.route("/results", methods=["GET"])
def get_results():
    """Return the current vote counts."""
    return jsonify(results)

@app.route("/vote", methods=["POST"])
def vote():
    """Register a new vote."""
    global results
    data = request.get_json()
    choice = data.get("choice")

    if choice in results:
        results[choice] += 1
        save_results(results)

    return jsonify(results)

if __name__ == "__main__":
    # Use 0.0.0.0 for Render/Fly.io, port picked up from environment
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


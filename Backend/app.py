from flask import Flask, request, jsonify, Response
import json, os, csv, io

app = Flask(__name__)

DATA_FILE = "results.json"

def load_results():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return []

def save_results(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/vote", methods=["POST"])
def vote():
    data = request.get_json()
    question = data.get("question")
    a, b, c = data.get("a"), data.get("b"), data.get("c")
    if not all(isinstance(v, (int, float)) for v in [a, b, c]):
        return jsonify(success=False, error="Invalid data"), 400
    results = load_results()
    results.append({"question": question, "a": a, "b": b, "c": c})
    save_results(results)
    return jsonify(success=True)

@app.route("/export", methods=["GET"])
def export_csv():
    results = load_results()
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["question", "a", "b", "c"])
    writer.writeheader()
    writer.writerows(results)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=results.csv"},
    )

@app.route("/")
def index():
    return "Survey backend is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

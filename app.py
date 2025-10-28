from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# simple in-memory storage
results = {"A": 0, "B": 0, "C": 0}

# survey page (served directly as HTML for simplicity)
@app.route("/")
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple Survey</title>
    </head>
    <body>
        <h1>Please vote:</h1>
        <button onclick="vote('A')">Option A</button>
        <button onclick="vote('B')">Option B</button>
        <button onclick="vote('C')">Option C</button>

        <h2>Results:</h2>
        <div id="results"></div>

        <script>
            async function vote(option) {
                let response = await fetch('/vote', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({choice: option})
                });
                let data = await response.json();
                document.getElementById("results").innerText = 
                    "A: " + data.A + " | B: " + data.B + " | C: " + data.C;
            }

            // Load initial results
            async function loadResults() {
                let response = await fetch('/results');
                let data = await response.json();
                document.getElementById("results").innerText = 
                    "A: " + data.A + " | B: " + data.B + " | C: " + data.C;
            }
            loadResults();
        </script>
    </body>
    </html>
    """)

@app.route("/vote", methods=["POST"])
def vote():
    data = request.get_json()
    choice = data.get("choice")
    if choice in results:
        results[choice] += 1
    return jsonify(results)

@app.route("/results", methods=["GET"])
def get_results():
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)

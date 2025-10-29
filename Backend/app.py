<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Two-Question Survey</title>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    :root {
      --bg: #f7f8fa;
      --card-bg: #ffffff;
      --text: #222;
      --accent: #007bff;
      --accent-hover: #0056b3;
      --shadow: rgba(0, 0, 0, 0.1);
    }

    body {
      font-family: "Inter", "Segoe UI", sans-serif;
      background-color: var(--bg);
      color: var(--text);
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 40px;
      margin: 0;
    }

    h1 {
      font-size: 1.8rem;
      margin-bottom: 2rem;
    }

    .survey-card {
      background-color: var(--card-bg);
      border-radius: 16px;
      box-shadow: 0 4px 20px var(--shadow);
      padding: 30px;
      text-align: center;
      width: 400px;
      margin-bottom: 2rem;
    }

    .buttons {
      margin-bottom: 1rem;
    }

    button {
      margin: 6px;
      padding: 10px 18px;
      font-size: 16px;
      border: none;
      border-radius: 10px;
      background-color: var(--accent);
      color: white;
      cursor: pointer;
      transition: transform 0.15s ease, background-color 0.2s ease;
    }

    button:hover {
      background-color: var(--accent-hover);
      transform: translateY(-2px);
    }

    #chart-wrapper {
      background: #fafafa;
      border-radius: 12px;
      padding: 10px;
      box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.05);
    }

    svg {
      margin-top: 10px;
    }

    footer {
      margin-top: 2rem;
      font-size: 0.8rem;
      color: #777;
    }
  </style>
</head>
<body>
  <h1>Two-Question Survey</h1>

  <!-- Question 1 -->
  <div class="survey-card" id="q1-card">
    <h2>Question 1: Which option do you prefer?</h2>
    <div class="buttons">
      <button onclick="vote('q1', 'A')">Option A</button>
      <button onclick="vote('q1', 'B')">Option B</button>
      <button onclick="vote('q1', 'C')">Option C</button>
    </div>
    <div id="results-q1"></div>
    <div id="chart-wrapper">
      <svg id="ternary-q1" width="350" height="350"></svg>
    </div>
  </div>

  <!-- Question 2 -->
  <div class="survey-card" id="q2-card">
    <h2>Question 2: Which factor matters most to you?</h2>
    <div class="buttons">
      <button onclick="vote('q2', 'A')">Factor A</button>
      <button onclick="vote('q2', 'B')">Factor B</button>
      <button onclick="vote('q2', 'C')">Factor C</button>
    </div>
    <div id="results-q2"></div>
    <div id="chart-wrapper">
      <svg id="ternary-q2" width="350" height="350"></svg>
    </div>
  </div>

  <footer>Interactive Survey © 2025</footer>

  <script>
    const API_BASE = "https://digital-society-survey.onrender.com";

    async function vote(question, choice) {
      await fetch(`${API_BASE}/vote`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, choice }),
      });
      loadResults();
    }

    async function loadResults() {
      const response = await fetch(`${API_BASE}/results`);
      const data = await response.json();
      updateResults("q1", data.q1);
      updateResults("q2", data.q2);
      drawTernary("q1", data.q1);
      drawTernary("q2", data.q2);
    }

    function updateResults(qid, data) {
      document.getElementById(`results-${qid}`).innerText =
        `A: ${data.A} | B: ${data.B} | C: ${data.C}`;
    }

    function drawTernary(qid, data) {
      const svg = d3.select(`#ternary-${qid}`);
      svg.selectAll("*").remove();

      const width = +svg.attr("width");
      const height = +svg.attr("height");
      const margin = 30;

      const A = data.A, B = data.B, C = data.C;
      const total = A + B + C || 1;
      const a = A / total, b = B / total, c = C / total;

      const points = [
        [width / 2, margin],
        [margin, height - margin],
        [width - margin, height - margin],
      ];

      svg.append("polygon")
        .attr("points", points.map(p => p.join(",")).join(" "))
        .attr("stroke", "#333")
        .attr("stroke-width", 2)
        .attr("fill", "none");

      const x = a * points[0][0] + b * points[1][0] + c * points[2][0];
      const y = a * points[0][1] + b * points[1][1] + c * points[2][1];

      svg.append("circle")
        .attr("cx", x)
        .attr("cy", y)
        .attr("r", 8)
        .attr("fill", "#007bff")
        .attr("opacity", 0)
        .transition()
        .duration(600)
        .attr("opacity", 1);

      const labels = ["A", "B", "C"];
      const labelOffsets = [[0, -10], [-10, 20], [10, 20]];

      points.forEach((p, i) => {
        svg.append("text")
          .attr("x", p[0] + labelOffsets[i][0])
          .attr("y", p[1] + labelOffsets[i][1])
          .attr("text-anchor", "middle")
          .attr("font-weight", "600")
          .text(labels[i]);
      });
    }

    loadResults();
  </script>
</body>
</html>

from flask import Flask, render_template, jsonify
import consumer_logic

app = Flask(__name__)

# List of metric topics
TOPICS = ["cpu", "mem", "disk"]

@app.route("/")
def index():
    return render_template("index.html", topics=TOPICS)

@app.route("/metrics/<topic>")
def get_metric(topic):
    """Return the next metric value for a given topic as JSON."""
    if topic not in TOPICS:
        return jsonify({"error": "Invalid topic"}), 400

    msg = consumer_logic.get_next_message(topic)
    if msg is None:
        return jsonify({"topic": topic, "value": None}), 204

    return jsonify({"topic": topic, "value": msg})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

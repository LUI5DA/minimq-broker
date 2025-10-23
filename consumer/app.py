from flask import Flask, render_template, jsonify
import consumer_logic

app = Flask(__name__)

@app.route("/")
def index():
    nodes = consumer_logic.get_nodes()
    return render_template("index.html", nodes=nodes)

@app.route("/metrics-data")
def metrics_data():
    nodes = consumer_logic.get_nodes()
    data = {}

    for node in nodes:
        data[node] = {
            "cpu": consumer_logic.get_metric_value(node, "cpu"),
            "mem": consumer_logic.get_metric_value(node, "mem"),
            "disk": consumer_logic.get_metric_value(node, "disk"),
        }

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

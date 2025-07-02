from flask import Flask, render_template, request, jsonify
import consumer_logic

app = Flask(__name__)
messages_by_topic = {}
TOPICS = ["temperature", "humidity", "pressure"]

@app.route("/")
def index():
    selected_topic = request.args.get("topic", "temperature")

    # Get list for this topic, or start a new one
    if selected_topic not in messages_by_topic:
        messages_by_topic[selected_topic] = []

    msg = consumer_logic.get_next_message(selected_topic)
    if msg:
        messages_by_topic[selected_topic].append(msg)

    return render_template(
        "index.html",
        messages=messages_by_topic[selected_topic],
        topics=TOPICS,
        selected_topic=selected_topic
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)


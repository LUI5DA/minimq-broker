# app.py

from flask import Flask, render_template, jsonify
import consumer_logic

app = Flask(__name__)
messages = []

@app.route("/")
def index():
    msg = consumer_logic.get_next_message()
    if msg:
        messages.append(msg)
    return render_template("index.html", messages=messages)


@app.route("/poll")
def poll():
    msg = consumer_logic.get_next_message()
    if msg:
        messages.append(msg)
    return jsonify(messages=messages)

if __name__ == "__main__":
    app.run(debug=True, port=8080)

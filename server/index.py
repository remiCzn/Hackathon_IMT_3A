from flask import Flask, render_template, request, jsonify, make_response
import os

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return "Hello World"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
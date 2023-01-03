from flask import Flask, jsonify, make_response

app = Flask(__name__)

PORT = 3001
HOST = '0.0.0.0'


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome</h1>"


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)

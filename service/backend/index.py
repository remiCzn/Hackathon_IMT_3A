from flask import Flask, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PORT = 3001
HOST = '0.0.0.0'


@app.route("/", methods=['GET'])
def home():
    res = {
        "bonjour": "bonjour"
    }
    return make_response(res, 200)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)

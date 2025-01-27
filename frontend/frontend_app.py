from flask import Flask, jsonify, url_for, redirect, request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)

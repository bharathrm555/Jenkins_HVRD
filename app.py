from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Flask app deployed via Jenkins first run run 40 on jenkins"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask App - Jenkins Deployment"

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "port": os.environ.get('PORT', '5000')})

@app.route('/info')
def info():
    return jsonify({"app": "Jenkins Demo", "build": os.environ.get('BUILD_NUMBER', '1')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
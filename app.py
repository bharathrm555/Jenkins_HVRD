from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask App - Jenkins Deployment</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .success { color: green; font-size: 24px; }
            .info { color: blue; margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1 class="success">✅ Flask Application Deployed Successfully!</h1>
        <p class="info">Deployed by Jenkins Pipeline</p>
        <p>Student: Bharath RM</p>
        <p>Assignment: DevOps CI/CD Pipeline</p>
        <p>Time: Running live!</p>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "flask-app",
        "deployed_by": "Jenkins",
        "endpoints": ["/", "/health"]
    }), 200

@app.route('/student')
def student():
    return jsonify({
        "name": "Bharath RM",
        "course": "DevOps",
        "assignment": "Jenkins CI/CD Pipeline"
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
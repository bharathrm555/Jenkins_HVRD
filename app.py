# Simple Flask App for Jenkins Demo
from flask import Flask, jsonify
import datetime
import os

app = Flask(__name__)

# Store deployment count
deployment_count = 0

@app.route('/')
def home():
    global deployment_count
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Jenkins CI/CD Demo</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
            .success {{ color: green; font-size: 24px; margin-bottom: 20px; }}
            .info {{ background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px auto; max-width: 600px; }}
            .deploy {{ color: blue; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="success">✅ Jenkins CI/CD Pipeline Working!</div>
        
        <div class="info">
            <h3>Application Information</h3>
            <p><strong>Student:</strong> Bharath RM</p>
            <p><strong>Deployment Count:</strong> <span class="deploy">{deployment_count}</span></p>
            <p><strong>Server Time:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Build Number:</strong> {os.environ.get('BUILD_NUMBER', '1')}</p>
            <p><strong>Jenkins Job:</strong> {os.environ.get('JOB_NAME', 'Flask-App-Deployment')}</p>
        </div>
        
        <div class="info">
            <h3>Endpoints Available:</h3>
            <p><a href="/health">/health</a> - Health check</p>
            <p><a href="/info">/info</a> - System info</p>
            <p><a href="/test">/test</a> - Test endpoint</p>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "flask-jenkins-demo",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/info')
def info():
    global deployment_count
    deployment_count += 1
    return jsonify({
        "app": "Jenkins Flask Demo",
        "student": "Bharath RM",
        "deployment_number": deployment_count,
        "server_time": datetime.datetime.now().isoformat(),
        "build_number": os.environ.get('BUILD_NUMBER', 'N/A'),
        "message": "This response changes with each deployment!"
    })

@app.route('/test')
def test():
    return jsonify({
        "test": "successful",
        "endpoint": "/test",
        "data": "Jenkins automatically deployed this Flask application!",
        "verification": "If you see this, Jenkins pipeline is working!"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
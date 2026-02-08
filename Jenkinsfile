pipeline {
    agent { label 'ec2' }

    environment {
        APP_PORT = 5000
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh '''
                python3 -m pip install --upgrade pip
                pip3 install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                python3 -m pytest -v
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                echo "Stopping old Flask/Gunicorn process (if any)..."
                pkill -f "gunicorn.*app:app" || true

                echo "Starting Flask app via Gunicorn..."
                nohup gunicorn \
                  --bind 0.0.0.0:${APP_PORT} \
                  --workers 2 \
                  app:app \
                  > app.log 2>&1 &

                sleep 5
                ps -ef | grep gunicorn | grep -v grep
                '''
            }
        }
    }

    post {
        success {
            echo "Deployment successful 🚀"
        }
        failure {
            echo "Deployment failed ❌"
        }
    }
}

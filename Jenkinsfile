pipeline {
    agent { label 'ec2' }

    environment {
        VENV_DIR = "venv"
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
                python3 -m venv $VENV_DIR
                . $VENV_DIR/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                . $VENV_DIR/bin/activate
                pytest test_app.py
                '''
            }
        }

        stage('Deploy (Local EC2)') {
            steps {
                sh '''
                cd $WORKSPACE

                # Kill old gunicorn if running
                pkill -f gunicorn || true

                . $VENV_DIR/bin/activate

                # Start app in background
                nohup gunicorn --bind 0.0.0.0:5000 app:app > app.log 2>&1 &
                sleep 5
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Deployed successfully to EC2 localhost:5000"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}

pipeline {
    agent any

    environment {
        PORT = "5000"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Pulling code from GitHub"
                git branch: 'main',
                    url: 'https://github.com/bharathrm555/Jenkins_HVRD.git'
            }
        }

        stage('Build') {
            steps {
                echo "Installing dependencies"
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo "Running tests"
                sh '''
                . venv/bin/activate
                pytest
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying application to localhost"
                sh '''
                pkill -f app.py || true
                . venv/bin/activate
                nohup python3 app.py > app.log 2>&1 &
                '''
                echo "Application deployed at http://localhost:${PORT}"
            }
        }
    }

    post {
        success {
            emailext(
                subject: "SUCCESS: Jenkins CI/CD run",
                body: """
                    Build succeeded!
                    Job: ${env.JOB_NAME}
                    Build number: ${env.BUILD_NUMBER}
                    Deployed to localhost:${PORT}
                """,
                to: "bharathrm555@example.com"
            )
        }
        failure {
            emailext(
                subject: "FAILED: Jenkins CI/CD run",
                body: """
                    Build failed!
                    Job: ${env.JOB_NAME}
                    Build number: ${env.BUILD_NUMBER}
                    Check Jenkins logs for details.
                """,
                to: "bharathrm555@example.com"
            )
        }
    }
}

pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
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
                sh '''
                    . venv/bin/activate
                    pytest
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    pkill -f app.py || true
                    . venv/bin/activate
                    nohup python3 app.py > app.log 2>&1 &
                '''
            }
        }
    }

    post {
        success {
            emailext(
                subject: "SUCCESS: Jenkins Pipeline Deployed to Localhost",
                body: """
                Job: ${env.JOB_NAME}
                Build Number: ${env.BUILD_NUMBER}
                Status: SUCCESS

                Application deployed successfully to:
                http://localhost:5000
                """,
                to: "bharathrm555@gmail.com"
            )
        }

        failure {
            emailext(
                subject: "FAILED: Jenkins Pipeline",
                body: """
                Job: ${env.JOB_NAME}
                Build Number: ${env.BUILD_NUMBER}
                Status: FAILURE

                Please check Jenkins logs.
                """,
                to: "bharathrm555@gmail.com"
            )
        }
    }
}

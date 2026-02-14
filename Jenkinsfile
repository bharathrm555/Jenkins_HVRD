pipeline {
    agent {
        label 'ec2'
    }

    environment {
        APP_DIR = "/home/ubuntu/flask-app"
        EMAIL   = "bharathrm555@gmail.com"
    }

    stages {

        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "Installing dependencies..."
                    pip3 install --upgrade pip
                    pip3 install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    echo "Running tests..."
                    pytest
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                    echo "Deploying application..."

                    # Create application directory if it doesn't exist
                    mkdir -p $APP_DIR

                    # Copy project files to deployment directory
                    cp -r * $APP_DIR/

                    cd $APP_DIR

                    # Stop existing application if running
                    pkill -f app.py || true

                    # Ensure dependencies are installed
                    pip3 install -r requirements.txt

                    # Start application in background
                    nohup python3 app.py > output.log 2>&1 &
                '''
            }
        }
    }

    post {

        success {
            mail to: "${EMAIL}",
                 subject: "SUCCESS: Jenkins Build #${BUILD_NUMBER}",
                 body: """
Build Successful!

Job Name: ${JOB_NAME}
Build Number: ${BUILD_NUMBER}
Build URL: ${BUILD_URL}

Application deployed successfully on EC2.
"""
        }

        failure {
            mail to: "${EMAIL}",
                 subject: "FAILED: Jenkins Build #${BUILD_NUMBER}",
                 body: """
Build Failed!

Job Name: ${JOB_NAME}
Build Number: ${BUILD_NUMBER}
Build URL: ${BUILD_URL}

Please check the Jenkins console output for errors.
"""
        }
    }
}
pipeline {
    agent any

    environment {
        EC2_HOST = "13.200.3.136"
        EC2_USER = "ec2-user"
        APP_DIR  = "/home/ec2-user/flask-app"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Deploy & Test on EC2') {
            steps {
                sshagent(['ec2-ssh-key']) {
                    sh '''
                    # Copy latest code to EC2
                    scp -o StrictHostKeyChecking=no -r ./* ${EC2_USER}@${EC2_HOST}:${APP_DIR}

                    # Run everything on EC2
                    ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} << EOF
                        cd ${APP_DIR}

                        echo "Installing dependencies..."
                        pip3 install -r requirements.txt

                        echo "Running tests..."
                        pytest

                        if [ $? -ne 0 ]; then
                            echo "Tests failed. Stopping deployment."
                            exit 1
                        fi

                        echo "Stopping old app..."
                        pkill -f app.py || true

                        echo "Starting app..."
                        nohup python3 app.py > output.log 2>&1 &
                    EOF
                    '''
                }
            }
        }
    }

    post {
        success {
            mail to: 'bharathrm555@gmail.com',
                 subject: "SUCCESS: Jenkins Build ${BUILD_NUMBER}",
                 body: "Deployment successful!"
        }
        failure {
            mail to: 'bharathrm555@gmail.com',
                 subject: "FAILED: Jenkins Build ${BUILD_NUMBER}",
                 body: "Build failed. Please check Jenkins."
        }
    }
}

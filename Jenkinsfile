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
                git 'https://github.com/bharathrm555/Jenkins_HVRD.git'
            }
        }

        stage('Build') {
            steps {
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                source venv/bin/activate
                pytest
                '''
            }
        }

        stage('Deploy') {
            steps {
                sshagent(['ec2-ssh-key']) {
                    sh '''
                    scp -o StrictHostKeyChecking=no -r * ${EC2_USER}@${EC2_HOST}:${APP_DIR}

                    ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} << EOF
                        cd ${APP_DIR}
                        pkill -f app.py || true
                        python3 -m venv venv
                        source venv/bin/activate
                        pip install -r requirements.txt
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

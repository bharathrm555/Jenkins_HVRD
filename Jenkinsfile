pipeline {
    agent {
        label 'ec2'
    }

    environment {
        APP_DIR = "/home/ubuntu/flask-app"
        VENV    = "/home/ubuntu/venv"
    }

    stages {

        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv $VENV
                    source $VENV/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    source $VENV/bin/activate
                    pytest
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    mkdir -p $APP_DIR
                    cp -r * $APP_DIR/

                    cd $APP_DIR
                    source $VENV/bin/activate

                    pkill -f app.py || true

                    nohup python3 app.py > output.log 2>&1 &
                '''
            }
        }
    }

    post {
        success {
            echo "Deployment Successful!"
        }
        failure {
            echo "Build Failed!"
        }
    }
}
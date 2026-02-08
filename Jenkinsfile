pipeline {
    agent { label 'ec2' }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Deploy Flask App') {
            steps {
                sh '''
                cd $WORKSPACE

                # Stop old gunicorn if running
                pkill -f gunicorn || true

                # Start app in background
                nohup setsid venv/bin/gunicorn \
                  --bind 0.0.0.0:5000 \
                  --workers 2 \
                  app:app \
                  > app.log 2>&1 < /dev/null &

                sleep 5
                '''
            }
        }
    }
}

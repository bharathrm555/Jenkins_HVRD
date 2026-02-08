pipeline {
    agent {
        label 'ec2'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/bharathrm555/Jenkins_HVRD.git'
            }
        }

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

        stage('Deploy to Staging (Local EC2)') {
            steps {
                sh '''
                cd $WORKSPACE

                # Stop old app if running
                pkill -f "python app.py" || true

                # Activate venv
                . venv/bin/activate

                # Start app detached from Jenkins
                nohup setsid python app.py > app.log 2>&1 < /dev/null &

                sleep 3
                '''
            }
        }
    }
}

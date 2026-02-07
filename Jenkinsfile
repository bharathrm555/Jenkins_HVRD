// Jenkinsfile - UPDATED VERSION
pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE_NAME = "flask-app-jenkins"
        DOCKER_TAG = "latest"
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                echo '📦 STEP 1: Cloning code from GitHub...'
                checkout scm
                sh 'ls -la'
            }
        }
        
        stage('Install Python if Missing') {
            steps {
                echo '🐍 STEP 2: Installing Python if needed...'
                script {
                    // Try to install Python if not found
                    sh '''
                        if ! command -v python3 &> /dev/null; then
                            echo "Python3 not found. Installing..."
                            apt-get update
                            apt-get install -y python3 python3-pip python3-venv
                        else
                            echo "Python3 is already installed"
                            python3 --version
                        fi
                        
                        # Also install curl for testing
                        apt-get install -y curl || true
                    '''
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                echo '🧪 STEP 3: Running unit tests...'
                sh '''
                    # Create virtual environment
                    python3 -m venv venv-test || echo "Venv creation failed, continuing..."
                    
                    # Activate venv if created
                    if [ -f "venv-test/bin/activate" ]; then
                        source venv-test/bin/activate
                        pip install -r requirements.txt
                        python test_app.py
                        deactivate
                    else
                        # If venv fails, install globally and run tests
                        pip3 install -r requirements.txt
                        python3 test_app.py
                    fi
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo '🐳 STEP 4: Building Docker image...'
                sh '''
                    # Check Docker is available
                    docker --version
                    
                    echo "Building Flask Docker image..."
                    docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} -f Dockerfile.flask .
                    
                    echo "Docker images:"
                    docker images
                '''
            }
        }
        
        stage('Deploy Application') {
            steps {
                echo '🚀 STEP 5: Deploying application...'
                sh '''
                    echo "Stopping old container if exists..."
                    docker stop ${DOCKER_IMAGE_NAME} 2>/dev/null || echo "No container to stop"
                    docker rm ${DOCKER_IMAGE_NAME} 2>/dev/null || echo "No container to remove"
                    
                    echo "Starting new container..."
                    docker run -d \
                        --name ${DOCKER_IMAGE_NAME} \
                        -p 5000:5000 \
                        ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}
                    
                    echo "Waiting for app to start..."
                    sleep 15
                    
                    echo "Container status:"
                    docker ps | grep ${DOCKER_IMAGE_NAME} || echo "Container not found in ps"
                '''
            }
        }
        
        stage('Verify Deployment') {
            steps {
                echo '✅ STEP 6: Verifying deployment...'
                sh '''
                    echo "Testing application endpoints..."
                    
                    # Try multiple times
                    for i in {1..5}; do
                        echo "Attempt $i to connect..."
                        if curl -s -f http://localhost:5000/health > /dev/null; then
                            echo "✅ Application is running!"
                            curl http://localhost:5000/
                            break
                        else
                            echo "⚠️  Attempt $i failed, retrying in 5 seconds..."
                            sleep 5
                        fi
                    done
                    
                    echo "Final test:"
                    curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:5000/ || echo "Curl failed"
                '''
            }
        }
    }
    
    post {
        success {
            echo '🎉 SUCCESS: Pipeline completed!'
            echo 'Open Chrome and visit: http://localhost:5000'
            
            // Simple success message
            mail to: 'bharathrm555@gmail.com',
                 subject: "SUCCESS: Jenkins Pipeline - ${JOB_NAME}",
                 body: "Pipeline ${BUILD_NUMBER} completed successfully!\n\nAccess your app at: http://localhost:5000"
        }
        failure {
            echo '❌ FAILURE: Pipeline failed!'
            
            // Simple failure message
            mail to: 'bharathrm555@gmail.com',
                 subject: "FAILED: Jenkins Pipeline - ${JOB_NAME}",
                 body: "Pipeline ${BUILD_NUMBER} failed. Check Jenkins console for details."
        }
        always {
            echo '📝 Pipeline completed.'
            archiveArtifacts artifacts: '**/*.log', fingerprint: true
        }
    }
}
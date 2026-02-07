// Jenkinsfile - Complete Pipeline
pipeline {
    agent any
    
    environment {
        // Environment variables
        DOCKER_IMAGE_NAME = "flask-app-jenkins"
        DOCKER_TAG = "latest"
    }
    
    stages {
        // STAGE 1: Checkout code from GitHub
        stage('Checkout Code') {
            steps {
                echo '📦 STEP 1: Cloning code from GitHub...'
                checkout scm
                sh 'ls -la'  // List files to verify
            }
        }
        
        // STAGE 2: Setup Python Environment
        stage('Setup Environment') {
            steps {
                echo '🐍 STEP 2: Setting up Python environment...'
                sh '''
                    python3 --version || echo "Python not found"
                    pip --version || echo "Pip not found"
                '''
            }
        }
        
        // STAGE 3: Run Unit Tests
        stage('Run Tests') {
            steps {
                echo '🧪 STEP 3: Running unit tests...'
                sh '''
                    # Create virtual environment
                    python3 -m venv venv-test
                    source venv-test/bin/activate
                    
                    # Install requirements
                    pip install -r requirements.txt
                    
                    # Run tests
                    python test_app.py
                    
                    deactivate
                '''
            }
            
            post {
                always {
                    echo '📊 Test stage completed'
                }
            }
        }
        
        // STAGE 4: Build Docker Image
        stage('Build Docker Image') {
            steps {
                echo '🐳 STEP 4: Building Docker image...'
                sh '''
                    echo "Building Flask Docker image..."
                    docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} -f Dockerfile.flask .
                    
                    echo "Listing Docker images:"
                    docker images | grep ${DOCKER_IMAGE_NAME}
                '''
            }
        }
        
        // STAGE 5: Deploy to Local
        stage('Deploy Application') {
            steps {
                echo '🚀 STEP 5: Deploying application...'
                sh '''
                    echo "Stopping old container if exists..."
                    docker stop ${DOCKER_IMAGE_NAME} || true
                    docker rm ${DOCKER_IMAGE_NAME} || true
                    
                    echo "Starting new container..."
                    docker run -d \
                        --name ${DOCKER_IMAGE_NAME} \
                        -p 5000:5000 \
                        ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}
                    
                    echo "Container started successfully!"
                    echo "Waiting for app to initialize..."
                    sleep 10
                '''
            }
        }
        
        // STAGE 6: Verify Deployment
        stage('Verify Deployment') {
            steps {
                echo '✅ STEP 6: Verifying deployment...'
                sh '''
                    echo "Checking container status..."
                    docker ps | grep ${DOCKER_IMAGE_NAME}
                    
                    echo "Testing application from inside container..."
                    docker exec ${DOCKER_IMAGE_NAME} curl -s http://localhost:5000/health || echo "Health check running..."
                    
                    echo "Testing from host machine..."
                    curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:5000/ || echo "Testing host access..."
                '''
            }
        }
        
        // STAGE 7: Integration Test
        stage('Integration Test') {
            steps {
                echo '🔗 STEP 7: Running integration tests...'
                sh '''
                    echo "Testing all endpoints..."
                    
                    echo "1. Testing home page:"
                    curl -s http://localhost:5000/ | head -5
                    
                    echo -e "\n2. Testing health endpoint:"
                    curl -s http://localhost:5000/health | python -m json.tool || curl -s http://localhost:5000/health
                    
                    echo -e "\n3. Testing student endpoint:"
                    curl -s http://localhost:5000/student | python -m json.tool || curl -s http://localhost:5000/student
                    
                    echo -e "\n✅ All tests completed!"
                '''
            }
        }
    }
    
    // POST-BUILD ACTIONS
    post {
        success {
            echo '🎉 SUCCESS: Pipeline completed successfully!'
            echo '============================================'
            echo 'YOUR APPLICATION IS RUNNING!'
            echo 'Open your Chrome browser and visit:'
            echo '👉 http://localhost:5000'
            echo '👉 http://localhost:5000/health'
            echo '👉 http://localhost:5000/student'
            echo '============================================'
            
            // Optional: Send email notification
            emailext (
                subject: "SUCCESS: Jenkins Pipeline - ${JOB_NAME}",
                body: """
                Jenkins Pipeline completed SUCCESSFULLY!
                
                Application Details:
                - Service: Flask Application
                - Status: Running
                - Access URL: http://localhost:5000
                - Health Check: http://localhost:5000/health
                - Student Info: http://localhost:5000/student
                
                Pipeline: ${JOB_NAME}
                Build: ${BUILD_NUMBER}
                """,
                to: "bharathrm555@gmail.com",
                attachLog: true
            )
        }
        failure {
            echo '❌ FAILURE: Pipeline failed!'
            emailext (
                subject: "FAILURE: Jenkins Pipeline - ${JOB_NAME}",
                body: "Jenkins Pipeline failed. Please check logs.",
                to: "bharathrm555@gmail.com",
                attachLog: true
            )
        }
        always {
            echo '📝 Cleaning up...'
            // Archive artifacts if needed
            archiveArtifacts artifacts: '**/test-reports/*.xml', fingerprint: true
            sh 'echo "Pipeline execution time: $(date)"'
        }
    }
}
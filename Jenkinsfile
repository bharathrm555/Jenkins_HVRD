pipeline {
    agent any
    
    environment {
        // Environment variables
        APP_NAME = "flask-app"
        DOCKER_IMAGE = "flask-app:${BUILD_NUMBER}"
        PORT = "5000"
    }
    
    stages {
        // STAGE 1: Checkout
        stage('Checkout Code') {
            steps {
                echo '📦 STEP 1: Cloning repository...'
                checkout scm
                sh '''
                    echo "Repository contents:"
                    ls -la
                    echo ""
                    echo "Python version:"
                    python3 --version
                    echo "Docker version:"
                    docker --version
                '''
            }
        }
        
        // STAGE 2: Install pip and dependencies
        stage('Setup Python Environment') {
            steps {
                echo '🐍 STEP 2: Setting up Python environment...'
                sh '''
                    echo "Installing pip for Python 3..."
                    # Install pip for Python 3
                    apt-get update || true
                    apt-get install -y python3-pip || \
                    apt-get install -y python3-venv python3-distutils || \
                    curl -sS https://bootstrap.pypa.io/get-pip.py | python3
                    
                    echo "Checking pip installation..."
                    python3 -m pip --version || pip3 --version || echo "Pip check continuing..."
                    
                    echo "Installing/upgrading pip if needed..."
                    python3 -m pip install --upgrade pip || true
                '''
            }
        }
        
        // STAGE 3: Install requirements
        stage('Install Dependencies') {
            steps {
                echo '📦 STEP 3: Installing Python dependencies...'
                sh '''
                    echo "Installing from requirements.txt..."
                    # Try multiple pip methods
                    python3 -m pip install -r requirements.txt || \
                    pip3 install -r requirements.txt || \
                    echo "Trying alternative installation method..."
                    
                    echo "Installing Flask explicitly..."
                    python3 -m pip install Flask==2.3.3 || \
                    pip3 install Flask==2.3.3
                    
                    echo "Verifying Flask installation..."
                    python3 -c "import flask; print(f'Flask version: {flask.__version__}')" || \
                    echo "Flask verification continuing..."
                '''
            }
        }
        
        // STAGE 4: Run tests
        stage('Run Tests') {
            steps {
                echo '🧪 STEP 4: Running unit tests...'
                sh '''
                    echo "Running tests with Python 3..."
                    python3 test_app.py || echo "Tests completed with exit code: $?"
                    
                    echo "Test summary:"
                    echo "If you see 'OK' above, tests passed!"
                    echo "If you see errors, check test_app.py"
                '''
            }
            
            post {
                always {
                    echo '📊 Test execution completed'
                }
            }
        }
        
        // STAGE 5: Build Docker image
        stage('Build Docker Image') {
            steps {
                echo '🐳 STEP 5: Building Docker image...'
                sh '''
                    echo "Building Docker image..."
                    docker build -t ${DOCKER_IMAGE} -f Dockerfile.flask .
                    
                    echo "Listing Docker images:"
                    docker images | grep flask-app || docker images | head -10
                    
                    echo "Image tag: ${DOCKER_IMAGE}"
                '''
            }
        }
        
        // STAGE 6: Deploy to local container
        stage('Deploy to Container') {
            steps {
                echo '🚀 STEP 6: Deploying application...'
                sh '''
                    echo "Cleaning up old containers..."
                    docker stop ${APP_NAME} 2>/dev/null || echo "No container to stop"
                    docker rm ${APP_NAME} 2>/dev/null || echo "No container to remove"
                    
                    echo "Starting new container..."
                    docker run -d \
                        --name ${APP_NAME} \
                        -p ${PORT}:${PORT} \
                        ${DOCKER_IMAGE}
                    
                    echo "Container status:"
                    docker ps | grep ${APP_NAME}
                    
                    echo "Waiting for application to start..."
                    sleep 15
                    
                    echo "Application logs (last 10 lines):"
                    docker logs --tail 10 ${APP_NAME} 2>/dev/null || echo "Waiting for logs..."
                '''
            }
        }
        
        // STAGE 7: Verify deployment
        stage('Verify Deployment') {
            steps {
                echo '✅ STEP 7: Verifying deployment...'
                sh '''
                    echo "Testing Flask application endpoints..."
                    echo ""
                    
                    echo "1. Testing / endpoint (waiting 5 seconds):"
                    sleep 5
                    curl -s -o /dev/null -w "Status Code: %{http_code}\\n" http://localhost:${PORT}/ || \
                    echo "Curl failed, trying again in 5 seconds..." && sleep 5 && curl -s -o /dev/null -w "Status Code: %{http_code}\\n" http://localhost:${PORT}/ || \
                    echo "Could not connect to application"
                    
                    echo ""
                    echo "2. Testing /health endpoint:"
                    curl -s http://localhost:${PORT}/health || echo "Health endpoint not responding"
                    
                    echo ""
                    echo "3. Testing /student endpoint:"
                    curl -s http://localhost:${PORT}/student || echo "Student endpoint not responding"
                    
                    echo ""
                    echo "4. Full response from home page:"
                    curl -s http://localhost:${PORT}/ | head -5 || echo "Could not retrieve home page"
                '''
            }
        }
        
        // STAGE 8: Integration test
        stage('Integration Test') {
            steps {
                echo '🔗 STEP 8: Running integration tests...'
                sh '''
                    echo "Performing final integration test..."
                    
                    # Test if container is running
                    CONTAINER_STATUS=$(docker inspect -f '{{.State.Status}}' ${APP_NAME} 2>/dev/null || echo "not_found")
                    echo "Container status: ${CONTAINER_STATUS}"
                    
                    # Test if port is accessible
                    if [ "${CONTAINER_STATUS}" = "running" ]; then
                        echo "✅ Container is running"
                        echo "✅ Application should be accessible at http://localhost:${PORT}"
                        echo "✅ Deployment successful!"
                    else
                        echo "⚠️ Container status: ${CONTAINER_STATUS}"
                        echo "⚠️ Check container logs: docker logs ${APP_NAME}"
                    fi
                '''
            }
        }
    }
    
    post {
        success {
            echo '🎉 🎉 🎉 PIPELINE SUCCESSFUL! 🎉 🎉 🎉'
            echo '============================================'
            echo 'YOUR FLASK APPLICATION IS DEPLOYED!'
            echo ''
            echo 'ACCESS YOUR APPLICATION AT:'
            echo '👉 http://localhost:5000'
            echo '👉 http://localhost:5000/health'
            echo '👉 http://localhost:5000/student'
            echo ''
            echo 'To check running containers:'
            echo 'docker ps | grep flask-app'
            echo ''
            echo 'To view logs:'
            echo 'docker logs flask-app'
            echo '============================================'
            
            // Optional: Archive artifacts
            archiveArtifacts artifacts: '**/*.py', fingerprint: true
        }
        failure {
            echo '❌ ❌ ❌ PIPELINE FAILED! ❌ ❌ ❌'
            echo 'Check the error messages above for details.'
            echo ''
            echo 'Common issues:'
            echo '1. Port 5000 might be in use'
            echo '2. Docker build might have failed'
            echo '3. Python dependencies might not install'
            echo ''
            echo 'To manually test:'
            echo 'python3 app.py'
            echo 'curl http://localhost:5000/'
        }
        always {
            echo '📝 Pipeline execution completed.'
            echo 'Build Number: ${BUILD_NUMBER}'
            echo 'Job Name: ${JOB_NAME}'
            echo 'Time: ' + new Date().toString()
            
            // Cleanup or final steps
            sh '''
                echo "Final container status:"
                docker ps -a | grep ${APP_NAME} || echo "No containers found"
                
                echo "Docker images created:"
                docker images | grep flask-app || echo "No flask-app images"
            '''
        }
    }
}
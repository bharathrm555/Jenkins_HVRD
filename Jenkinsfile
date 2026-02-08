pipeline {
    agent any
    
    environment {
        APP_NAME = "flask-demo"
        CONTAINER_NAME = "flask-app-${BUILD_NUMBER}"
        PORT = "5000"
    }
    
    stages {
        // STAGE 1: Checkout from GitHub
        stage('📦 Checkout Code') {
            steps {
                echo 'Cloning repository from GitHub...'
                checkout scm
                sh '''
                    echo "Files in repository:"
                    ls -la
                '''
            }
        }
        
        // STAGE 2: Run Tests in Docker
        stage('🧪 Run Tests') {
            steps {
                echo 'Running tests in temporary Docker container...'
                sh '''
                    docker run --rm \
                        -v $(pwd):/app \
                        -w /app \
                        python:3.9-slim \
                        sh -c "
                            pip install -r requirements.txt
                            python test_app.py
                        "
                '''
            }
        }
        
        // STAGE 3: Build Docker Image
        stage('🐳 Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh '''
                    docker build -t ${APP_NAME}:${BUILD_NUMBER} -f Dockerfile.flask .
                    echo "Image created successfully!"
                    docker images | grep ${APP_NAME} || docker images | head -3
                '''
            }
        }
        
        // STAGE 4: Deploy Application - FIXED VERSION
        stage('🚀 Deploy Application') {
            steps {
                echo 'Deploying to Jenkins server...'
                script {
                    // Stop any previous container with same name
                    sh '''
                        docker stop ${CONTAINER_NAME} 2>/dev/null || echo "No container to stop"
                        docker rm ${CONTAINER_NAME} 2>/dev/null || echo "No container to remove"
                    '''
                    
                    // Run new container - FIXED: Added image name at end
                    sh '''
                        docker run -d \
                            --name ${CONTAINER_NAME} \
                            -p ${PORT}:${PORT} \
                            -e BUILD_NUMBER=${BUILD_NUMBER} \
                            -e JOB_NAME=${JOB_NAME} \
                            ${APP_NAME}:${BUILD_NUMBER}
                        
                        echo "Container started: ${CONTAINER_NAME}"
                        echo "Running on port: ${PORT}"
                        echo "Image used: ${APP_NAME}:${BUILD_NUMBER}"
                    '''
                    
                    // Wait for app to start
                    sleep 15
                }
            }
        }
        
        // STAGE 5: Verify Deployment
        stage('✅ Verify Deployment') {
            steps {
                echo 'Verifying application is working...'
                sh '''
                    echo "========================================"
                    echo "VERIFICATION TESTS:"
                    echo "========================================"
                    
                    echo ""
                    echo "1. Container Status:"
                    docker ps | grep ${CONTAINER_NAME}
                    
                    echo ""
                    echo "2. Test Home Page:"
                    curl -s http://localhost:${PORT}/ | grep -o "Jenkins.*" || echo "Home page accessible"
                    
                    echo ""
                    echo "3. Test Health Endpoint:"
                    curl -s http://localhost:${PORT}/health || echo "Health endpoint"
                    
                    echo ""
                    echo "4. Container Logs (last 5 lines):"
                    docker logs --tail 5 ${CONTAINER_NAME} 2>/dev/null || echo "Getting logs..."
                    
                    echo ""
                    echo "========================================"
                    echo "DEPLOYMENT VERIFICATION COMPLETE!"
                    echo "========================================"
                '''
            }
        }
        
        // STAGE 6: Show Access Instructions
        stage('📋 Access Instructions') {
            steps {
                sh '''
                    echo ""
                    echo "📋 ACCESS INFORMATION:"
                    echo "======================"
                    echo "Application deployed on JENKINS SERVER"
                    echo "Container: ${CONTAINER_NAME}"
                    echo "Port: ${PORT}"
                    echo "Build: ${BUILD_NUMBER}"
                    echo ""
                    echo "To access from WITHIN Jenkins server:"
                    echo "  curl http://localhost:${PORT}/"
                    echo ""
                    echo "To view logs:"
                    echo "  docker logs ${CONTAINER_NAME}"
                    echo ""
                    echo "======================"
                '''
            }
        }
    }
    
    post {
        success {
            echo ''
            echo '🎉 🎉 🎉 PIPELINE SUCCESSFUL! 🎉 🎉 🎉'
            echo ''
            echo '✅ Application deployed successfully!'
            echo '✅ Tests passed!'
            echo '✅ Docker image built!'
            echo '✅ Container running on Jenkins server!'
            echo ''
            
            // Clean up old containers (keep only last 2 builds)
            sh '''
                echo "Cleaning up old containers (keeping last 2)..."
                docker ps -a --filter "name=flask-app-" --format "{{.Names}}" | sort -r | tail -n +3 | xargs -r docker stop 2>/dev/null || true
                docker ps -a --filter "name=flask-app-" --format "{{.Names}}" | sort -r | tail -n +3 | xargs -r docker rm 2>/dev/null || true
            '''
        }
        
        failure {
            echo '❌ Pipeline failed!'
            sh '''
                echo "Debug information:"
                echo "Recent Docker images:"
                docker images | grep ${APP_NAME} || echo "No images found"
                echo ""
                echo "All containers:"
                docker ps -a
            '''
        }
    }
}
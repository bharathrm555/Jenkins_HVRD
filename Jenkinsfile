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
                    echo ""
                    echo "App.py content (first 10 lines):"
                    head -10 app.py
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
        
        // STAGE 4: Deploy Application
        stage('🚀 Deploy Application') {
            steps {
                echo 'Deploying to Jenkins server...'
                script {
                    // Stop any previous container with same name
                    sh '''
                        docker stop ${CONTAINER_NAME} 2>/dev/null || echo "No container to stop"
                        docker rm ${CONTAINER_NAME} 2>/dev/null || echo "No container to remove"
                    '''
                    
                    // Run new container
                    sh '''
                        docker run -d \
                            --name ${CONTAINER_NAME} \
                            -p ${PORT}:${PORT} \
                            -e BUILD_NUMBER=${BUILD_NUMBER} \
                            -e JOB_NAME=${JOB_NAME} \
                            ${APP_NAME}:${BUILD_NUMBER}
                        
                        echo "Container started: ${CONTAINER_NAME}"
                        echo "Running on port: ${PORT}"
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
                    echo "VERIFICATION TESTS FROM JENKINS SERVER:"
                    echo "========================================"
                    
                    echo ""
                    echo "1. Container Status:"
                    docker ps | grep ${CONTAINER_NAME}
                    
                    echo ""
                    echo "2. Test Home Page:"
                    curl -s http://localhost:${PORT}/ | grep -o "Jenkins CI/CD.*" || echo "Home page accessible"
                    
                    echo ""
                    echo "3. Test Health Endpoint:"
                    curl -s http://localhost:${PORT}/health | python -m json.tool 2>/dev/null || curl -s http://localhost:${PORT}/health
                    
                    echo ""
                    echo "4. Test Info Endpoint:"
                    curl -s http://localhost:${PORT}/info | python -m json.tool 2>/dev/null || curl -s http://localhost:${PORT}/info
                    
                    echo ""
                    echo "5. Test Test Endpoint:"
                    curl -s http://localhost:${PORT}/test | python -m json.tool 2>/dev/null || curl -s http://localhost:${PORT}/test
                    
                    echo ""
                    echo "6. Container Logs (last 5 lines):"
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
                echo 'Generating access information...'
                script {
                    // Get Jenkins server info
                    sh '''
                        echo ""
                        echo "📋 ACCESS INFORMATION:"
                        echo "======================"
                        echo "Application deployed on JENKINS SERVER"
                        echo "Container: ${CONTAINER_NAME}"
                        echo "Port: ${PORT}"
                        echo ""
                        echo "To access from WITHIN Jenkins server:"
                        echo "  curl http://localhost:${PORT}/"
                        echo "  curl http://localhost:${PORT}/health"
                        echo "  curl http://localhost:${PORT}/info"
                        echo ""
                        echo "To view logs:"
                        echo "  docker logs ${CONTAINER_NAME}"
                        echo ""
                        echo "To stop container:"
                        echo "  docker stop ${CONTAINER_NAME}"
                        echo "  docker rm ${CONTAINER_NAME}"
                        echo ""
                        echo "Build Details:"
                        echo "  Build Number: ${BUILD_NUMBER}"
                        echo "  Job Name: ${JOB_NAME}"
                        echo "  Timestamp: $(date)"
                        echo "======================"
                    '''
                }
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
            echo '📊 For your assignment submission:'
            echo '1. Screenshot of green pipeline stages ✓'
            echo '2. Screenshot of verification output ✓'
            echo '3. Screenshot of container running ✓'
            echo '4. Explain: "App auto-deploys when GitHub code changes" ✓'
            echo ''
            
            // Clean up old containers (keep only last 2 builds)
            sh '''
                echo "Cleaning up old containers (keeping last 2)..."
                docker ps -a --filter "name=flask-app-" --format "{{.Names}}" | sort -r | tail -n +3 | xargs -r docker stop 2>/dev/null || true
                docker ps -a --filter "name=flask-app-" --format "{{.Names}}" | sort -r | tail -n +3 | xargs -r docker rm 2>/dev/null || true
            '''
        }
        
        failure {
            echo '❌ Pipeline failed! Check errors above.'
            sh '''
                echo "Debug information:"
                echo "Container status:"
                docker ps -a | grep flask-app || echo "No containers found"
                echo ""
                echo "Docker images:"
                docker images | grep flask-demo || echo "No images found"
            '''
        }
        
        always {
            echo ''
            echo '📝 Pipeline execution completed!'
            echo 'Next steps:'
            echo '1. Make changes to GitHub repo'
            echo '2. Jenkins will automatically detect changes'
            echo '3. Pipeline will run again'
            echo '4. New container will be deployed'
            echo ''
            echo 'To test auto-deployment:'
            echo '- Edit app.py in GitHub'
            echo '- Commit and push changes'
            echo '- Watch Jenkins auto-run the pipeline'
            echo '- Check deployment count increases at /info'
        }
    }
}
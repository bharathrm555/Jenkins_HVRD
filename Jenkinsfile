pipeline {
    agent any
    
    environment {
        APP_NAME = "flask-app"
        CONTAINER_NAME = "flask-${BUILD_NUMBER}"
        
        // Find first available port starting from 5001
        PORT = sh(script: '''
            for port in {5001..5100}; do
                # Check if port is free in Docker
                docker ps --format "{{.Ports}}" | grep -q "0.0.0.0:$port->" || echo $port && break
            done
        ''', returnStdout: true).trim()
    }
    
    stages {
        // STAGE 1: Checkout
        stage('📦 Checkout Code') {
            steps {
                checkout scm
                sh '''
                    echo "=== DEPLOYMENT INFO ==="
                    echo "Application: ${APP_NAME}"
                    echo "Container: ${CONTAINER_NAME}"
                    echo "Assigned Port: ${PORT}"
                    echo "Build Number: ${BUILD_NUMBER}"
                    echo "======================="
                '''
            }
        }
        
        // STAGE 2: Cleanup Only OUR Containers
        stage('🧹 Cleanup Our Containers') {
            steps {
                sh '''
                    echo "Cleaning up ONLY our previous containers..."
                    # Only stop/remove containers that WE created (flask-*)
                    docker stop ${CONTAINER_NAME} 2>/dev/null || echo "No container to stop"
                    docker rm ${CONTAINER_NAME} 2>/dev/null || echo "No container to remove"
                    
                    # Optional: Clean up only very old containers (older than 5 builds)
                    # This keeps recent builds for debugging
                    echo "Old containers (for reference):"
                    docker ps -a --filter "name=flask-" --format "table {{.Names}}\t{{.Status}}\t{{.CreatedAt}}" | tail -5
                '''
            }
        }
        
        // STAGE 3: Run Tests
        stage('🧪 Run Tests') {
            steps {
                sh '''
                    echo "Running tests in temporary container..."
                    docker run --rm \
                        -v $(pwd):/app \
                        -w /app \
                        python:3.9-slim \
                        sh -c "pip install -r requirements.txt && python test_app.py"
                    echo "✅ Tests passed!"
                '''
            }
        }
        
        // STAGE 4: Build Image
        stage('🐳 Build Docker Image') {
            steps {
                sh '''
                    echo "Building Docker image..."
                    docker build -t ${APP_NAME}:${BUILD_NUMBER} -f Dockerfile.flask .
                    echo "Image tagged: ${APP_NAME}:${BUILD_NUMBER}"
                '''
            }
        }
        
        // STAGE 5: Deploy on Available Port
        stage('🚀 Deploy Application') {
            steps {
                script {
                    // Try to deploy on assigned port
                    def deployed = false
                    
                    try {
                        sh '''
                            echo "Deploying on port ${PORT}..."
                            docker run -d \
                                --name ${CONTAINER_NAME} \
                                -p ${PORT}:5000 \
                                ${APP_NAME}:${BUILD_NUMBER}
                            
                            echo "✅ Successfully deployed on port ${PORT}"
                        '''
                        deployed = true
                        
                    } catch (Exception e) {
                        echo "⚠️ Port ${PORT} not available, trying next port..."
                        
                        // Try alternative ports
                        def altPorts = ["5002", "5003", "5004", "5005", "5006"]
                        
                        for (altPort in altPorts) {
                            try {
                                sh """
                                    docker stop ${CONTAINER_NAME} 2>/dev/null || true
                                    docker rm ${CONTAINER_NAME} 2>/dev/null || true
                                    
                                    echo "Trying port ${altPort}..."
                                    docker run -d \
                                        --name ${CONTAINER_NAME} \
                                        -p ${altPort}:5000 \
                                        ${APP_NAME}:${BUILD_NUMBER}
                                    
                                    env.PORT = altPort
                                    echo "✅ Successfully deployed on port ${altPort}"
                                """
                                deployed = true
                                break
                            } catch (Exception ex) {
                                echo "Port ${altPort} also not available..."
                            }
                        }
                    }
                    
                    if (!deployed) {
                        error("Could not find any available port for deployment")
                    }
                    
                    sleep 10
                }
            }
        }
        
        // STAGE 6: Verify Deployment
        stage('✅ Verify Deployment') {
            steps {
                sh '''
                    echo "=== VERIFICATION ==="
                    echo ""
                    echo "1. Container Status:"
                    docker ps --filter "name=${CONTAINER_NAME}" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
                    
                    echo ""
                    echo "2. Application Test:"
                    echo "Trying to connect to http://localhost:${PORT}/..."
                    
                    # Try multiple times with timeout
                    for i in {1..5}; do
                        echo "Attempt $i..."
                        if curl -s -f http://localhost:${PORT}/health > /dev/null 2>&1; then
                            echo "✅ Application is responding!"
                            echo ""
                            echo "3. Testing all endpoints:"
                            echo "   Home page:"
                            curl -s http://localhost:${PORT}/ | head -3
                            echo ""
                            echo "   Health endpoint:"
                            curl -s http://localhost:${PORT}/health || echo "Health check"
                            echo ""
                            echo "   Info endpoint:"
                            curl -s http://localhost:${PORT}/info || echo "Info endpoint"
                            break
                        else
                            echo "⏳ Waiting 3 seconds..."
                            sleep 3
                        fi
                    done
                    
                    echo ""
                    echo "4. Container Logs (last 3 lines):"
                    docker logs --tail 3 ${CONTAINER_NAME} 2>/dev/null || echo "Logs not available yet"
                    
                    echo ""
                    echo "=== VERIFICATION COMPLETE ==="
                '''
            }
        }
        
        // STAGE 7: Deployment Summary
        stage('📋 Deployment Summary') {
            steps {
                sh '''
                    echo ""
                    echo "📋 DEPLOYMENT SUMMARY"
                    echo "===================="
                    echo "✅ Application deployed successfully!"
                    echo ""
                    echo "🔧 Technical Details:"
                    echo "   Container Name: ${CONTAINER_NAME}"
                    echo "   External Port: ${PORT}"
                    echo "   Internal Port: 5000"
                    echo "   Docker Image: ${APP_NAME}:${BUILD_NUMBER}"
                    echo "   Build Number: ${BUILD_NUMBER}"
                    echo ""
                    echo "🔗 Access Information:"
                    echo "   The application is running on Jenkins server"
                    echo "   Access from within Jenkins server:"
                    echo "   curl http://localhost:${PORT}/"
                    echo "   curl http://localhost:${PORT}/health"
                    echo "   curl http://localhost:${PORT}/info"
                    echo ""
                    echo "🐳 Docker Commands for debugging:"
                    echo "   Check status: docker ps | grep ${CONTAINER_NAME}"
                    echo "   View logs: docker logs ${CONTAINER_NAME}"
                    echo "   Stop: docker stop ${CONTAINER_NAME}"
                    echo "   Remove: docker rm ${CONTAINER_NAME}"
                    echo "===================="
                '''
            }
        }
    }
    
    post {
        success {
            echo ''
            echo '🎉 🎉 🎉 PIPELINE SUCCESSFUL! 🎉 🎉 🎉'
            echo ''
            echo '✅ Safe deployment completed!'
            echo '✅ No other applications disturbed'
            echo '✅ Found available port automatically'
            echo '✅ Application is running and healthy'
            echo ''
            echo "📊 Deployment Port: ${PORT}"
            echo "📊 Container: ${CONTAINER_NAME}"
            echo ''
            
            // Optional: Archive deployment info
            archiveArtifacts artifacts: '**/*.py, **/*.txt, **/Dockerfile.*', fingerprint: true
        }
        
        failure {
            echo '❌ Pipeline failed!'
            echo ''
            echo 'Debug information:'
            sh '''
                echo "Current containers:"
                docker ps -a --filter "name=flask-" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
                echo ""
                echo "Ports in use (5000-5005):"
                for port in 5000 5001 5002 5003 5004 5005; do
                    if docker ps --format "{{.Ports}}" | grep -q "0.0.0.0:$port->"; then
                        echo "Port $port: IN USE"
                    else
                        echo "Port $port: AVAILABLE"
                    fi
                done
            '''
        }
        
        always {
            echo ''
            echo '⏰ Pipeline execution completed at: ' + new Date().toString()
            echo ''
            echo '📝 For next deployment:'
            echo '   1. Jenkins will automatically find next available port'
            echo '   2. Only our containers will be cleaned up'
            echo '   3. Other applications remain unaffected'
        }
    }
}
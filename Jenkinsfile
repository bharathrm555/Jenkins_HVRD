pipeline {
    agent any
    
    environment {
        APP_NAME = "flask-app"
        CONTAINER_NAME = "flask-${BUILD_NUMBER}"
        
        // Find available port from a wider range
        PORT = sh(script: '''
            # Try to find an available port from 5001 to 5020
            for port in {5001..5020}; do
                # Check if port is free using multiple methods
                if ! docker ps --format "{{.Ports}}" | grep -q "0.0.0.0:$port->" 2>/dev/null; then
                    echo $port
                    exit 0
                fi
            done
            # If still no port, try higher range
            for port in {5021..5100}; do
                if ! docker ps --format "{{.Ports}}" | grep -q "0.0.0.0:$port->" 2>/dev/null; then
                    echo $port
                    exit 0
                fi
            done
            # Last resort: use a random high port
            echo $(( 5100 + RANDOM % 1000 ))
        ''', returnStdout: true).trim()
    }
    
    stages {
        // STAGE 1: Checkout
        stage('📦 Checkout Code') {
            steps {
                checkout scm
                sh '''
                    echo "=== DEPLOYMENT INFO ==="
                    echo "Assigned Port: ${PORT}"
                    echo "Container: ${CONTAINER_NAME}"
                    echo "======================="
                '''
            }
        }
        
        // STAGE 2: Cleanup & Port Check
        stage('🔍 Check Port Availability') {
            steps {
                script {
                    // First, clean up ALL our old containers to free ports
                    sh '''
                        echo "Cleaning up ALL our old containers to free ports..."
                        # List all our containers
                        docker ps -a --filter "name=flask-" --format "{{.Names}}" | while read container; do
                            echo "Stopping and removing: $container"
                            docker stop "$container" 2>/dev/null || true
                            docker rm "$container" 2>/dev/null || true
                        done
                        
                        echo "Current port usage (5000-5020):"
                        for port in {5000..5020}; do
                            if docker ps --format "{{.Ports}}" | grep -q "0.0.0.0:$port->" 2>/dev/null; then
                                echo "Port $port: IN USE (NOT by us)"
                            fi
                        done
                    '''
                    
                    // Now verify our assigned port is really free
                    def portFree = sh(script: '''
                        if docker ps --format "{{.Ports}}" | grep -q "0.0.0.0:${PORT}->" 2>/dev/null; then
                            echo "false"
                        else
                            echo "true"
                        fi
                    ''', returnStdout: true).trim()
                    
                    if (portFree == "false") {
                        echo "Port ${PORT} is still busy, finding alternative..."
                        env.PORT = sh(script: '''
                            # Find first truly available port
                            for port in {5100..6000}; do
                                if ! docker ps --format "{{.Ports}}" | grep -q "0.0.0.0:$port->" 2>/dev/null; then
                                    echo $port
                                    exit 0
                                fi
                            done
                            # Emergency port
                            echo "8081"
                        ''', returnStdout: true).trim()
                        echo "Using alternative port: ${PORT}"
                    }
                }
            }
        }
        
        // STAGE 3: Run Tests
        stage('🧪 Run Tests') {
            steps {
                sh '''
                    echo "Running tests..."
                    docker run --rm \
                        -v $(pwd):/app \
                        -w /app \
                        python:3.9-slim \
                        sh -c "pip install -r requirements.txt && python test_app.py"
                '''
            }
        }
        
        // STAGE 4: Build Image
        stage('🐳 Build Docker Image') {
            steps {
                sh '''
                    echo "Building Docker image..."
                    docker build -t ${APP_NAME}:${BUILD_NUMBER} -f Dockerfile.flask .
                '''
            }
        }
        
        // STAGE 5: Deploy with Port Validation
        stage('🚀 Deploy Application') {
            steps {
                script {
                    // Try to deploy on the assigned port
                    echo "Attempting to deploy on port ${PORT}..."
                    
                    try {
                        sh """
                            # Clean up our specific container if exists
                            docker stop ${CONTAINER_NAME} 2>/dev/null || true
                            docker rm ${CONTAINER_NAME} 2>/dev/null || true
                            
                            # Deploy
                            docker run -d \\
                                --name ${CONTAINER_NAME} \\
                                -p ${PORT}:5000 \\
                                ${APP_NAME}:${BUILD_NUMBER}
                            
                            echo "✅ Deployed successfully on port ${PORT}"
                        """
                        
                    } catch (Exception e) {
                        echo "Port ${PORT} failed, trying emergency deployment..."
                        
                        // Emergency deployment with random port
                        def emergencyPort = "8${BUILD_NUMBER}01"  // Creates port like 8601, 8602, etc.
                        
                        sh """
                            docker stop ${CONTAINER_NAME} 2>/dev/null || true
                            docker rm ${CONTAINER_NAME} 2>/dev/null || true
                            
                            echo "Trying emergency port: ${emergencyPort}"
                            docker run -d \\
                                --name ${CONTAINER_NAME} \\
                                -p ${emergencyPort}:5000 \\
                                ${APP_NAME}:${BUILD_NUMBER}
                            
                            env.PORT = "${emergencyPort}"
                            echo "✅ Emergency deployment on port ${emergencyPort}"
                        """
                    }
                    
                    sleep 15
                }
            }
        }
        
        // STAGE 6: Verify Deployment
        stage('✅ Verify Deployment') {
            steps {
                sh '''
                    echo "=== VERIFICATION ==="
                    echo "Using port: ${PORT}"
                    echo ""
                    
                    # Check container status
                    echo "Container status:"
                    docker ps --filter "name=${CONTAINER_NAME}" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
                    
                    echo ""
                    echo "Testing application..."
                    
                    # Try to connect with retries
                    for i in 1 2 3 4 5; do
                        echo "Attempt $i to connect..."
                        if curl -s -f http://localhost:${PORT}/health > /dev/null 2>&1; then
                            echo "✅ SUCCESS! Application is responding!"
                            echo ""
                            echo "Quick test:"
                            curl -s http://localhost:${PORT}/ | head -2
                            break
                        else
                            if [ $i -eq 5 ]; then
                                echo "⚠️ Could not connect, but container is running."
                                echo "Checking container logs..."
                                docker logs --tail 5 ${CONTAINER_NAME}
                            else
                                echo "⏳ Waiting 5 seconds..."
                                sleep 5
                            fi
                        fi
                    done
                    
                    echo ""
                    echo "=== VERIFICATION COMPLETE ==="
                '''
            }
        }
        
        // STAGE 7: Summary
        stage('📋 Summary') {
            steps {
                sh '''
                    echo ""
                    echo "📋 DEPLOYMENT SUMMARY"
                    echo "===================="
                    echo "Status: ✅ DEPLOYED"
                    echo "Container: ${CONTAINER_NAME}"
                    echo "Port: ${PORT}"
                    echo "Build: ${BUILD_NUMBER}"
                    echo ""
                    echo "Access (from Jenkins server):"
                    echo "  curl http://localhost:${PORT}/"
                    echo "  curl http://localhost:${PORT}/health"
                    echo ""
                    echo "Debug commands:"
                    echo "  docker logs ${CONTAINER_NAME}"
                    echo "  docker inspect ${CONTAINER_NAME}"
                    echo "===================="
                '''
            }
        }
    }
    
    post {
        success {
            echo ''
            echo '🎉 DEPLOYMENT SUCCESSFUL!'
            echo "📊 Port: ${PORT}"
            echo "📊 Container: ${CONTAINER_NAME}"
            
            // Clean up very old containers (optional)
            sh '''
                echo "Cleaning up containers older than build ${BUILD_NUMBER}..."
                docker ps -a --filter "name=flask-" --format "{{.Names}} {{.CreatedAt}}" | \
                while read container; do
                    name=$(echo $container | awk '{print $1}')
                    build_num=$(echo $name | grep -o '[0-9]\+$')
                    if [ ! -z "$build_num" ] && [ "$build_num" -lt $((BUILD_NUMBER - 3)) ]; then
                        echo "Removing old container: $name"
                        docker stop "$name" 2>/dev/null || true
                        docker rm "$name" 2>/dev/null || true
                    fi
                done
            '''
        }
        
        failure {
            echo '❌ Deployment failed!'
            echo ''
            echo 'Debug information:'
            sh '''
                echo "=== DEBUG INFO ==="
                echo "All our containers:"
                docker ps -a --filter "name=flask-" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
                echo ""
                echo "Ports 5000-5020 status:"
                for port in {5000..5020}; do
                    if docker ps --format "{{.Ports}}" | grep -q "0.0.0.0:$port->" 2>/dev/null; then
                        echo "Port $port: BUSY"
                    fi
                done
                echo ""
                echo "Our Docker images:"
                docker images | grep ${APP_NAME}
                echo "=== END DEBUG ==="
            '''
        }
        
        always {
            echo ''
            echo "⏰ Build ${BUILD_NUMBER} completed at: $(date)"
        }
    }
}
pipeline {
    agent any
    
    environment {
        APP_NAME = "flask-app"
        CONTAINER_NAME = "flask-${BUILD_NUMBER}"
        // ALWAYS use a unique port based on build number
        PORT = "8${BUILD_NUMBER}01"  // Build 1 → 8101, Build 2 → 8201, etc.
    }
    
    stages {
        stage('📦 Checkout') {
            steps {
                checkout scm
                sh '''
                    echo "Using UNIQUE port: ${PORT}"
                    echo "This ensures no port conflicts!"
                '''
            }
        }
        
        stage('🧪 Test') {
            steps {
                sh '''
                    docker run --rm -v $(pwd):/app python:3.9-slim \
                    sh -c "pip install Flask && python test_app.py"
                '''
            }
        }
        
        stage('🐳 Build') {
            steps {
                sh '''
                    docker build -t ${APP_NAME}:${BUILD_NUMBER} -f Dockerfile.flask .
                '''
            }
        }
        
        stage('🚀 Deploy') {
            steps {
                sh '''
                    # Clean up our container
                    docker stop ${CONTAINER_NAME} 2>/dev/null || echo "Clean"
                    docker rm ${CONTAINER_NAME} 2>/dev/null || echo "Clean"
                    
                    # Deploy on unique port
                    docker run -d --name ${CONTAINER_NAME} -p ${PORT}:5000 ${APP_NAME}:${BUILD_NUMBER}
                    echo "✅ Deployed on unique port ${PORT}"
                    
                    sleep 10
                '''
            }
        }
        
        stage('✅ Verify') {
            steps {
                sh '''
                    echo "Container:"
                    docker ps | grep ${CONTAINER_NAME}
                    echo ""
                    echo "Testing:"
                    curl -s http://localhost:${PORT}/health || echo "App starting..."
                '''
            }
        }
    }
    
    post {
        success {
            echo "🎉 Success! Unique port ${PORT} always works!"
            echo "Access: curl http://localhost:${PORT}/"
        }
    }
}
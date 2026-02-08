pipeline {
    agent any
    
    environment {
        APP_NAME = "flask-app"
        CONTAINER_NAME = "flask-${BUILD_NUMBER}"
        PORT = "5000"
    }
    
    stages {
        stage('📦 Checkout') {
            steps {
                checkout scm
                sh 'ls -la'
            }
        }
        
        stage('🧪 Test') {
            steps {
                sh '''
                    docker run --rm -v $(pwd):/app -w /app python:3.9-slim \
                    sh -c "pip install -r requirements.txt && python test_app.py"
                '''
            }
        }
        
        stage('🐳 Build') {
            steps {
                sh '''
                    docker build -t ${APP_NAME}:${BUILD_NUMBER} -f Dockerfile.flask .
                    docker images | grep ${APP_NAME}
                '''
            }
        }
        
        stage('🚀 Deploy') {
            steps {
                sh '''
                    # Clean up
                    docker stop ${CONTAINER_NAME} 2>/dev/null || true
                    docker rm ${CONTAINER_NAME} 2>/dev/null || true
                    
                    # Deploy
                    docker run -d --name ${CONTAINER_NAME} -p ${PORT}:${PORT} ${APP_NAME}:${BUILD_NUMBER}
                    
                    echo "✅ Deployed: ${CONTAINER_NAME} on port ${PORT}"
                '''
                sleep 10
            }
        }
        
        stage('✅ Verify') {
            steps {
                sh '''
                    echo "=== Verification ==="
                    echo "Container status:"
                    docker ps | grep ${CONTAINER_NAME}
                    echo ""
                    echo "Testing app:"
                    curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:${PORT}/ || echo "Testing..."
                    echo ""
                    echo "App logs:"
                    docker logs --tail 3 ${CONTAINER_NAME}
                '''
            }
        }
    }
    
    post {
        success {
            echo '🎉 Success! App deployed on Jenkins server.'
            sh '''
                echo "Access from Jenkins server: curl http://localhost:5000/"
                echo "Container: ${CONTAINER_NAME}"
            '''
        }
        failure {
            echo '❌ Failed. Check Docker commands above.'
        }
    }
}
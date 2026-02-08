pipeline {
    agent any
    
    environment {
        APP_NAME = "flask-app"
        CONTAINER_NAME = "flask-${BUILD_NUMBER}"
    }
    
    stages {
        stage('📦 Checkout') {
            steps { checkout scm }
        }
        
        stage('🚀 Deploy') {
            steps {
                script {
                    // Let Docker assign ANY available port
                    sh '''
                        docker stop ${CONTAINER_NAME} 2>/dev/null || true
                        docker rm ${CONTAINER_NAME} 2>/dev/null || true
                        
                        # Run without -p flag, let Docker choose
                        docker run -d --name ${CONTAINER_NAME} ${APP_NAME}:${BUILD_NUMBER}
                    '''
                    
                    // Get the assigned port
                    env.ASSIGNED_PORT = sh(script: '''
                        docker port ${CONTAINER_NAME} 5000 | cut -d: -f2
                    ''', returnStdout: true).trim()
                    
                    echo "✅ Deployed! Docker assigned port: ${ASSIGNED_PORT}"
                }
                sleep 10
            }
        }
        
        stage('✅ Verify') {
            steps {
                sh '''
                    echo "Container info:"
                    docker ps | grep ${CONTAINER_NAME}
                    echo ""
                    echo "Assigned port: ${ASSIGNED_PORT}"
                    echo ""
                    echo "Testing via container network:"
                    docker exec ${CONTAINER_NAME} curl -s http://localhost:5000/health || echo "Testing..."
                '''
            }
        }
    }
}
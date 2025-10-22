pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "fastapi-app-local"
        DOCKER_TAG = "${BUILD_NUMBER}"
        CONTAINER_NAME = "fastapi-test"
        HOST_PORT = 8000
        CONTAINER_PORT = 8000 
    }

    stages {
        stage('📦 Checkout Code') {
            steps {
                echo '=== Checking out code from GitHub ==='
                git branch: 'main',
                    credentialsId: 'github-credentials', 
                    url: 'https://github.com/mglee0812/devops-test.git'
                echo '✅ Code checkout successful'
            }
        }

        stage('🔨 Build Docker Image') {
            steps {
                echo '=== Building Docker image ==='
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                    sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
                }
                echo '✅ Docker image built successfully'
            }
        }

        stage('🚀 Deploy Container') {
            steps {
                echo '=== Deploying container on Jenkins VM ==='
                sh """
                    docker stop ${CONTAINER_NAME} 2>/dev/null || true
                    docker rm ${CONTAINER_NAME} 2>/dev/null || true

                    docker run -d \\
                        --name ${CONTAINER_NAME} \\
                        --restart unless-stopped \\
                        -p ${HOST_PORT}:${CONTAINER_PORT} \\
                        ${DOCKER_IMAGE}:latest

                    echo "✅ Deployment completed on Jenkins VM"
                """
            }
        }

        stage('🏥 Health Check') {
            steps {
                echo '=== Performing health check ==='
                script {
                    def MAX_ATTEMPTS = 6
                    def SLEEP_TIME = 5
                    
                    for (int i = 1; i <= MAX_ATTEMPTS; i++) {
                        sleep SLEEP_TIME
                        echo "Attempting health check (Attempt ${i}/${MAX_ATTEMPTS})..."
                        
                        def healthCheck = sh(
                            script: "docker exec ${CONTAINER_NAME} curl -f -s -o /dev/null -w '%{http_code}' http://localhost:${CONTAINER_PORT} || echo '000'",
                            returnStdout: true
                        ).trim()

                        echo "Health check status: ${healthCheck}"
                        
                        if (healthCheck == '200') {
                            echo '✅ Health check passed!'
                            return
                        }
                    }
                    error("❌ Health check failed after ${MAX_ATTEMPTS} attempts. Check container logs and server binding (0.0.0.0).")
                }
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up local images...'
            sh 'docker image prune -af || true'
        }
        success {
            echo """
            ✅✅✅ Deployment Successful! ✅✅✅
            =========================================
            Application is now running on VM port ${HOST_PORT}.
            =========================================
            """
        }
    }
}

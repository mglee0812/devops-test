pipeline {
    agent any

    environment {
        // Docker 이미지 이름
        DOCKER_IMAGE = "fastapi-app-local"
        DOCKER_TAG = "${BUILD_NUMBER}"

        // Jenkins VM 내부에서 실행할 컨테이너 이름
        CONTAINER_NAME = "fastapi-test"
        
        // 컨테이너 포트 설정 (VM의 8000 포트에 연결)
        HOST_PORT = 8000
        CONTAINER_PORT = 8000 
    }

    stages {
        stage('📦 Checkout Code') {
            steps {
                echo '=== Checking out code from GitHub ==='
                // TODO: 'github-credentials' ID를 Jenkins에 설정한 실제 Git Credentials ID로 변경해야 합니다.
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
                    echo "=== Stopping old container (${CONTAINER_NAME}) ==="
                    docker stop ${CONTAINER_NAME} 2>/dev/null || true
                    docker rm ${CONTAINER_NAME} 2>/dev/null || true

                    echo "=== Starting new container ==="
                    // VM의 ${HOST_PORT}를 컨테이너의 ${CONTAINER_PORT}로 연결하여 새 컨테이너 실행
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
                    sleep 10 // 컨테이너 시작 대기

                    // VM 내부의 HOST_PORT (8000)로 헬스 체크를 수행합니다.
                    def healthCheck = sh(
                        script: "curl -f -s -o /dev/null -w \"%{http_code}\" http://localhost:${HOST_PORT}/health || echo '000'",
                        returnStdout: true
                    ).trim()

                    echo "Health check status: ${healthCheck}"

                    if (healthCheck == '200') {
                        echo '✅ Health check passed!'
                    } else {
                        error("❌ Health check failed with status: ${healthCheck}. Check container logs.")
                    }
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

            Access URL (VM internal): http://10.0.2.10:${HOST_PORT}
            Access URL (Host PC/External via NAT): http://<Your_Host_IP>:${HOST_PORT}
            =========================================
            """
        }
    }
}
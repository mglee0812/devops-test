pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "fastapi-app-local"
        CONTAINER_NAME = "fastapi-test"
        VM_IP = "10.0.2.10"
        HOST_PORT = 8000
        CONTAINER_PORT = 8000 
    }

    stages {
        // ... Checkout Code 단계는 그대로 둠 ...

        stage('🔨 Build Docker Image') {
            steps {
                echo '=== Building Docker image ==='
                script {
                    // 🚨 날짜 태그 변수를 이 단계에서 정의하여 안정성을 높입니다.
                    def dateTag = sh(returnStdout: true, script: 'date +%Y%m%d-%H%M%S').trim()
                    env.DATE_TAG = dateTag // 환경 변수로 설정

                    // DATE_TAG 형식으로 이미지 빌드
                    sh "docker build -t ${env.DOCKER_IMAGE}:${env.DATE_TAG} ."
                }
                echo "✅ Docker image built successfully with tag: ${env.DATE_TAG}"
            }
        }

        stage('🚀 Deploy Container') {
            steps {
                echo '=== Deploying container on Jenkins VM ==='
                sh """
                    echo "=== Stopping old container (${env.CONTAINER_NAME}) ==="
                    docker stop ${env.CONTAINER_NAME} 2>/dev/null || true
                    docker rm ${env.CONTAINER_NAME} 2>/dev/null || true

                    echo "=== Starting new container ==="
                    docker run -d \\
                        --name ${env.CONTAINER_NAME} \\
                        --restart unless-stopped \\
                        -p ${env.HOST_PORT}:${env.CONTAINER_PORT} \\
                        ${env.DOCKER_IMAGE}:${env.DATE_TAG}

                    echo "✅ Deployment completed on Jenkins VM"
                """
            }
        }
    }
    // ... post 블록은 env.DATE_TAG를 사용하여 그대로 둡니다. ...
}
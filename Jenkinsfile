pipeline {
    agent any

    environment {
        // Docker 이미지 이름 (변하지 않는 부분)
        DOCKER_IMAGE = "fastapi-app-local"
        
        // 현재 날짜와 시간으로 태그 생성 (예: 20251022-211153)
        DATE_TAG = sh(returnStdout: true, script: 'date +%Y%m%d-%H%M%S').trim()

        // Jenkins VM의 내부 IP 주소 (변수 처리)
        VM_IP = "10.0.2.10"
        
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
                // 'github-credentials' ID를 Jenkins에 설정한 실제 Git Credentials ID로 변경해야 합니다.
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
                    // DATE_TAG 형식으로 이미지 빌드
                    sh "docker build -t ${DOCKER_IMAGE}:${DATE_TAG} ."
                }
                echo "✅ Docker image built successfully with tag: ${DATE_TAG}"
            }
        }

        stage('🚀 Deploy Container') {
            steps {
                echo '=== Deploying container on Jenkins VM ==='
                sh """
                    echo "=== Stopping old container (${CONTAINER_NAME}) ==="
                    # 기존 컨테이너 정지 및 제거 (충돌 방지)
                    docker stop ${CONTAINER_NAME} 2>/dev/null || true
                    docker rm ${CONTAINER_NAME} 2>/dev/null || true

                    echo "=== Starting new container ==="
                    # DATE_TAG로 빌드된 이미지를 사용하여 컨테이너 실행
                    docker run -d \\
                        --name ${CONTAINER_NAME} \\
                        --restart unless-stopped \\
                        -p ${HOST_PORT}:${CONTAINER_PORT} \\
                        ${DOCKER_IMAGE}:${DATE_TAG}

                    echo "✅ Deployment completed on Jenkins VM"
                """
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up local images (untagged or old)...'
            // 태그 없는 이미지들만 정리
            sh 'docker image prune -af || true'
        }
        success {
            echo """
            ✅✅✅ Deployment Successful! ✅✅✅
            =========================================
            Image Tag Used: ${DATE_TAG}
            Application is now running on VM port ${HOST_PORT}.
            
            Access URL (VM internal): http://${VM_IP}:${HOST_PORT} 
            Access URL (Host PC/External via NAT): http://<Your_Host_IP>:${HOST_PORT}
            =========================================
            """
        }
    }
}
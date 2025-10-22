pipeline {
    agent any

    environment {
        // Docker 이미지 이름
        DOCKER_IMAGE = "fastapi-app-local"
        // 빌드 번호를 태그로 사용 (이미지 덮어쓰기 방지)
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
                    // 새로운 빌드 번호 태그로 이미지 빌드
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                    // 기존 'latest' 태그 업데이트 코드는 제거하여 덮어쓰기를 방지합니다.
                }
                echo '✅ Docker image built successfully'
            }
        }

        stage('🚀 Deploy Container') {
            steps {
                echo '=== Deploying container on Jenkins VM ==='
                sh """
                    // ⚠️ 경고: 기존 컨테이너를 정지/제거하는 코드가 없으므로, 두 번째 실행 시 충돌이 발생합니다.
                    // docker stop ${CONTAINER_NAME} 2>/dev/null || true
                    // docker rm ${CONTAINER_NAME} 2>/dev/null || true

                    echo "=== Starting new container ==="
                    // VM의 ${HOST_PORT}를 컨테이너의 ${CONTAINER_PORT}로 연결하여 새 컨테이너 실행
                    // 배포 시 DOCKER_TAG (빌드 번호)를 명시적으로 사용합니다.
                    docker run -d \\
                        --name ${CONTAINER_NAME} \\
                        --restart unless-stopped \\
                        -p ${HOST_PORT}:${CONTAINER_PORT} \\
                        ${DOCKER_IMAGE}:${DOCKER_TAG}

                    echo "✅ Deployment completed on Jenkins VM"
                """
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up local images...'
            // 태그 없는 이미지들만 정리
            sh 'docker image prune -af || true'
        }
        success {
            echo """
            ✅✅✅ Deployment Successful! ✅✅✅
            =========================================
            Application deployment initiated on VM port ${HOST_PORT}.
            
            Access URL (VM internal): http://10.0.2.10:${HOST_PORT}
            Access URL (Host PC/External via NAT): http://<Your_Host_IP>:${HOST_PORT}
            =========================================
            """
        }
    }
}
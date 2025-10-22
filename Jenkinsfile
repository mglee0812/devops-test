pipeline {
    agent any

    environment {
        // Docker 이미지 이름
        DOCKER_IMAGE = "fastapi-img"
        CONTAINER_NAME = "fastapi-app"
        
        // 배포 대상 서버 정보
        DEPLOY_SERVER_IP = "10.0.2.11" // WebApp Server IP
        HOST_PORT = 8000
        CONTAINER_PORT = 8000 
        
        // 💡 Docker Hub 인증 정보
        DOCKER_HUB_ID = "mglee08122" 
        DOCKER_HUB_CRED = 'dockerhub-credentials' // Jenkins Credentials ID
        
        // 💡 SSH 인증 정보
        SSH_CREDENTIALS = 'ssh-webapp-server' // Jenkins Credentials ID
        REMOTE_USER = 'appadmin' // WebApp 서버 접속 사용자 ID (수동 테스트 기반으로 'appadmin'으로 변경)
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
                    // 현재 날짜 및 시간으로 태그 생성
                    def dateTag = sh(returnStdout: true, script: 'date +%Y%m%d-%H%M%S').trim()
                    env.DATE_TAG = dateTag

                    // Docker Hub Full Tag (예: mglee08122/fastapi-img:20251022-211153)
                    env.FULL_IMAGE_TAG = "${env.DOCKER_HUB_ID}/${env.DOCKER_IMAGE}:${env.DATE_TAG}"

                    // 이미지 빌드 (Full Tag 사용)
                    sh "docker build -t ${env.FULL_IMAGE_TAG} ."
                }
                echo "✅ Docker image built successfully with tag: ${env.FULL_IMAGE_TAG}"
            }
        }

        stage('⬆️ Push Docker Image') {
            steps {
                echo "=== Pushing image to Docker Hub: ${env.FULL_IMAGE_TAG} ==="
                // Docker Hub Credential을 사용하여 로그인 및 Push
                withCredentials([usernamePassword(credentialsId: "${env.DOCKER_HUB_CRED}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"
                    sh "docker push ${env.FULL_IMAGE_TAG}"
                    sh 'docker logout'
                }
                echo "✅ Image push successful"
            }
        }

        stage('🚀 Remote Pull & Deploy') {
            steps {
                echo "=== Deploying on WebApp Server: ${env.DEPLOY_SERVER_IP} ==="
                
                // Groovy 변수 선언 및 복잡한 로직 처리를 위한 script 블록
                script {
                    // WebApp 서버 쉘에서 실행할 명령어 문자열 정의 (세미콜론으로 연결)
                    def remoteCommands = """
                        # 1. 이미지 Pull
                        docker pull ${env.FULL_IMAGE_TAG};

                        # 2. 기존 컨테이너 정리
                        docker stop ${env.CONTAINER_NAME} 2>/dev/null || true;
                        docker rm ${env.CONTAINER_NAME} 2>/dev/null || true;

                        # 3. 새로운 컨테이너 실행
                        docker run -d --name ${env.CONTAINER_NAME} --restart unless-stopped -p ${env.HOST_PORT}:${env.CONTAINER_PORT} ${env.FULL_IMAGE_TAG}
                    """
                    
                    // SSH Agent를 사용하여 WebApp 서버에 원격 접속 및 명령 실행
                    sshagent(credentials: ["${env.SSH_CREDENTIALS}"]) {
                        // ssh -tt 옵션 제거하여 자동화 환경에 적합하도록 수정
                        sh "ssh ${env.REMOTE_USER}@${env.DEPLOY_SERVER_IP} '${remoteCommands}'"
                    }
                }
                echo "✅ Deployment completed on WebApp Server."
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up local images (untagged or old) on Jenkins VM...'
            // 이미지 정리
            sh 'docker image prune -af || true'
        }
        success {
            echo """
            ✅✅✅ Deployment Successful! ✅✅✅
            =========================================
            Image Tag Pushed: ${env.FULL_IMAGE_TAG}
            Deployment Target: ${env.DEPLOY_SERVER_IP}
            
            Application Access URL: http://${env.DEPLOY_SERVER_IP}:${env.HOST_PORT} 
            =========================================
            """
        }
    }
}
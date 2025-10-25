pipeline {
    agent any

    environment {
    
        // 배포 대상 서버 정보
        DEPLOY_SERVER_IP = "192.168.55.101"
        HOST_PORT = 8000
        CONTAINER_PORT = 8000 

        // SSH 인증 정보
        SSH_CREDENTIALS = 'webapp-server'
        REMOTE_USER = 'appadmin'

        // Docker, Container 정보
        DOCKER_IMAGE = "fastapi-img"
        CONTAINER_NAME = "fastapi-app"
        
        // Docker Hub 인증 정보
        DOCKER_HUB_ID = "mglee08122" 
        DOCKER_HUB_CRED = 'dockerhub-credentials'
        
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo '=== Checking out code from GitHub ==='
                git branch: 'main',
                    credentialsId: 'github-credentials', 
                    url: 'https://github.com/mglee0812/devops-test.git'
                echo 'Code checkout successful'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '=== Building Docker image ==='
                script {

                    // 태그명 지정
                    def dateTag = sh(returnStdout: true, script: 'date +%Y%m%d-%H%M').trim()
                    env.DATE_TAG = dateTag

                    env.FULL_IMAGE_TAG = "${env.DOCKER_HUB_ID}/${env.DOCKER_IMAGE}:${env.DATE_TAG}"

                    // 이미지 빌드
                    sh "docker build -t ${env.FULL_IMAGE_TAG} ."
                }
                echo "Docker image built successfully with tag: ${env.FULL_IMAGE_TAG}"
            }
        }

        stage('Push Docker Image') {
            steps {
                echo "=== Pushing image to Docker Hub: ${env.FULL_IMAGE_TAG} ==="

                // Docker Hub 로그인 및 Push
                withCredentials([usernamePassword(credentialsId: "${env.DOCKER_HUB_CRED}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"
                    sh "docker push ${env.FULL_IMAGE_TAG}"
                    sh 'docker logout'
                }
                echo "Image push successful"
            }
        }

        stage('Remote Pull & Deploy') {
            steps {
                echo "=== Deploying on WebApp Server: ${env.DEPLOY_SERVER_IP} ==="
                
                script {
                    
                    def remoteCommands = """
                        docker pull ${env.FULL_IMAGE_TAG};
                        docker stop ${env.CONTAINER_NAME} 2>/dev/null || true;
                        docker rm ${env.CONTAINER_NAME} 2>/dev/null || true;
                        docker run -d --name ${env.CONTAINER_NAME} --restart unless-stopped -p ${env.HOST_PORT}:${env.CONTAINER_PORT} ${env.FULL_IMAGE_TAG}
                    """
                    
                    sshagent(credentials: ["${env.SSH_CREDENTIALS}"]) {
                        sh "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${env.REMOTE_USER}@${env.DEPLOY_SERVER_IP} '${remoteCommands}'"
                    }
                }
                echo "Deployment completed on WebApp Server."
            }
        }
    }
}
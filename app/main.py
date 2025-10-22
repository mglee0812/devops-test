from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# FastAPI 앱 생성 및 버전 업데이트
app = FastAPI(
    title="Simple CI/CD Test App",
    description="극도로 단순화된 배포 테스트 앱",
    version="1.1.0-DEPLOY-TEST" # 배포 확인을 위한 버전 태그
)

# 1. 홈페이지 (HTML 렌더링)
@app.get("/info", response_class=HTMLResponse)
async def read_root():
    """메인 페이지: 배포 성공 메시지 출력"""
    
    # 💡 배포 성공 확인 메시지
    message = "<h1>✅ Jenkins CI/CD 파이프라인 배포 성공 확인! (V1.1.0)</h1>"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{app.title}</title>
    </head>
    <body>
        {message}
        <p>현재 애플리케이션 버전: {app.version}</p>
        <p>배포 서버 IP: (현재 실행 중인 10.0.2.11)</p>
        <p>Health Check: <a href="/health">/health</a> 엔드포인트 확인</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# 2. Health Check (Jenkins/모니터링에서 사용)
@app.get("/health")
async def health_check():
    """서버 상태 확인"""
    return {
        "status": "healthy", 
        "version": app.version,
        "message": "Application is running successfully on webapp-server"
    }
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import pytz
import os

# FastAPI 앱 생성
app = FastAPI(
    title="DevOps CI/CD Demo",
    description="Jenkins를 통한 자동 배포 데모",
    version="2.0.0"
)

# 정적 파일 및 템플릿 설정
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 한국 타임존 설정
KST = pytz.timezone('Asia/Seoul')

# 간단한 상품 데이터 (in-memory)
products = [
    {"id": 1, "name": "MacBook Pro", "price": 3500000, "stock": 5},
    {"id": 2, "name": "iPad Air", "price": 850000, "stock": 12},
    {"id": 3, "name": "AirPods Pro", "price": 350000, "stock": 0},
    {"id": 4, "name": "Apple Watch", "price": 550000, "stock": 8},
    {"id": 5, "name": "Apple", "price": 1000000, "stock": 0},
    {"id": 6, "name": "New Product", "price": 3000000, "stock": 10}
]

# 배포 정보 - 모든 키를 미리 정의
deployment_info = {
    "version": "2.0.0",
    "build_number": os.getenv("BUILD_NUMBER", "dev"),
    "build_timestamp": os.getenv("BUILD_TIMESTAMP", "unknown"),
    "deployed_at": None,
    "server": "10.0.2.6"
}

# ==================== 웹 페이지 ====================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """메인 홈페이지"""
    total_products = len(products)
    in_stock = sum(1 for p in products if p["stock"] > 0)
    out_of_stock = total_products - in_stock
    total_value = sum(p["price"] * p["stock"] for p in products)
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "DevOps CI/CD Demo",
            "deployment": deployment_info,
            "products": products,
            "stats": {
                "total": total_products,
                "in_stock": in_stock,
                "out_of_stock": out_of_stock,
                "total_value": total_value
            }
        }
    )

# ==================== API 엔드포인트 ====================

@app.get("/health")
async def health_check():
    """Health Check (Jenkins에서 사용)"""
    return {
        "status": "healthy",
        "version": deployment_info["version"],
        "build": deployment_info["build_number"],
        "message": "Application is running successfully!"
    }

@app.get("/api/info")
async def app_info():
    """애플리케이션 정보"""
    return {
        "app_name": app.title,
        "version": app.version,
        "deployment": deployment_info,
        "features": [
            "✅ GitHub Webhook 연동",
            "✅ Jenkins 자동 빌드",
            "✅ Docker 컨테이너 배포",
            "✅ Health Check 지원"
        ]
    }

@app.get("/api/products")
async def get_products():
    """상품 목록 조회"""
    return products

@app.get("/api/products/{product_id}")
async def get_product(product_id: int):
    """특정 상품 조회"""
    for product in products:
        if product["id"] == product_id:
            return product
    return {"error": "Product not found"}

@app.get("/api/stats")
async def get_stats():
    """통계 정보"""
    total_products = len(products)
    in_stock = sum(1 for p in products if p["stock"] > 0)
    total_value = sum(p["price"] * p["stock"] for p in products)
    
    return {
        "total_products": total_products,
        "in_stock_count": in_stock,
        "out_of_stock_count": total_products - in_stock,
        "total_inventory_value": total_value,
        "average_price": sum(p["price"] for p in products) / total_products
    }

# ==================== 시작/종료 이벤트 ====================

@app.on_event("startup")
async def startup_event():
    # 한국 시간으로 배포 시간 설정
    now_kst = datetime.now(KST)
    deployment_info["deployed_at"] = now_kst.strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 60)
    print(f"🚀 FastAPI Application Started")
    print(f"📦 Version: {deployment_info['version']}")
    print(f"🔨 Build Number: {deployment_info['build_number']}")
    print(f"🏗️  Build Time: {deployment_info['build_timestamp']}")
    print(f"🖥️  Server: {deployment_info['server']}")
    print(f"📅 Deployed At: {deployment_info['deployed_at']} KST")
    print("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    print("👋 Application shutting down...")
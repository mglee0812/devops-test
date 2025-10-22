from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import uvicorn

# FastAPI 앱 생성
app = FastAPI(
    title="My First FastAPI App",
    description="DevOps 과제용 웹 애플리케이션",
    version="1.1.0-DEPLOY-TEST"
)

# 정적 파일 (CSS, JS) 경로 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML 템플릿 경로 설정
templates = Jinja2Templates(directory="templates")

# 데이터 모델 정의 (Pydantic)
class Item(BaseModel):
    id: int
    name: str
    description: str = None
    price: float
    
class Message(BaseModel):
    message: str

# 간단한 in-memory 데이터베이스 (실습용)
items_db: List[Item] = [
    Item(id=1, name="Laptop", description="고성능 노트북", price=1500000),
    Item(id=2, name="Mouse", description="무선 마우스", price=30000),
    Item(id=3, name="Keyboard", description="기계식 키보드", price=150000),
]

# ==================== API 엔드포인트 ====================

# 1. 홈페이지 (HTML 렌더링)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """메인 페이지"""
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": "FastAPI 웹 애플리케이션"}
    )

# 2. Health Check (Jenkins에서 사용)
@app.get("/health")
async def health_check():
    """서버 상태 확인"""
    return {"status": "healthy", "message": "Application is running"}

# 3. 모든 아이템 조회
@app.get("/api/items", response_model=List[Item])
async def get_items():
    """전체 아이템 목록 반환"""
    return items_db

# 4. 특정 아이템 조회
@app.get("/api/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """ID로 아이템 조회"""
    for item in items_db:
        if item.id == item_id:
            return item
    return {"error": "Item not found"}

# 5. 아이템 추가
@app.post("/api/items", response_model=Item)
async def create_item(item: Item):
    """새 아이템 추가"""
    items_db.append(item)
    return item

# 6. 아이템 삭제
@app.delete("/api/items/{item_id}")
async def delete_item(item_id: int):
    """ID로 아이템 삭제"""
    global items_db
    items_db = [item for item in items_db if item.id != item_id]
    return {"message": f"Item {item_id} deleted"}

# 7. 간단한 계산 API
@app.get("/api/calculate")
async def calculate(a: int, b: int, operation: str = "add"):
    """간단한 계산기 API"""
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        result = a / b if b != 0 else "Error: Division by zero"
    else:
        result = "Invalid operation"
    
    return {
        "a": a,
        "b": b,
        "operation": operation,
        "result": result
    }

# 8. 서버 정보
@app.get("/api/info")
async def server_info():
    """서버 정보 반환"""
    return {
        "app_name": "FastAPI DevOps Demo",
        "version": "1.0.0",
        "python_version": "3.11",
        "framework": "FastAPI",
        "total_items": len(items_db)
    }

# ==================== 메인 실행 ====================
if __name__ == "__main__":
    # 개발 환경에서 직접 실행시
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # 코드 변경시 자동 재시작
    )
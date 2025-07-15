from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import uvicorn
from typing import List, Optional
import shutil
from pathlib import Path

from api.endpoints import router as api_router
from services.analyzer import AnalyzerService
from utils.file_processor import FileProcessor

# 앱 초기화
app = FastAPI(
    title="Fitcruit API",
    description="AI 기반 채용 자동화 SaaS - 이력서 및 포트폴리오 분석 시스템",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React 개발 서버
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")

# 업로드 디렉토리 확인/생성
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# 라우터 등록
app.include_router(api_router, prefix="/api/v1")

# 서비스 초기화
analyzer_service = AnalyzerService()
file_processor = FileProcessor()

@app.get("/")
async def root():
    return {
        "message": "Fitcruit API에 오신 것을 환영합니다!",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Fitcruit API"}

# 파일 업로드 엔드포인트
@app.post("/api/v1/upload")
async def upload_file(file: UploadFile = File(...)):
    """파일 업로드 (이력서 또는 포트폴리오)"""
    try:
        # 파일 유효성 검사
        if not file.filename:
            raise HTTPException(status_code=400, detail="파일명이 없습니다.")
        
        # 파일 확장자 검사
        allowed_extensions = ['.pdf', '.docx', '.doc', '.txt']
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"지원하지 않는 파일 형식입니다. 지원 형식: {', '.join(allowed_extensions)}"
            )
        
        # 파일 저장
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 파일 처리 및 분석 시작
        extracted_text = await file_processor.extract_text(file_path)
        
        return {
            "message": "파일 업로드 성공",
            "filename": file.filename,
            "file_size": file_path.stat().st_size,
            "file_type": file_extension,
            "extracted_text_length": len(extracted_text),
            "file_path": str(file_path)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 업로드 중 오류 발생: {str(e)}")

# 이력서 분석 엔드포인트
@app.post("/api/v1/analyze/resume")
async def analyze_resume(file: UploadFile = File(...)):
    """이력서 분석"""
    try:
        # 파일 저장
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 이력서 분석 수행
        analysis_result = await analyzer_service.analyze_resume(file_path)
        
        return {
            "status": "success",
            "filename": file.filename,
            "analysis": analysis_result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이력서 분석 중 오류 발생: {str(e)}")

# 포트폴리오 분석 엔드포인트
@app.post("/api/v1/analyze/portfolio")
async def analyze_portfolio(file: UploadFile = File(...)):
    """포트폴리오 분석"""
    try:
        # 파일 저장
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 포트폴리오 분석 수행
        analysis_result = await analyzer_service.analyze_portfolio(file_path)
        
        return {
            "status": "success",
            "filename": file.filename,
            "analysis": analysis_result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"포트폴리오 분석 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
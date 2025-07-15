from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from typing import List, Optional, Dict, Any
import json
import csv
import io
from pathlib import Path
import tempfile
import zipfile
from datetime import datetime

from models.schemas import (
    BaseResponse, AnalysisStatus, FileType, ComparisonAnalysis,
    JobMatchingResponse, InterviewQuestionsResponse
)
from services.analyzer import AnalyzerService

# 라우터 생성
router = APIRouter()

# 분석 서비스 인스턴스 (의존성 주입)
def get_analyzer_service():
    return AnalyzerService()

@router.get("/status/{analysis_id}")
async def get_analysis_status(
    analysis_id: str,
    analyzer: AnalyzerService = Depends(get_analyzer_service)
):
    """분석 상태를 조회합니다."""
    try:
        status = analyzer.get_analysis_status(analysis_id)
        
        if status is None:
            raise HTTPException(status_code=404, detail="분석 ID를 찾을 수 없습니다.")
        
        return {
            "analysis_id": analysis_id,
            "status": status,
            "timestamp": datetime.now()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"상태 조회 중 오류 발생: {str(e)}")

@router.get("/result/{analysis_id}")
async def get_analysis_result(
    analysis_id: str,
    analyzer: AnalyzerService = Depends(get_analyzer_service)
):
    """분석 결과를 조회합니다."""
    try:
        result = analyzer.get_cached_result(analysis_id)
        
        if result is None:
            raise HTTPException(status_code=404, detail="분석 결과를 찾을 수 없습니다.")
        
        return {
            "analysis_id": analysis_id,
            "result": result['result'],
            "processing_time": result['processing_time'],
            "timestamp": result['timestamp']
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"결과 조회 중 오류 발생: {str(e)}")

@router.post("/batch-analyze")
async def batch_analyze_files(
    files: List[UploadFile] = File(...),
    job_position: Optional[str] = Form(None),
    analyzer: AnalyzerService = Depends(get_analyzer_service)
):
    """여러 파일을 동시에 분석합니다."""
    try:
        if len(files) > 10:
            raise HTTPException(status_code=400, detail="한 번에 최대 10개 파일까지만 분석 가능합니다.")
        
        # 임시 파일 저장
        temp_paths = []
        for file in files:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix)
            content = await file.read()
            temp_file.write(content)
            temp_file.close()
            temp_paths.append(Path(temp_file.name))
        
        # 배치 분석 수행
        results = await analyzer.batch_analyze(temp_paths)
        
        # 결과 정리
        batch_results = []
        for i, (file, result) in enumerate(zip(files, results)):
            if result is not None:
                batch_results.append({
                    "filename": file.filename,
                    "analysis_result": result,
                    "status": "success"
                })
            else:
                batch_results.append({
                    "filename": file.filename,
                    "analysis_result": None,
                    "status": "failed"
                })
        
        # 임시 파일 정리
        for temp_path in temp_paths:
            temp_path.unlink()
        
        return {
            "message": "배치 분석 완료",
            "total_files": len(files),
            "successful_analyses": len([r for r in batch_results if r["status"] == "success"]),
            "results": batch_results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"배치 분석 중 오류 발생: {str(e)}")

@router.post("/compare-candidates")
async def compare_candidates(
    files: List[UploadFile] = File(...),
    job_position: Optional[str] = Form(None),
    analyzer: AnalyzerService = Depends(get_analyzer_service)
):
    """후보자들을 비교 분석합니다."""
    try:
        if len(files) < 2:
            raise HTTPException(status_code=400, detail="비교를 위해서는 최소 2개의 파일이 필요합니다.")
        
        if len(files) > 5:
            raise HTTPException(status_code=400, detail="한 번에 최대 5명까지만 비교 가능합니다.")
        
        # 임시 파일 저장
        temp_paths = []
        for file in files:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix)
            content = await file.read()
            temp_file.write(content)
            temp_file.close()
            temp_paths.append(Path(temp_file.name))
        
        # 비교 분석 수행
        comparison_result = await analyzer.compare_candidates(temp_paths, job_position)
        
        # 임시 파일 정리
        for temp_path in temp_paths:
            temp_path.unlink()
        
        return {
            "message": "후보자 비교 분석 완료",
            "comparison_result": comparison_result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"후보자 비교 중 오류 발생: {str(e)}")

@router.get("/analytics")
async def get_analytics(
    analyzer: AnalyzerService = Depends(get_analyzer_service)
):
    """분석 통계를 반환합니다."""
    try:
        analytics = analyzer.get_analytics_summary()
        
        return {
            "message": "분석 통계 조회 완료",
            "analytics": analytics
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"통계 조회 중 오류 발생: {str(e)}")

@router.post("/clear-cache")
async def clear_cache(
    older_than_hours: int = Query(24, description="지정된 시간(시간)보다 오래된 캐시 삭제"),
    analyzer: AnalyzerService = Depends(get_analyzer_service)
):
    """캐시를 정리합니다."""
    try:
        analyzer.clear_cache(older_than_hours)
        
        return {
            "message": f"{older_than_hours}시간 이상 된 캐시가 정리되었습니다."
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"캐시 정리 중 오류 발생: {str(e)}")

@router.get("/export/{analysis_id}")
async def export_analysis_result(
    analysis_id: str,
    format: str = Query("json", description="내보내기 형식 (json, csv)"),
    analyzer: AnalyzerService = Depends(get_analyzer_service)
):
    """분석 결과를 내보냅니다."""
    try:
        result = analyzer.get_cached_result(analysis_id)
        
        if result is None:
            raise HTTPException(status_code=404, detail="분석 결과를 찾을 수 없습니다.")
        
        if format.lower() == "json":
            # JSON 형식으로 내보내기
            export_data = {
                "analysis_id": analysis_id,
                "result": result['result'],
                "processing_time": result['processing_time'],
                "timestamp": result['timestamp'].isoformat(),
                "exported_at": datetime.now().isoformat()
            }
            
            # JSON 파일 생성
            json_content = json.dumps(export_data, ensure_ascii=False, indent=2)
            
            return JSONResponse(
                content=export_data,
                headers={
                    "Content-Disposition": f"attachment; filename=analysis_{analysis_id}.json"
                }
            )
        
        elif format.lower() == "csv":
            # CSV 형식으로 내보내기 (요약 정보만)
            analysis_result = result['result']
            
            # CSV 데이터 준비
            csv_data = []
            
            # 기본 정보
            csv_data.append(["분석 ID", analysis_id])
            csv_data.append(["분석 시간", result['timestamp'].isoformat()])
            csv_data.append(["처리 시간", f"{result['processing_time']:.2f}초"])
            
            # 점수 정보
            if hasattr(analysis_result, 'score'):
                csv_data.append(["전체 점수", f"{analysis_result.score.overall_score:.1f}"])
                csv_data.append(["기술 점수", f"{analysis_result.score.breakdown.technical_skills:.1f}"])
                csv_data.append(["경험 점수", f"{analysis_result.score.breakdown.experience_relevance:.1f}"])
                csv_data.append(["교육 점수", f"{analysis_result.score.breakdown.education_background:.1f}"])
            
            # 스킬 정보
            if hasattr(analysis_result, 'skills'):
                csv_data.append(["스킬 수", len(analysis_result.skills)])
                for skill in analysis_result.skills[:5]:  # 상위 5개만
                    csv_data.append([f"스킬: {skill.name}", f"{skill.level}, 신뢰도: {skill.confidence:.2f}"])
            
            # CSV 파일 생성
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerows(csv_data)
            
            return JSONResponse(
                content={"csv_data": output.getvalue()},
                headers={
                    "Content-Disposition": f"attachment; filename=analysis_{analysis_id}.csv"
                }
            )
        
        else:
            raise HTTPException(status_code=400, detail="지원하지 않는 형식입니다. (json, csv만 지원)")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"내보내기 중 오류 발생: {str(e)}")

@router.post("/analyze-with-job-requirements")
async def analyze_with_job_requirements(
    file: UploadFile = File(...),
    job_title: str = Form(...),
    job_requirements: str = Form(...),
    company_name: Optional[str] = Form(None),
    analyzer: AnalyzerService = Depends(get_analyzer_service)
):
    """직무 요구사항과 함께 분석합니다."""
    try:
        # 임시 파일 저장
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix)
        content = await file.read()
        temp_file.write(content)
        temp_file.close()
        temp_path = Path(temp_file.name)
        
        # 기본 분석 수행
        analysis_result = await analyzer.analyze_file(temp_path, job_position=job_title)
        
        # 직무 요구사항 매칭 분석
        job_requirements_list = [req.strip() for req in job_requirements.split(',')]
        
        # 매칭 점수 계산
        matching_score = calculate_job_matching_score(analysis_result, job_requirements_list)
        
        # 임시 파일 정리
        temp_path.unlink()
        
        return {
            "message": "직무 매칭 분석 완료",
            "filename": file.filename,
            "job_title": job_title,
            "company_name": company_name,
            "analysis_result": analysis_result,
            "job_matching": {
                "matching_score": matching_score,
                "requirements": job_requirements_list,
                "matched_skills": get_matched_skills(analysis_result, job_requirements_list),
                "missing_skills": get_missing_skills(analysis_result, job_requirements_list)
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"직무 매칭 분석 중 오류 발생: {str(e)}")

@router.get("/generate-interview-questions")
async def generate_interview_questions(
    position: str = Query(..., description="직무명"),
    experience_level: str = Query("intermediate", description="경험 수준 (junior, intermediate, senior)"),
    question_count: int = Query(5, description="질문 수"),
    categories: Optional[str] = Query(None, description="질문 카테고리 (technical,behavioral,situational)")
):
    """면접 질문을 생성합니다."""
    try:
        # 카테고리 파싱
        if categories:
            category_list = [cat.strip() for cat in categories.split(',')]
        else:
            category_list = ["technical", "behavioral", "situational"]
        
        # 면접 질문 생성
        questions = generate_interview_questions_for_position(
            position, experience_level, question_count, category_list
        )
        
        return InterviewQuestionsResponse(
            message="면접 질문 생성 완료",
            questions=questions,
            total_questions=len(questions),
            position=position,
            estimated_duration=len(questions) * 10  # 질문당 10분 추정
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"면접 질문 생성 중 오류 발생: {str(e)}")

@router.post("/bulk-export")
async def bulk_export_results(
    analysis_ids: List[str],
    format: str = Query("json", description="내보내기 형식"),
    analyzer: AnalyzerService = Depends(get_analyzer_service)
):
    """여러 분석 결과를 일괄 내보냅니다."""
    try:
        if len(analysis_ids) > 20:
            raise HTTPException(status_code=400, detail="한 번에 최대 20개까지만 내보낼 수 있습니다.")
        
        export_data = []
        for analysis_id in analysis_ids:
            result = analyzer.get_cached_result(analysis_id)
            if result:
                export_data.append({
                    "analysis_id": analysis_id,
                    "result": result['result'],
                    "processing_time": result['processing_time'],
                    "timestamp": result['timestamp'].isoformat()
                })
        
        if format.lower() == "json":
            return {
                "message": "일괄 내보내기 완료",
                "total_results": len(export_data),
                "exported_at": datetime.now().isoformat(),
                "data": export_data
            }
        
        elif format.lower() == "zip":
            # ZIP 파일로 내보내기
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for i, data in enumerate(export_data):
                    filename = f"analysis_{data['analysis_id']}.json"
                    json_content = json.dumps(data, ensure_ascii=False, indent=2)
                    zip_file.writestr(filename, json_content)
            
            zip_buffer.seek(0)
            
            return JSONResponse(
                content={"message": "ZIP 파일이 생성되었습니다."},
                headers={
                    "Content-Disposition": f"attachment; filename=bulk_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                }
            )
        
        else:
            raise HTTPException(status_code=400, detail="지원하지 않는 형식입니다.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"일괄 내보내기 중 오류 발생: {str(e)}")

# 헬퍼 함수들
def calculate_job_matching_score(analysis_result, job_requirements: List[str]) -> float:
    """직무 요구사항과의 매칭 점수를 계산합니다."""
    if not hasattr(analysis_result, 'skills'):
        return 0.0
    
    user_skills = [skill.name.lower() for skill in analysis_result.skills]
    required_skills = [req.lower() for req in job_requirements]
    
    matched_count = sum(1 for req in required_skills if any(req in skill for skill in user_skills))
    
    return (matched_count / len(required_skills)) * 100 if required_skills else 0.0

def get_matched_skills(analysis_result, job_requirements: List[str]) -> List[str]:
    """매칭된 스킬을 반환합니다."""
    if not hasattr(analysis_result, 'skills'):
        return []
    
    user_skills = [skill.name for skill in analysis_result.skills]
    matched_skills = []
    
    for req in job_requirements:
        for skill in user_skills:
            if req.lower() in skill.lower():
                matched_skills.append(skill)
                break
    
    return matched_skills

def get_missing_skills(analysis_result, job_requirements: List[str]) -> List[str]:
    """부족한 스킬을 반환합니다."""
    if not hasattr(analysis_result, 'skills'):
        return job_requirements
    
    user_skills = [skill.name.lower() for skill in analysis_result.skills]
    missing_skills = []
    
    for req in job_requirements:
        if not any(req.lower() in skill for skill in user_skills):
            missing_skills.append(req)
    
    return missing_skills

def generate_interview_questions_for_position(position: str, experience_level: str, 
                                           question_count: int, categories: List[str]):
    """직무별 면접 질문을 생성합니다."""
    from models.schemas import InterviewQuestion
    
    # 기본 질문 템플릿 (실제로는 더 정교한 AI 생성 로직 필요)
    questions = []
    
    # 기술 질문
    if "technical" in categories:
        questions.append(InterviewQuestion(
            question=f"{position} 개발자로서 가장 중요하다고 생각하는 기술은 무엇인가요?",
            category="technical",
            difficulty="medium",
            expected_answer="해당 직무에 필요한 핵심 기술에 대한 이해도 평가",
            evaluation_criteria=["기술 이해도", "실무 경험", "학습 의지"]
        ))
    
    # 행동 질문
    if "behavioral" in categories:
        questions.append(InterviewQuestion(
            question="팀 프로젝트에서 의견 충돌이 있었던 경험과 해결 방법을 설명해주세요.",
            category="behavioral",
            difficulty="medium",
            expected_answer="협업 능력과 갈등 해결 능력 평가",
            evaluation_criteria=["소통 능력", "문제 해결 능력", "협업 능력"]
        ))
    
    # 상황 질문
    if "situational" in categories:
        questions.append(InterviewQuestion(
            question="프로젝트 마감일이 임박했는데 예상치 못한 기술적 문제가 발생했다면 어떻게 대처하시겠습니까?",
            category="situational",
            difficulty="hard",
            expected_answer="문제 해결 능력과 우선순위 판단 능력 평가",
            evaluation_criteria=["문제 해결 능력", "우선순위 판단", "스트레스 대처"]
        ))
    
    return questions[:question_count]
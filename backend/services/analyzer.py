import asyncio
import logging
from pathlib import Path
from typing import Optional, Union, Dict, Any
from datetime import datetime
import hashlib
import json

from ai_analyzer.resume_analyzer import ResumeAnalyzer
from ai_analyzer.portfolio_analyzer import PortfolioAnalyzer
from utils.file_processor import FileProcessor
from models.schemas import (
    ResumeAnalysis, PortfolioAnalysis, FileType, 
    AnalysisStatus, AnalysisResponse
)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalyzerService:
    """분석 서비스 메인 클래스"""
    
    def __init__(self):
        self.resume_analyzer = ResumeAnalyzer()
        self.portfolio_analyzer = PortfolioAnalyzer()
        self.file_processor = FileProcessor()
        
        # 결과 캐싱을 위한 딕셔너리
        self.analysis_cache = {}
        
        # 분석 상태 추적
        self.analysis_status = {}
    
    async def analyze_resume(self, file_path: Path, job_position: Optional[str] = None) -> ResumeAnalysis:
        """이력서를 분석합니다."""
        try:
            # 분석 ID 생성
            analysis_id = self._generate_analysis_id(file_path, "resume")
            
            # 상태 업데이트
            self.analysis_status[analysis_id] = AnalysisStatus.PROCESSING
            
            logger.info(f"이력서 분석 시작: {file_path}")
            
            # 파일 유효성 검사
            is_valid, error_message = self.file_processor.validate_file(file_path)
            if not is_valid:
                raise ValueError(f"파일 유효성 검사 실패: {error_message}")
            
            # 텍스트 추출
            text = await self.file_processor.extract_text(file_path)
            
            if not text or len(text.strip()) < 50:
                raise ValueError("추출된 텍스트가 너무 짧습니다. 최소 50자 이상이어야 합니다.")
            
            # 이력서 분석 수행
            start_time = datetime.now()
            
            analysis_result = await self.resume_analyzer.analyze_resume(text, job_position)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # 상태 업데이트
            self.analysis_status[analysis_id] = AnalysisStatus.COMPLETED
            
            # 결과 캐싱
            self.analysis_cache[analysis_id] = {
                'result': analysis_result,
                'processing_time': processing_time,
                'timestamp': datetime.now()
            }
            
            logger.info(f"이력서 분석 완료: {file_path} (소요시간: {processing_time:.2f}초)")
            
            return analysis_result
            
        except Exception as e:
            self.analysis_status[analysis_id] = AnalysisStatus.FAILED
            logger.error(f"이력서 분석 중 오류 발생: {e}")
            raise
    
    async def analyze_portfolio(self, file_path: Path, github_url: Optional[str] = None) -> PortfolioAnalysis:
        """포트폴리오를 분석합니다."""
        try:
            # 분석 ID 생성
            analysis_id = self._generate_analysis_id(file_path, "portfolio")
            
            # 상태 업데이트
            self.analysis_status[analysis_id] = AnalysisStatus.PROCESSING
            
            logger.info(f"포트폴리오 분석 시작: {file_path}")
            
            # 파일 유효성 검사
            is_valid, error_message = self.file_processor.validate_file(file_path)
            if not is_valid:
                raise ValueError(f"파일 유효성 검사 실패: {error_message}")
            
            # 텍스트 추출
            text = await self.file_processor.extract_text(file_path)
            
            if not text or len(text.strip()) < 50:
                raise ValueError("추출된 텍스트가 너무 짧습니다. 최소 50자 이상이어야 합니다.")
            
            # 포트폴리오 분석 수행
            start_time = datetime.now()
            
            analysis_result = await self.portfolio_analyzer.analyze_portfolio(text, github_url)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # 상태 업데이트
            self.analysis_status[analysis_id] = AnalysisStatus.COMPLETED
            
            # 결과 캐싱
            self.analysis_cache[analysis_id] = {
                'result': analysis_result,
                'processing_time': processing_time,
                'timestamp': datetime.now()
            }
            
            logger.info(f"포트폴리오 분석 완료: {file_path} (소요시간: {processing_time:.2f}초)")
            
            return analysis_result
            
        except Exception as e:
            self.analysis_status[analysis_id] = AnalysisStatus.FAILED
            logger.error(f"포트폴리오 분석 중 오류 발생: {e}")
            raise
    
    async def analyze_file(self, file_path: Path, file_type: Optional[FileType] = None,
                          job_position: Optional[str] = None, 
                          github_url: Optional[str] = None) -> Union[ResumeAnalysis, PortfolioAnalysis]:
        """파일을 자동으로 분석합니다 (타입 자동 감지)."""
        try:
            # 파일 타입 자동 감지
            if not file_type:
                file_type = await self._detect_file_type(file_path)
            
            # 파일 타입에 따라 분석 수행
            if file_type == FileType.RESUME:
                return await self.analyze_resume(file_path, job_position)
            elif file_type == FileType.PORTFOLIO:
                return await self.analyze_portfolio(file_path, github_url)
            else:
                raise ValueError(f"지원하지 않는 파일 타입: {file_type}")
                
        except Exception as e:
            logger.error(f"파일 분석 중 오류 발생: {e}")
            raise
    
    async def _detect_file_type(self, file_path: Path) -> FileType:
        """파일 타입을 자동으로 감지합니다."""
        try:
            # 텍스트 추출
            text = await self.file_processor.extract_text(file_path)
            text_lower = text.lower()
            
            # 이력서 키워드
            resume_keywords = [
                "이력서", "resume", "cv", "curriculum vitae", "경력", "학력", 
                "자기소개", "지원동기", "career", "education", "experience"
            ]
            
            # 포트폴리오 키워드
            portfolio_keywords = [
                "포트폴리오", "portfolio", "프로젝트", "project", "작품", "github",
                "개발", "development", "구현", "implementation", "demo"
            ]
            
            # 키워드 점수 계산
            resume_score = sum(1 for keyword in resume_keywords if keyword in text_lower)
            portfolio_score = sum(1 for keyword in portfolio_keywords if keyword in text_lower)
            
            # 추가 특징 분석
            
            # 개인정보 패턴 (이력서에 더 많이 나타남)
            personal_patterns = [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # 이메일
                r'(?:\+82|0)(?:\d{1,3})-?\d{3,4}-?\d{4}',  # 전화번호
                r'\d{4}년\s*\d{1,2}월',  # 날짜 형식
            ]
            
            # 기술 관련 패턴 (포트폴리오에 더 많이 나타남)
            tech_patterns = [
                r'github\.com',
                r'https?://',
                r'기술스택|tech stack',
                r'데모|demo',
                r'구현|implementation'
            ]
            
            import re
            
            personal_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) 
                               for pattern in personal_patterns)
            tech_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) 
                           for pattern in tech_patterns)
            
            # 최종 점수 계산
            final_resume_score = resume_score + personal_count * 0.5
            final_portfolio_score = portfolio_score + tech_count * 0.5
            
            # 결정
            if final_resume_score > final_portfolio_score:
                return FileType.RESUME
            elif final_portfolio_score > final_resume_score:
                return FileType.PORTFOLIO
            else:
                # 동점인 경우 파일명으로 판단
                filename = file_path.name.lower()
                if any(keyword in filename for keyword in ['resume', 'cv', '이력서']):
                    return FileType.RESUME
                elif any(keyword in filename for keyword in ['portfolio', 'project', '포트폴리오']):
                    return FileType.PORTFOLIO
                else:
                    # 기본적으로 이력서로 분류
                    return FileType.RESUME
        
        except Exception as e:
            logger.error(f"파일 타입 감지 중 오류: {e}")
            # 오류 발생시 기본값 반환
            return FileType.RESUME
    
    def _generate_analysis_id(self, file_path: Path, analysis_type: str) -> str:
        """분석 ID를 생성합니다."""
        content = f"{file_path.name}_{analysis_type}_{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get_analysis_status(self, analysis_id: str) -> Optional[AnalysisStatus]:
        """분석 상태를 반환합니다."""
        return self.analysis_status.get(analysis_id)
    
    def get_cached_result(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """캐시된 분석 결과를 반환합니다."""
        return self.analysis_cache.get(analysis_id)
    
    def clear_cache(self, older_than_hours: int = 24):
        """오래된 캐시를 정리합니다."""
        current_time = datetime.now()
        
        to_remove = []
        for analysis_id, cache_data in self.analysis_cache.items():
            cache_time = cache_data['timestamp']
            if (current_time - cache_time).total_seconds() > older_than_hours * 3600:
                to_remove.append(analysis_id)
        
        for analysis_id in to_remove:
            del self.analysis_cache[analysis_id]
            if analysis_id in self.analysis_status:
                del self.analysis_status[analysis_id]
        
        logger.info(f"캐시 정리 완료: {len(to_remove)}개 항목 삭제")
    
    async def batch_analyze(self, file_paths: list[Path], 
                          analysis_types: Optional[list[FileType]] = None) -> list[Union[ResumeAnalysis, PortfolioAnalysis]]:
        """여러 파일을 동시에 분석합니다."""
        try:
            tasks = []
            
            for i, file_path in enumerate(file_paths):
                file_type = analysis_types[i] if analysis_types and i < len(analysis_types) else None
                task = self.analyze_file(file_path, file_type)
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 예외 처리
            processed_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"파일 {file_paths[i]} 분석 중 오류: {result}")
                    processed_results.append(None)
                else:
                    processed_results.append(result)
            
            return processed_results
            
        except Exception as e:
            logger.error(f"배치 분석 중 오류 발생: {e}")
            raise
    
    async def compare_candidates(self, file_paths: list[Path], 
                               job_position: Optional[str] = None) -> Dict[str, Any]:
        """후보자들을 비교 분석합니다."""
        try:
            # 모든 파일 분석
            results = await self.batch_analyze(file_paths)
            
            # 유효한 결과만 필터링
            valid_results = [(fp, result) for fp, result in zip(file_paths, results) if result is not None]
            
            if len(valid_results) < 2:
                raise ValueError("비교를 위해서는 최소 2개의 유효한 분석 결과가 필요합니다.")
            
            # 비교 분석 수행
            comparison_data = {
                'candidates': [],
                'comparison_metrics': {},
                'ranking': [],
                'summary': ""
            }
            
            for file_path, result in valid_results:
                candidate_data = {
                    'filename': file_path.name,
                    'overall_score': result.score.overall_score,
                    'technical_skills': len(result.skills) if hasattr(result, 'skills') else 0,
                    'projects': len(result.projects) if hasattr(result, 'projects') else 0,
                    'strengths': result.score.strengths,
                    'weaknesses': result.score.weaknesses
                }
                comparison_data['candidates'].append(candidate_data)
            
            # 랭킹 생성
            sorted_candidates = sorted(comparison_data['candidates'], 
                                     key=lambda x: x['overall_score'], reverse=True)
            
            comparison_data['ranking'] = [
                {'rank': i+1, 'filename': candidate['filename'], 'score': candidate['overall_score']}
                for i, candidate in enumerate(sorted_candidates)
            ]
            
            # 비교 메트릭 계산
            scores = [candidate['overall_score'] for candidate in comparison_data['candidates']]
            comparison_data['comparison_metrics'] = {
                'highest_score': max(scores),
                'lowest_score': min(scores),
                'average_score': sum(scores) / len(scores),
                'score_difference': max(scores) - min(scores)
            }
            
            # 요약 생성
            winner = sorted_candidates[0]
            comparison_data['summary'] = f"최고 점수: {winner['filename']} ({winner['overall_score']:.1f}점)"
            
            return comparison_data
            
        except Exception as e:
            logger.error(f"후보자 비교 중 오류 발생: {e}")
            raise
    
    def get_analytics_summary(self) -> Dict[str, Any]:
        """분석 통계를 반환합니다."""
        try:
            total_analyses = len(self.analysis_cache)
            
            # 상태별 통계
            status_counts = {}
            for status in self.analysis_status.values():
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # 처리 시간 통계
            processing_times = [
                cache_data['processing_time'] 
                for cache_data in self.analysis_cache.values()
            ]
            
            avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
            
            return {
                'total_analyses': total_analyses,
                'status_breakdown': status_counts,
                'average_processing_time': avg_processing_time,
                'cache_size': len(self.analysis_cache),
                'last_analysis': max([cache_data['timestamp'] for cache_data in self.analysis_cache.values()]) if self.analysis_cache else None
            }
            
        except Exception as e:
            logger.error(f"통계 생성 중 오류 발생: {e}")
            return {}
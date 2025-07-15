from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union
from datetime import datetime
from enum import Enum

class FileType(str, Enum):
    RESUME = "resume"
    PORTFOLIO = "portfolio"
    COVER_LETTER = "cover_letter"

class AnalysisStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

# 기본 응답 모델
class BaseResponse(BaseModel):
    status: str = "success"
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)

# 파일 업로드 응답
class FileUploadResponse(BaseResponse):
    filename: str
    file_size: int
    file_type: str
    extracted_text_length: int
    file_path: str

# 스킬 모델
class Skill(BaseModel):
    name: str
    level: SkillLevel
    confidence: float = Field(ge=0.0, le=1.0)
    category: str  # 예: "programming", "framework", "tool", "language"
    years_of_experience: Optional[int] = None

# 경력 모델
class Experience(BaseModel):
    company: str
    position: str
    duration: str
    description: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_current: bool = False
    achievements: List[str] = []

# 교육 모델
class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    graduation_year: Optional[int] = None
    gpa: Optional[float] = None

# 프로젝트 모델
class Project(BaseModel):
    name: str
    description: str
    technologies: List[str]
    duration: Optional[str] = None
    role: Optional[str] = None
    achievements: List[str] = []
    github_url: Optional[str] = None
    demo_url: Optional[str] = None

# 스코어링 모델
class ScoreBreakdown(BaseModel):
    technical_skills: float = Field(ge=0.0, le=100.0)
    experience_relevance: float = Field(ge=0.0, le=100.0)
    education_background: float = Field(ge=0.0, le=100.0)
    project_quality: float = Field(ge=0.0, le=100.0)
    communication_skills: float = Field(ge=0.0, le=100.0)
    overall_presentation: float = Field(ge=0.0, le=100.0)

class FinalScore(BaseModel):
    overall_score: float = Field(ge=0.0, le=100.0)
    breakdown: ScoreBreakdown
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]

# 이력서 분석 결과
class ResumeAnalysis(BaseModel):
    personal_info: Dict[str, str]
    skills: List[Skill]
    experiences: List[Experience]
    education: List[Education]
    projects: List[Project]
    languages: List[str]
    certifications: List[str]
    summary: str
    score: FinalScore
    keywords: List[str]
    ats_compatibility: float = Field(ge=0.0, le=100.0)

# 포트폴리오 분석 결과
class PortfolioAnalysis(BaseModel):
    projects: List[Project]
    technical_skills: List[Skill]
    creativity_score: float = Field(ge=0.0, le=100.0)
    technical_depth: float = Field(ge=0.0, le=100.0)
    project_diversity: float = Field(ge=0.0, le=100.0)
    code_quality: float = Field(ge=0.0, le=100.0)
    documentation_quality: float = Field(ge=0.0, le=100.0)
    score: FinalScore
    github_stats: Optional[Dict[str, Union[int, float]]] = None

# 분석 요청
class AnalysisRequest(BaseModel):
    file_path: str
    file_type: FileType
    job_position: Optional[str] = None
    job_requirements: Optional[List[str]] = None
    company_name: Optional[str] = None

# 분석 응답
class AnalysisResponse(BaseResponse):
    analysis_id: str
    file_type: FileType
    analysis_status: AnalysisStatus
    resume_analysis: Optional[ResumeAnalysis] = None
    portfolio_analysis: Optional[PortfolioAnalysis] = None
    processing_time: Optional[float] = None

# 비교 분석
class ComparisonAnalysis(BaseModel):
    candidate_a: str
    candidate_b: str
    comparison_metrics: Dict[str, float]
    winner: str
    detailed_comparison: Dict[str, Dict[str, float]]
    recommendation: str

# 직무 매칭
class JobMatch(BaseModel):
    job_title: str
    company: str
    match_score: float = Field(ge=0.0, le=100.0)
    matching_skills: List[str]
    missing_skills: List[str]
    salary_range: Optional[str] = None
    location: Optional[str] = None

class JobMatchingResponse(BaseResponse):
    matches: List[JobMatch]
    total_matches: int
    candidate_profile_summary: str

# 면접 질문 생성
class InterviewQuestion(BaseModel):
    question: str
    category: str  # "technical", "behavioral", "situational"
    difficulty: str  # "easy", "medium", "hard"
    expected_answer: str
    evaluation_criteria: List[str]

class InterviewQuestionsResponse(BaseResponse):
    questions: List[InterviewQuestion]
    total_questions: int
    position: str
    estimated_duration: int  # 분

# 에러 응답
class ErrorResponse(BaseModel):
    status: str = "error"
    error_code: str
    error_message: str
    details: Optional[Dict] = None
    timestamp: datetime = Field(default_factory=datetime.now)
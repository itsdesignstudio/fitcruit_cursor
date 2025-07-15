// 기본 타입 정의
export interface BaseResponse {
  status: string;
  message: string;
  timestamp: string;
}

export interface ErrorResponse extends BaseResponse {
  error_code: string;
  error_message: string;
  details?: Record<string, any>;
}

// 파일 관련 타입
export enum FileType {
  RESUME = 'resume',
  PORTFOLIO = 'portfolio',
  COVER_LETTER = 'cover_letter',
}

export enum AnalysisStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed',
}

export enum SkillLevel {
  BEGINNER = 'beginner',
  INTERMEDIATE = 'intermediate',
  ADVANCED = 'advanced',
  EXPERT = 'expert',
}

// 스킬 관련 타입
export interface Skill {
  name: string;
  level: SkillLevel;
  confidence: number;
  category: string;
  years_of_experience?: number;
}

// 경력 관련 타입
export interface Experience {
  company: string;
  position: string;
  duration: string;
  description: string;
  start_date?: string;
  end_date?: string;
  is_current: boolean;
  achievements: string[];
}

// 교육 관련 타입
export interface Education {
  institution: string;
  degree: string;
  field_of_study: string;
  graduation_year?: number;
  gpa?: number;
}

// 프로젝트 관련 타입
export interface Project {
  name: string;
  description: string;
  technologies: string[];
  duration?: string;
  role?: string;
  achievements: string[];
  github_url?: string;
  demo_url?: string;
}

// 점수 관련 타입
export interface ScoreBreakdown {
  technical_skills: number;
  experience_relevance: number;
  education_background: number;
  project_quality: number;
  communication_skills: number;
  overall_presentation: number;
}

export interface FinalScore {
  overall_score: number;
  breakdown: ScoreBreakdown;
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
}

// 이력서 분석 결과
export interface ResumeAnalysis {
  personal_info: Record<string, string>;
  skills: Skill[];
  experiences: Experience[];
  education: Education[];
  projects: Project[];
  languages: string[];
  certifications: string[];
  summary: string;
  score: FinalScore;
  keywords: string[];
  ats_compatibility: number;
}

// 포트폴리오 분석 결과
export interface PortfolioAnalysis {
  projects: Project[];
  technical_skills: Skill[];
  creativity_score: number;
  technical_depth: number;
  project_diversity: number;
  code_quality: number;
  documentation_quality: number;
  score: FinalScore;
  github_stats?: Record<string, any>;
}

// 분석 요청/응답 타입
export interface AnalysisRequest {
  file_path: string;
  file_type: FileType;
  job_position?: string;
  job_requirements?: string[];
  company_name?: string;
}

export interface AnalysisResponse extends BaseResponse {
  analysis_id: string;
  file_type: FileType;
  analysis_status: AnalysisStatus;
  resume_analysis?: ResumeAnalysis;
  portfolio_analysis?: PortfolioAnalysis;
  processing_time?: number;
}

// 파일 업로드 관련 타입
export interface FileUploadResponse extends BaseResponse {
  filename: string;
  file_size: number;
  file_type: string;
  extracted_text_length: number;
  file_path: string;
}

// 비교 분석 타입
export interface ComparisonAnalysis {
  candidate_a: string;
  candidate_b: string;
  comparison_metrics: Record<string, number>;
  winner: string;
  detailed_comparison: Record<string, Record<string, number>>;
  recommendation: string;
}

// 직무 매칭 타입
export interface JobMatch {
  job_title: string;
  company: string;
  match_score: number;
  matching_skills: string[];
  missing_skills: string[];
  salary_range?: string;
  location?: string;
}

export interface JobMatchingResponse extends BaseResponse {
  matches: JobMatch[];
  total_matches: number;
  candidate_profile_summary: string;
}

// 면접 질문 타입
export interface InterviewQuestion {
  question: string;
  category: string;
  difficulty: string;
  expected_answer: string;
  evaluation_criteria: string[];
}

export interface InterviewQuestionsResponse extends BaseResponse {
  questions: InterviewQuestion[];
  total_questions: number;
  position: string;
  estimated_duration: number;
}

// 배치 분석 타입
export interface BatchAnalysisResult {
  filename: string;
  analysis_result: ResumeAnalysis | PortfolioAnalysis | null;
  status: 'success' | 'failed';
}

export interface BatchAnalysisResponse extends BaseResponse {
  total_files: number;
  successful_analyses: number;
  results: BatchAnalysisResult[];
}

// 후보자 비교 타입
export interface CandidateComparison {
  filename: string;
  overall_score: number;
  technical_skills: number;
  projects: number;
  strengths: string[];
  weaknesses: string[];
}

export interface ComparisonResult {
  candidates: CandidateComparison[];
  comparison_metrics: {
    highest_score: number;
    lowest_score: number;
    average_score: number;
    score_difference: number;
  };
  ranking: Array<{
    rank: number;
    filename: string;
    score: number;
  }>;
  summary: string;
}

// 통계 타입
export interface AnalyticsData {
  total_analyses: number;
  status_breakdown: Record<string, number>;
  average_processing_time: number;
  cache_size: number;
  last_analysis?: string;
}

// UI 상태 타입
export interface UploadState {
  files: File[];
  uploading: boolean;
  progress: number;
  error?: string;
}

export interface AnalysisState {
  current_analysis?: ResumeAnalysis | PortfolioAnalysis;
  analysis_history: Array<{
    id: string;
    filename: string;
    type: FileType;
    score: number;
    timestamp: string;
  }>;
  loading: boolean;
  error?: string;
}

// 폼 데이터 타입
export interface JobRequirementsForm {
  job_title: string;
  job_requirements: string;
  company_name?: string;
}

export interface ComparisonForm {
  files: File[];
  job_position?: string;
}

export interface InterviewQuestionForm {
  position: string;
  experience_level: 'junior' | 'intermediate' | 'senior';
  question_count: number;
  categories: string[];
}

// API 응답 타입
export interface ApiResponse<T> {
  data: T;
  status: number;
  statusText: string;
  headers: Record<string, string>;
}

// 차트 데이터 타입
export interface ChartData {
  labels: string[];
  datasets: Array<{
    label: string;
    data: number[];
    backgroundColor?: string | string[];
    borderColor?: string | string[];
    borderWidth?: number;
  }>;
}

// 대시보드 타입
export interface DashboardStats {
  total_analyses: number;
  today_analyses: number;
  average_score: number;
  top_skills: Array<{
    name: string;
    count: number;
  }>;
  recent_analyses: Array<{
    id: string;
    filename: string;
    score: number;
    timestamp: string;
  }>;
}

// 필터 타입
export interface AnalysisFilter {
  file_type?: FileType;
  score_range?: [number, number];
  date_range?: [string, string];
  skills?: string[];
  sort_by?: 'score' | 'date' | 'filename';
  sort_order?: 'asc' | 'desc';
}

// 테마 타입
export interface Theme {
  name: string;
  primary: string;
  secondary: string;
  accent: string;
  background: string;
  text: string;
}

// 사용자 설정 타입
export interface UserSettings {
  theme: 'light' | 'dark' | 'system';
  language: 'ko' | 'en';
  notifications: boolean;
  auto_save: boolean;
  max_file_size: number;
}
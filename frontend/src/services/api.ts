import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import toast from 'react-hot-toast';
import {
  ResumeAnalysis,
  PortfolioAnalysis,
  FileUploadResponse,
  BatchAnalysisResponse,
  ComparisonResult,
  AnalyticsData,
  InterviewQuestionsResponse,
  JobRequirementsForm,
  InterviewQuestionForm,
  AnalysisStatus,
  ApiResponse,
} from '@/types';

// API 클라이언트 설정
class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // 요청 인터셉터
    this.client.interceptors.request.use(
      (config) => {
        // 로딩 시작 (필요한 경우)
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // 응답 인터셉터
    this.client.interceptors.response.use(
      (response) => {
        return response;
      },
      (error) => {
        // 에러 처리
        const message = error.response?.data?.detail || error.message || '알 수 없는 오류가 발생했습니다.';
        
        if (error.response?.status === 413) {
          toast.error('파일 크기가 너무 큽니다. 10MB 이하의 파일을 업로드해주세요.');
        } else if (error.response?.status === 422) {
          toast.error('파일 형식이 올바르지 않습니다.');
        } else if (error.response?.status >= 500) {
          toast.error('서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
        } else {
          toast.error(message);
        }
        
        return Promise.reject(error);
      }
    );
  }

  // 기본 HTTP 메서드
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config);
    return response.data;
  }

  // 파일 업로드용 메서드
  async postFormData<T>(url: string, formData: FormData, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, formData, {
      ...config,
      headers: {
        'Content-Type': 'multipart/form-data',
        ...config?.headers,
      },
    });
    return response.data;
  }
}

// API 클라이언트 인스턴스
const apiClient = new ApiClient();

// API 함수들
export const api = {
  // 헬스 체크
  async healthCheck() {
    return apiClient.get('/health');
  },

  // 파일 업로드
  async uploadFile(file: File): Promise<FileUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    
    return apiClient.postFormData('/upload', formData);
  },

  // 이력서 분석
  async analyzeResume(file: File): Promise<{ status: string; filename: string; analysis: ResumeAnalysis }> {
    const formData = new FormData();
    formData.append('file', file);
    
    return apiClient.postFormData('/analyze/resume', formData);
  },

  // 포트폴리오 분석
  async analyzePortfolio(file: File): Promise<{ status: string; filename: string; analysis: PortfolioAnalysis }> {
    const formData = new FormData();
    formData.append('file', file);
    
    return apiClient.postFormData('/analyze/portfolio', formData);
  },

  // 직무 요구사항과 함께 분석
  async analyzeWithJobRequirements(file: File, jobData: JobRequirementsForm): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('job_title', jobData.job_title);
    formData.append('job_requirements', jobData.job_requirements);
    if (jobData.company_name) {
      formData.append('company_name', jobData.company_name);
    }
    
    return apiClient.postFormData('/analyze-with-job-requirements', formData);
  },

  // 배치 분석
  async batchAnalyze(files: File[], jobPosition?: string): Promise<BatchAnalysisResponse> {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));
    if (jobPosition) {
      formData.append('job_position', jobPosition);
    }
    
    return apiClient.postFormData('/batch-analyze', formData);
  },

  // 후보자 비교
  async compareCandidates(files: File[], jobPosition?: string): Promise<{ message: string; comparison_result: ComparisonResult }> {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));
    if (jobPosition) {
      formData.append('job_position', jobPosition);
    }
    
    return apiClient.postFormData('/compare-candidates', formData);
  },

  // 분석 상태 조회
  async getAnalysisStatus(analysisId: string): Promise<{ analysis_id: string; status: AnalysisStatus; timestamp: string }> {
    return apiClient.get(`/status/${analysisId}`);
  },

  // 분석 결과 조회
  async getAnalysisResult(analysisId: string): Promise<any> {
    return apiClient.get(`/result/${analysisId}`);
  },

  // 통계 조회
  async getAnalytics(): Promise<{ message: string; analytics: AnalyticsData }> {
    return apiClient.get('/analytics');
  },

  // 캐시 정리
  async clearCache(olderThanHours: number = 24): Promise<{ message: string }> {
    return apiClient.post('/clear-cache', null, {
      params: { older_than_hours: olderThanHours }
    });
  },

  // 분석 결과 내보내기
  async exportAnalysisResult(analysisId: string, format: 'json' | 'csv' = 'json'): Promise<any> {
    return apiClient.get(`/export/${analysisId}`, {
      params: { format }
    });
  },

  // 일괄 내보내기
  async bulkExportResults(analysisIds: string[], format: 'json' | 'zip' = 'json'): Promise<any> {
    return apiClient.post('/bulk-export', analysisIds, {
      params: { format }
    });
  },

  // 면접 질문 생성
  async generateInterviewQuestions(params: InterviewQuestionForm): Promise<InterviewQuestionsResponse> {
    return apiClient.get('/generate-interview-questions', {
      params: {
        position: params.position,
        experience_level: params.experience_level,
        question_count: params.question_count,
        categories: params.categories.join(',')
      }
    });
  },

  // 파일 다운로드
  async downloadFile(url: string, filename: string): Promise<void> {
    const response = await axios.get(url, {
      responseType: 'blob',
    });
    
    const blob = new Blob([response.data]);
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = filename;
    link.click();
    window.URL.revokeObjectURL(link.href);
  },

  // 업로드 진행률 추적
  async uploadWithProgress(
    file: File,
    endpoint: string,
    onProgress?: (progress: number) => void
  ): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    
    return apiClient.postFormData(endpoint, formData, {
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total && onProgress) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(progress);
        }
      }
    });
  },

  // 여러 파일 업로드 (진행률 추적)
  async uploadMultipleFiles(
    files: File[],
    endpoint: string,
    onProgress?: (progress: number) => void
  ): Promise<any> {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));
    
    return apiClient.postFormData(endpoint, formData, {
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total && onProgress) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(progress);
        }
      }
    });
  },
};

// 유틸리티 함수들
export const apiUtils = {
  // 파일 크기 검증
  validateFileSize(file: File, maxSizeMB: number = 10): boolean {
    const maxSizeBytes = maxSizeMB * 1024 * 1024;
    return file.size <= maxSizeBytes;
  },

  // 파일 형식 검증
  validateFileType(file: File, allowedTypes: string[] = ['pdf', 'docx', 'doc', 'txt']): boolean {
    const fileExtension = file.name.split('.').pop()?.toLowerCase();
    return allowedTypes.includes(fileExtension || '');
  },

  // 파일 크기 포맷팅
  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  },

  // 에러 메시지 추출
  extractErrorMessage(error: any): string {
    if (error.response?.data?.detail) {
      return error.response.data.detail;
    }
    if (error.response?.data?.message) {
      return error.response.data.message;
    }
    if (error.message) {
      return error.message;
    }
    return '알 수 없는 오류가 발생했습니다.';
  },

  // 성공 메시지 표시
  showSuccess(message: string): void {
    toast.success(message);
  },

  // 에러 메시지 표시
  showError(message: string): void {
    toast.error(message);
  },

  // 로딩 토스트
  showLoading(message: string): string {
    return toast.loading(message);
  },

  // 토스트 해제
  dismissToast(toastId: string): void {
    toast.dismiss(toastId);
  },
};

export default api;
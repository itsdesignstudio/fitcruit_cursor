import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Upload, 
  FileText, 
  BarChart3, 
  Clock, 
  CheckCircle, 
  AlertCircle,
  ArrowLeft,
  Download
} from 'lucide-react';
import FileUploadZone from '../components/FileUploadZone';
import AnalysisResults from '../components/AnalysisResults';
import { ResumeAnalysis, PortfolioAnalysis, FileType } from '../types';

const AnalyzePage: React.FC = () => {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [analysisType, setAnalysisType] = useState<FileType | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<ResumeAnalysis | PortfolioAnalysis | null>(null);
  const [analysisError, setAnalysisError] = useState<string | null>(null);

  const handleFileUpload = (file: File) => {
    setUploadedFile(file);
    setAnalysisResult(null);
    setAnalysisError(null);
    
    // 파일 타입 자동 감지 (간단한 로직)
    const fileName = file.name.toLowerCase();
    if (fileName.includes('portfolio') || fileName.includes('포트폴리오')) {
      setAnalysisType(FileType.PORTFOLIO);
    } else {
      setAnalysisType(FileType.RESUME);
    }
  };

  const handleAnalyze = async () => {
    if (!uploadedFile) return;

    setIsAnalyzing(true);
    setAnalysisError(null);

    try {
      // TODO: 실제 API 호출로 교체
      await new Promise(resolve => setTimeout(resolve, 3000)); // 시뮬레이션
      
      // 모의 데이터
      const mockResult = {
        personal_info: {
          name: "홍길동",
          email: "hong@example.com",
          phone: "010-1234-5678"
        },
        skills: [
          { name: "React", level: "advanced", confidence: 0.9, category: "frontend" },
          { name: "TypeScript", level: "intermediate", confidence: 0.8, category: "programming" },
          { name: "Node.js", level: "intermediate", confidence: 0.7, category: "backend" }
        ],
        experiences: [],
        education: [],
        projects: [],
        languages: ["Korean", "English"],
        certifications: [],
        summary: "React와 TypeScript를 활용한 프론트엔드 개발 경험이 풍부한 지원자입니다.",
        score: {
          overall_score: 87,
          breakdown: {
            technical_skills: 85,
            experience_relevance: 90,
            education_background: 80,
            project_quality: 88,
            communication_skills: 85,
            overall_presentation: 86
          },
          strengths: ["풍부한 React 경험", "TypeScript 활용 능력", "최신 기술 트렌드 이해"],
          weaknesses: ["백엔드 경험 부족", "프로젝트 규모 다양성 부족"],
          recommendations: ["백엔드 기술 학습 권장", "대규모 프로젝트 경험 추가"]
        },
        keywords: ["React", "TypeScript", "JavaScript", "Frontend"],
        ats_compatibility: 92
      };

      setAnalysisResult(mockResult);
      
    } catch (error) {
      setAnalysisError(error instanceof Error ? error.message : '분석 중 오류가 발생했습니다.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="analyze-page min-h-screen bg-gray-50">
      {/* 헤더 */}
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link to="/" className="flex items-center text-gray-600 hover:text-primary-600">
                <ArrowLeft className="w-5 h-5 mr-2" />
                <span>홈으로</span>
              </Link>
              <div className="text-2xl font-bold gradient-text">Fitcruit</div>
            </div>
            <div className="text-sm text-gray-500">
              AI 기반 채용 분석 시스템
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        {/* 페이지 헤더 */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4 text-gray-900">
            AI 포트폴리오 분석
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            이력서와 포트폴리오를 업로드하면 AI가 자동으로 분석하여 상세한 평가 리포트를 제공합니다.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
          {/* 파일 업로드 섹션 */}
          <div className="lg:col-span-2">
            <div className="card mb-6">
              <div className="card-header">
                <h2 className="card-title flex items-center">
                  <Upload className="w-6 h-6 mr-2" />
                  파일 업로드
                </h2>
                <p className="card-description">
                  PDF, Word, 텍스트 파일을 업로드하세요 (최대 10MB)
                </p>
              </div>
              <div className="card-content">
                <FileUploadZone onFileUpload={handleFileUpload} />
                
                {uploadedFile && (
                  <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <FileText className="w-5 h-5 text-green-600 mr-2" />
                        <div>
                          <p className="font-medium text-green-800">{uploadedFile.name}</p>
                          <p className="text-sm text-green-600">
                            {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        {analysisType && (
                          <span className={`px-2 py-1 rounded text-xs font-medium ${
                            analysisType === FileType.RESUME 
                              ? 'bg-blue-100 text-blue-800' 
                              : 'bg-purple-100 text-purple-800'
                          }`}>
                            {analysisType === FileType.RESUME ? '이력서' : '포트폴리오'}
                          </span>
                        )}
                        <button
                          onClick={handleAnalyze}
                          disabled={isAnalyzing}
                          className="btn btn-primary btn-sm"
                        >
                          {isAnalyzing ? (
                            <div className="flex items-center">
                              <div className="spinner w-4 h-4 mr-2"></div>
                              분석 중...
                            </div>
                          ) : (
                            <>
                              <BarChart3 className="w-4 h-4 mr-2" />
                              분석 시작
                            </>
                          )}
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* 분석 결과 */}
            {analysisResult && (
              <AnalysisResults 
                result={analysisResult} 
                fileType={analysisType || FileType.RESUME}
              />
            )}

            {/* 분석 에러 */}
            {analysisError && (
              <div className="card">
                <div className="card-content">
                  <div className="flex items-center text-red-600">
                    <AlertCircle className="w-5 h-5 mr-2" />
                    <span>{analysisError}</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* 사이드바 */}
          <div className="space-y-6">
            {/* 분석 단계 */}
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">분석 단계</h3>
              </div>
              <div className="card-content">
                <div className="space-y-4">
                  <div className={`flex items-center ${uploadedFile ? 'text-green-600' : 'text-gray-400'}`}>
                    <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center mr-3 ${
                      uploadedFile ? 'bg-green-100 border-green-600' : 'border-gray-300'
                    }`}>
                      {uploadedFile ? <CheckCircle className="w-4 h-4" /> : <span className="text-xs">1</span>}
                    </div>
                    <span className="text-sm">파일 업로드</span>
                  </div>
                  
                  <div className={`flex items-center ${isAnalyzing ? 'text-blue-600' : analysisResult ? 'text-green-600' : 'text-gray-400'}`}>
                    <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center mr-3 ${
                      isAnalyzing ? 'bg-blue-100 border-blue-600' : 
                      analysisResult ? 'bg-green-100 border-green-600' : 'border-gray-300'
                    }`}>
                      {isAnalyzing ? (
                        <div className="spinner w-3 h-3"></div>
                      ) : analysisResult ? (
                        <CheckCircle className="w-4 h-4" />
                      ) : (
                        <span className="text-xs">2</span>
                      )}
                    </div>
                    <span className="text-sm">AI 분석 중</span>
                  </div>
                  
                  <div className={`flex items-center ${analysisResult ? 'text-green-600' : 'text-gray-400'}`}>
                    <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center mr-3 ${
                      analysisResult ? 'bg-green-100 border-green-600' : 'border-gray-300'
                    }`}>
                      {analysisResult ? <CheckCircle className="w-4 h-4" /> : <span className="text-xs">3</span>}
                    </div>
                    <span className="text-sm">결과 확인</span>
                  </div>
                </div>
              </div>
            </div>

            {/* 기능 설명 */}
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">분석 기능</h3>
              </div>
              <div className="card-content">
                <div className="space-y-3">
                  <div className="flex items-start">
                    <BarChart3 className="w-5 h-5 text-primary-600 mr-3 mt-0.5" />
                    <div>
                      <p className="font-medium text-sm">종합 점수 평가</p>
                      <p className="text-xs text-gray-600">다차원 평가 시스템</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start">
                    <FileText className="w-5 h-5 text-primary-600 mr-3 mt-0.5" />
                    <div>
                      <p className="font-medium text-sm">상세 분석 리포트</p>
                      <p className="text-xs text-gray-600">강점과 개선점 제시</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start">
                    <Clock className="w-5 h-5 text-primary-600 mr-3 mt-0.5" />
                    <div>
                      <p className="font-medium text-sm">빠른 분석 속도</p>
                      <p className="text-xs text-gray-600">5분 내 결과 제공</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* 분석 결과 다운로드 */}
            {analysisResult && (
              <div className="card">
                <div className="card-header">
                  <h3 className="card-title">결과 다운로드</h3>
                </div>
                <div className="card-content">
                  <div className="space-y-2">
                    <button className="btn btn-outline btn-sm w-full">
                      <Download className="w-4 h-4 mr-2" />
                      PDF 리포트 다운로드
                    </button>
                    <button className="btn btn-outline btn-sm w-full">
                      <Download className="w-4 h-4 mr-2" />
                      JSON 데이터 다운로드
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyzePage;
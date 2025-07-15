# Fitcruit - AI 기반 채용 자동화 SaaS

<div align="center">
  <h3>🚀 AI 기반 포지션 제안, 이력서 스코어링, 포트폴리오 평가, 면접 질문 생성까지 제공하는 종합 채용 자동화 플랫폼</h3>
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
  [![React](https://img.shields.io/badge/React-18.2+-blue.svg)](https://reactjs.org/)
  [![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
</div>

## 📋 목차

- [개요](#개요)
- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [시스템 아키텍처](#시스템-아키텍처)
- [빠른 시작](#빠른-시작)
- [설치 및 설정](#설치-및-설정)
- [API 문서](#api-문서)
- [사용법](#사용법)
- [개발 가이드](#개발-가이드)
- [배포](#배포)
- [기여하기](#기여하기)
- [라이선스](#라이선스)

## 🌟 개요

Fitcruit은 AI 기술을 활용하여 채용 과정을 자동화하는 혁신적인 SaaS 플랫폼입니다. 이력서와 포트폴리오를 자동으로 분석하고, 직무 요구사항과 매칭하여 객관적인 평가를 제공합니다.

### 🎯 해결하는 문제

- **비효율적인 서류 심사**: 수많은 이력서를 일일이 검토하는 시간 소모
- **주관적인 평가**: 담당자별로 다른 평가 기준으로 인한 불일치
- **스킬 매칭의 어려움**: 직무 요구사항과 지원자 역량의 정확한 매칭
- **면접 질문 준비**: 직무와 지원자에 맞는 면접 질문 생성의 어려움

### 💡 제공하는 솔루션

- **AI 기반 자동 분석**: 이력서와 포트폴리오를 자동으로 분석하여 구조화된 데이터 제공
- **객관적 스코어링**: 다차원 평가 시스템으로 일관된 평가 기준 적용
- **스킬 매칭**: 직무 요구사항과 지원자 역량의 정확한 매칭 점수 제공
- **자동 면접 질문 생성**: 직무와 지원자 수준에 맞는 맞춤형 면접 질문 생성

## 🚀 주요 기능

### 📄 이력서 분석
- **자동 텍스트 추출**: PDF, Word, 텍스트 파일에서 내용 추출
- **구조화된 데이터 변환**: 개인정보, 경력, 학력, 스킬 등 자동 분류
- **ATS 호환성 분석**: 지원자 추천 시스템 호환성 검사
- **키워드 분석**: 직무 관련 키워드 밀도 분석

### 💼 포트폴리오 평가
- **프로젝트 분석**: 개발 프로젝트의 기술 스택과 복잡도 평가
- **창의성 점수**: 프로젝트의 독창성과 혁신성 평가
- **기술적 깊이**: 사용된 기술의 난이도와 구현 수준 분석
- **GitHub 통합**: GitHub 통계와 기여도 분석

### 🎯 스킬 매칭
- **다차원 평가**: 기술 스킬, 경험, 교육 배경 등 종합 평가
- **직무 매칭**: 특정 직무 요구사항과의 적합도 분석
- **부족한 스킬 식별**: 개선이 필요한 영역 제안
- **성장 가능성 평가**: 지원자의 학습 능력과 발전 잠재력 분석

### 🔍 면접 질문 생성
- **맞춤형 질문**: 직무와 지원자 수준에 맞는 질문 생성
- **카테고리별 분류**: 기술, 행동, 상황 질문으로 구분
- **평가 기준 제공**: 각 질문별 평가 포인트 제시
- **면접 시간 추정**: 예상 면접 소요시간 계산

### 📊 후보자 비교
- **일괄 분석**: 여러 후보자 동시 분석 및 비교
- **순위 매기기**: 종합 점수 기반 후보자 랭킹
- **강점/약점 분석**: 각 후보자의 장단점 시각화
- **추천 시스템**: 최적 후보자 추천 및 근거 제시

## 🛠 기술 스택

### 백엔드
- **Framework**: FastAPI (Python)
- **AI/ML**: OpenAI API, spaCy, NLTK, scikit-learn
- **Document Processing**: PyPDF2, python-docx
- **Database**: PostgreSQL, Redis (캐시)
- **Authentication**: JWT, OAuth2
- **Testing**: pytest, httpx

### 프론트엔드
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **UI Library**: Tailwind CSS
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Charts**: Chart.js, Recharts
- **Animations**: Framer Motion

### 인프라
- **Containerization**: Docker, Docker Compose
- **Monitoring**: Prometheus, Grafana
- **Logging**: Structured logging with JSON
- **CI/CD**: GitHub Actions
- **Deployment**: AWS/GCP/Azure

## 🏗 시스템 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Web    │    │   FastAPI       │    │   PostgreSQL    │
│   Frontend      │◄──►│   Backend       │◄──►│   Database      │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   AI Services   │
                       │   (OpenAI API)  │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   File Storage  │
                       │   (Local/S3)    │
                       └─────────────────┘
```

## ⚡ 빠른 시작

### 전체 시스템 한 번에 시작하기

```bash
# 저장소 클론
git clone https://github.com/your-org/fitcruit.git
cd fitcruit

# 자동 설치 및 시작
chmod +x start.sh
./start.sh
```

### 개별 실행

#### 백엔드 실행
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### 프론트엔드 실행
```bash
cd frontend
npm install
npm run dev
```

## 🔧 설치 및 설정

### 시스템 요구사항
- **Python**: 3.8 이상
- **Node.js**: 18 이상
- **PostgreSQL**: 13 이상 (선택사항)
- **Redis**: 6 이상 (선택사항)

### 환경 변수 설정

#### 백엔드 설정 (backend/.env)
```env
# 복사하여 사용
cp backend/.env.example backend/.env

# 필수 설정
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://user:password@localhost:5432/fitcruit
SECRET_KEY=your_secret_key
```

#### 프론트엔드 설정 (frontend/.env)
```env
# 복사하여 사용
cp frontend/.env.example frontend/.env

# 필수 설정
VITE_API_URL=http://localhost:8000/api/v1
```

## 📚 API 문서

### 자동 생성 문서
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 주요 엔드포인트

#### 파일 업로드 및 분석
```bash
# 이력서 분석
POST /api/v1/analyze/resume
Content-Type: multipart/form-data

# 포트폴리오 분석
POST /api/v1/analyze/portfolio
Content-Type: multipart/form-data

# 직무 요구사항과 함께 분석
POST /api/v1/analyze-with-job-requirements
Content-Type: multipart/form-data
```

#### 비교 및 매칭
```bash
# 후보자 비교
POST /api/v1/compare-candidates
Content-Type: multipart/form-data

# 면접 질문 생성
GET /api/v1/generate-interview-questions?position=frontend&experience_level=senior
```

#### 관리 기능
```bash
# 분석 통계
GET /api/v1/analytics

# 캐시 정리
POST /api/v1/clear-cache

# 결과 내보내기
GET /api/v1/export/{analysis_id}?format=json
```

## 🎮 사용법

### 1. 이력서 분석하기

1. **파일 업로드**: 대시보드에서 이력서 파일 드래그 앤 드롭
2. **분석 시작**: "분석 시작" 버튼 클릭
3. **결과 확인**: 실시간으로 분석 진행 상황 확인
4. **결과 검토**: 종합 점수 및 세부 분석 결과 확인

### 2. 포트폴리오 평가하기

1. **포트폴리오 업로드**: PDF 또는 Word 형태의 포트폴리오 업로드
2. **GitHub 연동**: GitHub 프로필 URL 입력 (선택사항)
3. **자동 분석**: 프로젝트 복잡도, 기술 스택, 창의성 자동 평가
4. **결과 활용**: 평가 결과를 바탕으로 채용 결정 지원

### 3. 후보자 비교하기

1. **다중 파일 업로드**: 여러 지원자의 이력서 한 번에 업로드
2. **직무 설정**: 채용하고자 하는 직무 정보 입력
3. **일괄 분석**: 모든 후보자 동시 분석 및 비교
4. **순위 확인**: 종합 점수 기반 후보자 랭킹 확인

### 4. 면접 질문 생성하기

1. **직무 정보 입력**: 채용 포지션 및 경험 레벨 설정
2. **질문 카테고리 선택**: 기술, 행동, 상황 질문 중 선택
3. **질문 생성**: AI가 생성한 맞춤형 면접 질문 확인
4. **면접 활용**: 평가 기준과 함께 면접에 활용

## 👨‍💻 개발 가이드

### 프로젝트 구조

```
fitcruit/
├── backend/                 # FastAPI 백엔드
│   ├── api/                # API 엔드포인트
│   ├── ai_analyzer/        # AI 분석 모듈
│   ├── models/             # 데이터 모델
│   ├── services/           # 비즈니스 로직
│   ├── utils/              # 유틸리티 함수
│   └── main.py             # 메인 애플리케이션
├── frontend/               # React 프론트엔드
│   ├── src/
│   │   ├── components/     # React 컴포넌트
│   │   ├── pages/          # 페이지 컴포넌트
│   │   ├── services/       # API 서비스
│   │   ├── types/          # TypeScript 타입
│   │   └── styles/         # CSS 스타일
│   └── public/             # 정적 자산
└── start.sh                # 시작 스크립트
```

### 개발 환경 설정

```bash
# 개발 의존성 설치
cd backend && pip install -r requirements-dev.txt
cd frontend && npm install

# 린팅 및 포매팅
cd backend && black . && flake8 .
cd frontend && npm run lint && npm run format

# 테스트 실행
cd backend && pytest
cd frontend && npm test
```

### 새로운 기능 추가하기

1. **백엔드 API 추가**
   - `api/endpoints.py`에 새로운 엔드포인트 추가
   - `models/schemas.py`에 필요한 데이터 모델 정의
   - `services/`에 비즈니스 로직 구현

2. **프론트엔드 기능 추가**
   - `src/components/`에 새로운 컴포넌트 생성
   - `src/services/api.ts`에 API 호출 함수 추가
   - `src/types/`에 TypeScript 타입 정의

3. **AI 분석 기능 추가**
   - `ai_analyzer/`에 새로운 분석 모듈 추가
   - 기존 분석 파이프라인에 통합
   - 테스트 케이스 작성

## 🚀 배포

### Docker를 사용한 배포

```bash
# Docker 이미지 빌드
docker build -t fitcruit-backend ./backend
docker build -t fitcruit-frontend ./frontend

# Docker Compose로 실행
docker-compose up -d
```

### 클라우드 배포

#### AWS 배포
```bash
# AWS CLI 설정
aws configure

# 인프라 배포 (Terraform 사용)
cd infrastructure/aws
terraform init
terraform plan
terraform apply
```

#### Google Cloud 배포
```bash
# gcloud CLI 설정
gcloud auth login
gcloud config set project your-project-id

# 애플리케이션 배포
gcloud app deploy
```

## 📊 모니터링 및 로깅

### 메트릭 수집
- **Prometheus**: 애플리케이션 메트릭 수집
- **Grafana**: 시각화 대시보드
- **Custom Metrics**: 분석 성공률, 처리 시간 등

### 로깅
- **Structured Logging**: JSON 형태의 구조화된 로그
- **Log Levels**: DEBUG, INFO, WARNING, ERROR
- **Log Rotation**: 자동 로그 파일 순환

## 🤝 기여하기

### 기여 방법

1. **이슈 리포팅**: 버그 발견 시 GitHub Issues에 등록
2. **기능 제안**: 새로운 기능 아이디어 제안
3. **코드 기여**: Fork → Branch → Pull Request 과정
4. **문서 개선**: README, API 문서 개선

### 개발 규칙

- **코드 스타일**: Black (Python), Prettier (JavaScript/TypeScript)
- **커밋 메시지**: Conventional Commits 규칙 준수
- **테스트**: 새로운 기능은 반드시 테스트 포함
- **문서**: 코드 변경 시 관련 문서 업데이트

### Pull Request 가이드

1. **브랜치 생성**: `feature/your-feature-name`
2. **테스트 통과**: 모든 테스트 통과 확인
3. **코드 리뷰**: 최소 1명의 리뷰어 승인
4. **문서 업데이트**: 필요시 문서 업데이트

## 🛡 보안

### 데이터 보호
- **파일 암호화**: 업로드된 파일 자동 암호화
- **개인정보 보호**: GDPR 준수 개인정보 처리
- **접근 제어**: 역할 기반 접근 제어 (RBAC)

### API 보안
- **인증**: JWT 기반 인증
- **권한 부여**: 세분화된 권한 관리
- **요청 제한**: Rate limiting 적용

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 📞 지원 및 문의

- **GitHub Issues**: 버그 리포트 및 기능 요청
- **이메일**: support@fitcruit.com
- **문서**: [공식 문서](https://docs.fitcruit.com)
- **커뮤니티**: [Discord 서버](https://discord.gg/fitcruit)

---

<div align="center">
  <p>Made with ❤️ by the Fitcruit Team</p>
  <p>© 2024 Fitcruit. All rights reserved.</p>
</div>
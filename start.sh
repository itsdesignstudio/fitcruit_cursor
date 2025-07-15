#!/bin/bash

# Fitcruit 프로젝트 시작 스크립트
echo "🚀 Fitcruit - AI 기반 채용 자동화 플랫폼 시작 중..."

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 함수 정의
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 환경 변수 파일 확인
check_env_files() {
    print_status "환경 변수 파일 확인 중..."
    
    if [ ! -f "backend/.env" ]; then
        print_warning "backend/.env 파일이 없습니다. 예시 파일을 복사합니다."
        cp backend/.env.example backend/.env
        print_warning "backend/.env 파일을 수정하여 올바른 설정을 입력하세요."
    fi
    
    if [ ! -f "frontend/.env" ]; then
        print_warning "frontend/.env 파일이 없습니다. 예시 파일을 복사합니다."
        cp frontend/.env.example frontend/.env
        print_warning "frontend/.env 파일을 수정하여 올바른 설정을 입력하세요."
    fi
    
    print_success "환경 변수 파일 확인 완료"
}

# 백엔드 의존성 설치
install_backend_deps() {
    print_status "백엔드 의존성 설치 중..."
    
    cd backend
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3이 설치되지 않았습니다."
        exit 1
    fi
    
    # 가상환경 생성
    if [ ! -d "venv" ]; then
        print_status "Python 가상환경 생성 중..."
        python3 -m venv venv
    fi
    
    # 가상환경 활성화
    source venv/bin/activate
    
    # 의존성 설치
    pip install -r requirements.txt
    
    print_success "백엔드 의존성 설치 완료"
    cd ..
}

# 프론트엔드 의존성 설치
install_frontend_deps() {
    print_status "프론트엔드 의존성 설치 중..."
    
    cd frontend
    
    if ! command -v npm &> /dev/null; then
        print_error "npm이 설치되지 않았습니다."
        exit 1
    fi
    
    npm install
    
    print_success "프론트엔드 의존성 설치 완료"
    cd ..
}

# 백엔드 서버 시작
start_backend() {
    print_status "백엔드 서버 시작 중..."
    
    cd backend
    source venv/bin/activate
    
    # 업로드 디렉토리 생성
    mkdir -p uploads
    mkdir -p logs
    
    # 서버 시작
    python main.py &
    BACKEND_PID=$!
    
    print_success "백엔드 서버 시작됨 (PID: $BACKEND_PID)"
    cd ..
}

# 프론트엔드 서버 시작
start_frontend() {
    print_status "프론트엔드 서버 시작 중..."
    
    cd frontend
    
    # 개발 서버 시작
    npm run dev &
    FRONTEND_PID=$!
    
    print_success "프론트엔드 서버 시작됨 (PID: $FRONTEND_PID)"
    cd ..
}

# 서버 상태 확인
check_servers() {
    print_status "서버 상태 확인 중..."
    
    # 백엔드 상태 확인
    sleep 5
    if curl -s http://localhost:8000/health > /dev/null; then
        print_success "백엔드 서버 정상 동작 중 (http://localhost:8000)"
    else
        print_error "백엔드 서버 연결 실패"
    fi
    
    # 프론트엔드 상태 확인
    sleep 5
    if curl -s http://localhost:3000 > /dev/null; then
        print_success "프론트엔드 서버 정상 동작 중 (http://localhost:3000)"
    else
        print_error "프론트엔드 서버 연결 실패"
    fi
}

# 종료 처리
cleanup() {
    print_status "서버 종료 중..."
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        print_success "백엔드 서버 종료됨"
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        print_success "프론트엔드 서버 종료됨"
    fi
    
    exit 0
}

# 신호 처리
trap cleanup SIGINT SIGTERM

# 메인 실행
main() {
    echo "==========================================="
    echo "  Fitcruit - AI 기반 채용 자동화 플랫폼"
    echo "==========================================="
    echo
    
    # 환경 변수 확인
    check_env_files
    
    # 의존성 설치
    install_backend_deps
    install_frontend_deps
    
    echo
    print_status "서버 시작 중..."
    echo
    
    # 서버 시작
    start_backend
    start_frontend
    
    # 서버 상태 확인
    check_servers
    
    echo
    echo "==========================================="
    echo "  🎉 Fitcruit 시스템이 시작되었습니다!"
    echo "==========================================="
    echo
    echo "📊 대시보드: http://localhost:3000"
    echo "🔧 API 문서: http://localhost:8000/docs"
    echo "❤️  상태 확인: http://localhost:8000/health"
    echo
    echo "종료하려면 Ctrl+C를 누르세요."
    echo
    
    # 서버 유지
    wait
}

# 스크립트 실행
main
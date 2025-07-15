import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Target, 
  BarChart3, 
  MessageSquare, 
  Zap, 
  Palette, 
  TrendingUp,
  Upload,
  Search,
  FileText,
  Users,
  Clock,
  CheckCircle
} from 'lucide-react';

const LandingPage: React.FC = () => {
  useEffect(() => {
    // 스크롤 애니메이션 설정
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-slide-in');
        }
      });
    }, observerOptions);

    // 애니메이션 적용할 요소들
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
      observer.observe(el);
    });

    // 헤더 스크롤 효과
    const handleScroll = () => {
      const header = document.querySelector('header');
      if (header) {
        if (window.pageYOffset > 100) {
          header.classList.add('scrolled');
        } else {
          header.classList.remove('scrolled');
        }
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="landing-page">
      {/* 헤더 */}
      <header className="fixed top-0 w-full bg-white/95 backdrop-blur-sm z-50 shadow-soft transition-all duration-300">
        <nav className="flex justify-between items-center py-4 px-6 max-w-7xl mx-auto">
          <div className="logo text-2xl font-bold gradient-text">
            Fitcruit
          </div>
          <div className="hidden md:flex items-center space-x-8">
            <a href="#features" className="text-gray-600 hover:text-primary-600 transition-colors">
              주요 기능
            </a>
            <a href="#pricing" className="text-gray-600 hover:text-primary-600 transition-colors">
              요금제
            </a>
            <a href="#about" className="text-gray-600 hover:text-primary-600 transition-colors">
              회사 소개
            </a>
            <Link 
              to="/analyze" 
              className="btn btn-primary btn-md"
            >
              무료로 시작하기
            </Link>
          </div>
          {/* 모바일 메뉴 버튼 */}
          <div className="md:hidden">
            <button className="text-gray-600 hover:text-primary-600">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </nav>
      </header>

      {/* 히어로 섹션 */}
      <section className="hero-section pt-24 pb-20 bg-gradient-to-br from-red-50 to-pink-50 min-h-screen flex items-center">
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <motion.div 
              className="hero-text"
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h1 className="text-5xl lg:text-6xl font-bold mb-6 leading-tight">
                채용 고민,<br />
                <span className="gradient-text">조금 덜어드려요</span>
              </h1>
              <p className="text-xl text-gray-600 mb-8 leading-relaxed">
                AI가 포트폴리오를 분석하고, 딱 맞는 인재를 찾아드립니다.<br />
                전문 인사팀이 없어도 똑똑한 채용이 가능해요.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 mb-12">
                <Link 
                  to="/analyze" 
                  className="btn btn-primary btn-lg"
                >
                  지금 바로 분석해보기
                </Link>
                <Link 
                  to="/demo" 
                  className="btn btn-outline btn-lg"
                >
                  기업용 데모 신청
                </Link>
              </div>
              <div className="flex flex-wrap gap-8 text-sm text-gray-600">
                <div className="flex items-center gap-2">
                  <Zap className="w-4 h-4 text-primary-600" />
                  <span>5분 만에 채용 분석 완료</span>
                </div>
                <div className="flex items-center gap-2">
                  <Users className="w-4 h-4 text-primary-600" />
                  <span>300개 기업이 선택</span>
                </div>
                <div className="flex items-center gap-2">
                  <BarChart3 className="w-4 h-4 text-primary-600" />
                  <span>99% 정확도</span>
                </div>
              </div>
            </motion.div>
            
            <motion.div 
              className="hero-visual"
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
            >
              <div className="dashboard-preview bg-white rounded-3xl shadow-strong p-6 hover-lift">
                <div className="flex justify-between items-center mb-6">
                  <h3 className="font-semibold text-gray-800">지원자 포트폴리오 분석</h3>
                  <span className="text-sm text-primary-600 font-medium">실시간</span>
                </div>
                <div className="score-display bg-gradient-to-r from-primary-500 to-primary-600 text-white p-8 rounded-2xl text-center mb-6">
                  <div className="text-5xl font-bold mb-2">87점</div>
                  <div className="text-primary-100">종합 평가 점수</div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-gray-50 p-4 rounded-lg flex justify-between items-center">
                    <span className="text-sm font-medium text-gray-700">시각적 완성도</span>
                    <span className="font-bold text-primary-600">92점</span>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg flex justify-between items-center">
                    <span className="text-sm font-medium text-gray-700">기획 역량</span>
                    <span className="font-bold text-primary-600">85점</span>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg flex justify-between items-center">
                    <span className="text-sm font-medium text-gray-700">경력 적합성</span>
                    <span className="font-bold text-primary-600">88점</span>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg flex justify-between items-center">
                    <span className="text-sm font-medium text-gray-700">성장 가능성</span>
                    <span className="font-bold text-primary-600">84점</span>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* 기능 섹션 */}
      <section id="features" className="py-20 bg-white">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4 text-gray-900">
              채용의 모든 순간을 AI가 도와드려요
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              포지션 정의부터 면접 질문까지, 채용 전 과정을 자동화합니다
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: <Target className="w-8 h-8" />,
                title: "포지션 정의 도우미",
                description: "우리 회사에 지금 필요한 포지션이 뭔지 모르겠다면? AI가 기업 상황을 분석해 최적의 포지션을 제안합니다."
              },
              {
                icon: <BarChart3 className="w-8 h-8" />,
                title: "포트폴리오 자동 평가",
                description: "디자인, 기획, 마케팅 포트폴리오를 AI가 분석해 객관적인 점수와 상세 리포트를 제공합니다."
              },
              {
                icon: <MessageSquare className="w-8 h-8" />,
                title: "맞춤형 면접 질문",
                description: "지원자의 이력서와 포트폴리오를 분석해 꼭 물어봐야 할 면접 질문을 자동으로 생성합니다."
              },
              {
                icon: <Zap className="w-8 h-8" />,
                title: "5분 스피드 분석",
                description: "수십 명의 지원자도 단 5분 만에 분석 완료. 채용에 들이는 시간을 90% 단축시켜드립니다."
              },
              {
                icon: <Palette className="w-8 h-8" />,
                title: "시각 중심 직군 특화",
                description: "디자이너, 마케터, 기획자 등 포트폴리오가 중요한 직군에 최적화된 평가 시스템입니다."
              },
              {
                icon: <TrendingUp className="w-8 h-8" />,
                title: "채용 리스크 분석",
                description: "잘못된 채용의 기회비용은 연봉의 3배. AI가 채용 리스크를 미리 분석해드립니다."
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                className="feature-card card hover-lift animate-on-scroll"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
              >
                <div className="card-content text-center">
                  <div className="feature-icon bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-xl p-4 inline-flex mb-6">
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-semibold mb-4 text-gray-900">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* 프로세스 섹션 */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4 text-gray-900">
              AI가 만드는 스마트한 채용 프로세스
            </h2>
            <p className="text-xl text-gray-600">
              복잡한 채용도 3단계면 충분합니다
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {[
              {
                number: "1",
                title: "지원서 업로드",
                description: "이력서와 포트폴리오를 한 번에 업로드하세요. AI가 자동으로 분류합니다.",
                icon: <Upload className="w-8 h-8" />
              },
              {
                number: "2",
                title: "AI 평가 확인",
                description: "지원자별 상세 분석 리포트와 순위를 확인하고 최적의 인재를 선별하세요.",
                icon: <Search className="w-8 h-8" />
              },
              {
                number: "3",
                title: "면접 준비 완료",
                description: "AI가 생성한 맞춤형 면접 질문으로 효과적인 인재 검증을 진행하세요.",
                icon: <FileText className="w-8 h-8" />
              }
            ].map((step, index) => (
              <motion.div
                key={index}
                className="text-center animate-on-scroll"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                viewport={{ once: true }}
              >
                <div className="step-number w-16 h-16 bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6">
                  {step.number}
                </div>
                <div className="mb-4 flex justify-center text-primary-600">
                  {step.icon}
                </div>
                <h3 className="text-xl font-semibold mb-4 text-gray-900">
                  {step.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {step.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* 가격 섹션 */}
      <section id="pricing" className="py-20 bg-white">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4 text-gray-900">
              합리적인 가격으로 시작하세요
            </h2>
            <p className="text-xl text-gray-600">
              규모와 필요에 따라 선택할 수 있는 다양한 요금제
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {[
              {
                name: "Free",
                price: "₩0",
                period: "영구 무료",
                features: [
                  "이력서 분석 3건/월",
                  "포지션 추천",
                  "기본 리포트",
                  "이메일 지원"
                ],
                buttonText: "무료로 시작",
                buttonStyle: "btn-outline"
              },
              {
                name: "Pro",
                price: "₩29,000",
                period: "월간 결제",
                features: [
                  "무제한 분석",
                  "포트폴리오 평가",
                  "면접 질문 생성",
                  "PDF 리포트 다운로드",
                  "우선 지원"
                ],
                buttonText: "Pro 시작하기",
                buttonStyle: "btn-primary",
                featured: true
              },
              {
                name: "Team",
                price: "₩49,000",
                period: "월간 결제",
                features: [
                  "Pro의 모든 기능",
                  "팀원 5명 계정",
                  "API 연동",
                  "전담 매니저",
                  "맞춤 교육"
                ],
                buttonText: "팀 문의하기",
                buttonStyle: "btn-outline"
              }
            ].map((plan, index) => (
              <motion.div
                key={index}
                className={`pricing-card card ${plan.featured ? 'ring-2 ring-primary-500 scale-105' : ''} animate-on-scroll`}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
              >
                {plan.featured && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-gradient-to-r from-primary-500 to-primary-600 text-white px-4 py-1 rounded-full text-sm font-medium">
                      인기
                    </span>
                  </div>
                )}
                
                <div className="card-content text-center">
                  <h3 className="text-xl font-semibold mb-2 text-gray-900">
                    {plan.name}
                  </h3>
                  <div className="text-4xl font-bold text-primary-600 mb-2">
                    {plan.price}
                  </div>
                  <p className="text-gray-600 mb-8">
                    {plan.period}
                  </p>
                  
                  <ul className="space-y-4 mb-8">
                    {plan.features.map((feature, idx) => (
                      <li key={idx} className="flex items-center text-gray-600">
                        <CheckCircle className="w-5 h-5 text-primary-600 mr-3 flex-shrink-0" />
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>
                  
                  <Link 
                    to="/signup" 
                    className={`btn ${plan.buttonStyle} w-full`}
                  >
                    {plan.buttonText}
                  </Link>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA 섹션 */}
      <section className="py-20 bg-gradient-to-r from-primary-600 to-primary-700 text-white text-center">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold mb-4">
              지금 바로 똑똑한 채용을 시작하세요
            </h2>
            <p className="text-xl mb-8 opacity-90">
              5분이면 충분해요. AI가 최고의 인재를 찾아드립니다.
            </p>
            <Link 
              to="/analyze" 
              className="btn bg-white text-primary-600 hover:bg-gray-100 btn-lg font-semibold"
            >
              무료로 분석 시작하기
            </Link>
          </motion.div>
        </div>
      </section>

      {/* 푸터 */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-6">
          <div className="flex flex-wrap justify-center gap-8 mb-8">
            <a href="#" className="text-gray-400 hover:text-white transition-colors">
              서비스 소개
            </a>
            <a href="#" className="text-gray-400 hover:text-white transition-colors">
              이용약관
            </a>
            <a href="#" className="text-gray-400 hover:text-white transition-colors">
              개인정보처리방침
            </a>
            <a href="#" className="text-gray-400 hover:text-white transition-colors">
              고객센터
            </a>
            <a href="#" className="text-gray-400 hover:text-white transition-colors">
              블로그
            </a>
            <a href="#" className="text-gray-400 hover:text-white transition-colors">
              채용
            </a>
          </div>
          <div className="text-center text-gray-500">
            <p>&copy; 2024 Fitcruit. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
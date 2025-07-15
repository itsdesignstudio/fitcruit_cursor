import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import spacy
import pandas as pd
from models.schemas import (
    ResumeAnalysis, Skill, Experience, Education, Project, 
    ScoreBreakdown, FinalScore, SkillLevel
)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeAnalyzer:
    """이력서 분석 클래스"""
    
    def __init__(self):
        # spaCy 모델 로드 (한국어 및 영어 지원)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("영어 spaCy 모델이 없습니다. 기본 기능으로 동작합니다.")
            self.nlp = None
        
        # 기술 스택 데이터베이스
        self.tech_skills = self._load_tech_skills()
        
        # 직무별 키워드
        self.job_keywords = self._load_job_keywords()
        
        # 경력 관련 키워드
        self.experience_keywords = [
            "경력", "근무", "재직", "담당", "개발", "설계", "구축", "운영", "관리",
            "프로젝트", "팀", "리더", "매니저", "연구", "분석", "기획"
        ]
    
    def _load_tech_skills(self) -> Dict[str, List[str]]:
        """기술 스택 데이터베이스를 로드합니다."""
        return {
            "programming": [
                "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust",
                "Swift", "Kotlin", "PHP", "Ruby", "Scala", "R", "MATLAB", "SQL"
            ],
            "frontend": [
                "React", "Vue.js", "Angular", "HTML", "CSS", "Sass", "Less", "Bootstrap",
                "Tailwind CSS", "jQuery", "Webpack", "Vite", "Next.js", "Nuxt.js"
            ],
            "backend": [
                "Node.js", "Express", "Django", "Flask", "FastAPI", "Spring Boot",
                "ASP.NET", "Laravel", "Ruby on Rails", "Gin", "Fiber"
            ],
            "database": [
                "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Oracle",
                "SQL Server", "Cassandra", "Elasticsearch"
            ],
            "cloud": [
                "AWS", "Google Cloud", "Azure", "Docker", "Kubernetes", "Terraform",
                "Jenkins", "GitLab CI", "GitHub Actions", "Heroku", "Netlify", "Vercel"
            ],
            "tools": [
                "Git", "GitHub", "GitLab", "Jira", "Confluence", "Slack", "Notion",
                "Figma", "Adobe", "Postman", "Swagger", "IntelliJ", "VS Code"
            ],
            "ai_ml": [
                "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas", "NumPy",
                "Matplotlib", "Seaborn", "OpenCV", "NLTK", "spaCy", "Hugging Face"
            ]
        }
    
    def _load_job_keywords(self) -> Dict[str, List[str]]:
        """직무별 키워드를 로드합니다."""
        return {
            "frontend": ["프론트엔드", "UI", "UX", "웹개발", "React", "Vue", "Angular"],
            "backend": ["백엔드", "서버", "API", "데이터베이스", "마이크로서비스"],
            "fullstack": ["풀스택", "전체", "프론트", "백엔드", "웹개발"],
            "mobile": ["모바일", "앱개발", "iOS", "Android", "React Native", "Flutter"],
            "devops": ["데브옵스", "인프라", "클라우드", "배포", "CI/CD", "도커"],
            "ai": ["AI", "머신러닝", "딥러닝", "데이터사이언스", "NLP", "컴퓨터비전"],
            "data": ["데이터", "분석", "빅데이터", "ETL", "데이터웨어하우스"]
        }
    
    async def analyze_resume(self, text: str, job_position: Optional[str] = None) -> ResumeAnalysis:
        """이력서를 종합적으로 분석합니다."""
        try:
            # 기본 정보 추출
            personal_info = self._extract_personal_info(text)
            
            # 스킬 분석
            skills = self._analyze_skills(text)
            
            # 경력 분석
            experiences = self._analyze_experience(text)
            
            # 교육 배경 분석
            education = self._analyze_education(text)
            
            # 프로젝트 분석
            projects = self._analyze_projects(text)
            
            # 언어 능력 분석
            languages = self._extract_languages(text)
            
            # 자격증 분석
            certifications = self._extract_certifications(text)
            
            # 요약 생성
            summary = self._generate_summary(text, skills, experiences)
            
            # 키워드 추출
            keywords = self._extract_keywords(text)
            
            # ATS 호환성 분석
            ats_compatibility = self._analyze_ats_compatibility(text)
            
            # 스코어링
            score = self._calculate_score(skills, experiences, education, projects, text)
            
            return ResumeAnalysis(
                personal_info=personal_info,
                skills=skills,
                experiences=experiences,
                education=education,
                projects=projects,
                languages=languages,
                certifications=certifications,
                summary=summary,
                score=score,
                keywords=keywords,
                ats_compatibility=ats_compatibility
            )
        
        except Exception as e:
            logger.error(f"이력서 분석 중 오류: {e}")
            raise
    
    def _extract_personal_info(self, text: str) -> Dict[str, str]:
        """개인정보를 추출합니다."""
        info = {}
        
        # 이메일 추출
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            info['email'] = emails[0]
        
        # 전화번호 추출
        phone_pattern = r'(?:\+82|0)(?:\d{1,3})-?\d{3,4}-?\d{4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            info['phone'] = phones[0]
        
        # GitHub 링크 추출
        github_pattern = r'github\.com/[\w-]+'
        github_links = re.findall(github_pattern, text)
        if github_links:
            info['github'] = f"https://{github_links[0]}"
        
        # LinkedIn 추출
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_links = re.findall(linkedin_pattern, text)
        if linkedin_links:
            info['linkedin'] = f"https://{linkedin_links[0]}"
        
        return info
    
    def _analyze_skills(self, text: str) -> List[Skill]:
        """스킬을 분석합니다."""
        skills = []
        text_lower = text.lower()
        
        for category, skill_list in self.tech_skills.items():
            for skill in skill_list:
                if skill.lower() in text_lower:
                    # 스킬 레벨 추정
                    level = self._estimate_skill_level(text, skill)
                    
                    # 신뢰도 계산
                    confidence = self._calculate_skill_confidence(text, skill)
                    
                    skills.append(Skill(
                        name=skill,
                        level=level,
                        confidence=confidence,
                        category=category
                    ))
        
        return skills
    
    def _estimate_skill_level(self, text: str, skill: str) -> SkillLevel:
        """스킬 레벨을 추정합니다."""
        text_lower = text.lower()
        skill_lower = skill.lower()
        
        # 전문가 키워드
        expert_keywords = ["전문가", "expert", "마스터", "master", "시니어", "senior", "리드", "lead"]
        
        # 고급 키워드
        advanced_keywords = ["고급", "advanced", "숙련", "proficient", "경험"]
        
        # 중급 키워드
        intermediate_keywords = ["중급", "intermediate", "사용가능", "활용", "개발"]
        
        # 키워드 매칭
        for keyword in expert_keywords:
            if keyword in text_lower and skill_lower in text_lower:
                return SkillLevel.EXPERT
        
        for keyword in advanced_keywords:
            if keyword in text_lower and skill_lower in text_lower:
                return SkillLevel.ADVANCED
        
        for keyword in intermediate_keywords:
            if keyword in text_lower and skill_lower in text_lower:
                return SkillLevel.INTERMEDIATE
        
        return SkillLevel.BEGINNER
    
    def _calculate_skill_confidence(self, text: str, skill: str) -> float:
        """스킬의 신뢰도를 계산합니다."""
        text_lower = text.lower()
        skill_lower = skill.lower()
        
        # 기본 점수
        base_score = 0.5
        
        # 언급 횟수
        mention_count = text_lower.count(skill_lower)
        mention_score = min(mention_count * 0.1, 0.3)
        
        # 컨텍스트 분석
        context_score = 0.0
        context_keywords = ["프로젝트", "개발", "구현", "사용", "경험", "활용"]
        
        for keyword in context_keywords:
            if keyword in text_lower:
                context_score += 0.05
        
        return min(base_score + mention_score + context_score, 1.0)
    
    def _analyze_experience(self, text: str) -> List[Experience]:
        """경력을 분석합니다."""
        experiences = []
        
        # 경력 섹션 패턴
        experience_patterns = [
            r'경력.*?(?=학력|교육|프로젝트|자격|기술|$)',
            r'근무경력.*?(?=학력|교육|프로젝트|자격|기술|$)',
            r'work experience.*?(?=education|project|skill|$)',
            r'employment.*?(?=education|project|skill|$)'
        ]
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                exp_data = self._parse_experience_section(match)
                experiences.extend(exp_data)
        
        return experiences
    
    def _parse_experience_section(self, text: str) -> List[Experience]:
        """경력 섹션을 파싱합니다."""
        experiences = []
        
        # 회사명과 직책 패턴
        company_patterns = [
            r'([가-힣a-zA-Z\s&.,]+)(?:\s+)([가-힣a-zA-Z\s]+)(?:\s+)(\d{4}.\d{1,2}(?:\s*[-~]\s*\d{4}.\d{1,2}|\s*[-~]\s*현재)?)',
            r'(\d{4}.\d{1,2}(?:\s*[-~]\s*\d{4}.\d{1,2}|\s*[-~]\s*현재)?)\s+([가-힣a-zA-Z\s&.,]+)\s+([가-힣a-zA-Z\s]+)'
        ]
        
        for pattern in company_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) >= 3:
                    company = match[0].strip() if match[0] else "Unknown"
                    position = match[1].strip() if match[1] else "Unknown"
                    duration = match[2].strip() if match[2] else "Unknown"
                    
                    experiences.append(Experience(
                        company=company,
                        position=position,
                        duration=duration,
                        description=text[:200],  # 첫 200자
                        is_current="현재" in duration
                    ))
        
        return experiences
    
    def _analyze_education(self, text: str) -> List[Education]:
        """교육 배경을 분석합니다."""
        education = []
        
        # 학력 패턴
        education_patterns = [
            r'([가-힣a-zA-Z\s]+대학교?)\s+([가-힣a-zA-Z\s]+과?)\s+(\d{4})',
            r'([가-힣a-zA-Z\s]+대학교?)\s+([가-힣a-zA-Z\s]+과?)',
            r'(\d{4})\s+([가-힣a-zA-Z\s]+대학교?)\s+([가-힣a-zA-Z\s]+과?)'
        ]
        
        for pattern in education_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) >= 3:
                    institution = match[0].strip()
                    field = match[1].strip()
                    year = int(match[2]) if match[2].isdigit() else None
                    
                    education.append(Education(
                        institution=institution,
                        degree="학사",  # 기본값
                        field_of_study=field,
                        graduation_year=year
                    ))
        
        return education
    
    def _analyze_projects(self, text: str) -> List[Project]:
        """프로젝트를 분석합니다."""
        projects = []
        
        # 프로젝트 섹션 찾기
        project_patterns = [
            r'프로젝트.*?(?=경력|학력|교육|자격|기술|$)',
            r'project.*?(?=experience|education|skill|$)',
            r'포트폴리오.*?(?=경력|학력|교육|자격|기술|$)'
        ]
        
        for pattern in project_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                project_data = self._parse_project_section(match)
                projects.extend(project_data)
        
        return projects
    
    def _parse_project_section(self, text: str) -> List[Project]:
        """프로젝트 섹션을 파싱합니다."""
        projects = []
        
        # 프로젝트명 패턴
        project_lines = text.split('\n')
        current_project = None
        
        for line in project_lines:
            line = line.strip()
            if not line:
                continue
            
            # 프로젝트 시작 패턴
            if any(keyword in line for keyword in ['프로젝트', 'project', '개발', '구현']):
                if current_project:
                    projects.append(current_project)
                
                # 기술 스택 추출
                technologies = self._extract_technologies_from_text(line)
                
                current_project = Project(
                    name=line[:50],  # 첫 50자를 프로젝트명으로
                    description=line,
                    technologies=technologies,
                    duration="Unknown"
                )
            elif current_project:
                # 프로젝트 설명 추가
                current_project.description += " " + line
        
        if current_project:
            projects.append(current_project)
        
        return projects
    
    def _extract_technologies_from_text(self, text: str) -> List[str]:
        """텍스트에서 기술 스택을 추출합니다."""
        technologies = []
        text_lower = text.lower()
        
        for category, tech_list in self.tech_skills.items():
            for tech in tech_list:
                if tech.lower() in text_lower:
                    technologies.append(tech)
        
        return technologies
    
    def _extract_languages(self, text: str) -> List[str]:
        """언어 능력을 추출합니다."""
        languages = []
        
        language_patterns = [
            r'(한국어|영어|일본어|중국어|스페인어|프랑스어|독일어)',
            r'(Korean|English|Japanese|Chinese|Spanish|French|German)',
            r'(TOEIC|TOEFL|IELTS|HSK|JLPT)\s*\d+'
        ]
        
        for pattern in language_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            languages.extend(matches)
        
        return list(set(languages))
    
    def _extract_certifications(self, text: str) -> List[str]:
        """자격증을 추출합니다."""
        certifications = []
        
        cert_patterns = [
            r'정보처리기사|컴활|MOS|리눅스마스터|네트워크관리사',
            r'AWS|Google Cloud|Azure|Oracle|Microsoft',
            r'PMP|CISSP|CISA|CISM'
        ]
        
        for pattern in cert_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            certifications.extend(matches)
        
        return list(set(certifications))
    
    def _generate_summary(self, text: str, skills: List[Skill], experiences: List[Experience]) -> str:
        """요약을 생성합니다."""
        # 주요 기술 스택
        main_skills = [skill.name for skill in skills if skill.confidence > 0.7][:5]
        
        # 경력 년수 계산
        total_years = len(experiences)
        
        summary = f"주요 기술스택: {', '.join(main_skills)}. "
        summary += f"총 경력: 약 {total_years}개 회사. "
        
        # 특징 추출
        if "리더" in text or "팀장" in text or "매니저" in text:
            summary += "리더십 경험 보유. "
        
        if "창업" in text or "스타트업" in text:
            summary += "스타트업 경험 보유. "
        
        return summary
    
    def _extract_keywords(self, text: str) -> List[str]:
        """키워드를 추출합니다."""
        keywords = []
        
        # 기술 키워드
        for skill_list in self.tech_skills.values():
            for skill in skill_list:
                if skill.lower() in text.lower():
                    keywords.append(skill)
        
        # 직무 키워드
        for job_keywords in self.job_keywords.values():
            for keyword in job_keywords:
                if keyword in text:
                    keywords.append(keyword)
        
        return list(set(keywords))
    
    def _analyze_ats_compatibility(self, text: str) -> float:
        """ATS 호환성을 분석합니다."""
        score = 0.0
        
        # 키워드 밀도
        keyword_count = len(self._extract_keywords(text))
        score += min(keyword_count * 2, 30)
        
        # 구조화된 정보
        if re.search(r'이메일|email', text, re.IGNORECASE):
            score += 10
        if re.search(r'전화|phone', text, re.IGNORECASE):
            score += 10
        if re.search(r'경력|experience', text, re.IGNORECASE):
            score += 15
        if re.search(r'학력|education', text, re.IGNORECASE):
            score += 10
        if re.search(r'기술|skill', text, re.IGNORECASE):
            score += 15
        
        # 텍스트 길이
        word_count = len(text.split())
        if 300 <= word_count <= 1000:
            score += 10
        
        return min(score, 100.0)
    
    def _calculate_score(self, skills: List[Skill], experiences: List[Experience], 
                        education: List[Education], projects: List[Project], text: str) -> FinalScore:
        """종합 점수를 계산합니다."""
        
        # 기술 점수
        tech_score = min(len(skills) * 5, 100)
        
        # 경력 점수
        exp_score = min(len(experiences) * 20, 100)
        
        # 학력 점수
        edu_score = min(len(education) * 30, 100)
        
        # 프로젝트 점수
        project_score = min(len(projects) * 15, 100)
        
        # 소통 점수 (문서 품질 기반)
        comm_score = self._calculate_communication_score(text)
        
        # 전체 표현 점수
        presentation_score = self._calculate_presentation_score(text)
        
        breakdown = ScoreBreakdown(
            technical_skills=tech_score,
            experience_relevance=exp_score,
            education_background=edu_score,
            project_quality=project_score,
            communication_skills=comm_score,
            overall_presentation=presentation_score
        )
        
        # 전체 점수 계산
        overall = (tech_score * 0.3 + exp_score * 0.25 + edu_score * 0.15 + 
                  project_score * 0.15 + comm_score * 0.1 + presentation_score * 0.05)
        
        return FinalScore(
            overall_score=overall,
            breakdown=breakdown,
            strengths=self._identify_strengths(skills, experiences),
            weaknesses=self._identify_weaknesses(skills, experiences),
            recommendations=self._generate_recommendations(skills, experiences)
        )
    
    def _calculate_communication_score(self, text: str) -> float:
        """소통 능력 점수를 계산합니다."""
        score = 50.0  # 기본 점수
        
        # 문장 구조
        sentences = re.split(r'[.!?]', text)
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        if 10 <= avg_sentence_length <= 20:
            score += 20
        
        # 전문 용어 사용
        professional_terms = ["담당", "개발", "구현", "설계", "분석", "관리", "운영"]
        term_count = sum(1 for term in professional_terms if term in text)
        score += min(term_count * 5, 20)
        
        # 구체적인 성과 언급
        achievement_keywords = ["향상", "개선", "증가", "감소", "달성", "성공"]
        achievement_count = sum(1 for keyword in achievement_keywords if keyword in text)
        score += min(achievement_count * 3, 10)
        
        return min(score, 100.0)
    
    def _calculate_presentation_score(self, text: str) -> float:
        """문서 표현 점수를 계산합니다."""
        score = 50.0
        
        # 적절한 길이
        word_count = len(text.split())
        if 500 <= word_count <= 1500:
            score += 20
        
        # 구조화
        sections = ["경력", "학력", "기술", "프로젝트"]
        section_count = sum(1 for section in sections if section in text)
        score += min(section_count * 10, 30)
        
        return min(score, 100.0)
    
    def _identify_strengths(self, skills: List[Skill], experiences: List[Experience]) -> List[str]:
        """강점을 식별합니다."""
        strengths = []
        
        if len(skills) > 10:
            strengths.append("다양한 기술 스택 보유")
        
        if len(experiences) > 2:
            strengths.append("풍부한 실무 경험")
        
        high_confidence_skills = [s for s in skills if s.confidence > 0.8]
        if high_confidence_skills:
            strengths.append(f"전문 기술: {', '.join([s.name for s in high_confidence_skills[:3]])}")
        
        return strengths
    
    def _identify_weaknesses(self, skills: List[Skill], experiences: List[Experience]) -> List[str]:
        """약점을 식별합니다."""
        weaknesses = []
        
        if len(skills) < 5:
            weaknesses.append("기술 스택 다양성 부족")
        
        if len(experiences) < 1:
            weaknesses.append("실무 경험 부족")
        
        low_confidence_skills = [s for s in skills if s.confidence < 0.5]
        if len(low_confidence_skills) > len(skills) * 0.5:
            weaknesses.append("기술 역량 증명 부족")
        
        return weaknesses
    
    def _generate_recommendations(self, skills: List[Skill], experiences: List[Experience]) -> List[str]:
        """개선 권장사항을 생성합니다."""
        recommendations = []
        
        if len(skills) < 5:
            recommendations.append("더 많은 기술 스택 학습 권장")
        
        if len(experiences) < 2:
            recommendations.append("프로젝트 경험 추가 권장")
        
        if not any("GitHub" in str(exp.description) for exp in experiences):
            recommendations.append("GitHub 포트폴리오 링크 추가 권장")
        
        recommendations.append("구체적인 성과 지표 추가 권장")
        
        return recommendations
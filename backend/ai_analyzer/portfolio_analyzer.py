import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import requests
from urllib.parse import urlparse
from models.schemas import (
    PortfolioAnalysis, Skill, Project, ScoreBreakdown, 
    FinalScore, SkillLevel
)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PortfolioAnalyzer:
    """포트폴리오 분석 클래스"""
    
    def __init__(self):
        # 기술 스택 카테고리
        self.tech_categories = {
            "frontend": ["React", "Vue", "Angular", "HTML", "CSS", "JavaScript", "TypeScript"],
            "backend": ["Node.js", "Python", "Java", "Django", "Flask", "Spring", "Express"],
            "mobile": ["React Native", "Flutter", "Swift", "Kotlin", "Ionic"],
            "database": ["MySQL", "PostgreSQL", "MongoDB", "Redis", "Firebase"],
            "cloud": ["AWS", "Google Cloud", "Azure", "Docker", "Kubernetes"],
            "ai_ml": ["TensorFlow", "PyTorch", "Scikit-learn", "OpenCV", "NLP"],
            "tools": ["Git", "GitHub", "GitLab", "Docker", "Jenkins", "Webpack"]
        }
        
        # 프로젝트 타입별 가중치
        self.project_weights = {
            "web_app": 1.0,
            "mobile_app": 1.2,
            "ai_ml": 1.5,
            "blockchain": 1.3,
            "game": 1.1,
            "desktop": 0.9,
            "library": 1.4,
            "api": 1.0
        }
        
        # 창의성 키워드
        self.creativity_keywords = [
            "혁신", "독창적", "창의적", "새로운", "unique", "innovative", "creative",
            "original", "novel", "breakthrough", "cutting-edge", "revolutionary"
        ]
        
        # 기술적 깊이 키워드
        self.depth_keywords = [
            "최적화", "성능", "확장성", "아키텍처", "디자인패턴", "알고리즘",
            "optimization", "performance", "scalability", "architecture", 
            "design pattern", "algorithm", "microservices", "distributed"
        ]
    
    async def analyze_portfolio(self, text: str, github_url: Optional[str] = None) -> PortfolioAnalysis:
        """포트폴리오를 종합적으로 분석합니다."""
        try:
            # 프로젝트 분석
            projects = self._analyze_projects(text)
            
            # 기술 스택 분석
            technical_skills = self._analyze_technical_skills(text, projects)
            
            # 창의성 점수 계산
            creativity_score = self._calculate_creativity_score(text, projects)
            
            # 기술적 깊이 분석
            technical_depth = self._analyze_technical_depth(text, projects)
            
            # 프로젝트 다양성 분석
            project_diversity = self._analyze_project_diversity(projects)
            
            # 코드 품질 평가
            code_quality = self._evaluate_code_quality(text, projects)
            
            # 문서화 품질 평가
            documentation_quality = self._evaluate_documentation_quality(text)
            
            # GitHub 통계 분석
            github_stats = None
            if github_url:
                github_stats = await self._analyze_github_stats(github_url)
            
            # 종합 스코어링
            score = self._calculate_portfolio_score(
                projects, technical_skills, creativity_score,
                technical_depth, project_diversity, code_quality,
                documentation_quality, github_stats
            )
            
            return PortfolioAnalysis(
                projects=projects,
                technical_skills=technical_skills,
                creativity_score=creativity_score,
                technical_depth=technical_depth,
                project_diversity=project_diversity,
                code_quality=code_quality,
                documentation_quality=documentation_quality,
                score=score,
                github_stats=github_stats
            )
            
        except Exception as e:
            logger.error(f"포트폴리오 분석 중 오류: {e}")
            raise
    
    def _analyze_projects(self, text: str) -> List[Project]:
        """프로젝트를 분석합니다."""
        projects = []
        
        # 프로젝트 섹션 패턴
        project_patterns = [
            r'프로젝트.*?(?=프로젝트|경력|학력|기술|$)',
            r'project.*?(?=project|experience|education|skill|$)',
            r'포트폴리오.*?(?=포트폴리오|경력|학력|기술|$)'
        ]
        
        for pattern in project_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                project_data = self._parse_project_details(match)
                projects.extend(project_data)
        
        return projects
    
    def _parse_project_details(self, text: str) -> List[Project]:
        """프로젝트 세부사항을 파싱합니다."""
        projects = []
        
        # 프로젝트 구분자로 텍스트 분할
        project_sections = re.split(r'\n\s*\n|(?=\d+\.|\-|\*)', text)
        
        for section in project_sections:
            if not section.strip():
                continue
                
            # 프로젝트 이름 추출
            lines = section.strip().split('\n')
            if not lines:
                continue
                
            project_name = lines[0].strip()
            
            # 기술 스택 추출
            technologies = self._extract_technologies(section)
            
            # URL 추출
            github_url = self._extract_github_url(section)
            demo_url = self._extract_demo_url(section)
            
            # 프로젝트 역할 추출
            role = self._extract_project_role(section)
            
            # 기간 추출
            duration = self._extract_project_duration(section)
            
            # 성과 추출
            achievements = self._extract_achievements(section)
            
            if project_name and len(project_name) > 5:  # 유효한 프로젝트명
                projects.append(Project(
                    name=project_name,
                    description=section.strip(),
                    technologies=technologies,
                    duration=duration,
                    role=role,
                    achievements=achievements,
                    github_url=github_url,
                    demo_url=demo_url
                ))
        
        return projects
    
    def _extract_technologies(self, text: str) -> List[str]:
        """기술 스택을 추출합니다."""
        technologies = []
        text_lower = text.lower()
        
        for category, tech_list in self.tech_categories.items():
            for tech in tech_list:
                if tech.lower() in text_lower:
                    technologies.append(tech)
        
        # 추가 기술 스택 패턴
        tech_patterns = [
            r'기술스택[:：]\s*([^\n]+)',
            r'사용기술[:：]\s*([^\n]+)',
            r'tech stack[:：]\s*([^\n]+)',
            r'technologies[:：]\s*([^\n]+)'
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # 쉼표, 슬래시, 공백으로 분리
                tech_items = re.split(r'[,/\s]+', match)
                technologies.extend([tech.strip() for tech in tech_items if tech.strip()])
        
        return list(set(technologies))
    
    def _extract_github_url(self, text: str) -> Optional[str]:
        """GitHub URL을 추출합니다."""
        github_pattern = r'https?://github\.com/[\w\-\./]+'
        matches = re.findall(github_pattern, text)
        return matches[0] if matches else None
    
    def _extract_demo_url(self, text: str) -> Optional[str]:
        """데모 URL을 추출합니다."""
        demo_patterns = [
            r'https?://[\w\-\.]+\.[\w]+/[\w\-\./?=&]*',
            r'데모[:：]\s*(https?://[^\s]+)',
            r'demo[:：]\s*(https?://[^\s]+)'
        ]
        
        for pattern in demo_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                url = match if isinstance(match, str) else match[0]
                # GitHub이 아닌 URL만 반환
                if 'github.com' not in url:
                    return url
        
        return None
    
    def _extract_project_role(self, text: str) -> Optional[str]:
        """프로젝트 역할을 추출합니다."""
        role_patterns = [
            r'역할[:：]\s*([^\n]+)',
            r'담당[:：]\s*([^\n]+)',
            r'role[:：]\s*([^\n]+)',
            r'position[:：]\s*([^\n]+)'
        ]
        
        for pattern in role_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0].strip()
        
        # 기본 역할 키워드 찾기
        role_keywords = ["개발", "설계", "기획", "PM", "팀장", "리더", "frontend", "backend", "fullstack"]
        for keyword in role_keywords:
            if keyword in text:
                return keyword
        
        return None
    
    def _extract_project_duration(self, text: str) -> Optional[str]:
        """프로젝트 기간을 추출합니다."""
        duration_patterns = [
            r'기간[:：]\s*([^\n]+)',
            r'개발기간[:：]\s*([^\n]+)',
            r'duration[:：]\s*([^\n]+)',
            r'period[:：]\s*([^\n]+)',
            r'(\d+주|\d+개월|\d+년|\d+일|\d+\s*weeks?|\d+\s*months?|\d+\s*years?|\d+\s*days?)'
        ]
        
        for pattern in duration_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0].strip()
        
        return None
    
    def _extract_achievements(self, text: str) -> List[str]:
        """성과를 추출합니다."""
        achievements = []
        
        achievement_patterns = [
            r'성과[:：]\s*([^\n]+)',
            r'결과[:：]\s*([^\n]+)',
            r'achievement[:：]\s*([^\n]+)',
            r'result[:：]\s*([^\n]+)'
        ]
        
        for pattern in achievement_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            achievements.extend(matches)
        
        # 수치 성과 찾기
        metric_patterns = [
            r'(\d+%\s*향상|\d+%\s*개선|\d+%\s*증가|\d+%\s*감소)',
            r'(\d+배\s*향상|\d+배\s*개선|\d+배\s*증가)',
            r'(\d+명\s*사용자|\d+건\s*처리|\d+개\s*기능)'
        ]
        
        for pattern in metric_patterns:
            matches = re.findall(pattern, text)
            achievements.extend(matches)
        
        return achievements
    
    def _analyze_technical_skills(self, text: str, projects: List[Project]) -> List[Skill]:
        """기술 스킬을 분석합니다."""
        skills = []
        skill_counts = {}
        
        # 프로젝트에서 기술 스택 수집
        for project in projects:
            for tech in project.technologies:
                skill_counts[tech] = skill_counts.get(tech, 0) + 1
        
        # 텍스트에서 직접 기술 스택 추출
        for category, tech_list in self.tech_categories.items():
            for tech in tech_list:
                if tech.lower() in text.lower():
                    skill_counts[tech] = skill_counts.get(tech, 0) + 1
        
        # 스킬 객체 생성
        for tech, count in skill_counts.items():
            level = self._determine_skill_level(tech, count, text)
            confidence = min(count * 0.2, 1.0)
            category = self._get_skill_category(tech)
            
            skills.append(Skill(
                name=tech,
                level=level,
                confidence=confidence,
                category=category
            ))
        
        return skills
    
    def _determine_skill_level(self, tech: str, count: int, text: str) -> SkillLevel:
        """기술 레벨을 결정합니다."""
        text_lower = text.lower()
        tech_lower = tech.lower()
        
        # 전문가 레벨 키워드
        if any(keyword in text_lower for keyword in ["전문가", "expert", "마스터", "master"]):
            if tech_lower in text_lower:
                return SkillLevel.EXPERT
        
        # 사용 횟수 기반 레벨 결정
        if count >= 5:
            return SkillLevel.EXPERT
        elif count >= 3:
            return SkillLevel.ADVANCED
        elif count >= 2:
            return SkillLevel.INTERMEDIATE
        else:
            return SkillLevel.BEGINNER
    
    def _get_skill_category(self, tech: str) -> str:
        """기술의 카테고리를 반환합니다."""
        for category, tech_list in self.tech_categories.items():
            if tech in tech_list:
                return category
        return "other"
    
    def _calculate_creativity_score(self, text: str, projects: List[Project]) -> float:
        """창의성 점수를 계산합니다."""
        score = 0.0
        
        # 창의성 키워드 점수
        creativity_count = sum(1 for keyword in self.creativity_keywords if keyword in text.lower())
        score += min(creativity_count * 10, 30)
        
        # 프로젝트 독창성 분석
        unique_projects = 0
        for project in projects:
            if any(keyword in project.description.lower() for keyword in self.creativity_keywords):
                unique_projects += 1
        
        score += min(unique_projects * 15, 45)
        
        # 기술 조합의 독창성
        tech_combinations = self._analyze_tech_combinations(projects)
        score += min(len(tech_combinations) * 5, 25)
        
        return min(score, 100.0)
    
    def _analyze_tech_combinations(self, projects: List[Project]) -> List[Tuple[str, str]]:
        """기술 조합을 분석합니다."""
        combinations = []
        
        for project in projects:
            techs = project.technologies
            for i in range(len(techs)):
                for j in range(i + 1, len(techs)):
                    combination = tuple(sorted([techs[i], techs[j]]))
                    if combination not in combinations:
                        combinations.append(combination)
        
        return combinations
    
    def _analyze_technical_depth(self, text: str, projects: List[Project]) -> float:
        """기술적 깊이를 분석합니다."""
        score = 0.0
        
        # 깊이 키워드 점수
        depth_count = sum(1 for keyword in self.depth_keywords if keyword in text.lower())
        score += min(depth_count * 8, 40)
        
        # 복잡한 프로젝트 분석
        complex_projects = 0
        for project in projects:
            if len(project.technologies) > 5:
                complex_projects += 1
            
            # 아키텍처 관련 키워드 확인
            if any(keyword in project.description.lower() for keyword in self.depth_keywords):
                complex_projects += 1
        
        score += min(complex_projects * 15, 60)
        
        return min(score, 100.0)
    
    def _analyze_project_diversity(self, projects: List[Project]) -> float:
        """프로젝트 다양성을 분석합니다."""
        if not projects:
            return 0.0
        
        # 기술 카테고리 다양성
        categories = set()
        for project in projects:
            for tech in project.technologies:
                category = self._get_skill_category(tech)
                categories.add(category)
        
        category_score = min(len(categories) * 15, 60)
        
        # 프로젝트 타입 다양성
        project_types = self._classify_project_types(projects)
        type_score = min(len(project_types) * 10, 40)
        
        return min(category_score + type_score, 100.0)
    
    def _classify_project_types(self, projects: List[Project]) -> List[str]:
        """프로젝트 타입을 분류합니다."""
        types = []
        
        for project in projects:
            description = project.description.lower()
            
            if any(keyword in description for keyword in ["웹", "web", "website"]):
                types.append("web")
            elif any(keyword in description for keyword in ["앱", "app", "mobile"]):
                types.append("mobile")
            elif any(keyword in description for keyword in ["ai", "ml", "머신러닝", "딥러닝"]):
                types.append("ai")
            elif any(keyword in description for keyword in ["게임", "game"]):
                types.append("game")
            elif any(keyword in description for keyword in ["api", "서버", "server"]):
                types.append("backend")
            else:
                types.append("other")
        
        return list(set(types))
    
    def _evaluate_code_quality(self, text: str, projects: List[Project]) -> float:
        """코드 품질을 평가합니다."""
        score = 50.0  # 기본 점수
        
        # 코드 품질 키워드
        quality_keywords = [
            "테스트", "test", "단위테스트", "unit test", "코드리뷰", "code review",
            "리팩토링", "refactoring", "최적화", "optimization", "성능", "performance"
        ]
        
        quality_count = sum(1 for keyword in quality_keywords if keyword in text.lower())
        score += min(quality_count * 10, 30)
        
        # GitHub 링크가 있는 프로젝트 점수
        github_projects = sum(1 for project in projects if project.github_url)
        score += min(github_projects * 5, 20)
        
        return min(score, 100.0)
    
    def _evaluate_documentation_quality(self, text: str) -> float:
        """문서화 품질을 평가합니다."""
        score = 50.0  # 기본 점수
        
        # 문서화 키워드
        doc_keywords = [
            "readme", "문서", "documentation", "주석", "comment", "설명", "description",
            "가이드", "guide", "매뉴얼", "manual", "wiki"
        ]
        
        doc_count = sum(1 for keyword in doc_keywords if keyword in text.lower())
        score += min(doc_count * 8, 32)
        
        # 상세한 설명 점수
        word_count = len(text.split())
        if word_count > 500:
            score += 18
        elif word_count > 300:
            score += 12
        elif word_count > 200:
            score += 6
        
        return min(score, 100.0)
    
    async def _analyze_github_stats(self, github_url: str) -> Optional[Dict]:
        """GitHub 통계를 분석합니다."""
        try:
            # GitHub API를 통한 통계 분석 (실제 구현에서는 API 키 필요)
            parsed_url = urlparse(github_url)
            path_parts = parsed_url.path.strip('/').split('/')
            
            if len(path_parts) >= 1:
                username = path_parts[0]
                
                # 기본 통계 반환 (실제로는 GitHub API 호출)
                return {
                    'username': username,
                    'public_repos': 0,  # API 호출 결과로 대체
                    'followers': 0,
                    'following': 0,
                    'total_stars': 0,
                    'total_forks': 0,
                    'contribution_streak': 0,
                    'languages': []
                }
        
        except Exception as e:
            logger.error(f"GitHub 통계 분석 중 오류: {e}")
        
        return None
    
    def _calculate_portfolio_score(self, projects: List[Project], technical_skills: List[Skill],
                                 creativity_score: float, technical_depth: float,
                                 project_diversity: float, code_quality: float,
                                 documentation_quality: float, github_stats: Optional[Dict]) -> FinalScore:
        """포트폴리오 종합 점수를 계산합니다."""
        
        # 프로젝트 품질 점수
        project_quality = min(len(projects) * 20, 100)
        
        # 기술 스킬 점수
        tech_score = min(len(technical_skills) * 5, 100)
        
        # 경험 관련성 점수 (프로젝트 기반)
        experience_score = min(len(projects) * 15, 100)
        
        # 소통 점수 (문서화 기반)
        communication_score = documentation_quality
        
        # 전체 표현 점수
        presentation_score = (code_quality + documentation_quality) / 2
        
        # 교육 배경 점수 (포트폴리오에서는 낮은 가중치)
        education_score = 70.0  # 기본 점수
        
        breakdown = ScoreBreakdown(
            technical_skills=tech_score,
            experience_relevance=experience_score,
            education_background=education_score,
            project_quality=project_quality,
            communication_skills=communication_score,
            overall_presentation=presentation_score
        )
        
        # 전체 점수 계산 (포트폴리오 중심 가중치)
        overall = (
            tech_score * 0.25 +
            experience_score * 0.15 +
            education_score * 0.05 +
            project_quality * 0.25 +
            communication_score * 0.15 +
            presentation_score * 0.15
        )
        
        return FinalScore(
            overall_score=overall,
            breakdown=breakdown,
            strengths=self._identify_portfolio_strengths(projects, technical_skills),
            weaknesses=self._identify_portfolio_weaknesses(projects, technical_skills),
            recommendations=self._generate_portfolio_recommendations(projects, technical_skills)
        )
    
    def _identify_portfolio_strengths(self, projects: List[Project], skills: List[Skill]) -> List[str]:
        """포트폴리오 강점을 식별합니다."""
        strengths = []
        
        if len(projects) >= 3:
            strengths.append("다양한 프로젝트 경험")
        
        if len(skills) >= 10:
            strengths.append("폭넓은 기술 스택")
        
        github_projects = sum(1 for project in projects if project.github_url)
        if github_projects >= 2:
            strengths.append("오픈소스 기여 활발")
        
        if any(project.demo_url for project in projects):
            strengths.append("실제 서비스 운영 경험")
        
        return strengths
    
    def _identify_portfolio_weaknesses(self, projects: List[Project], skills: List[Skill]) -> List[str]:
        """포트폴리오 약점을 식별합니다."""
        weaknesses = []
        
        if len(projects) < 2:
            weaknesses.append("프로젝트 수 부족")
        
        if len(skills) < 5:
            weaknesses.append("기술 스택 다양성 부족")
        
        github_projects = sum(1 for project in projects if project.github_url)
        if github_projects == 0:
            weaknesses.append("GitHub 포트폴리오 부족")
        
        if not any(project.demo_url for project in projects):
            weaknesses.append("실제 서비스 링크 부족")
        
        return weaknesses
    
    def _generate_portfolio_recommendations(self, projects: List[Project], skills: List[Skill]) -> List[str]:
        """포트폴리오 개선 권장사항을 생성합니다."""
        recommendations = []
        
        if len(projects) < 3:
            recommendations.append("더 많은 프로젝트 추가 권장")
        
        if not any(project.github_url for project in projects):
            recommendations.append("GitHub 링크 추가 권장")
        
        if not any(project.demo_url for project in projects):
            recommendations.append("라이브 데모 링크 추가 권장")
        
        if len(skills) < 8:
            recommendations.append("더 다양한 기술 스택 경험 권장")
        
        recommendations.append("프로젝트별 상세한 설명 추가 권장")
        recommendations.append("기술적 도전과제와 해결 과정 명시 권장")
        
        return recommendations
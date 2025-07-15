import os
import re
import PyPDF2
import docx
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileProcessor:
    """파일 처리 유틸리티 클래스"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.doc', '.txt']
        
    async def extract_text(self, file_path: Path) -> str:
        """파일에서 텍스트를 추출합니다."""
        try:
            file_extension = file_path.suffix.lower()
            
            if file_extension == '.pdf':
                return await self._extract_pdf_text(file_path)
            elif file_extension in ['.docx', '.doc']:
                return await self._extract_word_text(file_path)
            elif file_extension == '.txt':
                return await self._extract_txt_text(file_path)
            else:
                raise ValueError(f"지원하지 않는 파일 형식: {file_extension}")
                
        except Exception as e:
            logger.error(f"텍스트 추출 중 오류 발생: {e}")
            raise
    
    async def _extract_pdf_text(self, file_path: Path) -> str:
        """PDF 파일에서 텍스트를 추출합니다."""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
            
            return self._clean_text(text)
        
        except Exception as e:
            logger.error(f"PDF 텍스트 추출 중 오류: {e}")
            raise
    
    async def _extract_word_text(self, file_path: Path) -> str:
        """Word 파일에서 텍스트를 추출합니다."""
        try:
            doc = docx.Document(file_path)
            text = ""
            
            # 단락 텍스트 추출
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            # 표 텍스트 추출
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        text += cell.text + "\t"
                    text += "\n"
            
            return self._clean_text(text)
        
        except Exception as e:
            logger.error(f"Word 텍스트 추출 중 오류: {e}")
            raise
    
    async def _extract_txt_text(self, file_path: Path) -> str:
        """텍스트 파일에서 텍스트를 추출합니다."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            return self._clean_text(text)
        
        except UnicodeDecodeError:
            # UTF-8로 실패하면 다른 인코딩 시도
            try:
                with open(file_path, 'r', encoding='cp949') as file:
                    text = file.read()
                return self._clean_text(text)
            except:
                with open(file_path, 'r', encoding='latin-1') as file:
                    text = file.read()
                return self._clean_text(text)
        
        except Exception as e:
            logger.error(f"텍스트 파일 추출 중 오류: {e}")
            raise
    
    def _clean_text(self, text: str) -> str:
        """텍스트를 정리합니다."""
        # 불필요한 공백 제거
        text = re.sub(r'\s+', ' ', text)
        
        # 특수 문자 정리
        text = re.sub(r'[^\w\s\-\.\@\(\)\[\]\{\}\:\;\,\!\?\'\"]', '', text)
        
        # 연속된 줄바꿈 정리
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text.strip()
    
    def get_file_info(self, file_path: Path) -> Dict:
        """파일 정보를 반환합니다."""
        try:
            stat = file_path.stat()
            return {
                'filename': file_path.name,
                'size': stat.st_size,
                'extension': file_path.suffix.lower(),
                'created_at': datetime.fromtimestamp(stat.st_ctime),
                'modified_at': datetime.fromtimestamp(stat.st_mtime),
                'is_supported': file_path.suffix.lower() in self.supported_formats
            }
        except Exception as e:
            logger.error(f"파일 정보 추출 중 오류: {e}")
            raise
    
    def validate_file(self, file_path: Path) -> Tuple[bool, str]:
        """파일 유효성을 검사합니다."""
        try:
            # 파일 존재 확인
            if not file_path.exists():
                return False, "파일이 존재하지 않습니다."
            
            # 파일 형식 확인
            if file_path.suffix.lower() not in self.supported_formats:
                return False, f"지원하지 않는 파일 형식입니다. 지원 형식: {', '.join(self.supported_formats)}"
            
            # 파일 크기 확인 (10MB 제한)
            max_size = 10 * 1024 * 1024  # 10MB
            if file_path.stat().st_size > max_size:
                return False, "파일 크기가 10MB를 초과합니다."
            
            return True, "유효한 파일입니다."
        
        except Exception as e:
            logger.error(f"파일 유효성 검사 중 오류: {e}")
            return False, f"파일 유효성 검사 중 오류: {str(e)}"
    
    def extract_metadata(self, file_path: Path) -> Dict:
        """파일 메타데이터를 추출합니다."""
        metadata = {
            'file_info': self.get_file_info(file_path),
            'text_stats': {},
            'structure_analysis': {}
        }
        
        try:
            # 텍스트 추출 후 통계 계산
            # 비동기 함수를 동기적으로 호출하기 위해 별도 처리 필요
            # 실제 구현시에는 async/await 패턴을 맞춰야 함
            
            if file_path.suffix.lower() == '.pdf':
                metadata['structure_analysis']['page_count'] = self._get_pdf_page_count(file_path)
            elif file_path.suffix.lower() in ['.docx', '.doc']:
                metadata['structure_analysis']['paragraph_count'] = self._get_word_paragraph_count(file_path)
            
            return metadata
        
        except Exception as e:
            logger.error(f"메타데이터 추출 중 오류: {e}")
            return metadata
    
    def _get_pdf_page_count(self, file_path: Path) -> int:
        """PDF 페이지 수를 반환합니다."""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return len(pdf_reader.pages)
        except:
            return 0
    
    def _get_word_paragraph_count(self, file_path: Path) -> int:
        """Word 문서의 단락 수를 반환합니다."""
        try:
            doc = docx.Document(file_path)
            return len(doc.paragraphs)
        except:
            return 0
    
    def calculate_text_statistics(self, text: str) -> Dict:
        """텍스트 통계를 계산합니다."""
        try:
            words = text.split()
            sentences = re.split(r'[.!?]+', text)
            paragraphs = text.split('\n\n')
            
            return {
                'character_count': len(text),
                'word_count': len(words),
                'sentence_count': len([s for s in sentences if s.strip()]),
                'paragraph_count': len([p for p in paragraphs if p.strip()]),
                'average_words_per_sentence': len(words) / max(len(sentences), 1),
                'average_sentences_per_paragraph': len(sentences) / max(len(paragraphs), 1)
            }
        
        except Exception as e:
            logger.error(f"텍스트 통계 계산 중 오류: {e}")
            return {}
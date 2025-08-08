"""
PDF文本提取服务
实现PDF文件的文本提取、验证和预处理功能
"""

import PyPDF2
import pdfplumber
import re
import os
from typing import Optional, Dict, Any
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFParseError(Exception):
    """PDF解析异常"""
    pass


class PDFParser:
    """PDF文本提取器"""
    
    def __init__(self):
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.supported_extensions = ['.pdf']
    
    def validate_pdf_file(self, file_path: str) -> Dict[str, Any]:
        """
        验证PDF文件格式和完整性
        
        Args:
            file_path: PDF文件路径
            
        Returns:
            验证结果字典，包含is_valid, error_message, file_info
            
        Raises:
            PDFParseError: 当文件验证失败时
        """
        result = {
            'is_valid': False,
            'error_message': '',
            'file_info': {}
        }
        
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                result['error_message'] = '文件不存在'
                return result
            
            # 检查文件扩展名
            file_extension = Path(file_path).suffix.lower()
            if file_extension not in self.supported_extensions:
                result['error_message'] = f'不支持的文件格式: {file_extension}'
                return result
            
            # 检查文件大小
            file_size = os.path.getsize(file_path)
            if file_size > self.max_file_size:
                result['error_message'] = f'文件大小超过限制 ({file_size / 1024 / 1024:.1f}MB > 10MB)'
                return result
            
            # 尝试打开PDF文件验证完整性
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    
                    # 检查是否加密
                    if pdf_reader.is_encrypted:
                        result['error_message'] = 'PDF文件已加密，无法处理'
                        return result
                    
                    # 获取基本信息
                    num_pages = len(pdf_reader.pages)
                    if num_pages == 0:
                        result['error_message'] = 'PDF文件为空'
                        return result
                    
                    # 尝试读取第一页验证可读性
                    first_page = pdf_reader.pages[0]
                    first_page.extract_text()
                    
                    result['file_info'] = {
                        'file_size': file_size,
                        'num_pages': num_pages,
                        'file_name': Path(file_path).name
                    }
                    
            except Exception as e:
                result['error_message'] = f'PDF文件损坏或格式错误: {str(e)}'
                return result
            
            result['is_valid'] = True
            logger.info(f"PDF文件验证成功: {file_path}")
            return result
            
        except Exception as e:
            logger.error(f"PDF文件验证失败: {str(e)}")
            result['error_message'] = f'文件验证过程中发生错误: {str(e)}'
            return result
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """
        从PDF文件中提取文本内容
        
        Args:
            file_path: PDF文件路径
            
        Returns:
            提取的文本内容
            
        Raises:
            PDFParseError: 当文本提取失败时
        """
        # 首先验证文件
        validation_result = self.validate_pdf_file(file_path)
        if not validation_result['is_valid']:
            raise PDFParseError(validation_result['error_message'])
        
        extracted_text = ""
        
        try:
            # 方法1: 优先使用pdfplumber，处理复杂布局更好
            logger.info("尝试使用pdfplumber提取文本...")
            extracted_text = self._extract_with_pdfplumber(file_path)
            
            # 如果pdfplumber提取的文本太少，尝试PyPDF2
            if len(extracted_text.strip()) < 50:
                logger.info("pdfplumber提取文本较少，尝试使用PyPDF2...")
                pypdf2_text = self._extract_with_pypdf2(file_path)
                if len(pypdf2_text.strip()) > len(extracted_text.strip()):
                    extracted_text = pypdf2_text
            
        except Exception as e:
            logger.error(f"PDF文本提取失败: {str(e)}")
            raise PDFParseError(f"无法提取PDF文本内容: {str(e)}")
        
        if not extracted_text.strip():
            raise PDFParseError("PDF文件中未找到可提取的文本内容")
        
        # 清理和预处理文本
        cleaned_text = self.clean_and_preprocess_text(extracted_text)
        
        logger.info(f"成功提取PDF文本，长度: {len(cleaned_text)} 字符")
        return cleaned_text
    
    def _extract_with_pdfplumber(self, file_path: str) -> str:
        """使用pdfplumber提取文本"""
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- 第{page_num + 1}页 ---\n"
                        text += page_text + "\n"
                except Exception as e:
                    logger.warning(f"第{page_num + 1}页文本提取失败: {str(e)}")
                    continue
        return text
    
    def _extract_with_pypdf2(self, file_path: str) -> str:
        """使用PyPDF2提取文本"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- 第{page_num + 1}页 ---\n"
                        text += page_text + "\n"
                except Exception as e:
                    logger.warning(f"第{page_num + 1}页文本提取失败: {str(e)}")
                    continue
        return text
    
    def clean_and_preprocess_text(self, raw_text: str) -> str:
        """
        清理和预处理提取的文本
        
        Args:
            raw_text: 原始提取的文本
            
        Returns:
            清理后的文本
        """
        if not raw_text:
            return ""
        
        # 移除页面分隔符
        text = re.sub(r'--- 第\d+页 ---\n?', '', raw_text)
        
        # 统一换行符
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # 移除多余的空白字符
        text = re.sub(r'\n\s*\n', '\n\n', text)  # 多个连续换行变为两个
        text = re.sub(r'[ \t]+', ' ', text)      # 多个空格/制表符变为一个空格
        
        # 移除行首行尾空白
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        # 移除开头和结尾的空白
        text = text.strip()
        
        # 修复常见的PDF提取问题
        text = self._fix_common_pdf_issues(text)
        
        return text
    
    def _fix_common_pdf_issues(self, text: str) -> str:
        """修复PDF提取中的常见问题"""
        
        # 修复被分割的单词（英文）
        text = re.sub(r'([a-z])-\s*\n\s*([a-z])', r'\1\2', text)
        
        # 修复电子邮件地址被分割的问题
        text = re.sub(r'([a-zA-Z0-9._%-]+)\s+([a-zA-Z0-9._%-]+)\s*@\s*([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', r'\1\2@\3', text)
        text = re.sub(r'([a-zA-Z0-9._%-]+)\s*@\s*([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', r'\1@\2', text)
        
        # 修复电话号码格式
        text = re.sub(r'(\d{3})\s*-\s*(\d{4})\s*-\s*(\d{4})', r'\1-\2-\3', text)
        text = re.sub(r'(\d{3})\s+(\d{4})\s+(\d{4})', r'\1-\2-\3', text)
        
        # 修复日期格式
        text = re.sub(r'(\d{4})\s*/\s*(\d{1,2})\s*/\s*(\d{1,2})', r'\1/\2/\3', text)
        text = re.sub(r'(\d{4})\s*-\s*(\d{1,2})\s*-\s*(\d{1,2})', r'\1-\2-\3', text)
        
        return text
    
    def get_text_statistics(self, text: str) -> Dict[str, Any]:
        """
        获取文本统计信息
        
        Args:
            text: 文本内容
            
        Returns:
            统计信息字典
        """
        if not text:
            return {
                'char_count': 0,
                'word_count': 0,
                'line_count': 0,
                'has_email': False,
                'has_phone': False,
                'estimated_sections': 0
            }
        
        # 基本统计
        char_count = len(text)
        word_count = len(text.split())
        line_count = len([line for line in text.split('\n') if line.strip()])
        
        # 检查是否包含关键信息
        has_email = bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text))
        has_phone = bool(re.search(r'(\d{3}[-.\s]?\d{3,4}[-.\s]?\d{4})', text))
        
        # 估算简历章节数量（基于常见标题关键词）
        section_keywords = [
            '个人信息', '基本信息', '联系方式',
            '工作经历', '工作经验', '职业经历',
            '教育背景', '教育经历', '学历',
            '技能', '专业技能', '技术技能',
            '项目经验', '项目经历',
            '自我评价', '个人简介'
        ]
        
        estimated_sections = 0
        for keyword in section_keywords:
            if keyword in text:
                estimated_sections += 1
        
        return {
            'char_count': char_count,
            'word_count': word_count,
            'line_count': line_count,
            'has_email': has_email,
            'has_phone': has_phone,
            'estimated_sections': estimated_sections
        }


# 创建全局实例
pdf_parser = PDFParser()
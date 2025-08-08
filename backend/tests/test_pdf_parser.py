"""
PDF解析器测试
"""

import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

from backend.services.pdf_parser import PDFParser, PDFParseError


class TestPDFParser:
    """PDF解析器测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.parser = PDFParser()
    
    def test_init(self):
        """测试初始化"""
        assert self.parser.max_file_size == 10 * 1024 * 1024
        assert self.parser.supported_extensions == ['.pdf']
    
    def test_validate_pdf_file_not_exists(self):
        """测试文件不存在的情况"""
        result = self.parser.validate_pdf_file("nonexistent.pdf")
        assert not result['is_valid']
        assert "文件不存在" in result['error_message']
    
    def test_validate_pdf_file_wrong_extension(self):
        """测试错误文件扩展名"""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp_file:
            tmp_file.write(b"test content")
            tmp_file.flush()
            tmp_file.close()  # 关闭文件句柄
            
            try:
                result = self.parser.validate_pdf_file(tmp_file.name)
                assert not result['is_valid']
                assert "不支持的文件格式" in result['error_message']
            finally:
                try:
                    os.unlink(tmp_file.name)
                except PermissionError:
                    pass  # 忽略Windows文件权限问题
    
    def test_validate_pdf_file_too_large(self):
        """测试文件过大的情况"""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            # 创建一个超过10MB的文件
            large_content = b'x' * (11 * 1024 * 1024)
            tmp_file.write(large_content)
            tmp_file.flush()
            tmp_file.close()  # 关闭文件句柄
            
            try:
                result = self.parser.validate_pdf_file(tmp_file.name)
                assert not result['is_valid']
                assert "文件大小超过限制" in result['error_message']
            finally:
                try:
                    os.unlink(tmp_file.name)
                except PermissionError:
                    pass  # 忽略Windows文件权限问题
    
    @patch('PyPDF2.PdfReader')
    def test_validate_pdf_file_encrypted(self, mock_pdf_reader):
        """测试加密PDF文件"""
        # 模拟加密的PDF
        mock_reader_instance = MagicMock()
        mock_reader_instance.is_encrypted = True
        mock_pdf_reader.return_value = mock_reader_instance
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            tmp_file.write(b"fake pdf content")
            tmp_file.flush()
            tmp_file.close()  # 关闭文件句柄
            
            try:
                result = self.parser.validate_pdf_file(tmp_file.name)
                assert not result['is_valid']
                assert "PDF文件已加密" in result['error_message']
            finally:
                try:
                    os.unlink(tmp_file.name)
                except PermissionError:
                    pass  # 忽略Windows文件权限问题
    
    @patch('PyPDF2.PdfReader')
    def test_validate_pdf_file_empty(self, mock_pdf_reader):
        """测试空PDF文件"""
        # 模拟空的PDF
        mock_reader_instance = MagicMock()
        mock_reader_instance.is_encrypted = False
        mock_reader_instance.pages = []
        mock_pdf_reader.return_value = mock_reader_instance
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            tmp_file.write(b"fake pdf content")
            tmp_file.flush()
            tmp_file.close()  # 关闭文件句柄
            
            try:
                result = self.parser.validate_pdf_file(tmp_file.name)
                assert not result['is_valid']
                assert "PDF文件为空" in result['error_message']
            finally:
                try:
                    os.unlink(tmp_file.name)
                except PermissionError:
                    pass  # 忽略Windows文件权限问题
    
    @patch('PyPDF2.PdfReader')
    def test_validate_pdf_file_success(self, mock_pdf_reader):
        """测试成功验证PDF文件"""
        # 模拟正常的PDF
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "test content"
        
        mock_reader_instance = MagicMock()
        mock_reader_instance.is_encrypted = False
        mock_reader_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_reader_instance
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            tmp_file.write(b"fake pdf content")
            tmp_file.flush()
            tmp_file.close()  # 关闭文件句柄
            
            try:
                result = self.parser.validate_pdf_file(tmp_file.name)
                assert result['is_valid']
                assert result['file_info']['num_pages'] == 1
                assert result['file_info']['file_size'] > 0
            finally:
                try:
                    os.unlink(tmp_file.name)
                except PermissionError:
                    pass  # 忽略Windows文件权限问题
    
    def test_clean_and_preprocess_text_empty(self):
        """测试清理空文本"""
        result = self.parser.clean_and_preprocess_text("")
        assert result == ""
        
        result = self.parser.clean_and_preprocess_text(None)
        assert result == ""
    
    def test_clean_and_preprocess_text_basic(self):
        """测试基本文本清理"""
        raw_text = """
        
        
        姓名：张三
        
        
        电话：138-1234-5678
        
        
        邮箱：zhangsan@example.com
        
        
        """
        
        result = self.parser.clean_and_preprocess_text(raw_text)
        
        # 检查多余空行被移除
        assert result.count('\n\n') <= 2
        # 检查内容保持完整
        assert "张三" in result
        assert "138-1234-5678" in result
        assert "zhangsan@example.com" in result
    
    def test_clean_and_preprocess_text_page_separators(self):
        """测试页面分隔符移除"""
        raw_text = """
        姓名：张三
        --- 第1页 ---
        电话：138-1234-5678
        --- 第2页 ---
        邮箱：zhangsan@example.com
        """
        
        result = self.parser.clean_and_preprocess_text(raw_text)
        
        # 检查页面分隔符被移除
        assert "--- 第1页 ---" not in result
        assert "--- 第2页 ---" not in result
        # 检查内容保持完整
        assert "张三" in result
        assert "138-1234-5678" in result
        assert "zhangsan@example.com" in result
    
    def test_fix_common_pdf_issues_email(self):
        """测试修复邮箱地址分割问题"""
        text_with_broken_email = "联系邮箱：zhang san @ example.com"
        result = self.parser._fix_common_pdf_issues(text_with_broken_email)
        assert "zhangsan@example.com" in result
    
    def test_fix_common_pdf_issues_phone(self):
        """测试修复电话号码格式"""
        text_with_broken_phone = "电话：138 1234 5678"
        result = self.parser._fix_common_pdf_issues(text_with_broken_phone)
        assert "138-1234-5678" in result
    
    def test_fix_common_pdf_issues_date(self):
        """测试修复日期格式"""
        text_with_broken_date = "入职时间：2020 / 01 / 15"
        result = self.parser._fix_common_pdf_issues(text_with_broken_date)
        assert "2020/01/15" in result or "2020/1/15" in result
    
    def test_get_text_statistics_empty(self):
        """测试空文本统计"""
        stats = self.parser.get_text_statistics("")
        assert stats['char_count'] == 0
        assert stats['word_count'] == 0
        assert stats['line_count'] == 0
        assert not stats['has_email']
        assert not stats['has_phone']
        assert stats['estimated_sections'] == 0
    
    def test_get_text_statistics_with_content(self):
        """测试有内容的文本统计"""
        text = """
        姓名：张三
        电话：138-1234-5678
        邮箱：zhangsan@example.com
        
        工作经历：
        2020-2023 ABC公司 软件工程师
        
        教育背景：
        2016-2020 清华大学 计算机科学与技术
        
        技能：
        Python, Java, JavaScript
        """
        
        stats = self.parser.get_text_statistics(text)
        
        assert stats['char_count'] > 0
        assert stats['word_count'] > 0
        assert stats['line_count'] > 0
        assert stats['has_email']
        assert stats['has_phone']
        assert stats['estimated_sections'] >= 3  # 工作经历、教育背景、技能
    
    @patch('backend.services.pdf_parser.PDFParser.validate_pdf_file')
    def test_extract_text_from_pdf_validation_failed(self, mock_validate):
        """测试文件验证失败时的异常"""
        mock_validate.return_value = {
            'is_valid': False,
            'error_message': '文件格式错误'
        }
        
        with pytest.raises(PDFParseError) as exc_info:
            self.parser.extract_text_from_pdf("test.pdf")
        
        assert "文件格式错误" in str(exc_info.value)
    
    @patch('backend.services.pdf_parser.PDFParser._extract_with_pypdf2')
    @patch('pdfplumber.open')
    @patch('backend.services.pdf_parser.PDFParser.validate_pdf_file')
    def test_extract_text_from_pdf_success(self, mock_validate, mock_pdfplumber, mock_pypdf2):
        """测试成功提取PDF文本"""
        # 模拟验证成功
        mock_validate.return_value = {
            'is_valid': True,
            'error_message': '',
            'file_info': {'num_pages': 1}
        }
        
        # 模拟pdfplumber提取文本
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "这是测试简历内容\n姓名：张三\n电话：138-1234-5678"
        
        mock_pdf = MagicMock()
        mock_pdf.pages = [mock_page]
        mock_pdf.__enter__.return_value = mock_pdf
        mock_pdfplumber.return_value = mock_pdf
        
        # 模拟PyPDF2备用方案
        mock_pypdf2.return_value = "备用文本内容"
        
        result = self.parser.extract_text_from_pdf("test.pdf")
        
        assert "张三" in result
        assert "138-1234-5678" in result
        assert len(result.strip()) > 0
    
    @patch('pdfplumber.open')
    @patch('backend.services.pdf_parser.PDFParser.validate_pdf_file')
    def test_extract_text_from_pdf_empty_result(self, mock_validate, mock_pdfplumber):
        """测试提取到空文本时的异常"""
        # 模拟验证成功
        mock_validate.return_value = {
            'is_valid': True,
            'error_message': '',
            'file_info': {'num_pages': 1}
        }
        
        # 模拟pdfplumber提取空文本
        mock_page = MagicMock()
        mock_page.extract_text.return_value = ""
        
        mock_pdf = MagicMock()
        mock_pdf.pages = [mock_page]
        mock_pdf.__enter__.return_value = mock_pdf
        mock_pdfplumber.return_value = mock_pdf
        
        # 模拟PyPDF2也提取空文本
        with patch('builtins.open', mock_open(read_data=b"fake pdf")):
            with patch('PyPDF2.PdfReader') as mock_pypdf2:
                mock_pypdf2_page = MagicMock()
                mock_pypdf2_page.extract_text.return_value = ""
                mock_pypdf2_reader = MagicMock()
                mock_pypdf2_reader.pages = [mock_pypdf2_page]
                mock_pypdf2.return_value = mock_pypdf2_reader
                
                with pytest.raises(PDFParseError) as exc_info:
                    self.parser.extract_text_from_pdf("test.pdf")
                
                assert "未找到可提取的文本内容" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__])
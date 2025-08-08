"""
PDF解析器演示脚本
展示如何使用PDF解析功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.pdf_parser import PDFParser, PDFParseError


def demo_pdf_parser():
    """演示PDF解析器功能"""
    parser = PDFParser()
    
    print("=== PDF解析器演示 ===\n")
    
    # 演示文件验证功能
    print("1. 文件验证功能演示:")
    
    # 测试不存在的文件
    print("\n测试不存在的文件:")
    result = parser.validate_pdf_file("nonexistent.pdf")
    print(f"验证结果: {result}")
    
    # 演示文本清理功能
    print("\n2. 文本清理功能演示:")
    
    raw_text = """
    
    
    姓名：张三
    --- 第1页 ---
    电话：138 1234 5678
    --- 第2页 ---
    邮箱：zhang san @ example.com
    
    工作经历：
    2020 / 01 / 15 - 2023 / 12 / 31
    ABC公司 软件工程师
    
    
    """
    
    print("原始文本:")
    print(repr(raw_text))
    
    cleaned_text = parser.clean_and_preprocess_text(raw_text)
    print("\n清理后的文本:")
    print(repr(cleaned_text))
    
    # 演示文本统计功能
    print("\n3. 文本统计功能演示:")
    stats = parser.get_text_statistics(cleaned_text)
    print(f"文本统计: {stats}")
    
    # 演示常见问题修复
    print("\n4. 常见问题修复演示:")
    
    problematic_text = """
    联系方式：
    电话：138 1234 5678
    邮箱：zhang san @ example.com
    入职时间：2020 / 01 / 15
    """
    
    print("问题文本:")
    print(problematic_text)
    
    fixed_text = parser._fix_common_pdf_issues(problematic_text)
    print("\n修复后的文本:")
    print(fixed_text)
    
    print("\n=== 演示完成 ===")


if __name__ == "__main__":
    demo_pdf_parser()
"""
测试真实PDF文件的读取逻辑
"""

import sys
import os
# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from backend.services.pdf_parser import PDFParser, PDFParseError


def test_real_pdf():
    """测试真实PDF文件"""
    parser = PDFParser()
    
    # PDF文件路径
    pdf_path = "D:\面试\简历\java开发工程师_陈俊杰.pdf"
    
    print("=== 测试真实PDF文件读取 ===\n")
    print(f"PDF文件路径: {pdf_path}")
    
    try:
        # 1. 验证PDF文件
        print("\n1. 验证PDF文件...")
        validation_result = parser.validate_pdf_file(pdf_path)
        
        if validation_result['is_valid']:
            print("✓ PDF文件验证成功")
            print(f"文件信息: {validation_result['file_info']}")
        else:
            print("✗ PDF文件验证失败")
            print(f"错误信息: {validation_result['error_message']}")
            return
        
        # 2. 提取PDF文本
        print("\n2. 提取PDF文本...")
        extracted_text = parser.extract_text_from_pdf(pdf_path)
        
        print("✓ PDF文本提取成功")
        print(f"提取文本长度: {len(extracted_text)} 字符")
        
        # 3. 显示提取的文本内容（前500字符）
        print("\n3. 提取的文本内容预览:")
        print("-" * 50)
        print(extracted_text[:500])
        if len(extracted_text) > 500:
            print("...")
            print(f"（还有 {len(extracted_text) - 500} 个字符）")
        print("-" * 50)
        
        # 4. 获取文本统计信息
        print("\n4. 文本统计信息:")
        stats = parser.get_text_statistics(extracted_text)
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # 5. 保存提取的文本到文件
        output_file = "extracted_resume_text.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        print(f"\n5. 提取的文本已保存到: {output_file}")
        
        print("\n=== 测试完成 ===")
        
    except PDFParseError as e:
        print(f"✗ PDF解析错误: {e}")
    except FileNotFoundError:
        print(f"✗ 文件未找到: {pdf_path}")
        print("请确认文件路径是否正确")
    except Exception as e:
        print(f"✗ 未知错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_real_pdf()
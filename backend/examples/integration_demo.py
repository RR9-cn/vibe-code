#!/usr/bin/env python3
"""
PDF解析和AI解析集成演示
展示从PDF文件到结构化数据的完整流程
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.pdf_parser import PDFParser, PDFParseError
from services.qwen_parser import QwenResumeParser, QwenParseError


def demo_full_pipeline():
    """演示完整的PDF到结构化数据的处理流程"""
    print("=== PDF + AI 解析完整流程演示 ===\n")
    
    # 检查API密钥
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("❌ 错误：未设置DASHSCOPE_API_KEY环境变量")
        print("请在.env文件中设置您的通义千问API密钥")
        return
    
    # 查找示例PDF文件
    pdf_files = list(project_root.glob("examples/*.pdf"))
    if not pdf_files:
        print("⚠️ 未找到示例PDF文件")
        print("请将PDF简历文件放在backend/examples/目录下")
        return
    
    pdf_file = pdf_files[0]
    print(f"📄 使用PDF文件: {pdf_file.name}")
    
    try:
        # 步骤1：PDF文本提取
        print("\n🔍 步骤1：提取PDF文本...")
        pdf_parser = PDFParser()
        
        # 验证PDF文件
        validation_result = pdf_parser.validate_pdf(str(pdf_file))
        print(f"PDF验证结果: {'✅ 通过' if validation_result['is_valid'] else '❌ 失败'}")
        
        if not validation_result['is_valid']:
            print("错误信息:")
            for error in validation_result['errors']:
                print(f"  - {error}")
            return
        
        # 提取文本
        extracted_text = pdf_parser.extract_text(str(pdf_file))
        print(f"提取文本长度: {len(extracted_text)} 字符")
        print(f"文本预览: {extracted_text[:200]}...")
        
        # 步骤2：AI解析
        print("\n🤖 步骤2：AI解析简历内容...")
        qwen_parser = QwenResumeParser()
        
        resume_data = qwen_parser.parse_resume_text(extracted_text)
        print("✅ AI解析完成！")
        
        # 步骤3：显示结果
        print("\n📊 步骤3：解析结果展示")
        print(f"简历ID: {resume_data.id}")
        
        print("\n个人信息:")
        print(f"  姓名: {resume_data.personal_info.name}")
        print(f"  邮箱: {resume_data.personal_info.email}")
        print(f"  电话: {resume_data.personal_info.phone}")
        
        print(f"\n工作经历: {len(resume_data.work_experience)}项")
        for exp in resume_data.work_experience:
            print(f"  - {exp.company}: {exp.position}")
        
        print(f"\n教育背景: {len(resume_data.education)}项")
        for edu in resume_data.education:
            print(f"  - {edu.institution}: {edu.degree}")
        
        print(f"\n技能: {len(resume_data.skills)}项")
        for skill in resume_data.skills:
            print(f"  - {skill.name} ({skill.category})")
        
        # 步骤4：质量验证
        print("\n✅ 步骤4：质量验证")
        validation = qwen_parser.validate_parsed_data(resume_data)
        print(f"验证状态: {'通过' if validation['is_valid'] else '失败'}")
        print(f"完整性评分: {validation['completeness_score']:.2%}")
        
        if validation['warnings']:
            print("警告:")
            for warning in validation['warnings']:
                print(f"  - {warning}")
        
        # 保存结果
        import json
        output_file = project_root / "examples" / f"parsed_{pdf_file.stem}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(resume_data.model_dump(), f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 结果已保存到: {output_file}")
        
    except PDFParseError as e:
        print(f"❌ PDF解析失败: {e}")
    except QwenParseError as e:
        print(f"❌ AI解析失败: {e}")
    except Exception as e:
        print(f"❌ 发生未知错误: {e}")


def demo_batch_processing():
    """演示批量处理多个PDF文件"""
    print("\n=== 批量处理演示 ===\n")
    
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("⚠️ 跳过批量处理演示（需要API密钥）")
        return
    
    pdf_files = list(project_root.glob("examples/*.pdf"))
    if len(pdf_files) < 2:
        print("⚠️ 需要至少2个PDF文件进行批量处理演示")
        return
    
    print(f"📁 找到 {len(pdf_files)} 个PDF文件")
    
    pdf_parser = PDFParser()
    qwen_parser = QwenResumeParser()
    
    results = []
    
    for i, pdf_file in enumerate(pdf_files[:3], 1):  # 限制处理前3个文件
        print(f"\n处理文件 {i}/{min(3, len(pdf_files))}: {pdf_file.name}")
        
        try:
            # 提取文本
            text = pdf_parser.extract_text(str(pdf_file))
            print(f"  文本长度: {len(text)} 字符")
            
            # AI解析
            resume_data = qwen_parser.parse_resume_text(text)
            
            # 验证质量
            validation = qwen_parser.validate_parsed_data(resume_data)
            
            results.append({
                'file': pdf_file.name,
                'name': resume_data.personal_info.name,
                'completeness': validation['completeness_score'],
                'valid': validation['is_valid']
            })
            
            print(f"  ✅ 成功 - {resume_data.personal_info.name} ({validation['completeness_score']:.1%})")
            
        except Exception as e:
            print(f"  ❌ 失败 - {e}")
            results.append({
                'file': pdf_file.name,
                'error': str(e)
            })
    
    # 汇总结果
    print("\n📈 批量处理结果汇总:")
    successful = [r for r in results if 'error' not in r]
    failed = [r for r in results if 'error' in r]
    
    print(f"成功: {len(successful)}/{len(results)}")
    print(f"失败: {len(failed)}/{len(results)}")
    
    if successful:
        avg_completeness = sum(r['completeness'] for r in successful) / len(successful)
        print(f"平均完整性: {avg_completeness:.1%}")


if __name__ == "__main__":
    # 加载环境变量
    from dotenv import load_dotenv
    load_dotenv()
    
    demo_full_pipeline()
    demo_batch_processing()
    
    print("\n=== 集成演示完成 ===")
    print("💡 提示：")
    print("1. 将PDF简历文件放在backend/examples/目录下进行测试")
    print("2. 确保PDF文件是文本格式，而不是扫描图片")
    print("3. 检查生成的JSON文件了解详细解析结果")
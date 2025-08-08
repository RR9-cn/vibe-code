#!/usr/bin/env python3
"""
通义千问解析器演示脚本
展示如何使用QwenResumeParser解析简历文本
"""

import os
import sys
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.qwen_parser import QwenResumeParser, QwenParseError


def demo_parse_resume():
    """演示简历解析功能"""
    print("=== 通义千问简历解析器演示 ===\n")
    
    # 检查API密钥
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("❌ 错误：未设置DASHSCOPE_API_KEY环境变量")
        print("请在.env文件中设置您的通义千问API密钥")
        return
    
    # 示例简历文本
    sample_resume_text = """
    张三
    软件工程师
    电话：138-1234-5678
    邮箱：zhangsan@example.com
    地址：北京市朝阳区
    
    个人简介：
    资深软件工程师，具有5年以上的全栈开发经验，熟悉多种编程语言和框架。
    
    工作经历：
    2020年1月 - 2023年12月  ABC科技有限公司  高级软件工程师
    • 负责公司核心产品的后端开发和架构设计
    • 带领5人团队完成多个重要项目
    • 使用Java、Spring Boot、MySQL等技术栈
    
    2018年6月 - 2019年12月  XYZ互联网公司  软件工程师
    • 参与电商平台的开发和维护
    • 负责用户管理模块的设计和实现
    • 使用Python、Django、Redis等技术
    
    教育背景：
    2014年9月 - 2018年6月  清华大学  计算机科学与技术  本科
    GPA: 3.8/4.0
    
    技能：
    编程语言：Java（精通）、Python（熟练）、JavaScript（熟练）
    框架：Spring Boot、Django、Vue.js
    数据库：MySQL、Redis、MongoDB
    工具：Git、Docker、Jenkins
    软技能：团队协作、项目管理、沟通能力
    """
    
    try:
        # 创建解析器实例
        print("🚀 初始化通义千问解析器...")
        parser = QwenResumeParser()
        
        # 解析简历文本
        print("📄 开始解析简历文本...")
        print(f"简历文本长度：{len(sample_resume_text)} 字符\n")
        
        resume_data = parser.parse_resume_text(sample_resume_text)
        
        print("✅ 简历解析成功！\n")
        
        # 显示解析结果
        print("=== 解析结果 ===")
        print(f"简历ID: {resume_data.id}")
        print(f"创建时间: {resume_data.created_at}")
        
        print("\n📋 个人信息:")
        print(f"  姓名: {resume_data.personal_info.name}")
        print(f"  邮箱: {resume_data.personal_info.email}")
        print(f"  电话: {resume_data.personal_info.phone}")
        print(f"  地址: {resume_data.personal_info.location}")
        print(f"  简介: {resume_data.personal_info.summary}")
        
        print(f"\n💼 工作经历 ({len(resume_data.work_experience)}项):")
        for i, exp in enumerate(resume_data.work_experience, 1):
            print(f"  {i}. {exp.company} - {exp.position}")
            print(f"     时间: {exp.start_date} 至 {exp.end_date or '至今'}")
            print(f"     描述: {len(exp.description)}条工作内容")
            if exp.technologies:
                print(f"     技术: {', '.join(exp.technologies)}")
        
        print(f"\n🎓 教育背景 ({len(resume_data.education)}项):")
        for i, edu in enumerate(resume_data.education, 1):
            print(f"  {i}. {edu.institution} - {edu.degree}")
            print(f"     专业: {edu.major}")
            print(f"     时间: {edu.start_date} 至 {edu.end_date}")
            if edu.gpa:
                print(f"     GPA: {edu.gpa}")
        
        print(f"\n🛠️ 技能列表 ({len(resume_data.skills)}项):")
        skill_categories = {}
        for skill in resume_data.skills:
            if skill.category not in skill_categories:
                skill_categories[skill.category] = []
            skill_categories[skill.category].append(skill)
        
        for category, skills in skill_categories.items():
            category_name = {
                'technical': '技术技能',
                'soft': '软技能',
                'language': '语言技能'
            }.get(category, category)
            print(f"  {category_name}:")
            for skill in skills:
                level_text = f"({skill.level})" if skill.level else ""
                print(f"    - {skill.name} {level_text}")
        
        # 验证解析质量
        print("\n=== 解析质量验证 ===")
        validation_result = parser.validate_parsed_data(resume_data)
        
        print(f"验证状态: {'✅ 通过' if validation_result['is_valid'] else '❌ 失败'}")
        print(f"完整性评分: {validation_result['completeness_score']:.2%}")
        
        if validation_result['errors']:
            print("❌ 错误:")
            for error in validation_result['errors']:
                print(f"  - {error}")
        
        if validation_result['warnings']:
            print("⚠️ 警告:")
            for warning in validation_result['warnings']:
                print(f"  - {warning}")
        
        # 导出JSON格式
        print("\n=== JSON格式导出 ===")
        json_data = resume_data.model_dump()
        json_str = json.dumps(json_data, ensure_ascii=False, indent=2)
        
        output_file = project_root / "examples" / "parsed_resume_output.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json_str)
        
        print(f"✅ 解析结果已保存到: {output_file}")
        print(f"JSON数据大小: {len(json_str)} 字符")
        
    except QwenParseError as e:
        print(f"❌ 解析失败: {e}")
    except Exception as e:
        print(f"❌ 发生未知错误: {e}")


def demo_error_handling():
    """演示错误处理功能"""
    print("\n=== 错误处理演示 ===\n")
    
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("⚠️ 跳过错误处理演示（需要API密钥）")
        return
    
    parser = QwenResumeParser()
    
    # 测试空文本
    print("1. 测试空文本处理:")
    try:
        parser.parse_resume_text("")
    except QwenParseError as e:
        print(f"   ✅ 正确捕获错误: {e}")
    
    # 测试无效文本
    print("\n2. 测试无效文本处理:")
    try:
        result = parser.parse_resume_text("这不是一份简历，只是随机文本。")
        print(f"   ⚠️ 解析完成，但可能质量较低")
        validation = parser.validate_parsed_data(result)
        print(f"   完整性评分: {validation['completeness_score']:.2%}")
    except QwenParseError as e:
        print(f"   ✅ 正确捕获错误: {e}")


if __name__ == "__main__":
    # 加载环境变量
    from dotenv import load_dotenv
    load_dotenv()
    
    demo_parse_resume()
    demo_error_handling()
    
    print("\n=== 演示完成 ===")
    print("💡 提示：")
    print("1. 确保在.env文件中设置了DASHSCOPE_API_KEY")
    print("2. 可以修改sample_resume_text来测试不同的简历格式")
    print("3. 查看生成的JSON文件了解详细的解析结果")
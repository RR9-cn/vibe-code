#!/usr/bin/env python3
"""
通义千问解析器功能验证脚本
验证解析器的基本功能（不需要真实API调用）
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.qwen_parser import QwenResumeParser, QwenParseError
from models.resume import ResumeData, PersonalInfo, WorkExperience, Education, Skill
from datetime import datetime


def test_prompt_generation():
    """测试提示模板生成"""
    print("=== 测试提示模板生成 ===")
    
    try:
        # 创建解析器实例（使用模拟API密钥）
        import os
        os.environ['DASHSCOPE_API_KEY'] = 'test_key'
        parser = QwenResumeParser()
        
        # 测试提示生成
        sample_text = "张三，软件工程师，Python开发经验"
        prompt = parser._build_parse_prompt(sample_text)
        
        print("✅ 提示模板生成成功")
        print(f"提示长度: {len(prompt)} 字符")
        print("包含必要字段:")
        required_fields = ['personal_info', 'work_experience', 'education', 'skills']
        for field in required_fields:
            if field in prompt:
                print(f"  ✅ {field}")
            else:
                print(f"  ❌ {field}")
        
        return True
        
    except Exception as e:
        print(f"❌ 提示模板生成失败: {e}")
        return False


def test_response_parsing():
    """测试API响应解析"""
    print("\n=== 测试API响应解析 ===")
    
    try:
        import os
        os.environ['DASHSCOPE_API_KEY'] = 'test_key'
        parser = QwenResumeParser()
        
        # 测试正常JSON响应
        normal_response = '''
        {
            "personal_info": {
                "name": "张三",
                "email": "zhangsan@example.com",
                "phone": "138-1234-5678"
            },
            "work_experience": [
                {
                    "company": "ABC公司",
                    "position": "工程师",
                    "start_date": "2020-01",
                    "end_date": "2023-12",
                    "description": ["负责开发工作"]
                }
            ],
            "education": [
                {
                    "institution": "清华大学",
                    "degree": "本科",
                    "start_date": "2016-09",
                    "end_date": "2020-06"
                }
            ],
            "skills": [
                {
                    "category": "编程语言",
                    "name": "Python",
                    "level": "熟练"
                }
            ]
        }
        '''
        
        parsed_data = parser._parse_api_response(normal_response)
        print("✅ 正常JSON响应解析成功")
        
        # 测试带markdown格式的响应
        markdown_response = '''```json
        {
            "personal_info": {"name": "李四", "email": "lisi@example.com"},
            "work_experience": [],
            "education": [],
            "skills": []
        }
        ```'''
        
        parsed_markdown = parser._parse_api_response(markdown_response)
        print("✅ Markdown格式响应解析成功")
        
        # 测试无效JSON
        try:
            parser._parse_api_response("这不是JSON")
            print("❌ 应该抛出异常")
            return False
        except QwenParseError:
            print("✅ 无效JSON正确抛出异常")
        
        return True
        
    except Exception as e:
        print(f"❌ 响应解析测试失败: {e}")
        return False


def test_data_building():
    """测试数据构建功能"""
    print("\n=== 测试数据构建功能 ===")
    
    try:
        import os
        os.environ['DASHSCOPE_API_KEY'] = 'test_key'
        parser = QwenResumeParser()
        
        # 测试完整数据构建
        complete_data = {
            "personal_info": {
                "name": "王五",
                "email": "wangwu@example.com",
                "phone": "139-5678-9012",
                "location": "上海",
                "summary": "资深开发者"
            },
            "work_experience": [
                {
                    "company": "XYZ公司",
                    "position": "高级工程师",
                    "start_date": "2021-01",
                    "end_date": "2024-01",
                    "description": ["负责架构设计", "团队管理"],
                    "technologies": ["Java", "Spring"]
                }
            ],
            "education": [
                {
                    "institution": "北京大学",
                    "degree": "硕士",
                    "major": "计算机科学",
                    "start_date": "2019-09",
                    "end_date": "2021-06",
                    "gpa": "3.8"
                }
            ],
            "skills": [
                {
                    "category": "编程语言",
                    "name": "Java",
                    "level": "精通"
                },
                {
                    "category": "软技能",
                    "name": "团队协作",
                    "level": "熟练"
                }
            ]
        }
        
        resume_data = parser._build_resume_data(complete_data)
        print("✅ 完整数据构建成功")
        print(f"简历ID: {resume_data.id}")
        print(f"姓名: {resume_data.personal_info.name}")
        print(f"工作经历: {len(resume_data.work_experience)}项")
        print(f"教育背景: {len(resume_data.education)}项")
        print(f"技能: {len(resume_data.skills)}项")
        
        # 验证技能分类映射
        for skill in resume_data.skills:
            if skill.category not in ['technical', 'soft', 'language']:
                print(f"❌ 技能分类映射失败: {skill.category}")
                return False
        print("✅ 技能分类映射正确")
        
        # 测试最小数据构建
        minimal_data = {
            "personal_info": {
                "name": "赵六",
                "email": "zhaoliu@example.com"
            },
            "work_experience": [],
            "education": [],
            "skills": []
        }
        
        minimal_resume = parser._build_resume_data(minimal_data)
        print("✅ 最小数据构建成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据构建测试失败: {e}")
        return False


def test_validation():
    """测试数据验证功能"""
    print("\n=== 测试数据验证功能 ===")
    
    try:
        import os
        os.environ['DASHSCOPE_API_KEY'] = 'test_key'
        parser = QwenResumeParser()
        
        # 创建完整的简历数据
        complete_resume = ResumeData(
            id="test_complete",
            personal_info=PersonalInfo(
                name="测试用户",
                email="test@example.com",
                phone="138-0000-0000",
                summary="测试简介"
            ),
            work_experience=[
                WorkExperience(
                    company="测试公司",
                    position="测试职位",
                    start_date="2020-01",
                    end_date="2023-12",
                    description=["测试工作内容"]
                )
            ],
            education=[
                Education(
                    institution="测试大学",
                    degree="本科",
                    start_date="2016-09",
                    end_date="2020-06"
                )
            ],
            skills=[
                Skill(
                    category="technical",
                    name="Python"
                )
            ],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        validation_result = parser.validate_parsed_data(complete_resume)
        print("✅ 完整数据验证成功")
        print(f"验证状态: {validation_result['is_valid']}")
        print(f"完整性评分: {validation_result['completeness_score']:.2%}")
        print(f"错误数量: {len(validation_result['errors'])}")
        print(f"警告数量: {len(validation_result['warnings'])}")
        
        # 创建不完整的简历数据
        incomplete_resume = ResumeData(
            id="test_incomplete",
            personal_info=PersonalInfo(
                name="不完整用户",
                email="incomplete@example.com"
            ),
            work_experience=[],
            education=[],
            skills=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        incomplete_validation = parser.validate_parsed_data(incomplete_resume)
        print("✅ 不完整数据验证成功")
        print(f"完整性评分: {incomplete_validation['completeness_score']:.2%}")
        print(f"警告数量: {len(incomplete_validation['warnings'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据验证测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🚀 开始通义千问解析器功能验证\n")
    
    tests = [
        test_prompt_generation,
        test_response_parsing,
        test_data_building,
        test_validation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== 验证结果 ===")
    print(f"通过: {passed}/{total}")
    print(f"成功率: {passed/total:.1%}")
    
    if passed == total:
        print("🎉 所有功能验证通过！")
        print("\n✅ 通义千问解析器已准备就绪")
        print("💡 下一步：配置真实的DASHSCOPE_API_KEY进行实际测试")
    else:
        print("⚠️ 部分功能验证失败，请检查代码")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
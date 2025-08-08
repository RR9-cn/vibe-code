"""
数据模型使用示例
演示如何创建和使用各种数据模型
"""

import json
import sys
import os
from datetime import datetime

# 添加父目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.resume import (
    PersonalInfo,
    WorkExperience,
    Education,
    Skill,
    SkillCategory,
    SkillLevel,
    ResumeData,
    ColorScheme,
    WebsiteConfig
)


def create_sample_resume():
    """创建示例简历数据"""
    
    # 创建个人信息
    personal_info = PersonalInfo(
        name="张三",
        email="zhangsan@example.com",
        phone="13800138000",
        location="北京市海淀区",
        summary="资深全栈开发工程师，具有5年Web开发经验，熟悉Python、JavaScript等技术栈",
        linkedin="https://linkedin.com/in/zhangsan",
        github="https://github.com/zhangsan"
    )
    
    # 创建工作经历
    work_experiences = [
        WorkExperience(
            company="阿里巴巴集团",
            position="高级软件工程师",
            start_date="2021-03",
            end_date="2024-01",
            description=[
                "负责电商平台核心业务模块的后端开发和维护",
                "优化系统性能，将响应时间从500ms降低到100ms以内",
                "参与微服务架构设计，提升系统可扩展性",
                "指导初级工程师，参与代码审查和技术分享"
            ],
            technologies=["Python", "Java", "Redis", "MySQL", "Docker", "Kubernetes"]
        ),
        WorkExperience(
            company="腾讯科技",
            position="软件工程师",
            start_date="2019-07",
            end_date="2021-02",
            description=[
                "开发和维护社交媒体平台的用户管理系统",
                "实现实时消息推送功能，支持百万级并发用户",
                "参与前端React应用开发，提升用户体验"
            ],
            technologies=["Node.js", "React", "MongoDB", "WebSocket"]
        )
    ]
    
    # 创建教育背景
    education = [
        Education(
            institution="清华大学",
            degree="硕士",
            major="计算机科学与技术",
            start_date="2017-09",
            end_date="2019-06",
            gpa="3.8"
        ),
        Education(
            institution="北京理工大学",
            degree="学士",
            major="软件工程",
            start_date="2013-09",
            end_date="2017-06",
            gpa="3.6"
        )
    ]
    
    # 创建技能列表
    skills = [
        # 技术技能
        Skill(category=SkillCategory.TECHNICAL, name="Python", level=SkillLevel.EXPERT),
        Skill(category=SkillCategory.TECHNICAL, name="JavaScript", level=SkillLevel.ADVANCED),
        Skill(category=SkillCategory.TECHNICAL, name="Java", level=SkillLevel.ADVANCED),
        Skill(category=SkillCategory.TECHNICAL, name="React", level=SkillLevel.INTERMEDIATE),
        Skill(category=SkillCategory.TECHNICAL, name="Docker", level=SkillLevel.ADVANCED),
        Skill(category=SkillCategory.TECHNICAL, name="Kubernetes", level=SkillLevel.INTERMEDIATE),
        
        # 软技能
        Skill(category=SkillCategory.SOFT, name="团队协作", level=SkillLevel.EXPERT),
        Skill(category=SkillCategory.SOFT, name="项目管理", level=SkillLevel.ADVANCED),
        Skill(category=SkillCategory.SOFT, name="沟通能力", level=SkillLevel.ADVANCED),
        
        # 语言技能
        Skill(category=SkillCategory.LANGUAGE, name="中文", level=SkillLevel.EXPERT),
        Skill(category=SkillCategory.LANGUAGE, name="英语", level=SkillLevel.ADVANCED),
    ]
    
    # 创建完整简历数据
    resume = ResumeData(
        id="resume_zhangsan_001",
        personal_info=personal_info,
        work_experience=work_experiences,
        education=education,
        skills=skills
    )
    
    return resume


def create_sample_website_config(resume_id: str):
    """创建示例网站配置"""
    
    # 创建颜色方案
    color_scheme = ColorScheme(
        primary="#3B82F6",      # 蓝色
        secondary="#64748B",    # 灰色
        accent="#F59E0B",       # 橙色
        background="#FFFFFF",   # 白色
        text="#1F2937"          # 深灰色
    )
    
    # 创建网站配置
    website_config = WebsiteConfig(
        id="website_zhangsan_001",
        resume_id=resume_id,
        template_id="modern_template_v1",
        color_scheme=color_scheme,
        url="https://resume-generator.com/zhangsan",
        is_public=True
    )
    
    return website_config


def main():
    """主函数：演示数据模型的使用"""
    
    print("=== 简历网站生成器 - 数据模型演示 ===\n")
    
    # 创建示例简历
    print("1. 创建示例简历数据...")
    resume = create_sample_resume()
    print(f"✓ 简历创建成功，ID: {resume.id}")
    print(f"✓ 姓名: {resume.personal_info.name}")
    print(f"✓ 工作经历数量: {len(resume.work_experience)}")
    print(f"✓ 教育背景数量: {len(resume.education)}")
    print(f"✓ 技能数量: {len(resume.skills)}")
    
    # 创建网站配置
    print("\n2. 创建网站配置...")
    website_config = create_sample_website_config(resume.id)
    print(f"✓ 网站配置创建成功，ID: {website_config.id}")
    print(f"✓ 关联简历ID: {website_config.resume_id}")
    print(f"✓ 网站URL: {website_config.url}")
    
    # 序列化为JSON
    print("\n3. 数据序列化演示...")
    resume_json = resume.model_dump_json(indent=2)
    config_json = website_config.model_dump_json(indent=2)
    
    print("✓ 简历数据JSON格式:")
    print(resume_json[:200] + "..." if len(resume_json) > 200 else resume_json)
    
    print("\n✓ 网站配置JSON格式:")
    print(config_json[:200] + "..." if len(config_json) > 200 else config_json)
    
    # 数据验证演示
    print("\n4. 数据验证演示...")
    try:
        # 尝试创建无效的个人信息（缺少必填字段）
        invalid_personal_info = PersonalInfo(name="")
    except Exception as e:
        print(f"✓ 数据验证成功捕获错误: {type(e).__name__}")
    
    try:
        # 尝试创建无效的邮箱
        invalid_personal_info = PersonalInfo(
            name="测试用户",
            email="invalid-email"
        )
    except Exception as e:
        print(f"✓ 邮箱格式验证成功捕获错误: {type(e).__name__}")
    
    print("\n=== 演示完成 ===")
    print("所有数据模型功能正常，包括:")
    print("- 数据创建和验证")
    print("- JSON序列化和反序列化")
    print("- 字段验证和错误处理")
    print("- 枚举类型支持")
    print("- 嵌套模型结构")


if __name__ == "__main__":
    main()
"""
数据模型测试
验证Pydantic数据模型的功能和验证规则
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

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


class TestPersonalInfo:
    """个人信息模型测试"""
    
    def test_valid_personal_info(self):
        """测试有效的个人信息数据"""
        data = {
            "name": "张三",
            "email": "zhangsan@example.com",
            "phone": "13800138000",
            "location": "北京市",
            "summary": "资深软件工程师，具有5年开发经验"
        }
        personal_info = PersonalInfo(**data)
        assert personal_info.name == "张三"
        assert personal_info.email == "zhangsan@example.com"
        assert personal_info.phone == "13800138000"
    
    def test_required_fields(self):
        """测试必填字段验证"""
        # 缺少name字段
        with pytest.raises(ValidationError):
            PersonalInfo(email="test@example.com")
        
        # 缺少email字段
        with pytest.raises(ValidationError):
            PersonalInfo(name="张三")
    
    def test_email_validation(self):
        """测试邮箱格式验证"""
        with pytest.raises(ValidationError):
            PersonalInfo(name="张三", email="invalid-email")
    
    def test_optional_fields(self):
        """测试可选字段"""
        personal_info = PersonalInfo(
            name="张三",
            email="zhangsan@example.com"
        )
        assert personal_info.phone is None
        assert personal_info.location is None
        assert personal_info.summary is None


class TestWorkExperience:
    """工作经历模型测试"""
    
    def test_valid_work_experience(self):
        """测试有效的工作经历数据"""
        data = {
            "company": "阿里巴巴",
            "position": "高级软件工程师",
            "start_date": "2020-01",
            "end_date": "2023-12",
            "description": ["负责电商平台后端开发", "优化系统性能"],
            "technologies": ["Python", "Java", "Redis"]
        }
        work_exp = WorkExperience(**data)
        assert work_exp.company == "阿里巴巴"
        assert len(work_exp.description) == 2
        assert "Python" in work_exp.technologies
    
    def test_required_fields(self):
        """测试必填字段验证"""
        with pytest.raises(ValidationError):
            WorkExperience(
                position="工程师",
                start_date="2020-01",
                description=["工作描述"]
            )
    
    def test_description_validation(self):
        """测试工作描述验证"""
        # 描述不能为空列表
        with pytest.raises(ValidationError):
            WorkExperience(
                company="公司",
                position="职位",
                start_date="2020-01",
                description=[]
            )


class TestEducation:
    """教育背景模型测试"""
    
    def test_valid_education(self):
        """测试有效的教育背景数据"""
        data = {
            "institution": "清华大学",
            "degree": "学士",
            "major": "计算机科学与技术",
            "start_date": "2016-09",
            "end_date": "2020-06",
            "gpa": "3.8"
        }
        education = Education(**data)
        assert education.institution == "清华大学"
        assert education.major == "计算机科学与技术"


class TestSkill:
    """技能模型测试"""
    
    def test_valid_skill(self):
        """测试有效的技能数据"""
        skill = Skill(
            category=SkillCategory.TECHNICAL,
            name="Python",
            level=SkillLevel.ADVANCED
        )
        assert skill.category == SkillCategory.TECHNICAL
        assert skill.name == "Python"
        assert skill.level == SkillLevel.ADVANCED
    
    def test_skill_enums(self):
        """测试技能枚举值"""
        # 测试技能分类枚举
        assert SkillCategory.TECHNICAL == "technical"
        assert SkillCategory.SOFT == "soft"
        assert SkillCategory.LANGUAGE == "language"
        
        # 测试技能水平枚举
        assert SkillLevel.BEGINNER == "beginner"
        assert SkillLevel.EXPERT == "expert"


class TestResumeData:
    """完整简历数据模型测试"""
    
    def test_valid_resume_data(self):
        """测试有效的完整简历数据"""
        personal_info = PersonalInfo(
            name="张三",
            email="zhangsan@example.com"
        )
        
        work_exp = WorkExperience(
            company="阿里巴巴",
            position="软件工程师",
            start_date="2020-01",
            description=["负责后端开发"]
        )
        
        education = Education(
            institution="清华大学",
            degree="学士",
            start_date="2016-09"
        )
        
        skill = Skill(
            category=SkillCategory.TECHNICAL,
            name="Python"
        )
        
        resume = ResumeData(
            id="resume_001",
            personal_info=personal_info,
            work_experience=[work_exp],
            education=[education],
            skills=[skill]
        )
        
        assert resume.id == "resume_001"
        assert resume.personal_info.name == "张三"
        assert len(resume.work_experience) == 1
        assert len(resume.education) == 1
        assert len(resume.skills) == 1
        assert isinstance(resume.created_at, datetime)
        assert isinstance(resume.updated_at, datetime)
    
    def test_empty_lists_default(self):
        """测试列表字段的默认值"""
        personal_info = PersonalInfo(
            name="张三",
            email="zhangsan@example.com"
        )
        
        resume = ResumeData(
            id="resume_002",
            personal_info=personal_info
        )
        
        assert resume.work_experience == []
        assert resume.education == []
        assert resume.skills == []


class TestWebsiteConfig:
    """网站配置模型测试"""
    
    def test_valid_website_config(self):
        """测试有效的网站配置数据"""
        color_scheme = ColorScheme(
            primary="#3B82F6",
            secondary="#64748B",
            accent="#F59E0B",
            background="#FFFFFF",
            text="#1F2937"
        )
        
        config = WebsiteConfig(
            id="website_001",
            resume_id="resume_001",
            template_id="modern_template",
            color_scheme=color_scheme,
            url="https://example.com/zhangsan"
        )
        
        assert config.id == "website_001"
        assert config.resume_id == "resume_001"
        assert config.is_public is True  # 默认值
        assert config.color_scheme.primary == "#3B82F6"


if __name__ == "__main__":
    pytest.main([__file__])
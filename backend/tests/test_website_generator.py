"""
网站生成器测试
测试个人网站生成功能
"""

import pytest
import asyncio
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

from backend.services.website_generator import WebsiteGenerator
from backend.models.resume import (
    ResumeData, PersonalInfo, WorkExperience, Education, Skill,
    WebsiteConfig, ColorScheme, SkillCategory, SkillLevel
)


@pytest.fixture
def sample_resume_data():
    """创建示例简历数据"""
    return ResumeData(
        id="test-resume-123",
        personal_info=PersonalInfo(
            name="张三",
            email="zhangsan@example.com",
            phone="13800138000",
            location="北京市",
            summary="资深软件工程师，专注于Web开发和人工智能应用",
            linkedin="https://linkedin.com/in/zhangsan",
            github="https://github.com/zhangsan"
        ),
        work_experience=[
            WorkExperience(
                company="科技有限公司",
                position="高级软件工程师",
                start_date="2020-01",
                end_date="2024-01",
                description=[
                    "负责Web应用的前后端开发",
                    "参与系统架构设计和技术选型",
                    "指导初级开发人员，提升团队技术水平"
                ],
                technologies=["Python", "JavaScript", "React", "Django"]
            ),
            WorkExperience(
                company="创新科技公司",
                position="软件工程师",
                start_date="2018-06",
                end_date="2019-12",
                description=[
                    "开发和维护公司核心产品",
                    "优化系统性能，提升用户体验"
                ],
                technologies=["Java", "Spring Boot", "MySQL"]
            )
        ],
        education=[
            Education(
                institution="清华大学",
                degree="计算机科学与技术学士",
                major="计算机科学与技术",
                start_date="2014-09",
                end_date="2018-06",
                gpa="3.8"
            )
        ],
        skills=[
            Skill(category=SkillCategory.TECHNICAL, name="Python", level=SkillLevel.EXPERT),
            Skill(category=SkillCategory.TECHNICAL, name="JavaScript", level=SkillLevel.ADVANCED),
            Skill(category=SkillCategory.TECHNICAL, name="React", level=SkillLevel.ADVANCED),
            Skill(category=SkillCategory.SOFT, name="团队协作", level=SkillLevel.ADVANCED),
            Skill(category=SkillCategory.LANGUAGE, name="英语", level=SkillLevel.INTERMEDIATE)
        ],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@pytest.fixture
def sample_website_config():
    """创建示例网站配置"""
    return WebsiteConfig(
        id="test-website-456",
        resume_id="test-resume-123",
        template_id="modern",
        color_scheme=ColorScheme(
            primary="#3B82F6",
            secondary="#6B7280",
            accent="#10B981",
            background="#FFFFFF",
            text="#1F2937"
        ),
        url="/website/test-website-456",
        is_public=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@pytest.fixture
def temp_output_dir():
    """创建临时输出目录"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


class TestWebsiteGenerator:
    """网站生成器测试类"""
    
    @pytest.mark.asyncio
    async def test_website_generator_initialization(self, temp_output_dir):
        """测试网站生成器初始化"""
        generator = WebsiteGenerator(output_dir=temp_output_dir)
        
        assert generator.output_dir == Path(temp_output_dir)
        assert generator.output_dir.exists()
        assert generator.templates_dir.exists()
    
    @pytest.mark.asyncio
    async def test_generate_website_success(self, sample_resume_data, sample_website_config, temp_output_dir):
        """测试成功生成网站"""
        generator = WebsiteGenerator(output_dir=temp_output_dir)
        
        result = await generator.generate_website(sample_resume_data, sample_website_config)
        
        assert result.success is True
        assert result.website_path is not None
        assert result.error_message is None
        
        # 检查生成的文件
        website_dir = Path(result.website_path)
        assert website_dir.exists()
        assert (website_dir / "index.html").exists()
        assert (website_dir / "style.css").exists()
        assert (website_dir / "script.js").exists()
        assert (website_dir / "metadata.json").exists()
    
    @pytest.mark.asyncio
    async def test_generated_html_content(self, sample_resume_data, sample_website_config, temp_output_dir):
        """测试生成的HTML内容"""
        generator = WebsiteGenerator(output_dir=temp_output_dir)
        
        result = await generator.generate_website(sample_resume_data, sample_website_config)
        
        html_file = Path(result.website_path) / "index.html"
        html_content = html_file.read_text(encoding="utf-8")
        
        # 检查个人信息是否正确嵌入
        assert sample_resume_data.personal_info.name in html_content
        assert sample_resume_data.personal_info.email in html_content
        assert sample_resume_data.personal_info.phone in html_content
        assert sample_resume_data.personal_info.summary in html_content
        
        # 检查工作经历是否包含
        assert sample_resume_data.work_experience[0].company in html_content
        assert sample_resume_data.work_experience[0].position in html_content
        
        # 检查教育背景是否包含
        assert sample_resume_data.education[0].institution in html_content
        assert sample_resume_data.education[0].degree in html_content
        
        # 检查技能是否包含
        assert sample_resume_data.skills[0].name in html_content
    
    @pytest.mark.asyncio
    async def test_generated_css_content(self, sample_resume_data, sample_website_config, temp_output_dir):
        """测试生成的CSS内容"""
        generator = WebsiteGenerator(output_dir=temp_output_dir)
        
        result = await generator.generate_website(sample_resume_data, sample_website_config)
        
        css_file = Path(result.website_path) / "style.css"
        css_content = css_file.read_text(encoding="utf-8")
        
        # 检查颜色方案是否正确应用
        assert sample_website_config.color_scheme.primary in css_content
        assert sample_website_config.color_scheme.secondary in css_content
        assert sample_website_config.color_scheme.accent in css_content
        assert sample_website_config.color_scheme.background in css_content
        assert sample_website_config.color_scheme.text in css_content
    
    @pytest.mark.asyncio
    async def test_work_experience_html_generation(self, temp_output_dir):
        """测试工作经历HTML生成"""
        generator = WebsiteGenerator(output_dir=temp_output_dir)
        
        work_experiences = [
            WorkExperience(
                company="测试公司",
                position="测试职位",
                start_date="2020-01",
                end_date="2024-01",
                description=["测试描述1", "测试描述2"],
                technologies=["Python", "JavaScript"]
            )
        ]
        
        html = generator._generate_work_experience_html(work_experiences)
        
        assert "测试公司" in html
        assert "测试职位" in html
        assert "2020-01" in html
        assert "2024-01" in html
        assert "测试描述1" in html
        assert "测试描述2" in html
        assert "Python, JavaScript" in html
    
    @pytest.mark.asyncio
    async def test_education_html_generation(self, temp_output_dir):
        """测试教育背景HTML生成"""
        generator = WebsiteGenerator(output_dir=temp_output_dir)
        
        educations = [
            Education(
                institution="测试大学",
                degree="测试学位",
                major="测试专业",
                start_date="2014-09",
                end_date="2018-06",
                gpa="3.8"
            )
        ]
        
        html = generator._generate_education_html(educations)
        
        assert "测试大学" in html
        assert "测试学位" in html
        assert "测试专业" in html
        assert "2014-09" in html
        assert "2018-06" in html
        assert "3.8" in html
    
    @pytest.mark.asyncio
    async def test_skills_html_generation(self, temp_output_dir):
        """测试技能HTML生成"""
        generator = WebsiteGenerator(output_dir=temp_output_dir)
        
        skills = [
            Skill(category=SkillCategory.TECHNICAL, name="Python", level=SkillLevel.EXPERT),
            Skill(category=SkillCategory.SOFT, name="团队协作", level=SkillLevel.ADVANCED)
        ]
        
        html = generator._generate_skills_html(skills)
        
        assert "技术技能" in html
        assert "软技能" in html
        assert "Python" in html
        assert "团队协作" in html
        assert "expert" in html
        assert "advanced" in html
    
    @pytest.mark.asyncio
    async def test_delete_website(self, sample_resume_data, sample_website_config, temp_output_dir):
        """测试删除网站"""
        generator = WebsiteGenerator(output_dir=temp_output_dir)
        
        # 先生成网站
        result = await generator.generate_website(sample_resume_data, sample_website_config)
        assert result.success is True
        
        website_dir = Path(result.website_path)
        assert website_dir.exists()
        
        # 删除网站
        delete_result = await generator.delete_website(sample_website_config.id)
        assert delete_result.success is True
        assert not website_dir.exists()
    
    @pytest.mark.asyncio
    async def test_delete_nonexistent_website(self, temp_output_dir):
        """测试删除不存在的网站"""
        generator = WebsiteGenerator(output_dir=temp_output_dir)
        
        # 删除不存在的网站应该成功（不报错）
        delete_result = await generator.delete_website("nonexistent-website")
        assert delete_result.success is True
    
    @pytest.mark.asyncio
    async def test_empty_work_experience(self, temp_output_dir):
        """测试空工作经历"""
        generator = WebsiteGenerator(output_dir=temp_output_dir)
        
        html = generator._generate_work_experience_html([])
        assert "暂无工作经历" in html
    
    @pytest.mark.asyncio
    async def test_empty_education(self, temp_output_dir):
        """测试空教育背景"""
        generator = WebsiteGenerator(output_dir=temp_output_dir)
        
        html = generator._generate_education_html([])
        assert "暂无教育背景" in html
    
    @pytest.mark.asyncio
    async def test_empty_skills(self, temp_output_dir):
        """测试空技能"""
        generator = WebsiteGenerator(output_dir=temp_output_dir)
        
        html = generator._generate_skills_html([])
        assert "暂无技能信息" in html


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])
"""
网站生成集成测试
测试完整的网站生成流程
"""

import pytest
import asyncio
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

from backend.services.website_generator import WebsiteGenerator
from backend.services.redis_manager import RedisDataManager
from backend.models.resume import (
    ResumeData, PersonalInfo, WorkExperience, Education, Skill,
    WebsiteConfig, ColorScheme, SkillCategory, SkillLevel
)


@pytest.fixture
def temp_output_dir():
    """创建临时输出目录"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_resume_data():
    """创建示例简历数据"""
    return ResumeData(
        id="integration-test-resume",
        personal_info=PersonalInfo(
            name="李四",
            email="lisi@example.com",
            phone="13900139000",
            location="上海市",
            summary="全栈开发工程师，具有5年Web开发经验",
            linkedin="https://linkedin.com/in/lisi",
            github="https://github.com/lisi",
            website="https://lisi.dev"
        ),
        work_experience=[
            WorkExperience(
                company="互联网科技公司",
                position="全栈开发工程师",
                start_date="2021-03",
                end_date=None,  # 当前工作
                description=[
                    "负责公司核心产品的前后端开发",
                    "设计和实现RESTful API接口",
                    "优化系统性能，提升用户体验",
                    "参与技术架构设计和代码审查"
                ],
                technologies=["Python", "FastAPI", "Vue.js", "PostgreSQL", "Redis"]
            ),
            WorkExperience(
                company="软件开发公司",
                position="前端开发工程师",
                start_date="2019-06",
                end_date="2021-02",
                description=[
                    "开发响应式Web应用",
                    "与设计师协作实现UI/UX设计",
                    "维护和优化现有代码库"
                ],
                technologies=["JavaScript", "React", "HTML5", "CSS3"]
            )
        ],
        education=[
            Education(
                institution="上海交通大学",
                degree="软件工程硕士",
                major="软件工程",
                start_date="2017-09",
                end_date="2019-06",
                gpa="3.9"
            ),
            Education(
                institution="华东师范大学",
                degree="计算机科学与技术学士",
                major="计算机科学与技术",
                start_date="2013-09",
                end_date="2017-06",
                gpa="3.7"
            )
        ],
        skills=[
            Skill(category=SkillCategory.TECHNICAL, name="Python", level=SkillLevel.EXPERT),
            Skill(category=SkillCategory.TECHNICAL, name="JavaScript", level=SkillLevel.EXPERT),
            Skill(category=SkillCategory.TECHNICAL, name="Vue.js", level=SkillLevel.ADVANCED),
            Skill(category=SkillCategory.TECHNICAL, name="FastAPI", level=SkillLevel.ADVANCED),
            Skill(category=SkillCategory.TECHNICAL, name="PostgreSQL", level=SkillLevel.INTERMEDIATE),
            Skill(category=SkillCategory.SOFT, name="团队协作", level=SkillLevel.EXPERT),
            Skill(category=SkillCategory.SOFT, name="项目管理", level=SkillLevel.INTERMEDIATE),
            Skill(category=SkillCategory.LANGUAGE, name="英语", level=SkillLevel.ADVANCED),
            Skill(category=SkillCategory.LANGUAGE, name="日语", level=SkillLevel.BEGINNER)
        ],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@pytest.fixture
def sample_website_config():
    """创建示例网站配置"""
    return WebsiteConfig(
        id="integration-test-website",
        resume_id="integration-test-resume",
        template_id="modern",
        color_scheme=ColorScheme(
            primary="#8B5CF6",  # 紫色主题
            secondary="#6B7280",
            accent="#F59E0B",
            background="#FFFFFF",
            text="#1F2937"
        ),
        url="/website/integration-test-website",
        is_public=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


class TestWebsiteIntegration:
    """网站生成集成测试类"""
    
    @pytest.mark.asyncio
    async def test_complete_website_generation_flow(
        self, 
        sample_resume_data, 
        sample_website_config, 
        temp_output_dir
    ):
        """测试完整的网站生成流程"""
        # 1. 初始化网站生成器
        generator = WebsiteGenerator(output_dir=temp_output_dir)
        
        # 2. 生成网站
        result = await generator.generate_website(sample_resume_data, sample_website_config)
        
        # 3. 验证生成结果
        assert result.success is True
        assert result.website_path is not None
        assert result.error_message is None
        
        # 4. 验证生成的文件
        website_dir = Path(result.website_path)
        assert website_dir.exists()
        
        # 检查必要文件
        required_files = ["index.html", "style.css", "script.js", "metadata.json"]
        for file_name in required_files:
            file_path = website_dir / file_name
            assert file_path.exists(), f"缺少文件: {file_name}"
            assert file_path.stat().st_size > 0, f"文件为空: {file_name}"
        
        # 5. 验证HTML内容
        html_content = (website_dir / "index.html").read_text(encoding="utf-8")
        
        # 检查个人信息
        assert sample_resume_data.personal_info.name in html_content
        assert sample_resume_data.personal_info.email in html_content
        assert sample_resume_data.personal_info.phone in html_content
        assert sample_resume_data.personal_info.location in html_content
        assert sample_resume_data.personal_info.summary in html_content
        
        # 检查工作经历
        for exp in sample_resume_data.work_experience:
            assert exp.company in html_content
            assert exp.position in html_content
            for desc in exp.description:
                assert desc in html_content
        
        # 检查教育背景
        for edu in sample_resume_data.education:
            assert edu.institution in html_content
            assert edu.degree in html_content
        
        # 检查技能
        for skill in sample_resume_data.skills:
            assert skill.name in html_content
        
        # 6. 验证CSS内容
        css_content = (website_dir / "style.css").read_text(encoding="utf-8")
        
        # 检查颜色方案
        assert sample_website_config.color_scheme.primary in css_content
        assert sample_website_config.color_scheme.secondary in css_content
        assert sample_website_config.color_scheme.accent in css_content
        
        # 7. 验证JavaScript内容
        js_content = (website_dir / "script.js").read_text(encoding="utf-8")
        assert "DOMContentLoaded" in js_content
        assert "个人简历网站加载完成" in js_content
        
        # 8. 验证元数据
        import json
        metadata_content = (website_dir / "metadata.json").read_text(encoding="utf-8")
        metadata = json.loads(metadata_content)
        
        assert metadata["website_id"] == sample_website_config.id
        assert metadata["resume_id"] == sample_website_config.resume_id
        assert metadata["template_id"] == sample_website_config.template_id
        assert "generated_at" in metadata
        assert "version" in metadata
    
    @pytest.mark.asyncio
    async def test_website_update_flow(
        self, 
        sample_resume_data, 
        sample_website_config, 
        temp_output_dir
    ):
        """测试网站更新流程"""
        generator = WebsiteGenerator(output_dir=temp_output_dir)
        
        # 1. 生成初始网站
        initial_result = await generator.generate_website(sample_resume_data, sample_website_config)
        assert initial_result.success is True
        
        initial_html = (Path(initial_result.website_path) / "index.html").read_text(encoding="utf-8")
        
        # 2. 更新简历数据
        updated_resume = sample_resume_data.model_copy()
        updated_resume.personal_info.summary = "更新后的个人简介：资深全栈开发工程师"
        updated_resume.updated_at = datetime.now()
        
        # 3. 更新网站配置（更换颜色方案）
        updated_config = sample_website_config.model_copy()
        updated_config.color_scheme.primary = "#10B981"  # 更换为绿色
        updated_config.updated_at = datetime.now()
        
        # 4. 重新生成网站
        updated_result = await generator.generate_website(updated_resume, updated_config)
        assert updated_result.success is True
        
        # 5. 验证更新后的内容
        updated_html = (Path(updated_result.website_path) / "index.html").read_text(encoding="utf-8")
        updated_css = (Path(updated_result.website_path) / "style.css").read_text(encoding="utf-8")
        
        # 检查内容更新
        assert "更新后的个人简介" in updated_html
        assert updated_config.color_scheme.primary in updated_css
        
        # 确保旧内容被替换
        assert sample_resume_data.personal_info.summary not in updated_html
        assert sample_website_config.color_scheme.primary not in updated_css
    
    @pytest.mark.asyncio
    async def test_multiple_websites_generation(self, sample_resume_data, temp_output_dir):
        """测试生成多个网站"""
        generator = WebsiteGenerator(output_dir=temp_output_dir)
        
        # 创建不同的网站配置
        configs = [
            WebsiteConfig(
                id=f"website-{i}",
                resume_id=sample_resume_data.id,
                template_id="modern",
                color_scheme=ColorScheme(
                    primary=color,
                    secondary="#6B7280",
                    accent="#10B981",
                    background="#FFFFFF",
                    text="#1F2937"
                ),
                url=f"/website/website-{i}",
                is_public=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            for i, color in enumerate(["#3B82F6", "#8B5CF6", "#EF4444"], 1)
        ]
        
        # 生成多个网站
        results = []
        for config in configs:
            result = await generator.generate_website(sample_resume_data, config)
            results.append(result)
            assert result.success is True
        
        # 验证所有网站都生成成功
        for i, result in enumerate(results, 1):
            website_dir = Path(result.website_path)
            assert website_dir.exists()
            assert website_dir.name == f"website-{i}"
            
            # 验证每个网站的颜色方案不同
            css_content = (website_dir / "style.css").read_text(encoding="utf-8")
            assert configs[i-1].color_scheme.primary in css_content
    
    @pytest.mark.asyncio
    async def test_website_deletion_flow(
        self, 
        sample_resume_data, 
        sample_website_config, 
        temp_output_dir
    ):
        """测试网站删除流程"""
        generator = WebsiteGenerator(output_dir=temp_output_dir)
        
        # 1. 生成网站
        result = await generator.generate_website(sample_resume_data, sample_website_config)
        assert result.success is True
        
        website_dir = Path(result.website_path)
        assert website_dir.exists()
        
        # 2. 删除网站
        delete_result = await generator.delete_website(sample_website_config.id)
        assert delete_result.success is True
        
        # 3. 验证网站目录已删除
        assert not website_dir.exists()
    
    @pytest.mark.asyncio
    async def test_edge_cases(self, temp_output_dir):
        """测试边界情况"""
        generator = WebsiteGenerator(output_dir=temp_output_dir)
        
        # 1. 测试最小简历数据
        minimal_resume = ResumeData(
            id="minimal-resume",
            personal_info=PersonalInfo(
                name="最小测试",
                email="minimal@test.com"
            ),
            work_experience=[],
            education=[],
            skills=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        minimal_config = WebsiteConfig(
            id="minimal-website",
            resume_id="minimal-resume",
            template_id="modern",
            color_scheme=ColorScheme(
                primary="#000000",
                secondary="#666666",
                accent="#999999",
                background="#FFFFFF",
                text="#000000"
            ),
            url="/website/minimal-website",
            is_public=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # 2. 生成最小网站
        result = await generator.generate_website(minimal_resume, minimal_config)
        assert result.success is True
        
        # 3. 验证生成的内容
        html_content = (Path(result.website_path) / "index.html").read_text(encoding="utf-8")
        assert "最小测试" in html_content
        assert "minimal@test.com" in html_content
        assert "暂无工作经历" in html_content
       
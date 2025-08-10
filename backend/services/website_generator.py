"""
网站生成器服务
实现个人网站的静态文件生成和管理功能
支持多种模板和自定义样式
"""

import os
import json
import shutil
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel

from backend.models.resume import ResumeData, WebsiteConfig

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebsiteGenerationResult(BaseModel):
    """网站生成结果模型"""
    success: bool
    website_path: Optional[str] = None
    error_message: Optional[str] = None


class WebsiteDeletionResult(BaseModel):
    """网站删除结果模型"""
    success: bool
    error_message: Optional[str] = None


class WebsiteGenerator:
    """网站生成器类"""
    
    def __init__(self, output_dir: str = "generated_websites"):
        """
        初始化网站生成器
        
        Args:
            output_dir: 生成网站的输出目录
        """
        self.output_dir = Path(output_dir)
        self.templates_dir = Path("templates")
        
        # 确保输出目录存在
        self.output_dir.mkdir(exist_ok=True)
        
        # 确保模板目录存在
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"网站生成器初始化完成，输出目录: {self.output_dir}")
    
    async def generate_website(
        self, 
        resume_data: ResumeData, 
        website_config: WebsiteConfig
    ) -> WebsiteGenerationResult:
        """
        生成个人网站
        
        Args:
            resume_data: 简历数据
            website_config: 网站配置
            
        Returns:
            WebsiteGenerationResult: 生成结果
        """
        try:
            logger.info(f"开始生成网站: {website_config.id}")
            
            # 1. 创建网站目录
            website_dir = self.output_dir / website_config.id
            website_dir.mkdir(exist_ok=True)
            
            # 2. 生成HTML内容
            html_content = await self._generate_html(resume_data, website_config)
            
            # 3. 生成CSS样式
            css_content = await self._generate_css(website_config)
            
            # 4. 生成JavaScript
            js_content = await self._generate_js(website_config)
            
            # 5. 写入文件
            (website_dir / "index.html").write_text(html_content, encoding="utf-8")
            (website_dir / "style.css").write_text(css_content, encoding="utf-8")
            (website_dir / "script.js").write_text(js_content, encoding="utf-8")
            
            # 6. 复制静态资源
            await self._copy_static_assets(website_config.template_id, website_dir)
            
            # 7. 生成网站元数据
            metadata = {
                "website_id": website_config.id,
                "resume_id": website_config.resume_id,
                "template_id": website_config.template_id,
                "generated_at": datetime.now().isoformat(),
                "version": "1.0.0"
            }
            
            (website_dir / "metadata.json").write_text(
                json.dumps(metadata, indent=2, ensure_ascii=False), 
                encoding="utf-8"
            )
            
            logger.info(f"网站生成成功: {website_config.id}")
            
            return WebsiteGenerationResult(
                success=True,
                website_path=str(website_dir)
            )
            
        except Exception as e:
            logger.error(f"生成网站失败: {e}")
            return WebsiteGenerationResult(
                success=False,
                error_message=str(e)
            )
    
    async def delete_website(self, website_id: str) -> WebsiteDeletionResult:
        """
        删除网站文件
        
        Args:
            website_id: 网站ID
            
        Returns:
            WebsiteDeletionResult: 删除结果
        """
        try:
            website_dir = self.output_dir / website_id
            
            if website_dir.exists():
                shutil.rmtree(website_dir)
                logger.info(f"网站文件删除成功: {website_id}")
            else:
                logger.warning(f"网站目录不存在: {website_id}")
            
            return WebsiteDeletionResult(success=True)
            
        except Exception as e:
            logger.error(f"删除网站文件失败: {e}")
            return WebsiteDeletionResult(
                success=False,
                error_message=str(e)
            )
    
    async def _generate_html(
        self, 
        resume_data: ResumeData, 
        website_config: WebsiteConfig
    ) -> str:
        """
        生成HTML内容
        
        Args:
            resume_data: 简历数据
            website_config: 网站配置
            
        Returns:
            str: HTML内容
        """
        # 获取模板
        template_content = await self._get_template_content(website_config.template_id)
        
        # 准备模板变量
        template_vars = {
            # 个人信息
            "name": resume_data.personal_info.name,
            "email": resume_data.personal_info.email,
            "phone": resume_data.personal_info.phone or "",
            "location": resume_data.personal_info.location or "",
            "summary": resume_data.personal_info.summary or "",
            "linkedin": resume_data.personal_info.linkedin or "",
            "github": resume_data.personal_info.github or "",
            "website": resume_data.personal_info.website or "",
            
            # 工作经历
            "work_experience_html": self._generate_work_experience_html(resume_data.work_experience),
            
            # 教育背景
            "education_html": self._generate_education_html(resume_data.education),
            
            # 技能
            "skills_html": self._generate_skills_html(resume_data.skills),
            
            # 颜色方案
            "primary_color": website_config.color_scheme.primary,
            "secondary_color": website_config.color_scheme.secondary,
            "accent_color": website_config.color_scheme.accent,
            "background_color": website_config.color_scheme.background,
            "text_color": website_config.color_scheme.text,
            
            # 元数据
            "page_title": f"{resume_data.personal_info.name} - 个人简历",
            "meta_description": resume_data.personal_info.summary or f"{resume_data.personal_info.name}的个人简历网站"
        }
        
        # 替换模板变量
        html_content = self._replace_template_vars(template_content, template_vars, resume_data)
        
        return html_content
    
    async def _generate_css(self, website_config: WebsiteConfig) -> str:
        """
        生成CSS样式
        
        Args:
            website_config: 网站配置
            
        Returns:
            str: CSS内容
        """
        # 获取基础CSS模板
        css_template = await self._get_css_template(website_config.template_id)
        
        # 替换颜色变量
        css_content = css_template.format(
            primary_color=website_config.color_scheme.primary,
            secondary_color=website_config.color_scheme.secondary,
            accent_color=website_config.color_scheme.accent,
            background_color=website_config.color_scheme.background,
            text_color=website_config.color_scheme.text
        )
        
        return css_content
    
    async def _generate_js(self, website_config: WebsiteConfig) -> str:
        """
        生成JavaScript代码
        
        Args:
            website_config: 网站配置
            
        Returns:
            str: JavaScript内容
        """
        # 获取基础JS模板
        js_template = await self._get_js_template(website_config.template_id)
        
        return js_template
    
    async def _get_template_content(self, template_id: str) -> str:
        """
        获取HTML模板内容
        
        Args:
            template_id: 模板ID
            
        Returns:
            str: 模板内容
        """
        template_file = self.templates_dir / template_id / "index.html"
        
        if template_file.exists():
            return template_file.read_text(encoding="utf-8")
        else:
            # 返回默认模板
            return await self._get_default_html_template()
    
    async def _get_css_template(self, template_id: str) -> str:
        """
        获取CSS模板内容
        
        Args:
            template_id: 模板ID
            
        Returns:
            str: CSS模板内容
        """
        css_file = self.templates_dir / template_id / "style.css"
        
        if css_file.exists():
            return css_file.read_text(encoding="utf-8")
        else:
            # 返回默认CSS
            return await self._get_default_css_template()
    
    async def _get_js_template(self, template_id: str) -> str:
        """
        获取JavaScript模板内容
        
        Args:
            template_id: 模板ID
            
        Returns:
            str: JavaScript模板内容
        """
        js_file = self.templates_dir / template_id / "script.js"
        
        if js_file.exists():
            return js_file.read_text(encoding="utf-8")
        else:
            # 返回默认JavaScript
            return await self._get_default_js_template()
    
    async def _copy_static_assets(self, template_id: str, website_dir: Path):
        """
        复制静态资源文件
        
        Args:
            template_id: 模板ID
            website_dir: 网站目录
        """
        assets_dir = self.templates_dir / template_id / "assets"
        
        if assets_dir.exists():
            target_assets_dir = website_dir / "assets"
            if target_assets_dir.exists():
                shutil.rmtree(target_assets_dir)
            shutil.copytree(assets_dir, target_assets_dir)
            logger.info(f"静态资源复制完成: {template_id}")
    
    def _generate_work_experience_html(self, work_experiences) -> str:
        """生成工作经历HTML"""
        if not work_experiences:
            return "<p>暂无工作经历</p>"
        
        html_parts = []
        for exp in work_experiences:
            end_date = exp.end_date or "至今"
            technologies = ", ".join(exp.technologies) if exp.technologies else ""
            
            descriptions_html = ""
            for desc in exp.description:
                descriptions_html += f"<li>{desc}</li>"
            
            exp_html = f"""
            <div class="experience-item">
                <div class="experience-header">
                    <h3>{exp.position}</h3>
                    <span class="company">{exp.company}</span>
                    <span class="duration">{exp.start_date} - {end_date}</span>
                </div>
                <ul class="experience-description">
                    {descriptions_html}
                </ul>
                {f'<div class="technologies"><strong>技术栈:</strong> {technologies}</div>' if technologies else ''}
            </div>
            """
            html_parts.append(exp_html)
        
        return "\n".join(html_parts)
    
    def _generate_education_html(self, educations) -> str:
        """生成教育背景HTML"""
        if not educations:
            return "<p>暂无教育背景</p>"
        
        html_parts = []
        for edu in educations:
            end_date = edu.end_date or "至今"
            major = edu.major or ""
            gpa = f" (GPA: {edu.gpa})" if edu.gpa else ""
            
            edu_html = f"""
            <div class="education-item">
                <div class="education-header">
                    <h3>{edu.degree}{f" - {major}" if major else ""}</h3>
                    <span class="institution">{edu.institution}</span>
                    <span class="duration">{edu.start_date} - {end_date}{gpa}</span>
                </div>
            </div>
            """
            html_parts.append(edu_html)
        
        return "\n".join(html_parts)
    
    def _generate_skills_html(self, skills) -> str:
        """生成技能HTML"""
        if not skills:
            return "<p>暂无技能信息</p>"
        
        # 按分类组织技能
        skills_by_category = {}
        for skill in skills:
            category = skill.category.value
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(skill)
        
        # 分类名称映射
        category_names = {
            "technical": "技术技能",
            "soft": "软技能",
            "language": "语言技能"
        }
        
        html_parts = []
        for category, category_skills in skills_by_category.items():
            category_name = category_names.get(category, category)
            
            skills_html = ""
            for skill in category_skills:
                level = f" ({skill.level.value})" if skill.level else ""
                skills_html += f'<span class="skill-tag">{skill.name}{level}</span>'
            
            category_html = f"""
            <div class="skills-category">
                <h4>{category_name}</h4>
                <div class="skills-list">
                    {skills_html}
                </div>
            </div>
            """
            html_parts.append(category_html)
        
        return "\n".join(html_parts)
    
    def _replace_template_vars(self, template: str, vars_dict: dict, resume_data: ResumeData) -> str:
        """
        替换模板变量，处理条件显示
        
        Args:
            template: 模板字符串
            vars_dict: 变量字典
            resume_data: 简历数据
            
        Returns:
            str: 替换后的内容
        """
        # 处理联系信息的条件显示
        contact_items = []
        
        # 邮箱（必须）
        contact_items.append(f'<div class="contact-item"><i class="fas fa-envelope"></i><a href="mailto:{resume_data.personal_info.email}">{resume_data.personal_info.email}</a></div>')
        
        # 电话（可选）
        if resume_data.personal_info.phone:
            contact_items.append(f'<div class="contact-item"><i class="fas fa-phone"></i><span>{resume_data.personal_info.phone}</span></div>')
        
        # 地址（可选）
        if resume_data.personal_info.location:
            contact_items.append(f'<div class="contact-item"><i class="fas fa-map-marker-alt"></i><span>{resume_data.personal_info.location}</span></div>')
        
        # LinkedIn（可选）
        if resume_data.personal_info.linkedin:
            contact_items.append(f'<div class="contact-item"><i class="fab fa-linkedin"></i><a href="{resume_data.personal_info.linkedin}" target="_blank">LinkedIn</a></div>')
        
        # GitHub（可选）
        if resume_data.personal_info.github:
            contact_items.append(f'<div class="contact-item"><i class="fab fa-github"></i><a href="{resume_data.personal_info.github}" target="_blank">GitHub</a></div>')
        
        # 个人网站（可选）
        if resume_data.personal_info.website:
            contact_items.append(f'<div class="contact-item"><i class="fas fa-globe"></i><a href="{resume_data.personal_info.website}" target="_blank">个人网站</a></div>')
        
        vars_dict["contact_items"] = "\n                        ".join(contact_items)
        
        # 处理个人简介的条件显示
        if resume_data.personal_info.summary:
            vars_dict["summary_section"] = f'''
            <section class="section">
                <h2 class="section-title">个人简介</h2>
                <div class="section-content">
                    <p class="summary">{resume_data.personal_info.summary}</p>
                </div>
            </section>'''
        else:
            vars_dict["summary_section"] = ""
        
        # 使用简单的字符串替换
        result = template
        for key, value in vars_dict.items():
            result = result.replace(f"{{{key}}}", str(value))
        
        return result
    
    async def _get_default_html_template(self) -> str:
        """获取默认HTML模板"""
        return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <meta name="description" content="{meta_description}">
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <!-- 头部区域 -->
        <header class="header">
            <div class="header-content">
                <div class="profile-info">
                    <h1 class="name">{name}</h1>
                    <p class="title">专业人士</p>
                    <div class="contact-info">
                        {contact_items}
                    </div>
                </div>
            </div>
        </header>

        <!-- 主要内容区域 -->
        <main class="main-content">
            <!-- 个人简介 -->
            {summary_section}

            <!-- 工作经历 -->
            <section class="section">
                <h2 class="section-title">工作经历</h2>
                <div class="section-content">
                    {work_experience_html}
                </div>
            </section>

            <!-- 教育背景 -->
            <section class="section">
                <h2 class="section-title">教育背景</h2>
                <div class="section-content">
                    {education_html}
                </div>
            </section>

            <!-- 技能 -->
            <section class="section">
                <h2 class="section-title">专业技能</h2>
                <div class="section-content">
                    {skills_html}
                </div>
            </section>
        </main>

        <!-- 页脚 -->
        <footer class="footer">
            <p>&copy; 2024 {name}. 由个人简历网站生成器创建。</p>
        </footer>
    </div>

    <script src="script.js"></script>
</body>
</html>'''
    
    async def _get_default_css_template(self) -> str:
        """获取默认CSS模板"""
        return '''/* 全局样式 */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --primary-color: {primary_color};
    --secondary-color: {secondary_color};
    --accent-color: {accent_color};
    --background-color: {background_color};
    --text-color: {text_color};
    --border-color: #e5e7eb;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}}

body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}}

/* 头部样式 */
.header {{
    background: var(--background-color);
    border-radius: 20px;
    padding: 3rem;
    margin-bottom: 2rem;
    box-shadow: var(--shadow-lg);
    text-align: center;
}}

.name {{
    font-size: 3rem;
    font-weight: 700;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}}

.title {{
    font-size: 1.25rem;
    color: var(--secondary-color);
    margin-bottom: 2rem;
}}

.contact-info {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1.5rem;
}}

.contact-item {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--secondary-color);
}}

.contact-item i {{
    color: var(--primary-color);
    width: 20px;
}}

.contact-item a {{
    color: var(--text-color);
    text-decoration: none;
    transition: color 0.3s ease;
}}

.contact-item a:hover {{
    color: var(--primary-color);
}}

/* 主要内容样式 */
.main-content {{
    display: grid;
    gap: 2rem;
}}

.section {{
    background: var(--background-color);
    border-radius: 16px;
    padding: 2rem;
    box-shadow: var(--shadow);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.section:hover {{
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}}

.section-title {{
    font-size: 1.75rem;
    font-weight: 600;
    color: var(--primary-color);
    margin-bottom: 1.5rem;
    position: relative;
    padding-bottom: 0.5rem;
}}

.section-title::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 50px;
    height: 3px;
    background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
    border-radius: 2px;
}}

.section-content {{
    color: var(--text-color);
}}

/* 个人简介样式 */
.summary {{
    font-size: 1.1rem;
    line-height: 1.8;
    color: var(--secondary-color);
}}

/* 工作经历样式 */
.experience-item {{
    margin-bottom: 2rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid var(--border-color);
}}

.experience-item:last-child {{
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
}}

.experience-header {{
    margin-bottom: 1rem;
}}

.experience-header h3 {{
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: 0.5rem;
}}

.company {{
    font-weight: 500;
    color: var(--primary-color);
    margin-right: 1rem;
}}

.duration {{
    color: var(--secondary-color);
    font-size: 0.9rem;
}}

.experience-description {{
    list-style: none;
    margin: 1rem 0;
}}

.experience-description li {{
    position: relative;
    padding-left: 1.5rem;
    margin-bottom: 0.5rem;
    color: var(--secondary-color);
}}

.experience-description li::before {{
    content: '▸';
    position: absolute;
    left: 0;
    color: var(--accent-color);
    font-weight: bold;
}}

.technologies {{
    margin-top: 1rem;
    padding: 0.75rem;
    background: #f8fafc;
    border-radius: 8px;
    font-size: 0.9rem;
    color: var(--secondary-color);
}}

/* 教育背景样式 */
.education-item {{
    margin-bottom: 1.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border-color);
}}

.education-item:last-child {{
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
}}

.education-header h3 {{
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: 0.5rem;
}}

.institution {{
    font-weight: 500;
    color: var(--primary-color);
    margin-right: 1rem;
}}

/* 技能样式 */
.skills-category {{
    margin-bottom: 2rem;
}}

.skills-category:last-child {{
    margin-bottom: 0;
}}

.skills-category h4 {{
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: 1rem;
}}

.skills-list {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
}}

.skill-tag {{
    display: inline-block;
    padding: 0.5rem 1rem;
    background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
    color: white;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 500;
    transition: transform 0.2s ease;
}}

.skill-tag:hover {{
    transform: translateY(-2px);
}}

/* 页脚样式 */
.footer {{
    text-align: center;
    margin-top: 3rem;
    padding: 2rem;
    color: rgba(255, 255, 255, 0.8);
    font-size: 0.9rem;
}}

/* 响应式设计 */
@media (max-width: 768px) {{
    .container {{
        padding: 1rem;
    }}
    
    .header {{
        padding: 2rem;
    }}
    
    .name {{
        font-size: 2rem;
    }}
    
    .contact-info {{
        flex-direction: column;
        align-items: center;
        gap: 1rem;
    }}
    
    .section {{
        padding: 1.5rem;
    }}
    
    .section-title {{
        font-size: 1.5rem;
    }}
}}

/* 动画效果 */
@keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translateY(30px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

.section {{
    animation: fadeInUp 0.6s ease-out;
}}

.section:nth-child(1) {{ animation-delay: 0.1s; }}
.section:nth-child(2) {{ animation-delay: 0.2s; }}
.section:nth-child(3) {{ animation-delay: 0.3s; }}
.section:nth-child(4) {{ animation-delay: 0.4s; }}'''
    
    async def _get_default_js_template(self) -> str:
        """获取默认JavaScript模板"""
        return '''// 个人简历网站交互功能

document.addEventListener('DOMContentLoaded', function() {
    // 平滑滚动效果
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // 滚动动画效果
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // 观察所有section元素
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });

    // 技能标签悬停效果
    const skillTags = document.querySelectorAll('.skill-tag');
    skillTags.forEach(tag => {
        tag.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px) scale(1.05)';
        });
        
        tag.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // 联系方式点击效果
    const contactItems = document.querySelectorAll('.contact-item a');
    contactItems.forEach(item => {
        item.addEventListener('click', function() {
            // 添加点击反馈效果
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });

    // 页面加载完成后的入场动画
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);

    // 打印功能（可选）
    function printResume() {
        window.print();
    }

    // 如果需要添加打印按钮，可以取消注释以下代码
    /*
    const printButton = document.createElement('button');
    printButton.textContent = '打印简历';
    printButton.className = 'print-button';
    printButton.onclick = printResume;
    document.querySelector('.header').appendChild(printButton);
    */

    console.log('个人简历网站加载完成');
});

// 页面性能优化
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // 可以在这里注册Service Worker进行缓存优化
        console.log('Service Worker支持已检测');
    });
}'''
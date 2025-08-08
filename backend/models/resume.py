"""
简历数据模型定义
使用Pydantic进行数据验证和序列化
"""

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class SkillCategory(str, Enum):
    """技能分类枚举"""
    TECHNICAL = "technical"
    SOFT = "soft"
    LANGUAGE = "language"

class SkillLevel(str, Enum):
    """技能水平枚举"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class PersonalInfo(BaseModel):
    """个人基本信息模型"""
    name: str = Field(..., min_length=1, max_length=100, description="姓名")
    email: EmailStr = Field(..., description="邮箱地址")
    phone: Optional[str] = Field(None, max_length=20, description="电话号码")
    location: Optional[str] = Field(None, max_length=100, description="所在地址")
    summary: Optional[str] = Field(None, max_length=500, description="个人简介")
    linkedin: Optional[str] = Field(None, description="LinkedIn链接")
    github: Optional[str] = Field(None, description="GitHub链接")
    website: Optional[str] = Field(None, description="个人网站")

class WorkExperience(BaseModel):
    """工作经历模型"""
    company: str = Field(..., min_length=1, max_length=100, description="公司名称")
    position: str = Field(..., min_length=1, max_length=100, description="职位名称")
    start_date: str = Field(..., description="开始时间")
    end_date: Optional[str] = Field(None, description="结束时间")
    description: List[str] = Field(..., min_items=1, description="工作描述")
    technologies: Optional[List[str]] = Field(None, description="使用的技术")

class Education(BaseModel):
    """教育背景模型"""
    institution: str = Field(..., min_length=1, max_length=100, description="学校名称")
    degree: str = Field(..., min_length=1, max_length=50, description="学位")
    major: Optional[str] = Field(None, max_length=100, description="专业")
    start_date: str = Field(..., description="开始时间")
    end_date: Optional[str] = Field(None, description="结束时间")
    gpa: Optional[str] = Field(None, max_length=10, description="GPA")

class Skill(BaseModel):
    """技能模型"""
    category: SkillCategory = Field(..., description="技能分类")
    name: str = Field(..., min_length=1, max_length=50, description="技能名称")
    level: Optional[SkillLevel] = Field(None, description="技能水平")

class ResumeData(BaseModel):
    """完整简历数据模型"""
    id: str = Field(..., description="简历唯一标识")
    personal_info: PersonalInfo = Field(..., description="个人基本信息")
    work_experience: List[WorkExperience] = Field(default=[], description="工作经历")
    education: List[Education] = Field(default=[], description="教育背景")
    skills: List[Skill] = Field(default=[], description="技能列表")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")

    class Config:
        """Pydantic配置"""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ColorScheme(BaseModel):
    """网站颜色方案模型"""
    primary: str = Field(..., description="主色调")
    secondary: str = Field(..., description="次要色调")
    accent: str = Field(..., description="强调色")
    background: str = Field(..., description="背景色")
    text: str = Field(..., description="文字色")

class WebsiteConfig(BaseModel):
    """网站配置模型"""
    id: str = Field(..., description="网站唯一标识")
    resume_id: str = Field(..., description="关联的简历ID")
    template_id: str = Field(..., description="模板ID")
    color_scheme: ColorScheme = Field(..., description="颜色方案")
    url: str = Field(..., description="网站访问URL")
    is_public: bool = Field(default=True, description="是否公开访问")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")

    class Config:
        """Pydantic配置"""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
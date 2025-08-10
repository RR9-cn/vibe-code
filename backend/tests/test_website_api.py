"""
网站API测试
测试网站生成和管理API接口
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from datetime import datetime

from backend.main import app
from backend.models.resume import (
    ResumeData, PersonalInfo, WorkExperience, Education, Skill,
    WebsiteConfig, ColorScheme, SkillCategory, SkillLevel
)


@pytest.fixture
def client():
    """创建测试客户端"""
    return TestClient(app)


@pytest.fixture
def sample_resume_data():
    """创建示例简历数据"""
    return {
        "id": "test-resume-123",
        "personal_info": {
            "name": "张三",
            "email": "zhangsan@example.com",
            "phone": "13800138000",
            "location": "北京市",
            "summary": "资深软件工程师，专注于Web开发和人工智能应用",
            "linkedin": "https://linkedin.com/in/zhangsan",
            "github": "https://github.com/zhangsan"
        },
        "work_experience": [
            {
                "company": "科技有限公司",
                "position": "高级软件工程师",
                "start_date": "2020-01",
                "end_date": "2024-01",
                "description": [
                    "负责Web应用的前后端开发",
                    "参与系统架构设计和技术选型"
                ],
                "technologies": ["Python", "JavaScript", "React"]
            }
        ],
        "education": [
            {
                "institution": "清华大学",
                "degree": "计算机科学与技术学士",
                "major": "计算机科学与技术",
                "start_date": "2014-09",
                "end_date": "2018-06",
                "gpa": "3.8"
            }
        ],
        "skills": [
            {
                "category": "technical",
                "name": "Python",
                "level": "expert"
            }
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }


class TestWebsiteAPI:
    """网站API测试类"""
    
    @patch('backend.api.website.RedisDataManager')
    @patch('backend.api.website.WebsiteGenerator')
    def test_generate_website_success(self, mock_generator_class, mock_redis_class, client, sample_resume_data):
        """测试成功生成网站"""
        # 模拟Redis管理器
        mock_redis = AsyncMock()
        mock_redis.get_resume.return_value = sample_resume_data
        mock_redis.save_website_config.return_value = "test-website-456"
        mock_redis_class.return_value = mock_redis
        
        # 模拟网站生成器
        mock_generator = AsyncMock()
        mock_generation_result = AsyncMock()
        mock_generation_result.success = True
        mock_generator.generate_website.return_value = mock_generation_result
        mock_generator_class.return_value = mock_generator
        
        # 发送请求
        response = client.post("/api/generate-website", json={
            "resume_id": "test-resume-123",
            "template_id": "modern",
            "is_public": True
        })
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "website_id" in data
        assert "website_url" in data
        assert "preview_url" in data
        assert data["message"] == "网站生成成功"
    
    @patch('backend.api.website.RedisDataManager')
    def test_generate_website_resume_not_found(self, mock_redis_class, client):
        """测试简历不存在的情况"""
        # 模拟Redis管理器返回None
        mock_redis = AsyncMock()
        mock_redis.get_resume.return_value = None
        mock_redis_class.return_value = mock_redis
        
        # 发送请求
        response = client.post("/api/generate-website", json={
            "resume_id": "nonexistent-resume",
            "template_id": "modern"
        })
        
        # 验证响应
        assert response.status_code == 404
        data = response.json()
        assert "简历不存在" in data["detail"]
    
    @patch('backend.api.website.RedisDataManager')
    def test_get_website_info_success(self, mock_redis_class, client):
        """测试成功获取网站信息"""
        # 模拟网站配置数据
        website_config_data = {
            "id": "test-website-456",
            "resume_id": "test-resume-123",
            "template_id": "modern",
            "color_scheme": {
                "primary": "#3B82F6",
                "secondary": "#6B7280",
                "accent": "#10B981",
                "background": "#FFFFFF",
                "text": "#1F2937"
            },
            "url": "/website/test-website-456",
            "is_public": True,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # 模拟Redis管理器
        mock_redis = AsyncMock()
        mock_redis.get_website_config.return_value = website_config_data
        mock_redis_class.return_value = mock_redis
        
        # 发送请求
        response = client.get("/api/website/test-website-456")
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert data["website_id"] == "test-website-456"
        assert data["resume_id"] == "test-resume-123"
        assert data["template_id"] == "modern"
        assert data["is_public"] is True
    
    @patch('backend.api.website.RedisDataManager')
    def test_get_website_info_not_found(self, mock_redis_class, client):
        """测试网站不存在的情况"""
        # 模拟Redis管理器返回None
        mock_redis = AsyncMock()
        mock_redis.get_website_config.return_value = None
        mock_redis_class.return_value = mock_redis
        
        # 发送请求
        response = client.get("/api/website/nonexistent-website")
        
        # 验证响应
        assert response.status_code == 404
        data = response.json()
        assert "网站不存在" in data["detail"]
    
    @patch('backend.api.website.RedisDataManager')
    @patch('backend.api.website.WebsiteGenerator')
    def test_update_website_success(self, mock_generator_class, mock_redis_class, client, sample_resume_data):
        """测试成功更新网站"""
        # 模拟现有网站配置
        existing_config = {
            "id": "test-website-456",
            "resume_id": "test-resume-123",
            "template_id": "modern",
            "color_scheme": {
                "primary": "#3B82F6",
                "secondary": "#6B7280",
                "accent": "#10B981",
                "background": "#FFFFFF",
                "text": "#1F2937"
            },
            "url": "/website/test-website-456",
            "is_public": True,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # 模拟Redis管理器
        mock_redis = AsyncMock()
        mock_redis.get_website_config.return_value = existing_config
        mock_redis.get_resume.return_value = sample_resume_data
        mock_redis.save_website_config.return_value = "test-website-456"
        mock_redis_class.return_value = mock_redis
        
        # 模拟网站生成器
        mock_generator = AsyncMock()
        mock_generation_result = AsyncMock()
        mock_generation_result.success = True
        mock_generator.generate_website.return_value = mock_generation_result
        mock_generator_class.return_value = mock_generator
        
        # 发送更新请求
        response = client.put("/api/website/test-website-456", json={
            "template_id": "professional"
        })
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["website_id"] == "test-website-456"
        assert data["message"] == "网站更新成功"
    
    def test_get_available_templates(self, client):
        """测试获取可用模板"""
        response = client.get("/api/templates")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "templates" in data
        assert len(data["templates"]) > 0
        
        # 检查模板结构
        template = data["templates"][0]
        assert "id" in template
        assert "name" in template
        assert "description" in template
        assert "features" in template
    
    def test_get_predefined_color_schemes(self, client):
        """测试获取预定义颜色方案"""
        response = client.get("/api/color-schemes")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "color_schemes" in data
        assert len(data["color_schemes"]) > 0
        
        # 检查颜色方案结构
        scheme = data["color_schemes"][0]
        assert "id" in scheme
        assert "name" in scheme
        assert "scheme" in scheme
        
        # 检查颜色方案内容
        colors = scheme["scheme"]
        assert "primary" in colors
        assert "secondary" in colors
        assert "accent" in colors
        assert "background" in colors
        assert "text" in colors
    
    @patch('backend.api.website.RedisDataManager')
    def test_get_websites_by_resume(self, mock_redis_class, client, sample_resume_data):
        """测试获取简历关联的网站"""
        # 模拟网站配置数据
        website_configs = [
            {
                "id": "website-1",
                "template_id": "modern",
                "url": "/website/website-1",
                "is_public": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "website-2",
                "template_id": "professional",
                "url": "/website/website-2",
                "is_public": False,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        ]
        
        # 模拟Redis管理器
        mock_redis = AsyncMock()
        mock_redis.get_resume.return_value = sample_resume_data
        mock_redis.get_websites_by_resume.return_value = ["website-1", "website-2"]
        mock_redis.get_website_config.side_effect = website_configs
        mock_redis_class.return_value = mock_redis
        
        # 发送请求
        response = client.get("/api/websites/by-resume/test-resume-123")
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["resume_id"] == "test-resume-123"
        assert len(data["websites"]) == 2
        assert data["total_count"] == 2


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])
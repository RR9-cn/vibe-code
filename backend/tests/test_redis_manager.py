"""
Redis数据管理器测试
测试RedisStack数据存储和检索功能
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, patch

from services.redis_manager import RedisDataManager, KnowledgeBaseManager
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


@pytest.fixture
def sample_resume_data():
    """创建示例简历数据"""
    personal_info = PersonalInfo(
        name="测试用户",
        email="test@example.com",
        phone="13800138000",
        location="北京市",
        summary="测试简历"
    )
    
    work_exp = WorkExperience(
        company="测试公司",
        position="软件工程师",
        start_date="2020-01",
        end_date="2023-12",
        description=["负责后端开发", "优化系统性能"],
        technologies=["Python", "Redis"]
    )
    
    education = Education(
        institution="测试大学",
        degree="学士",
        major="计算机科学",
        start_date="2016-09",
        end_date="2020-06"
    )
    
    skill = Skill(
        category=SkillCategory.TECHNICAL,
        name="Python",
        level=SkillLevel.ADVANCED
    )
    
    resume = ResumeData(
        id="test_resume_001",
        personal_info=personal_info,
        work_experience=[work_exp],
        education=[education],
        skills=[skill]
    )
    
    return resume


@pytest.fixture
def sample_website_config():
    """创建示例网站配置"""
    color_scheme = ColorScheme(
        primary="#3B82F6",
        secondary="#64748B",
        accent="#F59E0B",
        background="#FFFFFF",
        text="#1F2937"
    )
    
    config = WebsiteConfig(
        id="test_website_001",
        resume_id="test_resume_001",
        template_id="modern_template",
        color_scheme=color_scheme,
        url="https://test.com/user"
    )
    
    return config


class TestRedisDataManager:
    """Redis数据管理器测试类"""
    
    @pytest.fixture
    def mock_redis_client(self):
        """模拟Redis客户端"""
        mock_client = Mock()
        mock_client.ping.return_value = True
        mock_client.json.return_value = Mock()
        mock_client.sadd.return_value = 1
        mock_client.hset.return_value = 1
        mock_client.smembers.return_value = set()
        mock_client.scard.return_value = 0
        mock_client.info.return_value = {"used_memory_human": "1MB"}
        return mock_client
    
    @patch('services.redis_manager.redis.from_url')
    def test_redis_manager_init_success(self, mock_redis_from_url, mock_redis_client):
        """测试Redis管理器初始化成功"""
        mock_redis_from_url.return_value = mock_redis_client
        
        manager = RedisDataManager("redis://localhost:6379")
        
        assert manager.redis_client == mock_redis_client
        mock_redis_client.ping.assert_called_once()
    
    @patch('services.redis_manager.redis.from_url')
    def test_redis_manager_init_failure(self, mock_redis_from_url):
        """测试Redis管理器初始化失败"""
        mock_redis_from_url.side_effect = Exception("连接失败")
        
        with pytest.raises(Exception):
            RedisDataManager("redis://invalid:6379")
    
    @patch('services.redis_manager.redis.from_url')
    @pytest.mark.asyncio
    async def test_save_resume(self, mock_redis_from_url, mock_redis_client, sample_resume_data):
        """测试保存简历数据"""
        mock_redis_from_url.return_value = mock_redis_client
        manager = RedisDataManager()
        
        result = await manager.save_resume(sample_resume_data)
        
        assert result == sample_resume_data.id
        mock_redis_client.json().set.assert_called_once()
        mock_redis_client.sadd.assert_called()
        mock_redis_client.hset.assert_called()
    
    @patch('services.redis_manager.redis.from_url')
    @pytest.mark.asyncio
    async def test_get_resume(self, mock_redis_from_url, mock_redis_client):
        """测试获取简历数据"""
        mock_redis_from_url.return_value = mock_redis_client
        mock_redis_client.json().get.return_value = {"id": "test_resume_001", "name": "测试用户"}
        
        manager = RedisDataManager()
        result = await manager.get_resume("test_resume_001")
        
        assert result is not None
        assert result["id"] == "test_resume_001"
        mock_redis_client.json().get.assert_called_once()
    
    @patch('services.redis_manager.redis.from_url')
    @pytest.mark.asyncio
    async def test_get_resume_not_found(self, mock_redis_from_url, mock_redis_client):
        """测试获取不存在的简历数据"""
        mock_redis_from_url.return_value = mock_redis_client
        mock_redis_client.json().get.return_value = None
        
        manager = RedisDataManager()
        result = await manager.get_resume("nonexistent_resume")
        
        assert result is None
    
    @patch('services.redis_manager.redis.from_url')
    @pytest.mark.asyncio
    async def test_update_resume(self, mock_redis_from_url, mock_redis_client, sample_resume_data):
        """测试更新简历数据"""
        mock_redis_from_url.return_value = mock_redis_client
        manager = RedisDataManager()
        
        original_updated_at = sample_resume_data.updated_at
        # 等待一小段时间确保时间戳不同
        import time
        time.sleep(0.001)
        
        result = await manager.update_resume(sample_resume_data)
        
        assert result is True
        assert sample_resume_data.updated_at >= original_updated_at
    
    @patch('services.redis_manager.redis.from_url')
    @pytest.mark.asyncio
    async def test_delete_resume(self, mock_redis_from_url, mock_redis_client):
        """测试删除简历数据"""
        mock_redis_from_url.return_value = mock_redis_client
        manager = RedisDataManager()
        
        result = await manager.delete_resume("test_resume_001")
        
        assert result is True
        mock_redis_client.json().delete.assert_called()
        mock_redis_client.delete.assert_called()
        mock_redis_client.srem.assert_called()
    
    @patch('services.redis_manager.redis.from_url')
    @pytest.mark.asyncio
    async def test_search_resumes_by_text(self, mock_redis_from_url, mock_redis_client):
        """测试文本搜索简历"""
        mock_redis_from_url.return_value = mock_redis_client
        mock_redis_client.smembers.return_value = {"test_resume_001", "test_resume_002"}
        mock_redis_client.hgetall.return_value = {"content": "Python 开发工程师"}
        
        manager = RedisDataManager()
        result = await manager.search_resumes_by_text("Python")
        
        assert isinstance(result, list)
        mock_redis_client.smembers.assert_called_with("resumes:all")
    
    @patch('services.redis_manager.redis.from_url')
    @pytest.mark.asyncio
    async def test_search_resumes_by_skill(self, mock_redis_from_url, mock_redis_client):
        """测试技能搜索简历"""
        mock_redis_from_url.return_value = mock_redis_client
        mock_redis_client.smembers.side_effect = [
            {"test_resume_001", "test_resume_002"},  # resumes:all
            {"Python", "Java"},  # resume:skills:test_resume_001
            {"JavaScript"}       # resume:skills:test_resume_002
        ]
        
        manager = RedisDataManager()
        result = await manager.search_resumes_by_skill("Python")
        
        assert isinstance(result, list)
    
    @patch('services.redis_manager.redis.from_url')
    @pytest.mark.asyncio
    async def test_save_website_config(self, mock_redis_from_url, mock_redis_client, sample_website_config):
        """测试保存网站配置"""
        mock_redis_from_url.return_value = mock_redis_client
        manager = RedisDataManager()
        
        result = await manager.save_website_config(sample_website_config)
        
        assert result == sample_website_config.id
        mock_redis_client.json().set.assert_called()
        mock_redis_client.sadd.assert_called()
    
    @patch('services.redis_manager.redis.from_url')
    @pytest.mark.asyncio
    async def test_get_database_stats(self, mock_redis_from_url, mock_redis_client):
        """测试获取数据库统计信息"""
        mock_redis_from_url.return_value = mock_redis_client
        mock_redis_client.scard.return_value = 5
        mock_redis_client.info.side_effect = [
            {"used_memory_human": "10MB"},
            {"connected_clients": 2},
            {"uptime_in_seconds": 3600}
        ]
        
        manager = RedisDataManager()
        result = await manager.get_database_stats()
        
        assert isinstance(result, dict)
        assert "total_resumes" in result
        assert "redis_info" in result
        assert "skills_by_category" in result
    
    def test_extract_text_for_search(self, sample_resume_data):
        """测试提取搜索文本功能"""
        manager = RedisDataManager.__new__(RedisDataManager)  # 不调用__init__
        
        text = manager._extract_text_for_search(sample_resume_data)
        
        assert isinstance(text, str)
        assert "测试用户" in text
        assert "测试公司" in text
        assert "Python" in text
        assert "软件工程师" in text


class TestKnowledgeBaseManager:
    """知识库管理器测试类"""
    
    def test_knowledge_base_manager_init(self):
        """测试知识库管理器初始化"""
        mock_redis_client = Mock()
        
        kb_manager = KnowledgeBaseManager(mock_redis_client)
        
        assert kb_manager.redis_client == mock_redis_client
    
    @pytest.mark.asyncio
    async def test_add_document_embedding(self):
        """测试添加文档向量嵌入（预留功能）"""
        mock_redis_client = Mock()
        kb_manager = KnowledgeBaseManager(mock_redis_client)
        
        # 这是预留功能，目前只测试不抛出异常
        await kb_manager.add_document_embedding("doc_001", [0.1, 0.2, 0.3])
    
    @pytest.mark.asyncio
    async def test_semantic_search(self):
        """测试语义搜索（预留功能）"""
        mock_redis_client = Mock()
        kb_manager = KnowledgeBaseManager(mock_redis_client)
        
        result = await kb_manager.semantic_search([0.1, 0.2, 0.3])
        
        assert isinstance(result, list)
        assert len(result) == 0  # 预留功能返回空列表
    
    @pytest.mark.asyncio
    async def test_build_knowledge_graph(self):
        """测试构建知识图谱（预留功能）"""
        mock_redis_client = Mock()
        kb_manager = KnowledgeBaseManager(mock_redis_client)
        
        # 这是预留功能，目前只测试不抛出异常
        await kb_manager.build_knowledge_graph(["resume_001", "resume_002"])


if __name__ == "__main__":
    pytest.main([__file__])
"""
RedisStack数据管理器
实现简历数据的存储、检索和搜索功能
支持JSON存储、全文搜索和知识库扩展
"""

import redis
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from redis.commands.json.path import Path

from models.resume import ResumeData, WebsiteConfig


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RedisDataManager:
    """RedisStack数据管理器类"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379", **kwargs):
        """
        初始化Redis连接
        
        Args:
            redis_url: Redis连接URL
            **kwargs: 其他Redis连接参数
        """
        try:
            self.redis_client = redis.from_url(
                redis_url, 
                decode_responses=True,
                health_check_interval=30,
                **kwargs
            )
            # 测试连接
            self.redis_client.ping()
            logger.info(f"成功连接到Redis: {redis_url}")
        except Exception as e:
            logger.error(f"Redis连接失败: {e}")
            raise
    
    async def save_resume(self, resume_data: ResumeData) -> str:
        """
        保存简历数据到RedisJSON
        
        Args:
            resume_data: 简历数据对象
            
        Returns:
            str: 简历ID
        """
        try:
            resume_key = f"resume:{resume_data.id}"
            resume_dict = resume_data.model_dump()
            
            # 使用RedisJSON存储结构化数据
            self.redis_client.json().set(resume_key, Path.root_path(), resume_dict)
            
            # 创建索引用于搜索
            self.redis_client.sadd("resumes:all", resume_data.id)
            
            # 为知识库功能预留：存储文本内容用于搜索
            text_content = self._extract_text_for_search(resume_data)
            self.redis_client.hset(f"resume:text:{resume_data.id}", mapping={
                "content": text_content,
                "created_at": resume_data.created_at.isoformat(),
                "name": resume_data.personal_info.name,
                "email": resume_data.personal_info.email
            })
            
            # 建立技能索引
            for skill in resume_data.skills:
                self.redis_client.sadd(f"skills:{skill.category.value}", skill.name)
                self.redis_client.sadd(f"resume:skills:{resume_data.id}", skill.name)
            
            # 建立公司索引
            for exp in resume_data.work_experience:
                self.redis_client.sadd("companies:all", exp.company)
                self.redis_client.sadd(f"resume:companies:{resume_data.id}", exp.company)
            
            logger.info(f"简历数据保存成功: {resume_data.id}")
            return resume_data.id
            
        except Exception as e:
            logger.error(f"保存简历数据失败: {e}")
            raise
    
    async def get_resume(self, resume_id: str) -> Optional[Dict[str, Any]]:
        """
        从RedisJSON获取简历数据
        
        Args:
            resume_id: 简历ID
            
        Returns:
            Dict[str, Any]: 简历数据字典，如果不存在返回None
        """
        try:
            resume_key = f"resume:{resume_id}"
            resume_data = self.redis_client.json().get(resume_key)
            
            if resume_data:
                logger.info(f"成功获取简历数据: {resume_id}")
            else:
                logger.warning(f"简历数据不存在: {resume_id}")
            
            return resume_data
            
        except Exception as e:
            logger.error(f"获取简历数据失败: {e}")
            raise
    
    async def update_resume(self, resume_data: ResumeData) -> bool:
        """
        更新简历数据
        
        Args:
            resume_data: 更新后的简历数据
            
        Returns:
            bool: 更新是否成功
        """
        try:
            # 更新时间戳
            resume_data.updated_at = datetime.now()
            
            # 保存更新后的数据
            await self.save_resume(resume_data)
            
            logger.info(f"简历数据更新成功: {resume_data.id}")
            return True
            
        except Exception as e:
            logger.error(f"更新简历数据失败: {e}")
            return False
    
    async def delete_resume(self, resume_id: str) -> bool:
        """
        删除简历数据
        
        Args:
            resume_id: 简历ID
            
        Returns:
            bool: 删除是否成功
        """
        try:
            resume_key = f"resume:{resume_id}"
            text_key = f"resume:text:{resume_id}"
            skills_key = f"resume:skills:{resume_id}"
            companies_key = f"resume:companies:{resume_id}"
            
            # 删除主要数据
            self.redis_client.json().delete(resume_key)
            self.redis_client.delete(text_key)
            self.redis_client.delete(skills_key)
            self.redis_client.delete(companies_key)
            
            # 从索引中移除
            self.redis_client.srem("resumes:all", resume_id)
            
            logger.info(f"简历数据删除成功: {resume_id}")
            return True
            
        except Exception as e:
            logger.error(f"删除简历数据失败: {e}")
            return False
    
    async def search_resumes_by_text(self, query: str, limit: int = 10) -> List[str]:
        """
        使用文本搜索简历
        
        Args:
            query: 搜索查询
            limit: 返回结果数量限制
            
        Returns:
            List[str]: 匹配的简历ID列表
        """
        try:
            matching_resumes = []
            all_resume_ids = self.redis_client.smembers("resumes:all")
            
            query_lower = query.lower()
            
            for resume_id in all_resume_ids:
                text_key = f"resume:text:{resume_id}"
                text_data = self.redis_client.hgetall(text_key)
                
                if text_data and "content" in text_data:
                    content = text_data["content"].lower()
                    if query_lower in content:
                        matching_resumes.append(resume_id)
                        
                        if len(matching_resumes) >= limit:
                            break
            
            logger.info(f"文本搜索完成，找到 {len(matching_resumes)} 个匹配结果")
            return matching_resumes
            
        except Exception as e:
            logger.error(f"文本搜索失败: {e}")
            return []
    
    async def search_resumes_by_skill(self, skill_name: str) -> List[str]:
        """
        根据技能搜索简历
        
        Args:
            skill_name: 技能名称
            
        Returns:
            List[str]: 拥有该技能的简历ID列表
        """
        try:
            matching_resumes = []
            all_resume_ids = self.redis_client.smembers("resumes:all")
            
            for resume_id in all_resume_ids:
                skills_key = f"resume:skills:{resume_id}"
                resume_skills = self.redis_client.smembers(skills_key)
                
                if skill_name in resume_skills:
                    matching_resumes.append(resume_id)
            
            logger.info(f"技能搜索完成，找到 {len(matching_resumes)} 个匹配结果")
            return matching_resumes
            
        except Exception as e:
            logger.error(f"技能搜索失败: {e}")
            return []
    
    async def search_resumes_by_company(self, company_name: str) -> List[str]:
        """
        根据公司搜索简历
        
        Args:
            company_name: 公司名称
            
        Returns:
            List[str]: 在该公司工作过的简历ID列表
        """
        try:
            matching_resumes = []
            all_resume_ids = self.redis_client.smembers("resumes:all")
            
            for resume_id in all_resume_ids:
                companies_key = f"resume:companies:{resume_id}"
                resume_companies = self.redis_client.smembers(companies_key)
                
                if company_name in resume_companies:
                    matching_resumes.append(resume_id)
            
            logger.info(f"公司搜索完成，找到 {len(matching_resumes)} 个匹配结果")
            return matching_resumes
            
        except Exception as e:
            logger.error(f"公司搜索失败: {e}")
            return []
    
    async def get_all_skills(self) -> Dict[str, List[str]]:
        """
        获取所有技能分类和技能列表
        
        Returns:
            Dict[str, List[str]]: 按分类组织的技能字典
        """
        try:
            skills_by_category = {}
            
            # 获取所有技能分类
            categories = ["technical", "soft", "language"]
            
            for category in categories:
                skills_key = f"skills:{category}"
                skills = list(self.redis_client.smembers(skills_key))
                if skills:
                    skills_by_category[category] = sorted(skills)
            
            logger.info(f"获取技能列表成功，共 {len(skills_by_category)} 个分类")
            return skills_by_category
            
        except Exception as e:
            logger.error(f"获取技能列表失败: {e}")
            return {}
    
    async def get_all_companies(self) -> List[str]:
        """
        获取所有公司列表
        
        Returns:
            List[str]: 公司名称列表
        """
        try:
            companies = list(self.redis_client.smembers("companies:all"))
            companies.sort()
            
            logger.info(f"获取公司列表成功，共 {len(companies)} 家公司")
            return companies
            
        except Exception as e:
            logger.error(f"获取公司列表失败: {e}")
            return []
    
    async def save_website_config(self, website_config: WebsiteConfig) -> str:
        """
        保存网站配置
        
        Args:
            website_config: 网站配置对象
            
        Returns:
            str: 网站配置ID
        """
        try:
            config_key = f"website:{website_config.id}"
            config_dict = website_config.model_dump()
            
            # 使用RedisJSON存储配置
            self.redis_client.json().set(config_key, Path.root_path(), config_dict)
            
            # 建立简历和网站的关联
            self.redis_client.sadd(f"resume:websites:{website_config.resume_id}", website_config.id)
            self.redis_client.sadd("websites:all", website_config.id)
            
            logger.info(f"网站配置保存成功: {website_config.id}")
            return website_config.id
            
        except Exception as e:
            logger.error(f"保存网站配置失败: {e}")
            raise
    
    async def get_website_config(self, website_id: str) -> Optional[Dict[str, Any]]:
        """
        获取网站配置
        
        Args:
            website_id: 网站ID
            
        Returns:
            Dict[str, Any]: 网站配置字典，如果不存在返回None
        """
        try:
            config_key = f"website:{website_id}"
            config_data = self.redis_client.json().get(config_key)
            
            if config_data:
                logger.info(f"成功获取网站配置: {website_id}")
            else:
                logger.warning(f"网站配置不存在: {website_id}")
            
            return config_data
            
        except Exception as e:
            logger.error(f"获取网站配置失败: {e}")
            raise
    
    async def get_websites_by_resume(self, resume_id: str) -> List[str]:
        """
        获取简历关联的所有网站
        
        Args:
            resume_id: 简历ID
            
        Returns:
            List[str]: 网站ID列表
        """
        try:
            websites_key = f"resume:websites:{resume_id}"
            website_ids = list(self.redis_client.smembers(websites_key))
            
            logger.info(f"获取简历关联网站成功: {resume_id}, 共 {len(website_ids)} 个网站")
            return website_ids
            
        except Exception as e:
            logger.error(f"获取简历关联网站失败: {e}")
            return []
    
    async def get_database_stats(self) -> Dict[str, Any]:
        """
        获取数据库统计信息
        
        Returns:
            Dict[str, Any]: 统计信息字典
        """
        try:
            stats = {
                "total_resumes": self.redis_client.scard("resumes:all"),
                "total_websites": self.redis_client.scard("websites:all"),
                "total_companies": self.redis_client.scard("companies:all"),
                "redis_info": {
                    "used_memory": self.redis_client.info("memory")["used_memory_human"],
                    "connected_clients": self.redis_client.info("clients")["connected_clients"],
                    "uptime_in_seconds": self.redis_client.info("server")["uptime_in_seconds"]
                }
            }
            
            # 获取技能统计
            skills_stats = {}
            for category in ["technical", "soft", "language"]:
                skills_key = f"skills:{category}"
                skills_stats[category] = self.redis_client.scard(skills_key)
            stats["skills_by_category"] = skills_stats
            
            logger.info("数据库统计信息获取成功")
            return stats
            
        except Exception as e:
            logger.error(f"获取数据库统计信息失败: {e}")
            return {}
    
    def _extract_text_for_search(self, resume_data: ResumeData) -> str:
        """
        提取简历文本用于搜索索引
        
        Args:
            resume_data: 简历数据对象
            
        Returns:
            str: 用于搜索的文本内容
        """
        text_parts = [
            resume_data.personal_info.name,
            resume_data.personal_info.summary or "",
            resume_data.personal_info.location or "",
        ]
        
        # 添加工作经历文本
        for exp in resume_data.work_experience:
            text_parts.extend([exp.company, exp.position])
            text_parts.extend(exp.description)
            if exp.technologies:
                text_parts.extend(exp.technologies)
        
        # 添加教育背景文本
        for edu in resume_data.education:
            text_parts.extend([edu.institution, edu.degree, edu.major or ""])
        
        # 添加技能文本
        for skill in resume_data.skills:
            text_parts.append(skill.name)
        
        return " ".join(filter(None, text_parts))
    
    def close(self):
        """关闭Redis连接"""
        try:
            self.redis_client.close()
            logger.info("Redis连接已关闭")
        except Exception as e:
            logger.error(f"关闭Redis连接失败: {e}")


# 知识库扩展预留类
class KnowledgeBaseManager:
    """为未来知识库功能预留的管理器"""
    
    def __init__(self, redis_client: redis.Redis):
        """
        初始化知识库管理器
        
        Args:
            redis_client: Redis客户端实例
        """
        self.redis_client = redis_client
        logger.info("知识库管理器初始化完成")
    
    async def add_document_embedding(self, doc_id: str, embedding: List[float]):
        """
        存储文档向量嵌入（使用Redis Vector Similarity Search）
        
        Args:
            doc_id: 文档ID
            embedding: 向量嵌入
        """
        # TODO: 实现向量嵌入存储
        # 使用RedisStack的向量搜索功能
        logger.info(f"向量嵌入存储功能待实现: {doc_id}")
        pass
    
    async def semantic_search(self, query_embedding: List[float], top_k: int = 5) -> List[str]:
        """
        语义搜索相关简历
        
        Args:
            query_embedding: 查询向量
            top_k: 返回结果数量
            
        Returns:
            List[str]: 相关文档ID列表
        """
        # TODO: 实现向量相似度搜索
        logger.info("语义搜索功能待实现")
        return []
    
    async def build_knowledge_graph(self, resume_ids: List[str]):
        """
        构建简历知识图谱
        
        Args:
            resume_ids: 简历ID列表
        """
        # TODO: 使用RedisGraph构建关系图谱
        logger.info(f"知识图谱构建功能待实现，涉及 {len(resume_ids)} 个简历")
        pass
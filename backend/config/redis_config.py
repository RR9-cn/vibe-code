"""
Redis配置文件
定义Redis连接参数和配置选项
"""

import os
from typing import Dict, Any


# Redis连接配置
REDIS_CONFIG: Dict[str, Any] = {
    "url": os.getenv("REDIS_URL", "redis://localhost:6379"),
    "decode_responses": True,
    "health_check_interval": 30,
    "socket_connect_timeout": 5,
    "socket_timeout": 5,
    "retry_on_timeout": True,
    "max_connections": 20
}

# RedisStack特性配置
REDIS_FEATURES = {
    "json_enabled": True,
    "search_enabled": True,
    "graph_enabled": True,
    "vector_enabled": True
}

# 数据键前缀配置
KEY_PREFIXES = {
    "resume": "resume:",
    "website": "website:",
    "resume_text": "resume:text:",
    "resume_skills": "resume:skills:",
    "resume_companies": "resume:companies:",
    "resume_websites": "resume:websites:",
    "skills_category": "skills:",
    "resumes_all": "resumes:all",
    "websites_all": "websites:all",
    "companies_all": "companies:all"
}

# 搜索配置
SEARCH_CONFIG = {
    "max_results": 100,
    "default_limit": 10,
    "text_search_timeout": 5000,  # 毫秒
    "vector_search_timeout": 3000  # 毫秒
}

# 缓存配置
CACHE_CONFIG = {
    "default_ttl": 3600,  # 1小时
    "resume_ttl": 7200,   # 2小时
    "website_ttl": 3600,  # 1小时
    "search_ttl": 300     # 5分钟
}

# 知识库配置（预留）
KNOWLEDGE_BASE_CONFIG = {
    "embedding_dimension": 768,  # 向量维度
    "similarity_threshold": 0.7,  # 相似度阈值
    "max_graph_nodes": 10000,    # 图数据库最大节点数
    "max_graph_edges": 50000     # 图数据库最大边数
}


def get_redis_url() -> str:
    """
    获取Redis连接URL
    
    Returns:
        str: Redis连接URL
    """
    return REDIS_CONFIG["url"]


def get_redis_config() -> Dict[str, Any]:
    """
    获取完整的Redis配置
    
    Returns:
        Dict[str, Any]: Redis配置字典
    """
    return REDIS_CONFIG.copy()


def validate_redis_config() -> bool:
    """
    验证Redis配置的有效性
    
    Returns:
        bool: 配置是否有效
    """
    required_keys = ["url", "decode_responses"]
    
    for key in required_keys:
        if key not in REDIS_CONFIG:
            return False
    
    return True
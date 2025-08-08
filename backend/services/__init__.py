"""
服务层包初始化文件
包含数据管理、业务逻辑等服务类
"""

from .pdf_parser import PDFParser, PDFParseError
from .qwen_parser import QwenResumeParser, QwenParseError

# Redis管理器需要时再导入，避免循环依赖
# from .redis_manager import RedisDataManager, KnowledgeBaseManager

__all__ = [
    "PDFParser",
    "PDFParseError",
    "QwenResumeParser",
    "QwenParseError"
]
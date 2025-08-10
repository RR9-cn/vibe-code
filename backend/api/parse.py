"""
简历解析API接口
实现PDF简历的异步解析和状态跟踪功能
"""

import os
import uuid
import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import logging
from datetime import datetime

from backend.services.pdf_parser import PDFParser
from backend.services.qwen_parser import QwenResumeParser
from backend.services.redis_manager import RedisDataManager
from backend.models.resume import ResumeData

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter(prefix="/api", tags=["简历解析"])

# 全局存储解析状态（生产环境应使用Redis）
parse_status = {}

# 初始化服务
pdf_parser = PDFParser()
qwen_parser = QwenResumeParser()
redis_manager = RedisDataManager()

class ParseStatus:
    """解析状态类"""
    PENDING = "pending"
    EXTRACTING = "extracting"
    PARSING = "parsing"
    VALIDATING = "validating"
    SAVING = "saving"
    SUCCESS = "success"
    ERROR = "error"

async def update_parse_progress(parse_id: str, status: str, progress: int = 0, message: str = "", data: Optional[Dict] = None):
    """
    更新解析进度状态
    
    Args:
        parse_id: 解析任务ID
        status: 状态
        progress: 进度百分比
        message: 状态消息
        data: 解析结果数据
    """
    parse_status[parse_id] = {
        "status": status,
        "progress": progress,
        "message": message,
        "data": data,
        "updated_at": datetime.now().isoformat()
    }

async def parse_resume_background(parse_id: str, file_path: str, upload_id: str):
    """
    后台异步解析简历任务
    
    Args:
        parse_id: 解析任务ID
        file_path: PDF文件路径
        upload_id: 上传任务ID
    """
    try:
        logger.info(f"开始后台解析任务: {parse_id}")
        
        # 步骤1: 提取PDF文本
        await update_parse_progress(parse_id, ParseStatus.EXTRACTING, 20, "正在提取PDF文本内容")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        extracted_text = await pdf_parser.extract_text_from_pdf(file_path)
        
        if not extracted_text or len(extracted_text.strip()) < 50:
            raise ValueError("PDF文本提取失败或内容过少，请检查文件是否为有效的简历")
        
        logger.info(f"PDF文本提取成功，长度: {len(extracted_text)}")
        
        # 步骤2: AI解析结构化数据
        await update_parse_progress(parse_id, ParseStatus.PARSING, 50, "正在使用AI解析简历内容")
        
        parsed_data = await qwen_parser.parse_resume_text(extracted_text)
        
        if not parsed_data:
            raise ValueError("AI解析失败，请检查简历内容格式")
        
        logger.info("AI解析完成")
        
        # 步骤3: 数据验证和转换
        await update_parse_progress(parse_id, ParseStatus.VALIDATING, 70, "正在验证和格式化数据")
        
        # 生成简历ID
        resume_id = str(uuid.uuid4())
        parsed_data["id"] = resume_id
        parsed_data["created_at"] = datetime.now()
        parsed_data["updated_at"] = datetime.now()
        
        # 验证数据结构
        try:
            resume_data = ResumeData(**parsed_data)
        except Exception as e:
            logger.error(f"数据验证失败: {e}")
            raise ValueError(f"简历数据格式验证失败: {str(e)}")
        
        # 步骤4: 保存到数据库
        await update_parse_progress(parse_id, ParseStatus.SAVING, 90, "正在保存简历数据")
        
        saved_id = await redis_manager.save_resume(resume_data)
        
        if not saved_id:
            raise ValueError("简历数据保存失败")
        
        # 步骤5: 完成
        await update_parse_progress(
            parse_id, 
            ParseStatus.SUCCESS, 
            100, 
            "简历解析完成",
            {
                "resume_id": resume_id,
                "resume_data": resume_data.model_dump(),
                "upload_id": upload_id
            }
        )
        
        logger.info(f"简历解析任务完成: {parse_id}, 简历ID: {resume_id}")
        
    except FileNotFoundError as e:
        logger.error(f"文件不存在错误: {e}")
        await update_parse_progress(parse_id, ParseStatus.ERROR, 0, f"文件不存在: {str(e)}")
        
    except ValueError as e:
        logger.error(f"数据验证错误: {e}")
        await update_parse_progress(parse_id, ParseStatus.ERROR, 0, str(e))
        
    except Exception as e:
        logger.error(f"解析任务失败: {e}")
        await update_parse_progress(parse_id, ParseStatus.ERROR, 0, f"解析失败: {str(e)}")

@router.post("/parse/{upload_id}")
async def parse_resume(
    upload_id: str,
    background_tasks: BackgroundTasks
) -> JSONResponse:
    """
    开始解析简历接口
    
    Args:
        upload_id: 上传任务ID
        
    Returns:
        JSONResponse: 解析任务信息
    """
    # 导入上传状态（这里应该从实际的存储中获取）
    from backend.api.upload import upload_status
    
    # 检查上传任务是否存在
    if upload_id not in upload_status:
        raise HTTPException(
            status_code=404,
            detail="上传任务不存在，请先上传文件"
        )
    
    upload_info = upload_status[upload_id]
    
    # 检查上传是否成功
    if upload_info["status"] != "success":
        raise HTTPException(
            status_code=400,
            detail="文件上传未完成或失败，无法开始解析"
        )
    
    # 检查文件是否存在
    file_path = upload_info.get("file_path")
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="上传的文件不存在"
        )
    
    # 生成解析任务ID
    parse_id = str(uuid.uuid4())
    
    try:
        # 初始化解析状态
        await update_parse_progress(parse_id, ParseStatus.PENDING, 0, "解析任务已创建，等待开始")
        
        # 添加后台解析任务
        background_tasks.add_task(parse_resume_background, parse_id, file_path, upload_id)
        
        logger.info(f"解析任务已创建: {parse_id}, 上传ID: {upload_id}")
        
        return JSONResponse(
            status_code=200,
            content={
                "parse_id": parse_id,
                "upload_id": upload_id,
                "message": "解析任务已开始，请使用parse_id查询进度",
                "status_url": f"/api/parse/{parse_id}/status"
            }
        )
        
    except Exception as e:
        logger.error(f"创建解析任务失败: {e}")
        raise HTTPException(
            status_code=500,
            detail="创建解析任务失败，请重试"
        )

@router.get("/parse/{parse_id}/status")
async def get_parse_status(parse_id: str) -> JSONResponse:
    """
    获取解析状态接口
    
    Args:
        parse_id: 解析任务ID
        
    Returns:
        JSONResponse: 解析状态信息
    """
    if parse_id not in parse_status:
        raise HTTPException(
            status_code=404,
            detail="解析任务不存在"
        )
    
    status_info = parse_status[parse_id]
    
    # 构建响应数据
    response_data = {
        "parse_id": parse_id,
        "status": status_info["status"],
        "progress": status_info["progress"],
        "message": status_info["message"],
        "updated_at": status_info["updated_at"]
    }
    
    # 如果解析成功，包含简历数据
    if status_info["status"] == ParseStatus.SUCCESS and status_info["data"]:
        response_data["resume_id"] = status_info["data"]["resume_id"]
        response_data["resume_data"] = status_info["data"]["resume_data"]
    
    return JSONResponse(
        status_code=200,
        content=response_data
    )

@router.post("/parse/{parse_id}/retry")
async def retry_parse(
    parse_id: str,
    background_tasks: BackgroundTasks
) -> JSONResponse:
    """
    重试解析任务接口
    
    Args:
        parse_id: 解析任务ID
        
    Returns:
        JSONResponse: 重试结果
    """
    if parse_id not in parse_status:
        raise HTTPException(
            status_code=404,
            detail="解析任务不存在"
        )
    
    status_info = parse_status[parse_id]
    
    # 只有失败的任务才能重试
    if status_info["status"] != ParseStatus.ERROR:
        raise HTTPException(
            status_code=400,
            detail="只有失败的解析任务才能重试"
        )
    
    try:
        # 获取原始文件信息
        from backend.api.upload import upload_status
        
        # 从解析状态中获取上传ID（如果有的话）
        upload_id = None
        for uid, uinfo in upload_status.items():
            if uinfo.get("file_path") and "file_path" in status_info:
                upload_id = uid
                break
        
        if not upload_id:
            raise HTTPException(
                status_code=400,
                detail="无法找到原始上传文件信息"
            )
        
        upload_info = upload_status[upload_id]
        file_path = upload_info.get("file_path")
        
        if not file_path or not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail="原始文件不存在，无法重试"
            )
        
        # 重置解析状态
        await update_parse_progress(parse_id, ParseStatus.PENDING, 0, "准备重试解析")
        
        # 添加后台解析任务
        background_tasks.add_task(parse_resume_background, parse_id, file_path, upload_id)
        
        logger.info(f"解析任务重试: {parse_id}")
        
        return JSONResponse(
            status_code=200,
            content={
                "parse_id": parse_id,
                "message": "解析任务已重新开始",
                "status_url": f"/api/parse/{parse_id}/status"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"重试解析任务失败: {e}")
        raise HTTPException(
            status_code=500,
            detail="重试解析任务失败"
        )

@router.delete("/parse/{parse_id}")
async def delete_parse_task(parse_id: str) -> JSONResponse:
    """
    删除解析任务接口
    
    Args:
        parse_id: 解析任务ID
        
    Returns:
        JSONResponse: 删除结果
    """
    if parse_id not in parse_status:
        raise HTTPException(
            status_code=404,
            detail="解析任务不存在"
        )
    
    try:
        # 删除解析状态记录
        del parse_status[parse_id]
        
        logger.info(f"解析任务删除成功: {parse_id}")
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "解析任务删除成功",
                "parse_id": parse_id
            }
        )
        
    except Exception as e:
        logger.error(f"删除解析任务失败: {e}")
        raise HTTPException(
            status_code=500,
            detail="删除解析任务失败"
        )

@router.get("/parses")
async def list_parse_tasks() -> JSONResponse:
    """
    获取所有解析任务列表接口（用于调试）
    
    Returns:
        JSONResponse: 解析任务列表
    """
    tasks = []
    for parse_id, status_info in parse_status.items():
        task_info = {
            "parse_id": parse_id,
            "status": status_info["status"],
            "progress": status_info["progress"],
            "message": status_info["message"],
            "updated_at": status_info["updated_at"]
        }
        
        # 如果有简历数据，添加简历ID
        if status_info.get("data") and status_info["data"].get("resume_id"):
            task_info["resume_id"] = status_info["data"]["resume_id"]
        
        tasks.append(task_info)
    
    return JSONResponse(
        status_code=200,
        content={
            "total": len(tasks),
            "tasks": tasks
        }
    )
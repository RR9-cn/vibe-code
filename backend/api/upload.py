"""
文件上传API接口
实现PDF简历文件的上传、验证和存储功能
"""

import os
import uuid
import aiofiles
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging
from datetime import datetime
import mimetypes

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter(prefix="/api", tags=["文件上传"])

# 配置常量
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_MIME_TYPES = ["application/pdf"]
UPLOAD_DIR = "backend/uploads"

# 确保上传目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 全局存储上传状态（生产环境应使用Redis）
upload_status = {}

class UploadStatus:
    """上传状态类"""
    PENDING = "pending"
    UPLOADING = "uploading"
    SUCCESS = "success"
    ERROR = "error"

async def validate_pdf_file(file: UploadFile) -> Dict[str, Any]:
    """
    验证PDF文件的格式和大小
    
    Args:
        file: 上传的文件对象
        
    Returns:
        Dict[str, Any]: 验证结果
        
    Raises:
        HTTPException: 验证失败时抛出异常
    """
    # 检查文件大小
    if hasattr(file, 'size') and file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"文件大小超过限制，最大允许 {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    # 检查文件扩展名
    if not file.filename or not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="只支持PDF格式的文件"
        )
    
    # 检查MIME类型
    mime_type, _ = mimetypes.guess_type(file.filename)
    if mime_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail="文件格式不正确，请上传PDF文件"
        )
    
    # 读取文件头部验证PDF格式
    content = await file.read(1024)  # 读取前1KB
    await file.seek(0)  # 重置文件指针
    
    if not content.startswith(b'%PDF-'):
        raise HTTPException(
            status_code=400,
            detail="文件格式验证失败，请确保是有效的PDF文件"
        )
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content) if not hasattr(file, 'size') else file.size
    }

async def save_uploaded_file(file: UploadFile, upload_id: str) -> str:
    """
    保存上传的文件到本地存储
    
    Args:
        file: 上传的文件对象
        upload_id: 上传任务ID
        
    Returns:
        str: 保存的文件路径
    """
    # 生成安全的文件名
    file_extension = os.path.splitext(file.filename)[1]
    safe_filename = f"{upload_id}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    try:
        # 异步保存文件
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        logger.info(f"文件保存成功: {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"文件保存失败: {e}")
        raise HTTPException(
            status_code=500,
            detail="文件保存失败，请重试"
        )

async def update_upload_progress(upload_id: str, status: str, progress: int = 0, message: str = ""):
    """
    更新上传进度状态
    
    Args:
        upload_id: 上传任务ID
        status: 状态
        progress: 进度百分比
        message: 状态消息
    """
    upload_status[upload_id] = {
        "status": status,
        "progress": progress,
        "message": message,
        "updated_at": datetime.now().isoformat()
    }

@router.post("/upload")
async def upload_resume(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PDF简历文件")
) -> JSONResponse:
    """
    上传PDF简历文件接口
    
    Args:
        file: 上传的PDF文件
        
    Returns:
        JSONResponse: 包含上传ID和状态信息的响应
    """
    # 生成唯一的上传ID
    upload_id = str(uuid.uuid4())
    
    try:
        # 初始化上传状态
        await update_upload_progress(upload_id, UploadStatus.PENDING, 0, "开始处理文件")
        
        logger.info(f"开始处理文件上传: {file.filename}, 上传ID: {upload_id}")
        
        # 验证文件
        await update_upload_progress(upload_id, UploadStatus.UPLOADING, 20, "验证文件格式")
        file_info = await validate_pdf_file(file)
        
        # 保存文件
        await update_upload_progress(upload_id, UploadStatus.UPLOADING, 60, "保存文件")
        file_path = await save_uploaded_file(file, upload_id)
        
        # 更新状态为成功
        await update_upload_progress(upload_id, UploadStatus.SUCCESS, 100, "文件上传成功")
        
        # 存储文件信息
        upload_status[upload_id].update({
            "file_info": file_info,
            "file_path": file_path,
            "created_at": datetime.now().isoformat()
        })
        
        logger.info(f"文件上传成功: {upload_id}")
        
        return JSONResponse(
            status_code=200,
            content={
                "upload_id": upload_id,
                "message": "文件上传成功",
                "file_info": {
                    "filename": file_info["filename"],
                    "size": file_info["size"]
                }
            }
        )
        
    except HTTPException:
        # 重新抛出HTTP异常
        await update_upload_progress(upload_id, UploadStatus.ERROR, 0, "文件验证失败")
        raise
        
    except Exception as e:
        logger.error(f"文件上传失败: {e}")
        await update_upload_progress(upload_id, UploadStatus.ERROR, 0, f"上传失败: {str(e)}")
        
        raise HTTPException(
            status_code=500,
            detail="文件上传失败，请重试"
        )

@router.get("/upload/{upload_id}/status")
async def get_upload_status(upload_id: str) -> JSONResponse:
    """
    获取上传状态接口
    
    Args:
        upload_id: 上传任务ID
        
    Returns:
        JSONResponse: 上传状态信息
    """
    if upload_id not in upload_status:
        raise HTTPException(
            status_code=404,
            detail="上传任务不存在"
        )
    
    status_info = upload_status[upload_id]
    
    return JSONResponse(
        status_code=200,
        content={
            "upload_id": upload_id,
            "status": status_info["status"],
            "progress": status_info["progress"],
            "message": status_info["message"],
            "updated_at": status_info["updated_at"]
        }
    )

@router.delete("/upload/{upload_id}")
async def delete_upload(upload_id: str) -> JSONResponse:
    """
    删除上传文件接口
    
    Args:
        upload_id: 上传任务ID
        
    Returns:
        JSONResponse: 删除结果
    """
    if upload_id not in upload_status:
        raise HTTPException(
            status_code=404,
            detail="上传任务不存在"
        )
    
    try:
        # 删除文件
        status_info = upload_status[upload_id]
        if "file_path" in status_info and os.path.exists(status_info["file_path"]):
            os.remove(status_info["file_path"])
            logger.info(f"文件删除成功: {status_info['file_path']}")
        
        # 删除状态记录
        del upload_status[upload_id]
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "文件删除成功",
                "upload_id": upload_id
            }
        )
        
    except Exception as e:
        logger.error(f"文件删除失败: {e}")
        raise HTTPException(
            status_code=500,
            detail="文件删除失败"
        )

@router.get("/uploads")
async def list_uploads() -> JSONResponse:
    """
    获取所有上传任务列表接口（用于调试）
    
    Returns:
        JSONResponse: 上传任务列表
    """
    uploads = []
    for upload_id, status_info in upload_status.items():
        uploads.append({
            "upload_id": upload_id,
            "status": status_info["status"],
            "progress": status_info["progress"],
            "message": status_info["message"],
            "updated_at": status_info["updated_at"],
            "file_info": status_info.get("file_info", {})
        })
    
    return JSONResponse(
        status_code=200,
        content={
            "total": len(uploads),
            "uploads": uploads
        }
    )
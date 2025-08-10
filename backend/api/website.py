"""
网站生成和管理API
实现个人网站的生成、更新和配置管理功能
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import uuid
import logging
from datetime import datetime

from backend.models.resume import ResumeData, WebsiteConfig, ColorScheme
from backend.services.redis_manager import RedisDataManager
from backend.services.website_generator import WebsiteGenerator

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter(prefix="/api", tags=["website"])

# 依赖注入：Redis数据管理器
async def get_redis_manager() -> RedisDataManager:
    """获取Redis数据管理器实例"""
    return RedisDataManager()

# 依赖注入：网站生成器
async def get_website_generator() -> WebsiteGenerator:
    """获取网站生成器实例"""
    return WebsiteGenerator()


class WebsiteGenerationRequest(BaseModel):
    """网站生成请求模型"""
    resume_id: str = Field(..., description="简历ID")
    template_id: str = Field(default="modern", description="模板ID")
    color_scheme: Optional[ColorScheme] = Field(None, description="自定义颜色方案")
    is_public: bool = Field(default=True, description="是否公开访问")


class WebsiteGenerationResponse(BaseModel):
    """网站生成响应模型"""
    success: bool = Field(..., description="生成是否成功")
    website_id: str = Field(..., description="网站ID")
    website_url: str = Field(..., description="网站访问URL")
    preview_url: str = Field(..., description="预览URL")
    message: str = Field(..., description="响应消息")


class WebsiteUpdateRequest(BaseModel):
    """网站更新请求模型"""
    resume_id: Optional[str] = Field(None, description="新的简历ID")
    template_id: Optional[str] = Field(None, description="新的模板ID")
    color_scheme: Optional[ColorScheme] = Field(None, description="新的颜色方案")
    is_public: Optional[bool] = Field(None, description="是否公开访问")


class WebsiteUpdateResponse(BaseModel):
    """网站更新响应模型"""
    success: bool = Field(..., description="更新是否成功")
    website_id: str = Field(..., description="网站ID")
    website_url: str = Field(..., description="网站访问URL")
    message: str = Field(..., description="响应消息")


class WebsiteInfoResponse(BaseModel):
    """网站信息响应模型"""
    website_id: str = Field(..., description="网站ID")
    resume_id: str = Field(..., description="关联的简历ID")
    template_id: str = Field(..., description="模板ID")
    color_scheme: ColorScheme = Field(..., description="颜色方案")
    website_url: str = Field(..., description="网站访问URL")
    is_public: bool = Field(..., description="是否公开访问")
    created_at: str = Field(..., description="创建时间")
    updated_at: str = Field(..., description="更新时间")


@router.post("/generate-website", response_model=WebsiteGenerationResponse)
async def generate_website(
    request: WebsiteGenerationRequest,
    redis_manager: RedisDataManager = Depends(get_redis_manager),
    website_generator: WebsiteGenerator = Depends(get_website_generator)
):
    """
    生成个人网站
    
    根据简历数据生成具有现代化设计风格的个人网站
    支持自定义模板和颜色方案
    """
    try:
        logger.info(f"开始生成网站，简历ID: {request.resume_id}")
        
        # 1. 验证简历是否存在
        resume_data_dict = await redis_manager.get_resume(request.resume_id)
        if not resume_data_dict:
            raise HTTPException(
                status_code=404,
                detail=f"简历不存在: {request.resume_id}"
            )
        
        # 2. 转换为ResumeData对象
        resume_data = ResumeData(**resume_data_dict)
        
        # 3. 生成网站ID和URL
        website_id = str(uuid.uuid4())
        website_url = f"/website/{website_id}"
        preview_url = f"/preview/{website_id}"
        
        # 4. 设置默认颜色方案（如果未提供）
        if not request.color_scheme:
            color_scheme = ColorScheme(
                primary="#3B82F6",      # 蓝色
                secondary="#6B7280",    # 灰色
                accent="#10B981",       # 绿色
                background="#FFFFFF",   # 白色
                text="#1F2937"          # 深灰色
            )
        else:
            color_scheme = request.color_scheme
        
        # 5. 创建网站配置
        website_config = WebsiteConfig(
            id=website_id,
            resume_id=request.resume_id,
            template_id=request.template_id,
            color_scheme=color_scheme,
            url=website_url,
            is_public=request.is_public,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # 6. 保存网站配置到Redis
        await redis_manager.save_website_config(website_config)
        
        # 7. 生成静态网站文件
        generation_result = await website_generator.generate_website(
            resume_data=resume_data,
            website_config=website_config
        )
        
        if not generation_result.success:
            raise HTTPException(
                status_code=500,
                detail=f"网站生成失败: {generation_result.error_message}"
            )
        
        logger.info(f"网站生成成功: {website_id}")
        
        return WebsiteGenerationResponse(
            success=True,
            website_id=website_id,
            website_url=website_url,
            preview_url=preview_url,
            message="网站生成成功"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"生成网站时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"生成网站时发生内部错误: {str(e)}"
        )


@router.get("/website/{website_id}", response_model=WebsiteInfoResponse)
async def get_website_info(
    website_id: str,
    redis_manager: RedisDataManager = Depends(get_redis_manager)
):
    """
    获取网站信息
    
    返回指定网站的配置信息和访问URL
    """
    try:
        logger.info(f"获取网站信息: {website_id}")
        
        # 从Redis获取网站配置
        website_config_dict = await redis_manager.get_website_config(website_id)
        if not website_config_dict:
            raise HTTPException(
                status_code=404,
                detail=f"网站不存在: {website_id}"
            )
        
        # 转换为响应模型
        return WebsiteInfoResponse(
            website_id=website_config_dict["id"],
            resume_id=website_config_dict["resume_id"],
            template_id=website_config_dict["template_id"],
            color_scheme=ColorScheme(**website_config_dict["color_scheme"]),
            website_url=website_config_dict["url"],
            is_public=website_config_dict["is_public"],
            created_at=website_config_dict["created_at"],
            updated_at=website_config_dict["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取网站信息时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"获取网站信息时发生内部错误: {str(e)}"
        )


@router.put("/website/{website_id}", response_model=WebsiteUpdateResponse)
async def update_website(
    website_id: str,
    request: WebsiteUpdateRequest,
    redis_manager: RedisDataManager = Depends(get_redis_manager),
    website_generator: WebsiteGenerator = Depends(get_website_generator)
):
    """
    更新网站内容
    
    支持更新简历数据、模板和颜色方案
    保持网站URL不变，仅更新内容
    """
    try:
        logger.info(f"开始更新网站: {website_id}")
        
        # 1. 验证网站是否存在
        website_config_dict = await redis_manager.get_website_config(website_id)
        if not website_config_dict:
            raise HTTPException(
                status_code=404,
                detail=f"网站不存在: {website_id}"
            )
        
        # 2. 转换为WebsiteConfig对象
        website_config = WebsiteConfig(**website_config_dict)
        
        # 3. 更新配置（只更新提供的字段）
        update_data = request.model_dump(exclude_unset=True)
        
        if "resume_id" in update_data:
            # 验证新的简历是否存在
            new_resume_data_dict = await redis_manager.get_resume(update_data["resume_id"])
            if not new_resume_data_dict:
                raise HTTPException(
                    status_code=404,
                    detail=f"简历不存在: {update_data['resume_id']}"
                )
            website_config.resume_id = update_data["resume_id"]
        
        if "template_id" in update_data:
            website_config.template_id = update_data["template_id"]
        
        if "color_scheme" in update_data:
            website_config.color_scheme = update_data["color_scheme"]
        
        if "is_public" in update_data:
            website_config.is_public = update_data["is_public"]
        
        # 4. 更新时间戳
        website_config.updated_at = datetime.now()
        
        # 5. 获取最新的简历数据
        resume_data_dict = await redis_manager.get_resume(website_config.resume_id)
        resume_data = ResumeData(**resume_data_dict)
        
        # 6. 重新生成网站
        generation_result = await website_generator.generate_website(
            resume_data=resume_data,
            website_config=website_config
        )
        
        if not generation_result.success:
            raise HTTPException(
                status_code=500,
                detail=f"网站更新失败: {generation_result.error_message}"
            )
        
        # 7. 保存更新后的配置
        await redis_manager.save_website_config(website_config)
        
        logger.info(f"网站更新成功: {website_id}")
        
        return WebsiteUpdateResponse(
            success=True,
            website_id=website_id,
            website_url=website_config.url,
            message="网站更新成功"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新网站时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"更新网站时发生内部错误: {str(e)}"
        )


@router.delete("/website/{website_id}")
async def delete_website(
    website_id: str,
    redis_manager: RedisDataManager = Depends(get_redis_manager),
    website_generator: WebsiteGenerator = Depends(get_website_generator)
):
    """
    删除网站
    
    删除网站配置和生成的静态文件
    """
    try:
        logger.info(f"开始删除网站: {website_id}")
        
        # 1. 验证网站是否存在
        website_config_dict = await redis_manager.get_website_config(website_id)
        if not website_config_dict:
            raise HTTPException(
                status_code=404,
                detail=f"网站不存在: {website_id}"
            )
        
        # 2. 删除生成的网站文件
        deletion_result = await website_generator.delete_website(website_id)
        if not deletion_result.success:
            logger.warning(f"删除网站文件失败: {deletion_result.error_message}")
        
        # 3. 从Redis删除网站配置
        config_key = f"website:{website_id}"
        redis_manager.redis_client.json().delete(config_key)
        
        # 4. 从索引中移除
        redis_manager.redis_client.srem("websites:all", website_id)
        
        # 5. 从简历关联中移除
        resume_id = website_config_dict["resume_id"]
        redis_manager.redis_client.srem(f"resume:websites:{resume_id}", website_id)
        
        logger.info(f"网站删除成功: {website_id}")
        
        return {"success": True, "message": "网站删除成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除网站时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"删除网站时发生内部错误: {str(e)}"
        )


@router.get("/websites/by-resume/{resume_id}")
async def get_websites_by_resume(
    resume_id: str,
    redis_manager: RedisDataManager = Depends(get_redis_manager)
):
    """
    获取简历关联的所有网站
    
    返回指定简历生成的所有网站列表
    """
    try:
        logger.info(f"获取简历关联的网站: {resume_id}")
        
        # 1. 验证简历是否存在
        resume_data_dict = await redis_manager.get_resume(resume_id)
        if not resume_data_dict:
            raise HTTPException(
                status_code=404,
                detail=f"简历不存在: {resume_id}"
            )
        
        # 2. 获取关联的网站ID列表
        website_ids = await redis_manager.get_websites_by_resume(resume_id)
        
        # 3. 获取每个网站的详细信息
        websites = []
        for website_id in website_ids:
            website_config_dict = await redis_manager.get_website_config(website_id)
            if website_config_dict:
                websites.append({
                    "website_id": website_config_dict["id"],
                    "template_id": website_config_dict["template_id"],
                    "website_url": website_config_dict["url"],
                    "is_public": website_config_dict["is_public"],
                    "created_at": website_config_dict["created_at"],
                    "updated_at": website_config_dict["updated_at"]
                })
        
        logger.info(f"获取简历关联网站成功: {resume_id}, 共 {len(websites)} 个网站")
        
        return {
            "success": True,
            "resume_id": resume_id,
            "websites": websites,
            "total_count": len(websites)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取简历关联网站时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"获取简历关联网站时发生内部错误: {str(e)}"
        )


@router.get("/templates")
async def get_available_templates():
    """
    获取可用的网站模板列表
    
    返回系统支持的所有网站模板
    """
    try:
        # 定义可用的模板
        templates = [
            {
                "id": "modern",
                "name": "现代风格",
                "description": "简洁现代的设计风格，适合技术人员",
                "preview_image": "/templates/modern/preview.jpg",
                "features": ["响应式设计", "渐变背景", "卡片布局", "动画效果"]
            },
            {
                "id": "professional",
                "name": "专业风格",
                "description": "正式专业的设计风格，适合商务人士",
                "preview_image": "/templates/professional/preview.jpg",
                "features": ["经典布局", "商务色调", "清晰排版", "专业外观"]
            },
            {
                "id": "creative",
                "name": "创意风格",
                "description": "富有创意的设计风格，适合设计师和艺术家",
                "preview_image": "/templates/creative/preview.jpg",
                "features": ["创意布局", "丰富色彩", "独特设计", "视觉冲击"]
            },
            {
                "id": "minimal",
                "name": "极简风格",
                "description": "极简主义设计风格，突出内容本身",
                "preview_image": "/templates/minimal/preview.jpg",
                "features": ["极简设计", "留白艺术", "内容为王", "优雅简洁"]
            }
        ]
        
        logger.info(f"获取模板列表成功，共 {len(templates)} 个模板")
        
        return {
            "success": True,
            "templates": templates,
            "total_count": len(templates)
        }
        
    except Exception as e:
        logger.error(f"获取模板列表时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"获取模板列表时发生内部错误: {str(e)}"
        )


@router.get("/color-schemes")
async def get_predefined_color_schemes():
    """
    获取预定义的颜色方案
    
    返回系统提供的预设颜色方案
    """
    try:
        # 定义预设颜色方案
        color_schemes = [
            {
                "id": "blue",
                "name": "蓝色主题",
                "scheme": {
                    "primary": "#3B82F6",
                    "secondary": "#6B7280",
                    "accent": "#10B981",
                    "background": "#FFFFFF",
                    "text": "#1F2937"
                }
            },
            {
                "id": "green",
                "name": "绿色主题",
                "scheme": {
                    "primary": "#10B981",
                    "secondary": "#6B7280",
                    "accent": "#3B82F6",
                    "background": "#FFFFFF",
                    "text": "#1F2937"
                }
            },
            {
                "id": "purple",
                "name": "紫色主题",
                "scheme": {
                    "primary": "#8B5CF6",
                    "secondary": "#6B7280",
                    "accent": "#F59E0B",
                    "background": "#FFFFFF",
                    "text": "#1F2937"
                }
            },
            {
                "id": "dark",
                "name": "深色主题",
                "scheme": {
                    "primary": "#60A5FA",
                    "secondary": "#9CA3AF",
                    "accent": "#34D399",
                    "background": "#111827",
                    "text": "#F9FAFB"
                }
            }
        ]
        
        logger.info(f"获取颜色方案成功，共 {len(color_schemes)} 个方案")
        
        return {
            "success": True,
            "color_schemes": color_schemes,
            "total_count": len(color_schemes)
        }
        
    except Exception as e:
        logger.error(f"获取颜色方案时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"获取颜色方案时发生内部错误: {str(e)}"
        )
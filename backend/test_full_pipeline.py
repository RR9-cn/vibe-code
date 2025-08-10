"""
完整后端流程测试
测试从PDF读取到Redis保存的完整流程
"""

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.services.pdf_parser import PDFParser
from backend.services.qwen_parser import QwenResumeParser
from backend.services.redis_manager import RedisDataManager
from backend.services.website_generator import WebsiteGenerator
from backend.models.resume import WebsiteConfig, ColorScheme


async def test_full_pipeline():
    """测试完整的后端流程"""
    
    # 测试文件路径
    pdf_path = r"D:\面试\简历\java开发工程师_陈俊杰.pdf"
    
    print("🚀 开始完整后端流程测试")
    print("=" * 60)
    
    # 检查PDF文件是否存在
    if not os.path.exists(pdf_path):
        print(f"❌ PDF文件不存在: {pdf_path}")
        return
    
    print(f"📄 PDF文件路径: {pdf_path}")
    
    try:
        # 步骤1: PDF文本提取
        print("\n📖 步骤1: PDF文本提取")
        print("-" * 30)
        
        pdf_parser = PDFParser()
        pdf_text = pdf_parser.extract_text_from_pdf(pdf_path)
        
        if pdf_text:
            print(f"✅ PDF文本提取成功")
            print(f"📝 提取文本长度: {len(pdf_text)} 字符")
            print(f"📝 文本预览: {pdf_text[:200]}...")
        else:
            print("❌ PDF文本提取失败")
            return
        
        # 步骤2: AI解析简历数据
        print("\n🤖 步骤2: AI解析简历数据")
        print("-" * 30)
        
        qwen_parser = QwenResumeParser()
        resume_data = qwen_parser.parse_resume_text(pdf_text)
        
        if resume_data:
            print("✅ AI解析成功")
            print(f"👤 姓名: {resume_data.personal_info.name}")
            print(f"📧 邮箱: {resume_data.personal_info.email}")
            print(f"📱 电话: {resume_data.personal_info.phone}")
            print(f"💼 工作经历数量: {len(resume_data.work_experience)}")
            print(f"🎓 教育背景数量: {len(resume_data.education)}")
            print(f"🛠️ 技能数量: {len(resume_data.skills)}")
        else:
            print("❌ AI解析失败")
            return
        
        # 步骤3: 保存到Redis
        print("\n💾 步骤3: 保存到Redis")
        print("-" * 30)
        
        redis_manager = RedisDataManager()
        print("✅ Redis连接成功")
        
        # 保存简历数据
        resume_id = await redis_manager.save_resume(resume_data)
        print(f"✅ 简历数据保存成功，ID: {resume_id}")
        
        # 验证保存的数据
        retrieved_data = await redis_manager.get_resume(resume_id)
        if retrieved_data:
            print("✅ 数据验证成功，可以正确读取保存的简历")
        else:
            print("❌ 数据验证失败")
            return
        
        # 步骤4: 生成个人网站
        print("\n🌐 步骤4: 生成个人网站")
        print("-" * 30)
        
        # 创建网站配置
        website_config = WebsiteConfig(
            id=f"website_{resume_id}",
            resume_id=resume_id,
            template_id="modern",
            color_scheme=ColorScheme(
                primary="#3B82F6",      # 蓝色
                secondary="#6B7280",    # 灰色
                accent="#10B981",       # 绿色
                background="#FFFFFF",   # 白色
                text="#1F2937"          # 深灰色
            ),
            url=f"/website/website_{resume_id}",
            is_public=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # 保存网站配置
        await redis_manager.save_website_config(website_config)
        print("✅ 网站配置保存成功")
        
        # 生成网站文件
        website_generator = WebsiteGenerator()
        generation_result = await website_generator.generate_website(
            resume_data=resume_data,
            website_config=website_config
        )
        
        if generation_result.success:
            print(f"✅ 网站生成成功")
            print(f"📁 网站路径: {generation_result.website_path}")
            
            # 检查生成的文件
            website_path = Path(generation_result.website_path)
            files = ["index.html", "style.css", "script.js", "metadata.json"]
            
            for file_name in files:
                file_path = website_path / file_name
                if file_path.exists():
                    file_size = file_path.stat().st_size
                    print(f"  ✅ {file_name} ({file_size} bytes)")
                else:
                    print(f"  ❌ {file_name} (缺失)")
        else:
            print(f"❌ 网站生成失败: {generation_result.error_message}")
        
        # 步骤5: 数据统计
        print("\n📊 步骤5: 数据统计")
        print("-" * 30)
        
        # 获取关联的网站
        websites = await redis_manager.get_websites_by_resume(resume_id)
        print(f"🌐 当前简历关联网站数: {len(websites)}")
        print(f"📋 当前简历ID: {resume_id}")
        
        # 显示详细信息
        print("\n📋 简历详细信息:")
        print(f"  👤 姓名: {resume_data.personal_info.name}")
        print(f"  📧 邮箱: {resume_data.personal_info.email}")
        print(f"  📱 电话: {resume_data.personal_info.phone or '未提供'}")
        print(f"  📍 地址: {resume_data.personal_info.location or '未提供'}")
        
        if resume_data.personal_info.summary:
            print(f"  📝 个人简介: {resume_data.personal_info.summary[:100]}...")
        
        print(f"\n💼 工作经历 ({len(resume_data.work_experience)} 项):")
        for i, exp in enumerate(resume_data.work_experience[:3], 1):  # 只显示前3项
            end_date = exp.end_date or "至今"
            print(f"  {i}. {exp.position} @ {exp.company} ({exp.start_date} - {end_date})")
        
        print(f"\n🎓 教育背景 ({len(resume_data.education)} 项):")
        for i, edu in enumerate(resume_data.education[:3], 1):  # 只显示前3项
            end_date = edu.end_date or "至今"
            print(f"  {i}. {edu.degree} @ {edu.institution} ({edu.start_date} - {end_date})")
        
        print(f"\n🛠️ 技能 ({len(resume_data.skills)} 项):")
        skill_categories = {}
        for skill in resume_data.skills:
            category = skill.category.value
            if category not in skill_categories:
                skill_categories[category] = []
            skill_categories[category].append(skill.name)
        
        for category, skills in skill_categories.items():
            category_name = {
                "technical": "技术技能",
                "soft": "软技能", 
                "language": "语言技能"
            }.get(category, category)
            print(f"  {category_name}: {', '.join(skills[:5])}{'...' if len(skills) > 5 else ''}")
        
        print("\n" + "=" * 60)
        print("🎉 完整后端流程测试成功完成！")
        print("=" * 60)
        
        # 返回关键信息
        return {
            "resume_id": resume_id,
            "website_id": website_config.id,
            "website_path": generation_result.website_path if generation_result.success else None,
            "name": resume_data.personal_info.name,
            "email": resume_data.personal_info.email
        }
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return None


async def cleanup_test_data(resume_id: str, website_id: str):
    """清理测试数据"""
    print("\n🧹 清理测试数据")
    print("-" * 30)
    
    try:
        redis_manager = RedisDataManager()
        website_generator = WebsiteGenerator()
        
        # 删除网站文件
        await website_generator.delete_website(website_id)
        print("✅ 网站文件删除成功")
        
        # 删除Redis数据
        # 注意：这里需要实现删除方法，当前RedisDataManager可能没有删除方法
        print("⚠️ Redis数据保留（需要手动清理或实现删除方法）")
        
    except Exception as e:
        print(f"❌ 清理数据时发生错误: {e}")


if __name__ == "__main__":
    # 运行测试
    result = asyncio.run(test_full_pipeline())
    
    if result:
        print(f"\n✨ 测试结果:")
        print(f"  简历ID: {result['resume_id']}")
        print(f"  网站ID: {result['website_id']}")
        print(f"  姓名: {result['name']}")
        print(f"  邮箱: {result['email']}")
        
        if result['website_path']:
            print(f"  网站路径: {result['website_path']}")
            print(f"\n🌐 可以通过以下方式访问生成的网站:")
            print(f"  1. 直接打开: {result['website_path']}/index.html")
            print(f"  2. 启动本地服务器查看")
        
        # 询问是否清理测试数据
        print(f"\n❓ 是否需要清理测试数据？")
        print(f"  简历ID: {result['resume_id']}")
        print(f"  网站ID: {result['website_id']}")
        print(f"  (手动运行清理函数或保留数据用于进一步测试)")
    else:
        print("\n❌ 测试失败，请检查错误信息")
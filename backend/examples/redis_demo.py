"""
Redis数据管理器使用示例
演示如何使用RedisStack进行数据存储和检索
"""

import asyncio
import sys
import os
from datetime import datetime

# 添加父目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
from config.redis_config import get_redis_url


def create_sample_resumes():
    """创建多个示例简历数据"""
    resumes = []
    
    # 简历1：Python开发工程师
    personal_info1 = PersonalInfo(
        name="李明",
        email="liming@example.com",
        phone="13800138001",
        location="北京市朝阳区",
        summary="资深Python开发工程师，专注于Web开发和数据分析",
        github="https://github.com/liming"
    )
    
    work_exp1 = [
        WorkExperience(
            company="字节跳动",
            position="高级Python工程师",
            start_date="2021-03",
            end_date="2024-01",
            description=[
                "负责推荐系统后端开发，处理日均千万级请求",
                "优化算法性能，将响应时间从200ms降低到50ms",
                "设计和实现微服务架构，提升系统可扩展性"
            ],
            technologies=["Python", "Django", "Redis", "PostgreSQL", "Docker"]
        ),
        WorkExperience(
            company="美团",
            position="Python开发工程师",
            start_date="2019-07",
            end_date="2021-02",
            description=[
                "开发外卖配送系统核心模块",
                "实现实时订单分配算法"
            ],
            technologies=["Python", "Flask", "MySQL", "RabbitMQ"]
        )
    ]
    
    education1 = [
        Education(
            institution="北京大学",
            degree="硕士",
            major="计算机科学与技术",
            start_date="2017-09",
            end_date="2019-06"
        )
    ]
    
    skills1 = [
        Skill(category=SkillCategory.TECHNICAL, name="Python", level=SkillLevel.EXPERT),
        Skill(category=SkillCategory.TECHNICAL, name="Django", level=SkillLevel.ADVANCED),
        Skill(category=SkillCategory.TECHNICAL, name="Redis", level=SkillLevel.ADVANCED),
        Skill(category=SkillCategory.TECHNICAL, name="PostgreSQL", level=SkillLevel.INTERMEDIATE),
        Skill(category=SkillCategory.SOFT, name="团队协作", level=SkillLevel.ADVANCED),
        Skill(category=SkillCategory.LANGUAGE, name="英语", level=SkillLevel.INTERMEDIATE)
    ]
    
    resume1 = ResumeData(
        id="resume_liming_001",
        personal_info=personal_info1,
        work_experience=work_exp1,
        education=education1,
        skills=skills1
    )
    resumes.append(resume1)
    
    # 简历2：前端开发工程师
    personal_info2 = PersonalInfo(
        name="王小红",
        email="wangxiaohong@example.com",
        phone="13800138002",
        location="上海市浦东新区",
        summary="前端开发专家，精通React和Vue.js框架",
        linkedin="https://linkedin.com/in/wangxiaohong"
    )
    
    work_exp2 = [
        WorkExperience(
            company="阿里巴巴",
            position="资深前端工程师",
            start_date="2020-06",
            end_date="2024-01",
            description=[
                "负责淘宝商家后台前端开发",
                "重构老旧代码，提升页面加载速度30%",
                "建立前端组件库，提高开发效率"
            ],
            technologies=["React", "TypeScript", "Webpack", "Ant Design"]
        )
    ]
    
    education2 = [
        Education(
            institution="复旦大学",
            degree="学士",
            major="软件工程",
            start_date="2016-09",
            end_date="2020-06"
        )
    ]
    
    skills2 = [
        Skill(category=SkillCategory.TECHNICAL, name="JavaScript", level=SkillLevel.EXPERT),
        Skill(category=SkillCategory.TECHNICAL, name="React", level=SkillLevel.EXPERT),
        Skill(category=SkillCategory.TECHNICAL, name="Vue.js", level=SkillLevel.ADVANCED),
        Skill(category=SkillCategory.TECHNICAL, name="TypeScript", level=SkillLevel.ADVANCED),
        Skill(category=SkillCategory.SOFT, name="UI设计", level=SkillLevel.INTERMEDIATE),
        Skill(category=SkillCategory.LANGUAGE, name="英语", level=SkillLevel.ADVANCED)
    ]
    
    resume2 = ResumeData(
        id="resume_wangxiaohong_001",
        personal_info=personal_info2,
        work_experience=work_exp2,
        education=education2,
        skills=skills2
    )
    resumes.append(resume2)
    
    return resumes


async def demo_basic_operations():
    """演示基本的CRUD操作"""
    print("=== Redis数据管理器基本操作演示 ===\n")
    
    # 注意：这里使用模拟的Redis URL，实际使用时需要确保Redis服务运行
    try:
        manager = RedisDataManager("redis://localhost:6379")
        print("✓ Redis连接成功")
    except Exception as e:
        print(f"✗ Redis连接失败: {e}")
        print("注意：此演示需要Redis服务运行在localhost:6379")
        return
    
    # 创建示例数据
    resumes = create_sample_resumes()
    
    print("\n1. 保存简历数据...")
    for resume in resumes:
        try:
            result = await manager.save_resume(resume)
            print(f"✓ 简历保存成功: {resume.personal_info.name} (ID: {result})")
        except Exception as e:
            print(f"✗ 简历保存失败: {e}")
    
    print("\n2. 获取简历数据...")
    for resume in resumes:
        try:
            retrieved_data = await manager.get_resume(resume.id)
            if retrieved_data:
                print(f"✓ 简历获取成功: {retrieved_data['personal_info']['name']}")
            else:
                print(f"✗ 简历不存在: {resume.id}")
        except Exception as e:
            print(f"✗ 简历获取失败: {e}")
    
    print("\n3. 搜索功能演示...")
    
    # 文本搜索
    try:
        search_results = await manager.search_resumes_by_text("Python")
        print(f"✓ 文本搜索 'Python' 找到 {len(search_results)} 个结果")
        for result_id in search_results:
            resume_data = await manager.get_resume(result_id)
            if resume_data:
                print(f"  - {resume_data['personal_info']['name']}")
    except Exception as e:
        print(f"✗ 文本搜索失败: {e}")
    
    # 技能搜索
    try:
        skill_results = await manager.search_resumes_by_skill("React")
        print(f"✓ 技能搜索 'React' 找到 {len(skill_results)} 个结果")
        for result_id in skill_results:
            resume_data = await manager.get_resume(result_id)
            if resume_data:
                print(f"  - {resume_data['personal_info']['name']}")
    except Exception as e:
        print(f"✗ 技能搜索失败: {e}")
    
    # 公司搜索
    try:
        company_results = await manager.search_resumes_by_company("阿里巴巴")
        print(f"✓ 公司搜索 '阿里巴巴' 找到 {len(company_results)} 个结果")
        for result_id in company_results:
            resume_data = await manager.get_resume(result_id)
            if resume_data:
                print(f"  - {resume_data['personal_info']['name']}")
    except Exception as e:
        print(f"✗ 公司搜索失败: {e}")
    
    print("\n4. 统计信息...")
    try:
        stats = await manager.get_database_stats()
        print("✓ 数据库统计信息:")
        print(f"  - 总简历数: {stats.get('total_resumes', 0)}")
        print(f"  - 总网站数: {stats.get('total_websites', 0)}")
        print(f"  - 总公司数: {stats.get('total_companies', 0)}")
        
        skills_stats = stats.get('skills_by_category', {})
        for category, count in skills_stats.items():
            print(f"  - {category}技能数: {count}")
        
        redis_info = stats.get('redis_info', {})
        if redis_info:
            print(f"  - Redis内存使用: {redis_info.get('used_memory', 'N/A')}")
    except Exception as e:
        print(f"✗ 获取统计信息失败: {e}")
    
    print("\n5. 网站配置演示...")
    try:
        # 创建网站配置
        color_scheme = ColorScheme(
            primary="#3B82F6",
            secondary="#64748B", 
            accent="#F59E0B",
            background="#FFFFFF",
            text="#1F2937"
        )
        
        website_config = WebsiteConfig(
            id="website_liming_001",
            resume_id="resume_liming_001",
            template_id="modern_template_v1",
            color_scheme=color_scheme,
            url="https://resume-generator.com/liming"
        )
        
        # 保存网站配置
        config_id = await manager.save_website_config(website_config)
        print(f"✓ 网站配置保存成功: {config_id}")
        
        # 获取网站配置
        retrieved_config = await manager.get_website_config(config_id)
        if retrieved_config:
            print(f"✓ 网站配置获取成功: {retrieved_config['url']}")
        
        # 获取简历关联的网站
        websites = await manager.get_websites_by_resume("resume_liming_001")
        print(f"✓ 简历关联网站数: {len(websites)}")
        
    except Exception as e:
        print(f"✗ 网站配置操作失败: {e}")
    
    # 清理演示数据
    print("\n6. 清理演示数据...")
    try:
        for resume in resumes:
            await manager.delete_resume(resume.id)
            print(f"✓ 删除简历: {resume.personal_info.name}")
    except Exception as e:
        print(f"✗ 清理数据失败: {e}")
    
    # 关闭连接
    manager.close()
    print("\n✓ Redis连接已关闭")


async def demo_knowledge_base():
    """演示知识库功能（预留）"""
    print("\n=== 知识库功能演示（预留） ===\n")
    
    try:
        manager = RedisDataManager("redis://localhost:6379")
        kb_manager = KnowledgeBaseManager(manager.redis_client)
        
        print("✓ 知识库管理器初始化成功")
        
        # 演示预留功能
        await kb_manager.add_document_embedding("doc_001", [0.1, 0.2, 0.3])
        print("✓ 文档向量嵌入功能（预留）")
        
        results = await kb_manager.semantic_search([0.1, 0.2, 0.3])
        print(f"✓ 语义搜索功能（预留），结果数: {len(results)}")
        
        await kb_manager.build_knowledge_graph(["resume_001", "resume_002"])
        print("✓ 知识图谱构建功能（预留）")
        
        manager.close()
        
    except Exception as e:
        print(f"✗ 知识库演示失败: {e}")


async def main():
    """主函数"""
    print("Redis数据管理器演示程序")
    print("=" * 50)
    
    await demo_basic_operations()
    await demo_knowledge_base()
    
    print("\n=== 演示完成 ===")
    print("Redis数据管理器功能包括:")
    print("- 简历数据的CRUD操作")
    print("- 多种搜索功能（文本、技能、公司）")
    print("- 网站配置管理")
    print("- 数据统计和索引")
    print("- 知识库扩展预留")
    print("\n注意：实际使用前请确保Redis服务正常运行")


if __name__ == "__main__":
    asyncio.run(main())
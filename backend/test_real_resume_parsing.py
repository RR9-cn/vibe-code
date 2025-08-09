#!/usr/bin/env python3
"""
真实简历解析测试
使用真实的PDF文件和通义千问API进行完整的简历解析测试
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from services.pdf_parser import PDFParser, PDFParseError
from services.qwen_parser import QwenResumeParser, QwenParseError
from models.resume import ResumeData


class RealResumeParsingTest:
    """真实简历解析测试类"""
    
    def __init__(self):
        """初始化测试类"""
        self.pdf_file_path = r"D:\面试\简历\java开发工程师_陈俊杰.pdf"
        self.output_dir = project_root / "test_outputs"
        self.output_dir.mkdir(exist_ok=True)
        
        # 检查API密钥
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("❌ 未找到DASHSCOPE_API_KEY环境变量，请确保已配置API密钥")
        
        print(f"✅ API密钥已配置: {self.api_key[:10]}...")
        
        # 初始化解析器
        self.pdf_parser = PDFParser()
        self.qwen_parser = QwenResumeParser()
        
        print(f"📄 目标PDF文件: {self.pdf_file_path}")
        print(f"📁 输出目录: {self.output_dir}")
    
    def check_pdf_file(self) -> bool:
        """检查PDF文件是否存在和可读"""
        print("\n=== 步骤1: 检查PDF文件 ===")
        
        if not os.path.exists(self.pdf_file_path):
            print(f"❌ PDF文件不存在: {self.pdf_file_path}")
            return False
        
        file_size = os.path.getsize(self.pdf_file_path) / 1024  # KB
        print(f"✅ PDF文件存在")
        print(f"📊 文件大小: {file_size:.2f} KB")
        
        # 验证PDF文件
        try:
            validation_result = self.pdf_parser.validate_pdf_file(self.pdf_file_path)
            print(f"📋 PDF验证结果: {'✅ 通过' if validation_result['is_valid'] else '❌ 失败'}")
            
            if not validation_result['is_valid']:
                print(f"❌ PDF验证失败: {validation_result['error_message']}")
                return False
            
            # 显示文件信息
            if validation_result['file_info']:
                file_info = validation_result['file_info']
                print(f"📄 文件信息:")
                print(f"  页数: {file_info.get('num_pages', 'N/A')}")
                print(f"  文件名: {file_info.get('file_name', 'N/A')}")
            
            return True
            
        except Exception as e:
            print(f"❌ PDF验证异常: {e}")
            return False
    
    def extract_pdf_text(self) -> str:
        """提取PDF文本内容"""
        print("\n=== 步骤2: 提取PDF文本 ===")
        
        try:
            # 提取文本
            extracted_text = self.pdf_parser.extract_text_from_pdf(self.pdf_file_path)
            
            print(f"✅ 文本提取成功")
            print(f"📊 提取文本长度: {len(extracted_text)} 字符")
            print(f"📊 文本行数: {len(extracted_text.splitlines())} 行")
            
            # 显示文本预览
            preview_length = 300
            preview_text = extracted_text[:preview_length]
            print(f"\n📖 文本预览 (前{preview_length}字符):")
            print("-" * 50)
            print(preview_text)
            if len(extracted_text) > preview_length:
                print("...")
            print("-" * 50)
            
            # 保存提取的文本
            text_output_file = self.output_dir / "extracted_text.txt"
            with open(text_output_file, 'w', encoding='utf-8') as f:
                f.write(extracted_text)
            print(f"💾 提取文本已保存到: {text_output_file}")
            
            return extracted_text
            
        except PDFParseError as e:
            print(f"❌ PDF文本提取失败: {e}")
            raise
        except Exception as e:
            print(f"❌ 文本提取异常: {e}")
            raise
    
    def parse_with_qwen(self, resume_text: str) -> ResumeData:
        """使用通义千问解析简历文本"""
        print("\n=== 步骤3: 通义千问AI解析 ===")
        
        try:
            print("🤖 开始调用通义千问API...")
            print(f"📊 输入文本长度: {len(resume_text)} 字符")
            
            # 记录开始时间
            start_time = datetime.now()
            
            # 调用AI解析
            resume_data = self.qwen_parser.parse_resume_text(resume_text)
            
            # 记录结束时间
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            print(f"✅ AI解析完成")
            print(f"⏱️ 处理时间: {processing_time:.2f} 秒")
            print(f"🆔 简历ID: {resume_data.id}")
            
            return resume_data
            
        except QwenParseError as e:
            print(f"❌ 通义千问解析失败: {e}")
            raise
        except Exception as e:
            print(f"❌ AI解析异常: {e}")
            raise
    
    def analyze_parsed_data(self, resume_data: ResumeData) -> dict:
        """分析解析结果"""
        print("\n=== 步骤4: 解析结果分析 ===")
        
        # 基本信息统计
        stats = {
            'personal_info': {
                'name': resume_data.personal_info.name,
                'email': resume_data.personal_info.email,
                'phone': resume_data.personal_info.phone,
                'location': resume_data.personal_info.location,
                'has_summary': bool(resume_data.personal_info.summary),
                'has_linkedin': bool(resume_data.personal_info.linkedin),
                'has_github': bool(resume_data.personal_info.github),
                'has_website': bool(resume_data.personal_info.website)
            },
            'work_experience': {
                'count': len(resume_data.work_experience),
                'companies': [exp.company for exp in resume_data.work_experience],
                'positions': [exp.position for exp in resume_data.work_experience],
                'has_technologies': sum(1 for exp in resume_data.work_experience if exp.technologies)
            },
            'education': {
                'count': len(resume_data.education),
                'institutions': [edu.institution for edu in resume_data.education],
                'degrees': [edu.degree for edu in resume_data.education],
                'has_gpa': sum(1 for edu in resume_data.education if edu.gpa)
            },
            'skills': {
                'count': len(resume_data.skills),
                'by_category': {},
                'by_level': {},
                'names': [skill.name for skill in resume_data.skills]
            }
        }
        
        # 技能分类统计
        for skill in resume_data.skills:
            category = skill.category
            level = skill.level or 'unknown'
            
            stats['skills']['by_category'][category] = stats['skills']['by_category'].get(category, 0) + 1
            stats['skills']['by_level'][level] = stats['skills']['by_level'].get(level, 0) + 1
        
        # 显示分析结果
        print("📊 个人信息:")
        print(f"  姓名: {stats['personal_info']['name']}")
        print(f"  邮箱: {stats['personal_info']['email']}")
        print(f"  电话: {stats['personal_info']['phone']}")
        print(f"  地址: {stats['personal_info']['location']}")
        print(f"  个人简介: {'✅' if stats['personal_info']['has_summary'] else '❌'}")
        print(f"  LinkedIn: {'✅' if stats['personal_info']['has_linkedin'] else '❌'}")
        print(f"  GitHub: {'✅' if stats['personal_info']['has_github'] else '❌'}")
        
        print(f"\n💼 工作经历 ({stats['work_experience']['count']}项):")
        for i, (company, position) in enumerate(zip(stats['work_experience']['companies'], 
                                                   stats['work_experience']['positions']), 1):
            print(f"  {i}. {company} - {position}")
        
        print(f"\n🎓 教育背景 ({stats['education']['count']}项):")
        for i, (institution, degree) in enumerate(zip(stats['education']['institutions'], 
                                                      stats['education']['degrees']), 1):
            print(f"  {i}. {institution} - {degree}")
        
        print(f"\n🛠️ 技能统计 ({stats['skills']['count']}项):")
        print("  按分类:")
        for category, count in stats['skills']['by_category'].items():
            category_name = {
                'technical': '技术技能',
                'soft': '软技能', 
                'language': '语言技能'
            }.get(category, category)
            print(f"    {category_name}: {count}项")
        
        print("  按水平:")
        for level, count in stats['skills']['by_level'].items():
            level_name = {
                'beginner': '初级',
                'intermediate': '中级',
                'advanced': '高级',
                'expert': '专家',
                'unknown': '未知'
            }.get(level, level)
            print(f"    {level_name}: {count}项")
        
        return stats
    
    def validate_quality(self, resume_data: ResumeData) -> dict:
        """验证解析质量"""
        print("\n=== 步骤5: 质量验证 ===")
        
        validation_result = self.qwen_parser.validate_parsed_data(resume_data)
        
        print(f"✅ 验证状态: {'通过' if validation_result['is_valid'] else '失败'}")
        print(f"📊 完整性评分: {validation_result['completeness_score']:.2%}")
        
        if validation_result['errors']:
            print("❌ 错误:")
            for error in validation_result['errors']:
                print(f"  - {error}")
        
        if validation_result['warnings']:
            print("⚠️ 警告:")
            for warning in validation_result['warnings']:
                print(f"  - {warning}")
        
        # 质量评估
        quality_score = validation_result['completeness_score']
        if quality_score >= 0.8:
            quality_level = "优秀"
            quality_emoji = "🌟"
        elif quality_score >= 0.6:
            quality_level = "良好"
            quality_emoji = "👍"
        elif quality_score >= 0.4:
            quality_level = "一般"
            quality_emoji = "⚠️"
        else:
            quality_level = "较差"
            quality_emoji = "❌"
        
        print(f"\n{quality_emoji} 整体质量评估: {quality_level} ({quality_score:.1%})")
        
        return validation_result
    
    def save_results(self, resume_data: ResumeData, stats: dict, validation: dict):
        """保存解析结果"""
        print("\n=== 步骤6: 保存结果 ===")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存完整的简历数据
        resume_file = self.output_dir / f"parsed_resume_{timestamp}.json"
        with open(resume_file, 'w', encoding='utf-8') as f:
            # 使用model_dump_json()方法，它会自动处理datetime序列化
            resume_json = resume_data.model_dump_json(indent=2)
            f.write(resume_json)
        print(f"💾 简历数据已保存: {resume_file}")
        
        # 保存统计信息
        stats_file = self.output_dir / f"parsing_stats_{timestamp}.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump({
                'stats': stats,
                'validation': validation,
                'metadata': {
                    'pdf_file': self.pdf_file_path,
                    'parsing_time': timestamp,
                    'api_model': self.qwen_parser.model
                }
            }, f, ensure_ascii=False, indent=2)
        print(f"📊 统计信息已保存: {stats_file}")
        
        # 生成可读的报告
        report_file = self.output_dir / f"parsing_report_{timestamp}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=== 简历解析报告 ===\n\n")
            f.write(f"PDF文件: {self.pdf_file_path}\n")
            f.write(f"解析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"使用模型: {self.qwen_parser.model}\n\n")
            
            f.write("个人信息:\n")
            f.write(f"  姓名: {resume_data.personal_info.name}\n")
            f.write(f"  邮箱: {resume_data.personal_info.email}\n")
            f.write(f"  电话: {resume_data.personal_info.phone}\n")
            f.write(f"  地址: {resume_data.personal_info.location}\n\n")
            
            f.write(f"工作经历 ({len(resume_data.work_experience)}项):\n")
            for i, exp in enumerate(resume_data.work_experience, 1):
                f.write(f"  {i}. {exp.company} - {exp.position}\n")
                f.write(f"     时间: {exp.start_date} 至 {exp.end_date or '至今'}\n")
                if exp.technologies:
                    f.write(f"     技术: {', '.join(exp.technologies)}\n")
                f.write("\n")
            
            f.write(f"教育背景 ({len(resume_data.education)}项):\n")
            for i, edu in enumerate(resume_data.education, 1):
                f.write(f"  {i}. {edu.institution} - {edu.degree}\n")
                if edu.major:
                    f.write(f"     专业: {edu.major}\n")
                f.write(f"     时间: {edu.start_date} 至 {edu.end_date}\n\n")
            
            f.write(f"技能列表 ({len(resume_data.skills)}项):\n")
            skill_categories = {}
            for skill in resume_data.skills:
                if skill.category not in skill_categories:
                    skill_categories[skill.category] = []
                skill_categories[skill.category].append(skill)
            
            for category, skills in skill_categories.items():
                category_name = {
                    'technical': '技术技能',
                    'soft': '软技能',
                    'language': '语言技能'
                }.get(category, category)
                f.write(f"  {category_name}:\n")
                for skill in skills:
                    level_text = f"({skill.level})" if skill.level else ""
                    f.write(f"    - {skill.name} {level_text}\n")
                f.write("\n")
            
            f.write(f"质量评估:\n")
            f.write(f"  完整性评分: {validation['completeness_score']:.2%}\n")
            f.write(f"  验证状态: {'通过' if validation['is_valid'] else '失败'}\n")
            if validation['warnings']:
                f.write("  警告:\n")
                for warning in validation['warnings']:
                    f.write(f"    - {warning}\n")
        
        print(f"📄 解析报告已保存: {report_file}")
        
        return {
            'resume_file': resume_file,
            'stats_file': stats_file,
            'report_file': report_file
        }
    
    def run_complete_test(self) -> bool:
        """运行完整的测试流程"""
        print("🚀 开始真实简历解析测试")
        print("=" * 60)
        
        try:
            # 步骤1: 检查PDF文件
            if not self.check_pdf_file():
                return False
            
            # 步骤2: 提取PDF文本
            resume_text = self.extract_pdf_text()
            
            # 步骤3: AI解析
            resume_data = self.parse_with_qwen(resume_text)
            
            # 步骤4: 分析结果
            stats = self.analyze_parsed_data(resume_data)
            
            # 步骤5: 质量验证
            validation = self.validate_quality(resume_data)
            
            # 步骤6: 保存结果
            output_files = self.save_results(resume_data, stats, validation)
            
            # 测试总结
            print("\n" + "=" * 60)
            print("🎉 测试完成！")
            print(f"✅ 成功解析简历: {resume_data.personal_info.name}")
            print(f"📊 完整性评分: {validation['completeness_score']:.2%}")
            print(f"📁 输出文件:")
            for file_type, file_path in output_files.items():
                print(f"  - {file_type}: {file_path}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """主函数"""
    try:
        # 创建测试实例
        test = RealResumeParsingTest()
        
        # 运行完整测试
        success = test.run_complete_test()
        
        if success:
            print("\n🌟 所有测试通过！")
            print("💡 提示: 查看test_outputs目录中的输出文件了解详细结果")
        else:
            print("\n💥 测试失败，请检查错误信息")
        
        return success
        
    except Exception as e:
        print(f"❌ 测试初始化失败: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
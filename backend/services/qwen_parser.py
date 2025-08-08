"""
通义千问API集成服务
实现简历文本的AI解析功能
"""

import json
import logging
import os
from typing import Dict, Any, Optional
from datetime import datetime
import dashscope
from dashscope import Generation
from pydantic import ValidationError

from backend.models.resume import ResumeData, PersonalInfo, WorkExperience, Education, Skill

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QwenParseError(Exception):
    """通义千问解析异常"""
    pass


class QwenResumeParser:
    """通义千问简历解析器"""
    
    def __init__(self):
        # 从环境变量获取API密钥
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("未找到DASHSCOPE_API_KEY环境变量，请配置通义千问API密钥")
        
        # 配置dashscope
        dashscope.api_key = self.api_key
        
        # 模型配置
        self.model = "qwen-turbo"  # 可选: qwen-plus, qwen-max
        self.max_tokens = 2000
        self.temperature = 0.1  # 较低的温度确保输出稳定
    
    def parse_resume_text(self, resume_text: str) -> ResumeData:
        """
        使用通义千问API解析简历文本
        
        Args:
            resume_text: 从PDF提取的简历文本
            
        Returns:
            解析后的结构化简历数据
            
        Raises:
            QwenParseError: 当AI解析失败时
        """
        if not resume_text or not resume_text.strip():
            raise QwenParseError("简历文本为空，无法进行解析")
        
        try:
            # 构建解析提示
            prompt = self._build_parse_prompt(resume_text)
            
            # 调用通义千问API
            logger.info("开始调用通义千问API解析简历...")
            response = self._call_qwen_api(prompt)
            
            # 解析API响应
            parsed_data = self._parse_api_response(response)
            
            # 验证和构建ResumeData对象
            resume_data = self._build_resume_data(parsed_data)
            
            logger.info("简历解析成功完成")
            return resume_data
            
        except Exception as e:
            logger.error(f"简历解析失败: {str(e)}")
            raise QwenParseError(f"简历解析过程中发生错误: {str(e)}")
    
    def _build_parse_prompt(self, resume_text: str) -> str:
        """构建解析提示模板"""
        prompt = f"""
你是一个专业的简历解析助手。请仔细分析以下简历文本，提取结构化信息。

简历文本：
{resume_text}

请严格按照以下JSON格式返回，确保所有字段都存在：

{{
  "personal_info": {{
    "name": "姓名（必填）",
    "email": "邮箱地址",
    "phone": "电话号码",
    "location": "所在地区",
    "summary": "个人简介或自我评价",
    "linkedin": "LinkedIn链接（如果有）",
    "github": "GitHub链接（如果有）",
    "website": "个人网站（如果有）"
  }},
  "work_experience": [
    {{
      "company": "公司名称",
      "position": "职位名称",
      "start_date": "开始时间（格式：YYYY-MM 或 YYYY年MM月）",
      "end_date": "结束时间（格式：YYYY-MM 或 YYYY年MM月，如果是当前工作则为null）",
      "description": ["工作描述1", "工作描述2", "工作描述3"],
      "technologies": ["技术栈1", "技术栈2"]
    }}
  ],
  "education": [
    {{
      "institution": "学校名称",
      "degree": "学位（如：本科、硕士、博士）",
      "major": "专业名称",
      "start_date": "开始时间",
      "end_date": "结束时间",
      "gpa": "GPA（如果有）"
    }}
  ],
  "skills": [
    {{
      "category": "技能分类（如：编程语言、框架、数据库、工具等）",
      "name": "具体技能名称",
      "level": "熟练程度（如：熟练、精通、了解）"
    }}
  ]
}}

解析要求：
1. 仔细识别个人基本信息，包括姓名、联系方式等
2. 按时间顺序整理工作经历，提取公司、职位、时间、工作内容
3. 提取教育背景信息
4. 从专业技能、项目经历中提取技能信息，并进行合理分类
5. 如果某些信息在简历中没有明确提及，对应字段可以为空字符串或null
6. 确保返回的是有效的JSON格式
7. 所有日期尽量统一为YYYY-MM格式

请只返回JSON数据，不要包含其他解释文字。
"""
        return prompt
    
    def _call_qwen_api(self, prompt: str) -> str:
        """调用通义千问API"""
        try:
            response = Generation.call(
                model=self.model,
                prompt=prompt,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=0.8,
                api_key=self.api_key
            )
            
            if response.status_code == 200:
                return response.output.text
            else:
                raise QwenParseError(f"API调用失败，状态码: {response.status_code}, 错误信息: {response.message}")
                
        except Exception as e:
            raise QwenParseError(f"调用通义千问API时发生错误: {str(e)}")
    
    def _parse_api_response(self, response_text: str) -> Dict[str, Any]:
        """解析API响应文本"""
        try:
            # 清理响应文本，移除可能的markdown格式
            cleaned_text = response_text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]
            cleaned_text = cleaned_text.strip()
            
            # 解析JSON
            parsed_data = json.loads(cleaned_text)
            
            # 验证必要字段
            required_fields = ['personal_info', 'work_experience', 'education', 'skills']
            for field in required_fields:
                if field not in parsed_data:
                    raise QwenParseError(f"API响应缺少必要字段: {field}")
            
            return parsed_data
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败，原始响应: {response_text}")
            raise QwenParseError(f"API响应不是有效的JSON格式: {str(e)}")
        except Exception as e:
            raise QwenParseError(f"解析API响应时发生错误: {str(e)}")
    
    def _build_resume_data(self, parsed_data: Dict[str, Any]) -> ResumeData:
        """构建ResumeData对象"""
        try:
            # 生成唯一ID
            resume_id = f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # 构建个人信息
            personal_info_data = parsed_data.get('personal_info', {})
            personal_info = PersonalInfo(
                name=personal_info_data.get('name', ''),
                email=personal_info_data.get('email', ''),
                phone=personal_info_data.get('phone'),
                location=personal_info_data.get('location'),
                summary=personal_info_data.get('summary'),
                linkedin=personal_info_data.get('linkedin'),
                github=personal_info_data.get('github'),
                website=personal_info_data.get('website')
            )
            
            # 构建工作经历
            work_experience = []
            for exp_data in parsed_data.get('work_experience', []):
                if exp_data.get('company') and exp_data.get('position'):
                    work_exp = WorkExperience(
                        company=exp_data.get('company', ''),
                        position=exp_data.get('position', ''),
                        start_date=exp_data.get('start_date', ''),
                        end_date=exp_data.get('end_date'),
                        description=exp_data.get('description', []),
                        technologies=exp_data.get('technologies')
                    )
                    work_experience.append(work_exp)
            
            # 构建教育背景
            education = []
            for edu_data in parsed_data.get('education', []):
                if edu_data.get('institution'):
                    edu = Education(
                        institution=edu_data.get('institution', ''),
                        degree=edu_data.get('degree', ''),
                        major=edu_data.get('major'),
                        start_date=edu_data.get('start_date', ''),
                        end_date=edu_data.get('end_date'),
                        gpa=edu_data.get('gpa')
                    )
                    education.append(edu)
            
            # 构建技能
            skills = []
            for skill_data in parsed_data.get('skills', []):
                if skill_data.get('name'):
                    skill = Skill(
                        category=skill_data.get('category', 'technical'),
                        name=skill_data.get('name', ''),
                        level=skill_data.get('level')
                    )
                    skills.append(skill)
            
            # 创建ResumeData对象
            resume_data = ResumeData(
                id=resume_id,
                personal_info=personal_info,
                work_experience=work_experience,
                education=education,
                skills=skills,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            return resume_data
            
        except ValidationError as e:
            logger.error(f"数据验证失败: {e}")
            raise QwenParseError(f"解析的数据不符合预期格式: {str(e)}")
        except Exception as e:
            logger.error(f"构建ResumeData对象失败: {e}")
            raise QwenParseError(f"构建简历数据对象时发生错误: {str(e)}")
    
    def validate_parsed_data(self, resume_data: ResumeData) -> Dict[str, Any]:
        """
        验证解析结果的质量
        
        Args:
            resume_data: 解析后的简历数据
            
        Returns:
            验证结果字典
        """
        validation_result = {
            'is_valid': True,
            'warnings': [],
            'errors': [],
            'completeness_score': 0.0
        }
        
        # 检查必要信息
        if not resume_data.personal_info.name:
            validation_result['errors'].append('缺少姓名信息')
            validation_result['is_valid'] = False
        
        if not resume_data.personal_info.email and not resume_data.personal_info.phone:
            validation_result['warnings'].append('缺少联系方式（邮箱或电话）')
        
        # 检查工作经历
        if not resume_data.work_experience:
            validation_result['warnings'].append('未找到工作经历信息')
        else:
            for i, exp in enumerate(resume_data.work_experience):
                if not exp.company or not exp.position:
                    validation_result['warnings'].append(f'第{i+1}个工作经历信息不完整')
        
        # 检查教育背景
        if not resume_data.education:
            validation_result['warnings'].append('未找到教育背景信息')
        
        # 检查技能
        if not resume_data.skills:
            validation_result['warnings'].append('未找到技能信息')
        
        # 计算完整性评分
        total_fields = 7  # 姓名、联系方式、工作经历、教育背景、技能、个人简介、其他信息
        completed_fields = 0
        
        if resume_data.personal_info.name:
            completed_fields += 1
        if resume_data.personal_info.email or resume_data.personal_info.phone:
            completed_fields += 1
        if resume_data.work_experience:
            completed_fields += 1
        if resume_data.education:
            completed_fields += 1
        if resume_data.skills:
            completed_fields += 1
        if resume_data.personal_info.summary:
            completed_fields += 1
        if (resume_data.personal_info.linkedin or 
            resume_data.personal_info.github or 
            resume_data.personal_info.website):
            completed_fields += 1
        
        validation_result['completeness_score'] = completed_fields / total_fields
        
        return validation_result


# 创建全局实例
qwen_parser = QwenResumeParser()
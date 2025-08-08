# 通义千问简历解析器使用指南

## 概述

通义千问简历解析器（QwenResumeParser）是一个基于阿里云通义千问大模型的智能简历解析工具，能够将PDF简历文本转换为结构化的数据格式。

## 功能特性

- ✅ **智能文本解析**：使用通义千问API解析简历内容
- ✅ **结构化输出**：生成符合Pydantic模型的结构化数据
- ✅ **中英文映射**：自动将中文分类和水平映射为英文枚举值
- ✅ **数据验证**：内置数据完整性和质量验证
- ✅ **错误处理**：完善的异常处理和错误提示
- ✅ **灵活配置**：支持多种模型和参数配置

## 安装和配置

### 1. 安装依赖

```bash
pip install dashscope pydantic
```

### 2. 获取API密钥

1. 访问 [阿里云DashScope控制台](https://dashscope.console.aliyun.com/)
2. 注册账号并创建API密钥
3. 在项目根目录创建 `.env` 文件：

```env
DASHSCOPE_API_KEY=your_api_key_here
```

### 3. 环境变量配置

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("DASHSCOPE_API_KEY")
```

## 基本使用

### 1. 导入和初始化

```python
from services.qwen_parser import QwenResumeParser, QwenParseError

# 创建解析器实例
parser = QwenResumeParser()
```

### 2. 解析简历文本

```python
# 简历文本（通常来自PDF提取）
resume_text = """
张三
软件工程师
电话：138-1234-5678
邮箱：zhangsan@example.com

工作经历：
2020年1月-2023年12月  ABC公司  高级工程师
• 负责后端开发
• 团队管理

教育背景：
2016年9月-2020年6月  清华大学  计算机科学  本科

技能：
编程语言：Java（精通）、Python（熟练）
"""

try:
    # 解析简历
    resume_data = parser.parse_resume_text(resume_text)
    
    # 访问解析结果
    print(f"姓名: {resume_data.personal_info.name}")
    print(f"邮箱: {resume_data.personal_info.email}")
    print(f"工作经历: {len(resume_data.work_experience)}项")
    
except QwenParseError as e:
    print(f"解析失败: {e}")
```

### 3. 数据验证

```python
# 验证解析质量
validation_result = parser.validate_parsed_data(resume_data)

print(f"验证状态: {validation_result['is_valid']}")
print(f"完整性评分: {validation_result['completeness_score']:.2%}")

if validation_result['warnings']:
    print("警告:")
    for warning in validation_result['warnings']:
        print(f"  - {warning}")
```

## 数据模型

### 个人信息 (PersonalInfo)

```python
{
    "name": "姓名",
    "email": "邮箱地址",
    "phone": "电话号码",
    "location": "所在地区",
    "summary": "个人简介",
    "linkedin": "LinkedIn链接",
    "github": "GitHub链接",
    "website": "个人网站"
}
```

### 工作经历 (WorkExperience)

```python
{
    "company": "公司名称",
    "position": "职位名称",
    "start_date": "开始时间",
    "end_date": "结束时间",
    "description": ["工作描述列表"],
    "technologies": ["技术栈列表"]
}
```

### 教育背景 (Education)

```python
{
    "institution": "学校名称",
    "degree": "学位",
    "major": "专业",
    "start_date": "开始时间",
    "end_date": "结束时间",
    "gpa": "GPA"
}
```

### 技能 (Skill)

```python
{
    "category": "technical|soft|language",  # 技能分类
    "name": "技能名称",
    "level": "beginner|intermediate|advanced|expert"  # 技能水平
}
```

## 中英文映射

### 技能分类映射

| 中文分类 | 英文枚举 |
|---------|---------|
| 编程语言、技术技能、框架、数据库、工具 | technical |
| 软技能、沟通能力、领导力、团队合作 | soft |
| 语言、外语 | language |

### 技能水平映射

| 中文水平 | 英文枚举 |
|---------|---------|
| 了解、初级 | beginner |
| 熟悉、熟练 | intermediate |
| 精通 | advanced |
| 专家、资深 | expert |

## 高级配置

### 1. 自定义模型参数

```python
parser = QwenResumeParser()
parser.model = "qwen-plus"  # 使用更高级的模型
parser.temperature = 0.1    # 降低随机性
parser.max_tokens = 3000    # 增加输出长度
```

### 2. 自定义提示模板

```python
# 继承并重写提示构建方法
class CustomQwenParser(QwenResumeParser):
    def _build_parse_prompt(self, resume_text: str) -> str:
        # 自定义提示逻辑
        return custom_prompt
```

## 错误处理

### 常见错误类型

1. **QwenParseError**: 通义千问解析相关错误
2. **ValidationError**: 数据验证错误
3. **APIError**: API调用错误

### 错误处理示例

```python
try:
    resume_data = parser.parse_resume_text(text)
except QwenParseError as e:
    if "API调用失败" in str(e):
        # 处理API错误
        print("请检查网络连接和API密钥")
    elif "JSON格式" in str(e):
        # 处理格式错误
        print("AI返回格式异常，请重试")
    else:
        # 其他解析错误
        print(f"解析失败: {e}")
```

## 性能优化

### 1. 批量处理

```python
def batch_parse_resumes(texts: List[str]) -> List[ResumeData]:
    parser = QwenResumeParser()
    results = []
    
    for text in texts:
        try:
            result = parser.parse_resume_text(text)
            results.append(result)
        except QwenParseError as e:
            print(f"解析失败: {e}")
            continue
    
    return results
```

### 2. 缓存机制

```python
import hashlib
import json

def parse_with_cache(parser, text: str) -> ResumeData:
    # 生成文本哈希作为缓存键
    text_hash = hashlib.md5(text.encode()).hexdigest()
    cache_file = f"cache/{text_hash}.json"
    
    # 检查缓存
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cached_data = json.load(f)
            return ResumeData(**cached_data)
    
    # 解析并缓存
    result = parser.parse_resume_text(text)
    os.makedirs("cache", exist_ok=True)
    with open(cache_file, 'w') as f:
        json.dump(result.model_dump(), f)
    
    return result
```

## 测试和验证

### 1. 运行单元测试

```bash
python -m pytest backend/tests/test_qwen_parser.py -v
```

### 2. 功能验证

```bash
python backend/examples/qwen_validation.py
```

### 3. 演示脚本

```bash
python backend/examples/qwen_parser_demo.py
```

## 最佳实践

### 1. 输入文本预处理

```python
def preprocess_resume_text(text: str) -> str:
    # 清理文本
    text = text.strip()
    # 移除多余空行
    text = re.sub(r'\n\s*\n', '\n\n', text)
    # 统一编码
    text = text.encode('utf-8').decode('utf-8')
    return text
```

### 2. 结果后处理

```python
def postprocess_resume_data(resume_data: ResumeData) -> ResumeData:
    # 标准化日期格式
    for exp in resume_data.work_experience:
        exp.start_date = standardize_date(exp.start_date)
        if exp.end_date:
            exp.end_date = standardize_date(exp.end_date)
    
    # 去重技能
    unique_skills = []
    seen_skills = set()
    for skill in resume_data.skills:
        if skill.name not in seen_skills:
            unique_skills.append(skill)
            seen_skills.add(skill.name)
    resume_data.skills = unique_skills
    
    return resume_data
```

### 3. 质量监控

```python
def monitor_parse_quality(resume_data: ResumeData) -> Dict[str, Any]:
    validation = parser.validate_parsed_data(resume_data)
    
    metrics = {
        'completeness_score': validation['completeness_score'],
        'has_name': bool(resume_data.personal_info.name),
        'has_contact': bool(resume_data.personal_info.email or resume_data.personal_info.phone),
        'work_experience_count': len(resume_data.work_experience),
        'education_count': len(resume_data.education),
        'skills_count': len(resume_data.skills)
    }
    
    return metrics
```

## 故障排除

### 1. API密钥问题

```bash
# 检查环境变量
echo $DASHSCOPE_API_KEY

# 测试API连接
python -c "import dashscope; dashscope.api_key='your_key'; print('API密钥有效')"
```

### 2. 解析质量问题

- 检查输入文本质量
- 调整模型参数
- 优化提示模板
- 增加后处理逻辑

### 3. 性能问题

- 使用更快的模型（qwen-turbo）
- 减少max_tokens参数
- 实现缓存机制
- 批量处理优化

## 更新日志

### v1.0.0 (2024-01-08)
- ✅ 基础解析功能实现
- ✅ 中英文映射支持
- ✅ 数据验证机制
- ✅ 完整的错误处理
- ✅ 单元测试覆盖

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue或联系开发团队。
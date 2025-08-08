# 设计文档

## 概述

个人简介网站生成器是一个全栈Web应用程序，它接收用户上传的PDF简历，使用AI技术解析内容，并生成具有现代化设计风格的个人简介网站。系统采用前后端分离架构，支持实时内容更新和响应式设计。

## 架构

### 整体架构
```
前端 (Vue + TypeScript)
    ↓ HTTP API
后端 (Python + FastAPI)
    ↓
PDF解析服务 (PyPDF2/pdfplumber + Qwen API)
    ↓
数据存储 (RedisStack + 文件系统)
    ↓
网站生成引擎 (Vue SSG)
```

### 技术栈选择
- **前端**: Vue 3 + TypeScript + Tailwind CSS + Vue Transition
- **后端**: Python 3.9+ + FastAPI + Pydantic
- **PDF解析**: PyPDF2/pdfplumber + 通义千问(Qwen) API
- **数据库**: RedisStack (Redis + RedisJSON + RediSearch)
- **文件存储**: 本地文件系统
- **网站生成**: Vue 3 + Nuxt.js (静态生成)
- **部署**: 支持本地运行和云部署

## 组件和接口

### 前端组件

#### 1. 文件上传组件 (FileUpload.vue)
```typescript
interface FileUploadProps {
  onFileSelect: (file: File) => void;
  acceptedTypes: string[];
  maxSize: number;
}
```

#### 2. 简历解析状态组件 (ParseStatus.vue)
```typescript
interface ParseStatusProps {
  status: 'idle' | 'parsing' | 'success' | 'error';
  progress: number;
  message: string;
}
```

#### 3. 网站预览组件 (WebsitePreview.vue)
```typescript
interface WebsitePreviewProps {
  resumeData: ResumeData;
  template: TemplateConfig;
}
```

#### 4. 生成的个人网站组件 (PersonalWebsite.vue)
```typescript
interface PersonalWebsiteProps {
  personalInfo: PersonalInfo;
  workExperience: WorkExperience[];
  education: Education[];
  skills: Skill[];
  template: TemplateConfig;
}
```

### 后端API接口 (FastAPI)

#### 1. 文件上传接口
```python
@app.post("/api/upload")
async def upload_resume(file: UploadFile = File(...)):
    # Content-Type: multipart/form-data
    # Response: { "upload_id": str, "message": str }
```

#### 2. 简历解析接口
```python
@app.post("/api/parse/{upload_id}")
async def parse_resume(upload_id: str):
    # Response: { 
    #   "status": str,
    #   "data": ResumeData,
    #   "website_url": Optional[str] 
    # }
```

#### 3. 网站生成接口
```python
@app.post("/api/generate-website")
async def generate_website(request: WebsiteGenerationRequest):
    # Body: { "resume_data": ResumeData, "template_id": str }
    # Response: { "website_url": str, "preview_url": str }
```

#### 4. 网站更新接口
```python
@app.put("/api/website/{website_id}")
async def update_website(website_id: str, request: WebsiteUpdateRequest):
    # Body: { "resume_data": ResumeData }
    # Response: { "success": bool, "website_url": str }
```

## 数据模型 (Pydantic)

### 用户简历数据模型
```python
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PersonalInfo(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None

class WorkExperience(BaseModel):
    company: str
    position: str
    start_date: str
    end_date: Optional[str] = None
    description: List[str]
    technologies: Optional[List[str]] = None

class Education(BaseModel):
    institution: str
    degree: str
    major: Optional[str] = None
    start_date: str
    end_date: Optional[str] = None
    gpa: Optional[str] = None

class Skill(BaseModel):
    category: str  # 'technical' | 'soft' | 'language'
    name: str
    level: Optional[str] = None  # 'beginner' | 'intermediate' | 'advanced' | 'expert'

class ResumeData(BaseModel):
    id: str
    personal_info: PersonalInfo
    work_experience: List[WorkExperience]
    education: List[Education]
    skills: List[Skill]
    created_at: datetime
    updated_at: datetime
```

### 网站配置模型
```python
class ColorScheme(BaseModel):
    primary: str
    secondary: str
    accent: str
    background: str
    text: str

class WebsiteConfig(BaseModel):
    id: str
    resume_id: str
    template_id: str
    color_scheme: ColorScheme
    url: str
    is_public: bool
```

### RedisStack数据存储模型
```python
import redis
from redis.commands.json.path import Path
import json
from datetime import datetime
from typing import Dict, Any

class RedisDataManager:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
    
    async def save_resume(self, resume_data: ResumeData) -> str:
        """保存简历数据到RedisJSON"""
        resume_key = f"resume:{resume_data.id}"
        resume_dict = resume_data.dict()
        
        # 使用RedisJSON存储结构化数据
        self.redis_client.json().set(resume_key, Path.root_path(), resume_dict)
        
        # 创建索引用于搜索
        self.redis_client.sadd("resumes:all", resume_data.id)
        
        # 为知识库功能预留：存储文本内容用于向量搜索
        text_content = self._extract_text_for_search(resume_data)
        self.redis_client.hset(f"resume:text:{resume_data.id}", mapping={
            "content": text_content,
            "created_at": resume_data.created_at.isoformat()
        })
        
        return resume_data.id
    
    async def get_resume(self, resume_id: str) -> Dict[str, Any]:
        """从RedisJSON获取简历数据"""
        resume_key = f"resume:{resume_id}"
        return self.redis_client.json().get(resume_key)
    
    async def search_resumes(self, query: str) -> List[str]:
        """使用RediSearch搜索简历（为知识库功能预留）"""
        # 这里可以使用RediSearch进行全文搜索
        # 或者结合向量搜索实现语义搜索
        pass
    
    async def save_website_config(self, website_config: WebsiteConfig) -> str:
        """保存网站配置"""
        config_key = f"website:{website_config.id}"
        config_dict = website_config.dict()
        
        self.redis_client.json().set(config_key, Path.root_path(), config_dict)
        
        # 建立简历和网站的关联
        self.redis_client.sadd(f"resume:websites:{website_config.resume_id}", website_config.id)
        
        return website_config.id
    
    def _extract_text_for_search(self, resume_data: ResumeData) -> str:
        """提取简历文本用于搜索索引"""
        text_parts = [
            resume_data.personal_info.name,
            resume_data.personal_info.summary or "",
        ]
        
        for exp in resume_data.work_experience:
            text_parts.extend([exp.company, exp.position])
            text_parts.extend(exp.description)
        
        for edu in resume_data.education:
            text_parts.extend([edu.institution, edu.degree, edu.major or ""])
        
        for skill in resume_data.skills:
            text_parts.append(skill.name)
        
        return " ".join(filter(None, text_parts))

# Redis配置
REDIS_CONFIG = {
    "url": "redis://localhost:6379",
    "decode_responses": True,
    "health_check_interval": 30
}
```

### 知识库扩展预留设计
```python
class KnowledgeBaseManager:
    """为未来知识库功能预留的管理器"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
    
    async def add_document_embedding(self, doc_id: str, embedding: List[float]):
        """存储文档向量嵌入（使用Redis Vector Similarity Search）"""
        # 使用RedisStack的向量搜索功能
        pass
    
    async def semantic_search(self, query_embedding: List[float], top_k: int = 5):
        """语义搜索相关简历"""
        # 实现向量相似度搜索
        pass
    
    async def build_knowledge_graph(self, resume_ids: List[str]):
        """构建简历知识图谱"""
        # 使用RedisGraph构建关系图谱
        pass
```

## PDF解析策略

### 解析流程
1. **文本提取**: 使用PyPDF2或pdfplumber提取PDF中的原始文本
2. **结构化分析**: 使用通义千问(Qwen) API分析文本结构
3. **信息提取**: 通过提示工程提取结构化数据
4. **数据验证**: 使用Pydantic验证提取的数据完整性和准确性

### Python PDF解析配置
```python
import PyPDF2
import pdfplumber
from dashscope import Generation
import os

# Qwen API配置
QWEN_CONFIG = {
    "api_key": os.getenv("DASHSCOPE_API_KEY"),
    "model": "qwen-turbo",  # 或 qwen-plus, qwen-max
}

def extract_text_from_pdf(pdf_path: str) -> str:
    """从PDF文件中提取文本"""
    text = ""
    try:
        # 优先使用pdfplumber，处理复杂布局更好
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    except Exception:
        # 备用方案：使用PyPDF2
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    return text
```

### Qwen API调用
```python
async def parse_resume_with_qwen(resume_text: str) -> dict:
    """使用Qwen API解析简历文本"""
    prompt = f"""
你是一个专业的简历解析助手。请分析以下简历文本，提取结构化信息。

简历文本：
{resume_text}

请严格按照以下JSON格式返回：
{{
  "personal_info": {{
    "name": "姓名",
    "email": "邮箱",
    "phone": "电话",
    "location": "地址",
    "summary": "个人简介"
  }},
  "work_experience": [
    {{
      "company": "公司名称",
      "position": "职位",
      "start_date": "开始时间",
      "end_date": "结束时间",
      "description": ["工作描述1", "工作描述2"]
    }}
  ],
  "education": [
    {{
      "institution": "学校名称",
      "degree": "学位",
      "major": "专业",
      "start_date": "开始时间",
      "end_date": "结束时间"
    }}
  ],
  "skills": [
    {{
      "category": "技术技能",
      "name": "技能名称",
      "level": "熟练程度"
    }}
  ]
}}
"""
    
    response = Generation.call(
        model=QWEN_CONFIG["model"],
        prompt=prompt,
        api_key=QWEN_CONFIG["api_key"]
    )
    
    return response.output.text
```

## 网站模板设计

### 模板特性
- **现代化设计**: 使用渐变背景、卡片式布局、微交互
- **响应式布局**: 支持桌面、平板、手机三种屏幕尺寸
- **动画效果**: 页面加载动画、滚动触发动画、悬停效果
- **可定制性**: 支持颜色主题、布局调整

### 布局结构
```
Header (个人信息 + 导航)
├── Hero Section (姓名 + 简介)
├── About Section (个人描述)
├── Experience Section (工作经历时间线)
├── Education Section (教育背景)
├── Skills Section (技能展示)
└── Contact Section (联系方式)
```

## 错误处理

### PDF解析错误
- 文件格式不支持
- 文件损坏或加密
- 文本提取失败
- AI解析超时或失败

### 网站生成错误
- 模板渲染失败
- 静态文件生成错误
- 部署失败

### 用户体验优化
- 进度指示器
- 友好的错误提示
- 重试机制
- 降级方案（手动输入）

## 测试策略

### 单元测试
- PDF解析功能测试
- 数据模型验证测试
- API接口测试
- 组件渲染测试

### 集成测试
- 完整的简历上传到网站生成流程
- 不同格式PDF文件的兼容性测试
- 响应式设计测试

### 端到端测试
- 用户完整使用流程测试
- 多种简历格式的真实场景测试
- 性能和加载速度测试

## 部署和扩展

### 本地开发环境
- Docker容器化部署
- 热重载开发服务器
- 本地数据库和文件存储

### 生产环境选项
- **选项1**: 单机部署（适合个人使用）
- **选项2**: 云服务部署（支持多用户）
- **选项3**: 静态网站托管（生成的网站）

### 扩展性考虑
- 支持多种模板主题
- 集成更多AI服务提供商
- 支持多语言简历
- 添加网站分析功能
##
 网站模板设计

### 模板特性
- **现代化设计**: 使用渐变背景、卡片式布局、微交互
- **响应式布局**: 支持桌面、平板、手机三种屏幕尺寸
- **Vue动画效果**: 使用Vue Transition和CSS动画实现页面加载动画、滚动触发动画、悬停效果
- **可定制性**: 支持颜色主题、布局调整

### Vue组件结构
```
PersonalWebsite.vue
├── HeaderSection.vue (个人信息 + 导航)
├── HeroSection.vue (姓名 + 简介)
├── AboutSection.vue (个人描述)
├── ExperienceSection.vue (工作经历时间线)
├── EducationSection.vue (教育背景)
├── SkillsSection.vue (技能展示)
└── ContactSection.vue (联系方式)
```

### Vue动画配置
```vue
<template>
  <Transition name="fade" appear>
    <div class="section">
      <TransitionGroup name="slide" tag="div">
        <div v-for="item in items" :key="item.id" class="item">
          {{ item.content }}
        </div>
      </TransitionGroup>
    </div>
  </Transition>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.slide-enter-active, .slide-leave-active {
  transition: all 0.3s ease;
}
.slide-enter-from {
  opacity: 0;
  transform: translateY(30px);
}
</style>
```

## 错误处理

### PDF解析错误
- 文件格式不支持
- 文件损坏或加密
- 文本提取失败
- Qwen API解析超时或失败

### 网站生成错误
- Vue模板渲染失败
- 静态文件生成错误
- 部署失败

### 用户体验优化
- Vue进度指示器组件
- 友好的错误提示
- 重试机制
- 降级方案（手动输入）

## 测试策略

### 单元测试
- PDF解析功能测试
- 数据模型验证测试
- API接口测试
- Vue组件渲染测试（使用Vue Test Utils）

### 集成测试
- 完整的简历上传到网站生成流程
- 不同格式PDF文件的兼容性测试
- Vue响应式设计测试

### 端到端测试
- 用户完整使用流程测试（使用Cypress）
- 多种简历格式的真实场景测试
- 性能和加载速度测试

## 部署和扩展

### 本地开发环境
- Docker容器化部署 (包含RedisStack)
- FastAPI自动重载开发服务器 (uvicorn --reload)
- Vite热重载开发服务器 (前端)
- RedisStack本地实例 (Redis + RedisJSON + RediSearch + RedisGraph)

### Docker Compose配置示例
```yaml
version: '3.8'
services:
  redis-stack:
    image: redis/redis-stack:latest
    ports:
      - "6379:6379"
      - "8001:8001"  # RedisInsight Web UI
    volumes:
      - redis_data:/data
    environment:
      - REDIS_ARGS=--save 60 1000
  
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - redis-stack
    environment:
      - REDIS_URL=redis://redis-stack:6379
      - DASHSCOPE_API_KEY=${DASHSCOPE_API_KEY}
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  redis_data:
```

### 生产环境选项
- **选项1**: 单机部署（适合个人使用）
- **选项2**: 云服务部署（支持多用户）
- **选项3**: 静态网站托管（使用Nuxt.js生成的网站）

### 扩展性考虑
- 支持多种Vue模板主题
- 集成更多AI服务提供商（除Qwen外）
- 支持多语言简历
- 添加网站分析功能
- Vue插件生态系统集成

### 知识库功能扩展路径
- **向量搜索**: 使用RedisStack的向量相似度搜索实现语义搜索
- **知识图谱**: 利用RedisGraph构建简历间的关系网络
- **智能推荐**: 基于简历内容推荐相关职位或技能
- **技能分析**: 分析行业技能趋势和个人技能匹配度
- **职业路径规划**: 基于历史数据提供职业发展建议

### RedisStack优势
- **高性能**: 内存数据库，读写速度快
- **多模态**: 支持JSON、搜索、图数据库、向量搜索
- **扩展性**: 易于水平扩展，支持集群模式
- **实时性**: 支持实时数据更新和搜索
- **简化架构**: 一个数据库解决多种数据需求
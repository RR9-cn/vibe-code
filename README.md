# 个人简历网站生成器

一个自动化的个人简历网站生成器，用户可以上传PDF格式的简历，系统会自动解析简历内容并生成具有现代化设计风格的个人简介网站。

## 功能特性

- 📄 **PDF简历解析**: 支持上传PDF格式简历，自动提取个人信息、工作经历、教育背景等
- 🤖 **AI智能解析**: 集成通义千问API，准确识别和结构化简历内容
- 🎨 **现代化设计**: 生成具有现代化视觉风格的响应式个人网站
- 🔄 **实时更新**: 支持重新上传简历更新网站内容
- 🚀 **快速部署**: 使用Docker容器化部署，支持一键启动

## 技术架构

### 前端
- Vue 3 + TypeScript
- Tailwind CSS
- Vue Router + Pinia
- Vite构建工具

### 后端
- Python + FastAPI
- Pydantic数据验证
- PDF解析：PyPDF2 + pdfplumber
- AI解析：通义千问(Qwen) API

### 数据存储
- RedisStack (Redis + RedisJSON + RediSearch)
- 支持结构化数据存储和搜索

## 快速开始

### 环境要求
- Docker & Docker Compose
- Node.js 18+ (本地开发)
- Python 3.11+ (本地开发)

### 使用Docker启动（推荐）

1. 克隆项目
```bash
git clone <repository-url>
cd resume-website-generator
```

2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入通义千问API密钥
```

3. 启动服务
```bash
docker-compose up -d
```

4. 访问应用
- 前端应用: http://localhost:3000
- 后端API: http://localhost:8000
- RedisInsight: http://localhost:8001

### 本地开发

#### 后端开发
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### 前端开发
```bash
cd frontend
npm install
npm run dev
```

## 项目结构

```
resume-website-generator/
├── backend/                 # FastAPI后端服务
│   ├── main.py             # 主应用文件
│   ├── requirements.txt    # Python依赖
│   ├── Dockerfile          # 后端Docker配置
│   └── .env.example        # 后端环境变量示例
├── frontend/               # Vue前端应用
│   ├── src/                # 源代码
│   ├── package.json        # Node.js依赖
│   ├── vite.config.ts      # Vite配置
│   ├── tailwind.config.js  # Tailwind CSS配置
│   └── Dockerfile          # 前端Docker配置
├── docker-compose.yml      # Docker Compose配置
├── .env.example           # 项目环境变量示例
└── README.md              # 项目说明文档
```

## API接口

### 文件上传
```
POST /api/upload
Content-Type: multipart/form-data
```

### 简历解析
```
POST /api/parse/{upload_id}
```

### 网站生成
```
POST /api/generate-website
```

### 健康检查
```
GET /health
```

## 开发指南

### 添加新功能
1. 在对应的目录下创建新的模块
2. 更新相关的配置文件
3. 编写单元测试
4. 更新文档

### 测试
```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm run test
```

## 部署说明

项目支持多种部署方式：
- Docker Compose（推荐）
- 单独部署前后端服务
- 云服务部署

详细部署指南请参考部署文档。

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进项目。
"""
个人简历网站生成器 - 后端主应用
使用FastAPI构建的REST API服务
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 创建FastAPI应用实例
app = FastAPI(
    title="个人简历网站生成器",
    description="自动解析PDF简历并生成个人网站的API服务",
    version="1.0.0"
)

# 配置CORS中间件，允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Vue开发服务器地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """根路径健康检查接口"""
    return {"message": "个人简历网站生成器API服务正在运行"}

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "service": "resume-website-generator"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
@echo off
echo 启动个人简历网站生成器开发环境
echo =====================================

echo.
echo 1. 启动后端服务...
cd backend
call venv\Scripts\activate
start "后端服务" cmd /k "uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo 2. 启动前端服务...
cd ..\frontend
start "前端服务" cmd /k "npm run dev"

echo.
echo 3. 服务启动完成！
echo 前端地址: http://localhost:3000
echo 后端API: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo.
echo 按任意键退出...
pause > nul
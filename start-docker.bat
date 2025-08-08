@echo off
echo 使用Docker启动个人简历网站生成器
echo =====================================

echo.
echo 检查环境变量文件...
if not exist .env (
    echo 警告: .env 文件不存在，请复制 .env.example 为 .env 并配置相关参数
    echo.
    pause
    exit /b 1
)

echo.
echo 启动Docker服务...
docker-compose up -d

echo.
echo 等待服务启动...
timeout /t 10 /nobreak > nul

echo.
echo 检查服务状态...
docker-compose ps

echo.
echo 服务启动完成！
echo 前端地址: http://localhost:3000
echo 后端API: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo RedisInsight: http://localhost:8001
echo.
echo 查看日志: docker-compose logs -f
echo 停止服务: docker-compose down
echo.
pause
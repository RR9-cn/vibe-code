#!/usr/bin/env python3
"""
个人简历网站生成器 - 项目设置脚本
用于初始化Python虚拟环境和安装依赖
"""

import os
import sys
import subprocess
import platform

def run_command(command, cwd=None):
    """执行命令并返回结果"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd,
            capture_output=True, 
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {command}")
        print(f"错误信息: {e.stderr}")
        return None

def setup_backend():
    """设置后端Python环境"""
    print("🐍 设置后端Python环境...")
    
    backend_dir = "backend"
    if not os.path.exists(backend_dir):
        print(f"错误: {backend_dir} 目录不存在")
        return False
    
    # 创建虚拟环境
    venv_path = os.path.join(backend_dir, "venv")
    if not os.path.exists(venv_path):
        print("创建Python虚拟环境...")
        result = run_command("python -m venv venv", cwd=backend_dir)
        if result is None:
            print("虚拟环境创建失败")
            return False
    
    # 确定激活脚本路径
    if platform.system() == "Windows":
        activate_script = os.path.join(venv_path, "Scripts", "activate")
        pip_path = os.path.join(venv_path, "Scripts", "pip")
    else:
        activate_script = os.path.join(venv_path, "bin", "activate")
        pip_path = os.path.join(venv_path, "bin", "pip")
    
    # 安装依赖
    print("安装Python依赖...")
    result = run_command(f"{pip_path} install -r requirements.txt", cwd=backend_dir)
    if result is None:
        print("依赖安装失败")
        return False
    
    print("✅ 后端环境设置完成")
    return True

def setup_frontend():
    """设置前端Node.js环境"""
    print("📦 设置前端Node.js环境...")
    
    frontend_dir = "frontend"
    if not os.path.exists(frontend_dir):
        print(f"错误: {frontend_dir} 目录不存在")
        return False
    
    # 检查npm是否可用
    result = run_command("npm --version")
    if result is None:
        print("错误: npm未安装，请先安装Node.js")
        return False
    
    # 安装依赖
    print("安装Node.js依赖...")
    result = run_command("npm install", cwd=frontend_dir)
    if result is None:
        print("依赖安装失败")
        return False
    
    print("✅ 前端环境设置完成")
    return True

def check_docker():
    """检查Docker是否可用"""
    print("🐳 检查Docker环境...")
    
    # 检查Docker
    result = run_command("docker --version")
    if result is None:
        print("⚠️  Docker未安装，无法使用容器化部署")
        return False
    
    # 检查Docker Compose
    result = run_command("docker-compose --version")
    if result is None:
        print("⚠️  Docker Compose未安装，无法使用容器化部署")
        return False
    
    print("✅ Docker环境检查完成")
    return True

def main():
    """主函数"""
    print("🚀 个人简历网站生成器 - 项目初始化")
    print("=" * 50)
    
    # 检查环境变量文件
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            print("📝 请复制 .env.example 为 .env 并配置相关参数")
        else:
            print("⚠️  未找到环境变量配置文件")
    
    # 设置后端环境
    backend_success = setup_backend()
    
    # 设置前端环境
    frontend_success = setup_frontend()
    
    # 检查Docker环境
    docker_available = check_docker()
    
    print("\n" + "=" * 50)
    print("📋 设置结果总结:")
    print(f"后端环境: {'✅ 成功' if backend_success else '❌ 失败'}")
    print(f"前端环境: {'✅ 成功' if frontend_success else '❌ 失败'}")
    print(f"Docker环境: {'✅ 可用' if docker_available else '❌ 不可用'}")
    
    if backend_success and frontend_success:
        print("\n🎉 项目初始化完成！")
        print("\n启动方式:")
        if docker_available:
            print("1. 使用Docker (推荐): docker-compose up -d")
        print("2. 本地开发:")
        print("   后端: cd backend && source venv/bin/activate && uvicorn main:app --reload")
        print("   前端: cd frontend && npm run dev")
    else:
        print("\n❌ 项目初始化失败，请检查错误信息")
        sys.exit(1)

if __name__ == "__main__":
    main()
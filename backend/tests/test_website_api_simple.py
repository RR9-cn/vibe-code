"""
网站API简单测试
测试不依赖外部服务的API端点
"""

import pytest
from fastapi.testclient import TestClient

# 直接导入FastAPI应用，避免复杂的依赖
from fastapi import FastAPI
from backend.api.website import router as website_router

# 创建简单的测试应用
test_app = FastAPI()
test_app.include_router(website_router)


@pytest.fixture
def client():
    """创建测试客户端"""
    return TestClient(test_app)


class TestWebsiteAPISimple:
    """网站API简单测试类"""
    
    def test_get_available_templates(self, client):
        """测试获取可用模板"""
        response = client.get("/api/templates")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "templates" in data
        assert len(data["templates"]) > 0
        
        # 检查模板结构
        template = data["templates"][0]
        assert "id" in template
        assert "name" in template
        assert "description" in template
        assert "features" in template
        
        # 检查是否包含现代风格模板
        template_ids = [t["id"] for t in data["templates"]]
        assert "modern" in template_ids
    
    def test_get_predefined_color_schemes(self, client):
        """测试获取预定义颜色方案"""
        response = client.get("/api/color-schemes")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "color_schemes" in data
        assert len(data["color_schemes"]) > 0
        
        # 检查颜色方案结构
        scheme = data["color_schemes"][0]
        assert "id" in scheme
        assert "name" in scheme
        assert "scheme" in scheme
        
        # 检查颜色方案内容
        colors = scheme["scheme"]
        required_colors = ["primary", "secondary", "accent", "background", "text"]
        for color in required_colors:
            assert color in colors
            assert colors[color].startswith("#")  # 确保是十六进制颜色
        
        # 检查是否包含蓝色主题
        scheme_ids = [s["id"] for s in data["color_schemes"]]
        assert "blue" in scheme_ids


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])
# 个人网站模板组件

这个目录包含了用于生成个人简历网站的所有Vue组件。这些组件实现了现代化的设计风格，包含丰富的动画效果和交互体验。

## 组件结构

### 主组件
- **PersonalWebsite.vue** - 主要的网站容器组件，整合所有子组件

### 子组件
- **HeaderSection.vue** - 网站头部导航组件
- **HeroSection.vue** - 英雄区域，展示个人基本信息
- **AboutSection.vue** - 关于我部分，详细个人信息
- **ExperienceSection.vue** - 工作经历时间线组件
- **EducationSection.vue** - 教育背景展示组件
- **SkillsSection.vue** - 技能展示组件
- **ContactSection.vue** - 联系方式组件

## 设计特性

### 现代化视觉设计
- 渐变背景和卡片式布局
- 圆角设计和阴影效果
- 响应式布局，支持多种设备
- 一致的颜色主题和字体系统

### 动画和交互效果
- Vue Transition 页面加载动画
- 滚动触发动画
- 悬停效果和微交互
- 平滑的页面滚动
- 回到顶部按钮

### 工作经历时间线
- 垂直时间线布局
- 交替左右显示（桌面端）
- 技能标签展示
- 工作时长统计
- 响应式移动端适配

## 使用方法

### 基本用法

```vue
<template>
  <PersonalWebsite :resume-data="resumeData" />
</template>

<script setup lang="ts">
import PersonalWebsite from '@/components/PersonalWebsite.vue'
import type { ResumeData } from '@/types'

const resumeData: ResumeData = {
  // 简历数据...
}
</script>
```

### 数据格式

组件需要符合 `ResumeData` 接口的数据：

```typescript
interface ResumeData {
  id: string
  personalInfo: PersonalInfo
  workExperience: WorkExperience[]
  education: Education[]
  skills: Skill[]
  createdAt: string
  updatedAt: string
}
```

详细的类型定义请参考 `src/types/index.ts`。

## 自定义样式

### 颜色主题
组件使用Tailwind CSS的颜色系统，主要颜色包括：
- 主色：蓝色系 (blue-500, blue-600, blue-700)
- 辅助色：靛蓝色系 (indigo-500, indigo-600)
- 强调色：紫色系 (purple-500, purple-600)

### 动画配置
动画效果通过CSS类和Vue Transition实现：
- 页面加载动画：`fade-up`, `slide-left`, `slide-right`
- 交互动画：`hover:scale-105`, `hover:-translate-y-1`
- 滚动动画：通过Intersection Observer API实现

## 响应式设计

组件采用移动优先的响应式设计：
- **移动端** (< 768px): 单列布局，简化导航
- **平板端** (768px - 1024px): 两列布局，保持核心功能
- **桌面端** (> 1024px): 完整布局，所有动画效果

## 性能优化

### 动画性能
- 使用 `transform` 和 `opacity` 属性进行动画
- 避免引起重排的CSS属性
- 合理使用 `will-change` 属性

### 图片和资源
- SVG图标减少HTTP请求
- 渐进式图片加载
- 懒加载非关键内容

## 浏览器兼容性

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 开发指南

### 添加新组件
1. 在 `website/` 目录下创建新的Vue组件
2. 遵循现有的命名约定和代码风格
3. 添加适当的TypeScript类型定义
4. 实现响应式设计和动画效果
5. 编写单元测试

### 修改样式
1. 优先使用Tailwind CSS类
2. 自定义样式使用scoped CSS
3. 保持设计系统的一致性
4. 测试不同屏幕尺寸的效果

### 测试
运行组件测试：
```bash
npm run test
```

运行特定组件测试：
```bash
npm run test PersonalWebsite
```

## 故障排除

### 常见问题

1. **动画不生效**
   - 检查Tailwind CSS配置是否正确
   - 确认动画类名拼写正确
   - 验证浏览器是否支持CSS动画

2. **响应式布局问题**
   - 检查Tailwind断点配置
   - 验证CSS Grid和Flexbox支持
   - 测试不同设备和屏幕尺寸

3. **数据不显示**
   - 检查数据格式是否符合TypeScript接口
   - 验证数据是否正确传递给组件
   - 查看浏览器控制台错误信息

### 调试技巧

1. 使用Vue DevTools检查组件状态
2. 在浏览器开发者工具中检查CSS样式
3. 使用console.log输出数据进行调试
4. 检查网络请求和API响应

## 贡献指南

欢迎提交Issue和Pull Request来改进这些组件！

### 提交规范
- 遵循现有的代码风格
- 添加适当的注释和文档
- 确保所有测试通过
- 更新相关文档

### 开发环境设置
```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 运行测试
npm run test

# 构建生产版本
npm run build
```
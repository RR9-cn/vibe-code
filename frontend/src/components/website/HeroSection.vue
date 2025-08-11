<template>
  <section class="hero-section relative min-h-screen flex items-center justify-center overflow-hidden">
    <!-- 背景装饰 -->
    <div class="absolute inset-0">
      <!-- 渐变背景 -->
      <div class="absolute inset-0 bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50"></div>
      
      <!-- 装饰性几何图形 -->
      <div class="absolute top-20 left-10 w-72 h-72 bg-blue-200/30 rounded-full blur-3xl"></div>
      <div class="absolute bottom-20 right-10 w-96 h-96 bg-indigo-200/30 rounded-full blur-3xl"></div>
      <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-purple-200/20 rounded-full blur-3xl"></div>
    </div>
    
    <!-- 主要内容 -->
    <div class="relative z-10 max-w-6xl mx-auto px-6 text-center">
      <div class="space-y-8">
        <!-- 头像区域 -->
        <div class="flex justify-center mb-8">
          <div class="relative group">
            <div class="w-32 h-32 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center shadow-2xl transform transition-all duration-500 group-hover:scale-110 group-hover:rotate-3">
              <span class="text-white font-bold text-4xl transition-all duration-300 group-hover:scale-110">
                {{ getInitials(personalInfo.name) }}
              </span>
            </div>
            <!-- 装饰性光环 -->
            <div class="absolute inset-0 rounded-full bg-gradient-to-r from-blue-400 to-indigo-500 opacity-20 animate-pulse scale-110 group-hover:opacity-40 transition-opacity duration-300"></div>
            <!-- 旋转装饰环 -->
            <div class="absolute inset-0 rounded-full border-2 border-blue-300 opacity-0 group-hover:opacity-100 animate-spin-slow transition-opacity duration-300 scale-125"></div>
          </div>
        </div>
        
        <!-- 姓名和标题 -->
        <div class="space-y-4">
          <h1 class="text-5xl md:text-7xl font-bold text-gray-900 leading-tight">
            <span class="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              {{ personalInfo.name }}
            </span>
          </h1>
          
          <!-- 职位信息（从工作经历中获取最新职位） -->
          <div v-if="latestPosition" class="text-xl md:text-2xl text-gray-600 font-medium">
            {{ latestPosition }}
          </div>
        </div>
        
        <!-- 个人简介 -->
        <div v-if="personalInfo.summary" class="max-w-3xl mx-auto">
          <p class="text-lg md:text-xl text-gray-700 leading-relaxed">
            {{ personalInfo.summary }}
          </p>
        </div>
        
        <!-- 联系方式快捷链接 -->
        <div class="flex flex-wrap justify-center gap-4 mt-8">
          <a 
            v-if="personalInfo.email"
            :href="`mailto:${personalInfo.email}`"
            class="group inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1 hover:scale-105 relative overflow-hidden"
          >
            <!-- 按钮背景动画 -->
            <div class="absolute inset-0 bg-gradient-to-r from-blue-700 to-indigo-700 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left"></div>
            <svg class="w-5 h-5 mr-2 relative z-10 transform group-hover:rotate-12 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
            </svg>
            <span class="relative z-10">联系我</span>
          </a>
          
          <a 
            v-if="personalInfo.linkedin"
            :href="personalInfo.linkedin"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex items-center px-6 py-3 bg-white text-blue-600 border-2 border-blue-600 rounded-full hover:bg-blue-600 hover:text-white transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
          >
            <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>
            LinkedIn
          </a>
          
          <a 
            v-if="personalInfo.github"
            :href="personalInfo.github"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex items-center px-6 py-3 bg-gray-900 text-white rounded-full hover:bg-gray-800 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
          >
            <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
            GitHub
          </a>
        </div>
        
        <!-- 向下滚动提示 -->
        <div class="mt-16">
          <div class="animate-bounce">
            <svg class="w-6 h-6 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
            </svg>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { PersonalInfo } from '@/types'

// Props
interface Props {
  personalInfo: PersonalInfo
}

const props = defineProps<Props>()

// 计算属性
const getInitials = (name: string): string => {
  return name
    .split(' ')
    .map(word => word.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

// 从个人简介中提取职位信息（简单实现）
const latestPosition = computed(() => {
  // 这里可以从工作经历中获取最新职位，暂时从summary中提取
  if (props.personalInfo.summary) {
    // 简单的职位提取逻辑，可以根据需要优化
    const summary = props.personalInfo.summary
    const positionKeywords = ['工程师', '开发者', '设计师', '经理', '总监', '专家', '顾问']
    
    for (const keyword of positionKeywords) {
      if (summary.includes(keyword)) {
        // 提取包含关键词的短语
        const sentences = summary.split(/[。，,.]/)
        for (const sentence of sentences) {
          if (sentence.includes(keyword)) {
            return sentence.trim()
          }
        }
      }
    }
  }
  return '专业人士'
})
</script>

<style scoped>
.hero-section {
  padding-top: 80px; /* 为固定header留出空间 */
}

/* 自定义动画 */
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}

/* 慢速旋转动画 */
@keyframes spin-slow {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin-slow {
  animation: spin-slow 8s linear infinite;
}

/* 文字渐变动画 */
.bg-gradient-to-r {
  background-size: 200% 200%;
  animation: gradient-shift 3s ease infinite;
}

@keyframes gradient-shift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

/* 按钮悬停效果增强 */
.group:hover .group-hover\:scale-x-100 {
  transform: scaleX(1);
}

.group:hover .group-hover\:rotate-12 {
  transform: rotate(12deg);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .hero-section {
    padding-top: 60px;
  }
}
</style>
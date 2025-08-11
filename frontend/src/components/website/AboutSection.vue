<template>
  <section id="about" class="py-20 bg-white">
    <div class="max-w-6xl mx-auto px-6">
      <!-- 标题 -->
      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          关于我
        </h2>
        <div class="w-24 h-1 bg-gradient-to-r from-blue-500 to-indigo-600 mx-auto rounded-full"></div>
      </div>
      
      <!-- 内容区域 -->
      <div class="grid lg:grid-cols-2 gap-12 items-center">
        <!-- 左侧：个人信息卡片 -->
        <div class="space-y-6">
          <!-- 个人简介 -->
          <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-8 shadow-lg">
            <h3 class="text-2xl font-bold text-gray-900 mb-4">个人简介</h3>
            <p class="text-gray-700 leading-relaxed text-lg">
              {{ personalInfo.summary || '一位充满激情的专业人士，致力于通过技术创新解决实际问题。' }}
            </p>
          </div>
          
          <!-- 联系信息 -->
          <div class="bg-white rounded-2xl p-8 shadow-lg border border-gray-100">
            <h3 class="text-2xl font-bold text-gray-900 mb-6">联系信息</h3>
            <div class="space-y-4">
              <!-- 邮箱 -->
              <div v-if="personalInfo.email" class="flex items-center space-x-4">
                <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                  <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                  </svg>
                </div>
                <div>
                  <p class="text-sm text-gray-500">邮箱</p>
                  <a :href="`mailto:${personalInfo.email}`" class="text-gray-900 hover:text-blue-600 transition-colors">
                    {{ personalInfo.email }}
                  </a>
                </div>
              </div>
              
              <!-- 电话 -->
              <div v-if="personalInfo.phone" class="flex items-center space-x-4">
                <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                  <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                  </svg>
                </div>
                <div>
                  <p class="text-sm text-gray-500">电话</p>
                  <a :href="`tel:${personalInfo.phone}`" class="text-gray-900 hover:text-green-600 transition-colors">
                    {{ personalInfo.phone }}
                  </a>
                </div>
              </div>
              
              <!-- 位置 -->
              <div v-if="personalInfo.location" class="flex items-center space-x-4">
                <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center">
                  <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  </svg>
                </div>
                <div>
                  <p class="text-sm text-gray-500">位置</p>
                  <p class="text-gray-900">{{ personalInfo.location }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 右侧：特色展示 -->
        <div class="space-y-8">
          <!-- 专业特点 -->
          <div class="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-2xl p-8 shadow-lg">
            <h3 class="text-2xl font-bold text-gray-900 mb-6">专业特点</h3>
            <div class="grid grid-cols-2 gap-4">
              <div class="text-center p-4 bg-white rounded-xl shadow-sm">
                <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
                  <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                  </svg>
                </div>
                <h4 class="font-semibold text-gray-900">高效执行</h4>
                <p class="text-sm text-gray-600 mt-1">快速响应需求</p>
              </div>
              
              <div class="text-center p-4 bg-white rounded-xl shadow-sm">
                <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
                  <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                  </svg>
                </div>
                <h4 class="font-semibold text-gray-900">创新思维</h4>
                <p class="text-sm text-gray-600 mt-1">持续学习进步</p>
              </div>
              
              <div class="text-center p-4 bg-white rounded-xl shadow-sm">
                <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-3">
                  <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                  </svg>
                </div>
                <h4 class="font-semibold text-gray-900">团队协作</h4>
                <p class="text-sm text-gray-600 mt-1">良好沟通能力</p>
              </div>
              
              <div class="text-center p-4 bg-white rounded-xl shadow-sm">
                <div class="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-3">
                  <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
                  </svg>
                </div>
                <h4 class="font-semibold text-gray-900">质量保证</h4>
                <p class="text-sm text-gray-600 mt-1">注重细节品质</p>
              </div>
            </div>
          </div>
          
          <!-- 社交链接 -->
          <div class="bg-white rounded-2xl p-8 shadow-lg border border-gray-100">
            <h3 class="text-2xl font-bold text-gray-900 mb-6">在线资料</h3>
            <div class="space-y-4">
              <a 
                v-if="personalInfo.linkedin"
                :href="personalInfo.linkedin"
                target="_blank"
                rel="noopener noreferrer"
                class="flex items-center space-x-4 p-4 bg-blue-50 rounded-xl hover:bg-blue-100 transition-colors group"
              >
                <div class="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center">
                  <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                  </svg>
                </div>
                <div>
                  <p class="font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">LinkedIn</p>
                  <p class="text-sm text-gray-600">专业档案</p>
                </div>
              </a>
              
              <a 
                v-if="personalInfo.github"
                :href="personalInfo.github"
                target="_blank"
                rel="noopener noreferrer"
                class="flex items-center space-x-4 p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors group"
              >
                <div class="w-12 h-12 bg-gray-900 rounded-full flex items-center justify-center">
                  <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                  </svg>
                </div>
                <div>
                  <p class="font-semibold text-gray-900 group-hover:text-gray-700 transition-colors">GitHub</p>
                  <p class="text-sm text-gray-600">代码仓库</p>
                </div>
              </a>
              
              <a 
                v-if="personalInfo.website"
                :href="personalInfo.website"
                target="_blank"
                rel="noopener noreferrer"
                class="flex items-center space-x-4 p-4 bg-green-50 rounded-xl hover:bg-green-100 transition-colors group"
              >
                <div class="w-12 h-12 bg-green-600 rounded-full flex items-center justify-center">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9m0 9c-5 0-9-4-9-9s4-9 9-9"></path>
                  </svg>
                </div>
                <div>
                  <p class="font-semibold text-gray-900 group-hover:text-green-600 transition-colors">个人网站</p>
                  <p class="text-sm text-gray-600">作品展示</p>
                </div>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { PersonalInfo } from '@/types'

// Props
interface Props {
  personalInfo: PersonalInfo
}

const props = defineProps<Props>()
</script>

<style scoped>
/* 添加一些自定义样式 */
.group:hover .group-hover\:text-blue-600 {
  color: #2563eb;
}

.group:hover .group-hover\:text-gray-700 {
  color: #374151;
}

.group:hover .group-hover\:text-green-600 {
  color: #059669;
}
</style>
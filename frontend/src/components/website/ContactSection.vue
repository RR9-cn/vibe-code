<template>
  <section id="contact" class="py-20 bg-gradient-to-br from-blue-900 via-indigo-900 to-purple-900 text-white">
    <div class="max-w-6xl mx-auto px-6">
      <!-- 标题 -->
      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-bold mb-4">
          联系我
        </h2>
        <div class="w-24 h-1 bg-gradient-to-r from-blue-400 to-indigo-400 mx-auto rounded-full"></div>
        <p class="text-xl text-blue-100 mt-6 max-w-2xl mx-auto">
          期待与您的合作交流，让我们一起创造更美好的未来
        </p>
      </div>
      
      <!-- 联系方式网格 -->
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
        <!-- 邮箱 -->
        <div v-if="personalInfo.email" class="bg-white/10 backdrop-blur-sm rounded-2xl p-8 hover:bg-white/20 transition-all duration-300 group">
          <div class="flex items-center mb-4">
            <div class="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center mr-4 group-hover:scale-110 transition-transform">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
              </svg>
            </div>
            <div>
              <h3 class="text-xl font-bold">邮箱</h3>
              <p class="text-blue-200">发送邮件</p>
            </div>
          </div>
          <a 
            :href="`mailto:${personalInfo.email}`"
            class="text-white hover:text-blue-200 transition-colors break-all"
          >
            {{ personalInfo.email }}
          </a>
        </div>
        
        <!-- 电话 -->
        <div v-if="personalInfo.phone" class="bg-white/10 backdrop-blur-sm rounded-2xl p-8 hover:bg-white/20 transition-all duration-300 group">
          <div class="flex items-center mb-4">
            <div class="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mr-4 group-hover:scale-110 transition-transform">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
              </svg>
            </div>
            <div>
              <h3 class="text-xl font-bold">电话</h3>
              <p class="text-blue-200">直接通话</p>
            </div>
          </div>
          <a 
            :href="`tel:${personalInfo.phone}`"
            class="text-white hover:text-green-200 transition-colors"
          >
            {{ personalInfo.phone }}
          </a>
        </div>
        
        <!-- 位置 -->
        <div v-if="personalInfo.location" class="bg-white/10 backdrop-blur-sm rounded-2xl p-8 hover:bg-white/20 transition-all duration-300 group">
          <div class="flex items-center mb-4">
            <div class="w-16 h-16 bg-purple-500 rounded-full flex items-center justify-center mr-4 group-hover:scale-110 transition-transform">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
            </div>
            <div>
              <h3 class="text-xl font-bold">位置</h3>
              <p class="text-blue-200">当前所在</p>
            </div>
          </div>
          <p class="text-white">{{ personalInfo.location }}</p>
        </div>
      </div>
      
      <!-- 社交媒体链接 -->
      <div class="text-center">
        <h3 class="text-2xl font-bold mb-8">关注我的社交媒体</h3>
        <div class="flex justify-center space-x-6">
          <!-- LinkedIn -->
          <a 
            v-if="personalInfo.linkedin"
            :href="personalInfo.linkedin"
            target="_blank"
            rel="noopener noreferrer"
            class="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center hover:bg-blue-700 hover:scale-110 transition-all duration-300 group"
          >
            <svg class="w-8 h-8 text-white group-hover:scale-110 transition-transform" fill="currentColor" viewBox="0 0 24 24">
              <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>
          </a>
          
          <!-- GitHub -->
          <a 
            v-if="personalInfo.github"
            :href="personalInfo.github"
            target="_blank"
            rel="noopener noreferrer"
            class="w-16 h-16 bg-gray-800 rounded-full flex items-center justify-center hover:bg-gray-700 hover:scale-110 transition-all duration-300 group"
          >
            <svg class="w-8 h-8 text-white group-hover:scale-110 transition-transform" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
          </a>
          
          <!-- 个人网站 -->
          <a 
            v-if="personalInfo.website"
            :href="personalInfo.website"
            target="_blank"
            rel="noopener noreferrer"
            class="w-16 h-16 bg-green-600 rounded-full flex items-center justify-center hover:bg-green-700 hover:scale-110 transition-all duration-300 group"
          >
            <svg class="w-8 h-8 text-white group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9m0 9c-5 0-9-4-9-9s4-9 9-9"></path>
            </svg>
          </a>
        </div>
      </div>
      
      <!-- 底部装饰 -->
      <div class="mt-16 text-center">
        <div class="inline-flex items-center space-x-2 text-blue-200">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
          </svg>
          <span>感谢您的关注</span>
        </div>
      </div>
    </div>
    
    <!-- 背景装饰 -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-blue-500/20 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl"></div>
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
/* 背景模糊效果 */
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}

/* 悬停缩放效果 */
.hover\:scale-110:hover {
  transform: scale(1.1);
}

/* 组内元素缩放 */
.group:hover .group-hover\:scale-110 {
  transform: scale(1.1);
}
</style>
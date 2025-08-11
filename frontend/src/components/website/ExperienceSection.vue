<template>
  <section id="experience" class="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
    <div class="max-w-6xl mx-auto px-6">
      <!-- 标题 -->
      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          工作经历
        </h2>
        <div class="w-24 h-1 bg-gradient-to-r from-blue-500 to-indigo-600 mx-auto rounded-full"></div>
      </div>
      
      <!-- 工作经历时间线 -->
      <div v-if="workExperience.length > 0" class="relative">
        <!-- 时间线主线 -->
        <div class="absolute left-8 md:left-1/2 transform md:-translate-x-1/2 top-0 bottom-0 w-1 bg-gradient-to-b from-blue-500 via-indigo-500 to-purple-500 rounded-full"></div>
        
        <!-- 工作经历项目 -->
        <div class="space-y-12">
          <div 
            v-for="(experience, index) in workExperience" 
            :key="index"
            class="relative flex flex-col md:flex-row items-start"
            :class="index % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse'"
          >
            <!-- 时间线节点 -->
            <div class="absolute left-8 md:left-1/2 transform -translate-x-1/2 w-6 h-6 bg-white border-4 border-blue-500 rounded-full shadow-lg z-10 flex items-center justify-center">
              <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
            </div>
            
            <!-- 工作经历卡片 -->
            <div 
              class="ml-20 md:ml-0 flex-1 max-w-lg group"
              :class="index % 2 === 0 ? 'md:mr-8' : 'md:ml-8'"
            >
              <div class="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-500 transform hover:-translate-y-2 hover:scale-105 border border-gray-100 group-hover:border-blue-200 relative overflow-hidden">
                <!-- 卡片背景动画 -->
                <div class="absolute inset-0 bg-gradient-to-br from-blue-50/0 to-indigo-50/0 group-hover:from-blue-50/50 group-hover:to-indigo-50/50 transition-all duration-500"></div>
                <div class="relative z-10">
                <!-- 公司和职位信息 -->
                <div class="flex items-start justify-between mb-6">
                  <div class="flex-1">
                    <h3 class="text-2xl font-bold text-gray-900 mb-2">
                      {{ experience.position }}
                    </h3>
                    <div class="flex items-center space-x-2 mb-3">
                      <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center">
                        <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                        </svg>
                      </div>
                      <div>
                        <p class="text-lg font-semibold text-blue-600">{{ experience.company }}</p>
                        <div class="flex items-center text-gray-500 text-sm">
                          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3a2 2 0 012-2h4a2 2 0 012 2v4m-6 0h6m-6 0l-2 13a2 2 0 002 2h6a2 2 0 002-2L16 7"></path>
                          </svg>
                          {{ formatDate(experience.startDate) }} - {{ experience.endDate ? formatDate(experience.endDate) : '至今' }}
                          <span class="ml-2 text-blue-500 font-medium">
                            ({{ calculateDuration(experience.startDate, experience.endDate) }})
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 工作年限标识 -->
                  <div class="text-center">
                    <div class="w-16 h-16 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-full flex items-center justify-center">
                      <div class="text-center">
                        <div class="text-lg font-bold text-blue-600">
                          {{ getExperienceYears(experience.startDate, experience.endDate) }}
                        </div>
                        <div class="text-xs text-gray-500">年</div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- 工作描述 -->
                <div class="mb-6">
                  <h4 class="text-lg font-semibold text-gray-900 mb-3">主要职责</h4>
                  <ul class="space-y-2">
                    <li 
                      v-for="(desc, descIndex) in experience.description" 
                      :key="descIndex"
                      class="flex items-start space-x-3"
                    >
                      <div class="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                      <p class="text-gray-700 leading-relaxed">{{ desc }}</p>
                    </li>
                  </ul>
                </div>
                
                <!-- 技术栈标签 -->
                <div v-if="experience.technologies && experience.technologies.length > 0" class="border-t border-gray-100 pt-6">
                  <h4 class="text-lg font-semibold text-gray-900 mb-3">技术栈</h4>
                  <div class="flex flex-wrap gap-2">
                    <span 
                      v-for="(tech, techIndex) in experience.technologies" 
                      :key="tech"
                      class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 hover:bg-blue-200 hover:scale-110 transition-all duration-300 cursor-default transform hover:-translate-y-1 hover:shadow-md"
                      :style="{ animationDelay: `${techIndex * 100}ms` }"
                    >
                      {{ tech }}
                    </span>
                  </div>
                </div>
                </div>
              </div>
            </div>
            
            <!-- 时间标签（移动端显示） -->
            <div class="md:hidden ml-20 mt-2 text-sm text-gray-500 font-medium">
              {{ formatDate(experience.startDate) }} - {{ experience.endDate ? formatDate(experience.endDate) : '至今' }}
            </div>
          </div>
        </div>
        
        <!-- 时间线底部装饰 -->
        <div class="absolute left-8 md:left-1/2 transform md:-translate-x-1/2 bottom-0 w-6 h-6 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full shadow-lg flex items-center justify-center">
          <svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
        </div>
      </div>
      
      <!-- 空状态 -->
      <div v-else class="text-center py-16">
        <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2V6"></path>
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-gray-600 mb-2">暂无工作经历</h3>
        <p class="text-gray-500">工作经历信息将在这里显示</p>
      </div>
      
      <!-- 统计信息 -->
      <div v-if="workExperience.length > 0" class="mt-16 bg-white rounded-2xl p-8 shadow-lg">
        <h3 class="text-2xl font-bold text-gray-900 mb-8 text-center">职业统计</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <!-- 总工作年限 -->
          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="text-2xl font-bold text-gray-900">{{ totalExperienceYears }}</div>
            <div class="text-sm text-gray-600">年工作经验</div>
          </div>
          
          <!-- 公司数量 -->
          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-600 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
            </div>
            <div class="text-2xl font-bold text-gray-900">{{ workExperience.length }}</div>
            <div class="text-sm text-gray-600">家公司</div>
          </div>
          
          <!-- 职位数量 -->
          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-600 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
            </div>
            <div class="text-2xl font-bold text-gray-900">{{ workExperience.length }}</div>
            <div class="text-sm text-gray-600">个职位</div>
          </div>
          
          <!-- 技术栈数量 -->
          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-to-r from-orange-500 to-red-600 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <div class="text-2xl font-bold text-gray-900">{{ totalTechnologies }}</div>
            <div class="text-sm text-gray-600">项技术</div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { WorkExperience } from '@/types'

// Props
interface Props {
  workExperience: WorkExperience[]
}

const props = defineProps<Props>()

// 格式化日期
const formatDate = (dateString: string): string => {
  try {
    const date = new Date(dateString)
    return `${date.getFullYear()}年${date.getMonth() + 1}月`
  } catch {
    return dateString
  }
}

// 计算工作时长
const calculateDuration = (startDate: string, endDate?: string): string => {
  try {
    const start = new Date(startDate)
    const end = endDate ? new Date(endDate) : new Date()
    
    const diffTime = Math.abs(end.getTime() - start.getTime())
    const diffMonths = Math.ceil(diffTime / (1000 * 60 * 60 * 24 * 30))
    
    const years = Math.floor(diffMonths / 12)
    const months = diffMonths % 12
    
    if (years > 0 && months > 0) {
      return `${years}年${months}个月`
    } else if (years > 0) {
      return `${years}年`
    } else {
      return `${months}个月`
    }
  } catch {
    return '1年'
  }
}

// 获取工作年限（用于显示）
const getExperienceYears = (startDate: string, endDate?: string): string => {
  try {
    const start = new Date(startDate)
    const end = endDate ? new Date(endDate) : new Date()
    
    const diffTime = Math.abs(end.getTime() - start.getTime())
    const diffYears = diffTime / (1000 * 60 * 60 * 24 * 365)
    
    return Math.max(1, Math.round(diffYears)).toString()
  } catch {
    return '1'
  }
}

// 计算总工作年限
const totalExperienceYears = computed(() => {
  if (props.workExperience.length === 0) return 0
  
  let totalMonths = 0
  
  props.workExperience.forEach(exp => {
    try {
      const start = new Date(exp.startDate)
      const end = exp.endDate ? new Date(exp.endDate) : new Date()
      
      const diffTime = Math.abs(end.getTime() - start.getTime())
      const months = Math.ceil(diffTime / (1000 * 60 * 60 * 24 * 30))
      totalMonths += months
    } catch {
      totalMonths += 12 // 默认1年
    }
  })
  
  return Math.round(totalMonths / 12)
})

// 计算总技术栈数量
const totalTechnologies = computed(() => {
  const allTechs = new Set<string>()
  
  props.workExperience.forEach(exp => {
    if (exp.technologies) {
      exp.technologies.forEach(tech => allTechs.add(tech))
    }
  })
  
  return allTechs.size
})
</script>

<style scoped>
/* 时间线动画效果 */
.hover\:shadow-xl:hover {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.hover\:-translate-y-2:hover {
  transform: translateY(-0.5rem);
}

.hover\:scale-105:hover {
  transform: scale(1.05);
}

/* 卡片悬停组合效果 */
.group:hover .hover\:-translate-y-2 {
  transform: translateY(-0.5rem) scale(1.05);
}

/* 技术标签动画 */
.hover\:-translate-y-1:hover {
  transform: translateY(-0.25rem) scale(1.1);
}

/* 时间线节点脉冲动画 */
@keyframes pulse-node {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7);
  }
  50% {
    box-shadow: 0 0 0 10px rgba(59, 130, 246, 0);
  }
}

.timeline-node {
  animation: pulse-node 2s infinite;
}

/* 卡片进入动画 */
@keyframes slideInFromLeft {
  from {
    opacity: 0;
    transform: translateX(-50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInFromRight {
  from {
    opacity: 0;
    transform: translateX(50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.slide-in-left {
  animation: slideInFromLeft 0.6s ease-out forwards;
}

.slide-in-right {
  animation: slideInFromRight 0.6s ease-out forwards;
}

/* 响应式时间线调整 */
@media (max-width: 768px) {
  .absolute.left-8 {
    left: 2rem;
  }
  
  .ml-20 {
    margin-left: 5rem;
  }
  
  .slide-in-left,
  .slide-in-right {
    animation: slideInFromLeft 0.6s ease-out forwards;
  }
}

/* 渐变时间线 */
.bg-gradient-to-b {
  background: linear-gradient(to bottom, #3b82f6, #6366f1, #8b5cf6);
}

/* 统计卡片悬停效果 */
.stats-card:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}
</style>
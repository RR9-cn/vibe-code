<template>
  <section id="education" class="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
    <div class="max-w-6xl mx-auto px-6">
      <!-- 标题 -->
      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          教育背景
        </h2>
        <div class="w-24 h-1 bg-gradient-to-r from-blue-500 to-indigo-600 mx-auto rounded-full"></div>
      </div>
      
      <!-- 教育经历列表 -->
      <div v-if="education.length > 0" class="space-y-8">
        <div 
          v-for="(edu, index) in education" 
          :key="index"
          class="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
        >
          <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between">
            <!-- 左侧：学校和专业信息 -->
            <div class="flex-1 mb-6 lg:mb-0">
              <div class="flex items-start space-x-4">
                <!-- 学校图标 -->
                <div class="w-16 h-16 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center flex-shrink-0">
                  <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"></path>
                  </svg>
                </div>
                
                <!-- 学校信息 -->
                <div class="flex-1">
                  <h3 class="text-2xl font-bold text-gray-900 mb-2">
                    {{ edu.institution }}
                  </h3>
                  <div class="space-y-1">
                    <p class="text-lg font-semibold text-blue-600">
                      {{ edu.degree }}
                      <span v-if="edu.major" class="text-gray-600">
                        · {{ edu.major }}
                      </span>
                    </p>
                    <div class="flex items-center space-x-4 text-gray-600">
                      <div class="flex items-center space-x-1">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3a2 2 0 012-2h4a2 2 0 012 2v4m-6 0h6m-6 0l-2 13a2 2 0 002 2h6a2 2 0 002-2L16 7"></path>
                        </svg>
                        <span class="text-sm">
                          {{ formatDate(edu.startDate) }} - {{ edu.endDate ? formatDate(edu.endDate) : '至今' }}
                        </span>
                      </div>
                      <div v-if="edu.gpa" class="flex items-center space-x-1">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"></path>
                        </svg>
                        <span class="text-sm">GPA: {{ edu.gpa }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 右侧：装饰性元素 -->
            <div class="lg:ml-8">
              <div class="w-24 h-24 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-full flex items-center justify-center">
                <div class="text-center">
                  <div class="text-2xl font-bold text-blue-600">
                    {{ getEducationYear(edu.startDate, edu.endDate) }}
                  </div>
                  <div class="text-xs text-gray-500">年</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 空状态 -->
      <div v-else class="text-center py-16">
        <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z"></path>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"></path>
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-gray-600 mb-2">暂无教育背景信息</h3>
        <p class="text-gray-500">教育背景信息将在这里显示</p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { Education } from '@/types'

// Props
interface Props {
  education: Education[]
}

const props = defineProps<Props>()

// 格式化日期
const formatDate = (dateString: string): string => {
  try {
    const date = new Date(dateString)
    return date.getFullYear().toString()
  } catch {
    return dateString
  }
}

// 计算教育年限
const getEducationYear = (startDate: string, endDate?: string): string => {
  try {
    const start = new Date(startDate).getFullYear()
    const end = endDate ? new Date(endDate).getFullYear() : new Date().getFullYear()
    const duration = end - start
    return duration > 0 ? duration.toString() : '1'
  } catch {
    return '4' // 默认4年
  }
}
</script>

<style scoped>
/* 添加一些自定义动画效果 */
.hover\:shadow-xl:hover {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.hover\:-translate-y-1:hover {
  transform: translateY(-0.25rem);
}
</style>
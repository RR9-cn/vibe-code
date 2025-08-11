<template>
  <section id="skills" class="py-20 bg-white">
    <div class="max-w-6xl mx-auto px-6">
      <!-- 标题 -->
      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          技能专长
        </h2>
        <div class="w-24 h-1 bg-gradient-to-r from-blue-500 to-indigo-600 mx-auto rounded-full"></div>
      </div>
      
      <!-- 技能内容 -->
      <div v-if="skills.length > 0">
        <!-- 技能分类 -->
        <div class="grid lg:grid-cols-3 gap-8 mb-12">
          <!-- 技术技能 -->
          <div v-if="technicalSkills.length > 0" class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-8 shadow-lg">
            <div class="flex items-center mb-6">
              <div class="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center mr-4">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"></path>
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-gray-900">技术技能</h3>
            </div>
            <div class="space-y-4">
              <div 
                v-for="skill in technicalSkills" 
                :key="skill.name"
                class="bg-white rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow"
              >
                <div class="flex items-center justify-between mb-2">
                  <span class="font-semibold text-gray-900">{{ skill.name }}</span>
                  <span v-if="skill.level" class="text-sm text-blue-600 font-medium">
                    {{ getLevelText(skill.level) }}
                  </span>
                </div>
                <div v-if="skill.level" class="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                  <div 
                    class="bg-gradient-to-r from-blue-500 to-indigo-600 h-2 rounded-full transition-all duration-1000 ease-out skill-progress"
                    :style="{ width: getLevelPercentage(skill.level) }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 软技能 -->
          <div v-if="softSkills.length > 0" class="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-8 shadow-lg">
            <div class="flex items-center mb-6">
              <div class="w-12 h-12 bg-green-600 rounded-full flex items-center justify-center mr-4">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-gray-900">软技能</h3>
            </div>
            <div class="space-y-4">
              <div 
                v-for="skill in softSkills" 
                :key="skill.name"
                class="bg-white rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow"
              >
                <div class="flex items-center justify-between mb-2">
                  <span class="font-semibold text-gray-900">{{ skill.name }}</span>
                  <span v-if="skill.level" class="text-sm text-green-600 font-medium">
                    {{ getLevelText(skill.level) }}
                  </span>
                </div>
                <div v-if="skill.level" class="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    class="bg-gradient-to-r from-green-500 to-emerald-600 h-2 rounded-full transition-all duration-500"
                    :style="{ width: getLevelPercentage(skill.level) }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 语言技能 -->
          <div v-if="languageSkills.length > 0" class="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-8 shadow-lg">
            <div class="flex items-center mb-6">
              <div class="w-12 h-12 bg-purple-600 rounded-full flex items-center justify-center mr-4">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"></path>
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-gray-900">语言能力</h3>
            </div>
            <div class="space-y-4">
              <div 
                v-for="skill in languageSkills" 
                :key="skill.name"
                class="bg-white rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow"
              >
                <div class="flex items-center justify-between mb-2">
                  <span class="font-semibold text-gray-900">{{ skill.name }}</span>
                  <span v-if="skill.level" class="text-sm text-purple-600 font-medium">
                    {{ getLevelText(skill.level) }}
                  </span>
                </div>
                <div v-if="skill.level" class="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    class="bg-gradient-to-r from-purple-500 to-pink-600 h-2 rounded-full transition-all duration-500"
                    :style="{ width: getLevelPercentage(skill.level) }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 技能标签云 -->
        <div class="bg-gradient-to-br from-gray-50 to-blue-50 rounded-2xl p-8 shadow-lg">
          <h3 class="text-2xl font-bold text-gray-900 mb-6 text-center">技能标签</h3>
          <div class="flex flex-wrap justify-center gap-3">
            <span 
              v-for="(skill, index) in skills" 
              :key="skill.name"
              class="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 hover:scale-110 hover:-translate-y-1 hover:shadow-lg cursor-default transform skill-tag"
              :class="getSkillTagClass(skill.category)"
              :style="{ animationDelay: `${index * 50}ms` }"
              @mouseenter="onSkillHover"
            >
              {{ skill.name }}
              <span v-if="skill.level" class="ml-2 text-xs opacity-75 transition-all duration-300 hover:opacity-100 hover:scale-125">
                {{ getLevelIcon(skill.level) }}
              </span>
            </span>
          </div>
        </div>
      </div>
      
      <!-- 空状态 -->
      <div v-else class="text-center py-16">
        <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-gray-600 mb-2">暂无技能信息</h3>
        <p class="text-gray-500">技能信息将在这里显示</p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Skill } from '@/types'

// Props
interface Props {
  skills: Skill[]
}

const props = defineProps<Props>()

// 计算属性：按类别分组技能
const technicalSkills = computed(() => 
  props.skills.filter(skill => skill.category === 'technical')
)

const softSkills = computed(() => 
  props.skills.filter(skill => skill.category === 'soft')
)

const languageSkills = computed(() => 
  props.skills.filter(skill => skill.category === 'language')
)

// 获取技能等级文本
const getLevelText = (level: string): string => {
  const levelMap: Record<string, string> = {
    'beginner': '初级',
    'intermediate': '中级',
    'advanced': '高级',
    'expert': '专家'
  }
  return levelMap[level] || level
}

// 获取技能等级百分比
const getLevelPercentage = (level: string): string => {
  const percentageMap: Record<string, string> = {
    'beginner': '25%',
    'intermediate': '50%',
    'advanced': '75%',
    'expert': '100%'
  }
  return percentageMap[level] || '50%'
}

// 获取技能等级图标
const getLevelIcon = (level: string): string => {
  const iconMap: Record<string, string> = {
    'beginner': '⭐',
    'intermediate': '⭐⭐',
    'advanced': '⭐⭐⭐',
    'expert': '⭐⭐⭐⭐'
  }
  return iconMap[level] || '⭐'
}

// 获取技能标签样式类
const getSkillTagClass = (category: string): string => {
  const classMap: Record<string, string> = {
    'technical': 'bg-blue-100 text-blue-800 hover:bg-blue-200 hover:text-blue-900',
    'soft': 'bg-green-100 text-green-800 hover:bg-green-200 hover:text-green-900',
    'language': 'bg-purple-100 text-purple-800 hover:bg-purple-200 hover:text-purple-900'
  }
  return classMap[category] || 'bg-gray-100 text-gray-800 hover:bg-gray-200'
}

// 技能标签悬停效果
const onSkillHover = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  target.style.transform = 'scale(1.1) translateY(-4px) rotate(2deg)'
  
  setTimeout(() => {
    target.style.transform = ''
  }, 200)
}
</script>

<style scoped>
/* 技能进度条动画 */
.skill-progress {
  position: relative;
  overflow: hidden;
}

.skill-progress::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

/* 技能标签动画 */
.skill-tag {
  opacity: 0;
  animation: fadeInUp 0.6s ease-out forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 悬停效果增强 */
.hover\:scale-110:hover {
  transform: scale(1.1) translateY(-4px);
}

.hover\:-translate-y-1:hover {
  transform: translateY(-4px);
}

/* 技能卡片悬停效果 */
.hover\:shadow-md:hover {
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

/* 进度条容器悬停效果 */
.bg-white:hover .skill-progress {
  animation-duration: 1s;
}

/* 技能分类卡片动画 */
.bg-gradient-to-br {
  position: relative;
  overflow: hidden;
}

.bg-gradient-to-br::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s ease;
}

.bg-gradient-to-br:hover::before {
  left: 100%;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .skill-tag {
    font-size: 0.875rem;
    padding: 0.5rem 0.75rem;
  }
}
</style>
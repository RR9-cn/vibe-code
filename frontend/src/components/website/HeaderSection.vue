<template>
  <header class="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-200/50 transition-all duration-300">
    <div class="max-w-6xl mx-auto px-6 py-4">
      <div class="flex items-center justify-between">
        <!-- Logo/Name -->
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center">
            <span class="text-white font-bold text-lg">
              {{ getInitials(personalInfo.name) }}
            </span>
          </div>
          <h1 class="text-xl font-bold text-gray-900">
            {{ personalInfo.name }}
          </h1>
        </div>
        
        <!-- Navigation Menu -->
        <nav class="hidden md:flex items-center space-x-8">
          <a 
            v-for="item in navigationItems" 
            :key="item.id"
            @click="$emit('scroll-to', item.id)"
            class="text-gray-600 hover:text-blue-600 font-medium cursor-pointer transition-colors duration-200"
          >
            {{ item.label }}
          </a>
        </nav>
        
        <!-- Mobile Menu Button -->
        <button 
          @click="toggleMobileMenu"
          class="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
          </svg>
        </button>
      </div>
      
      <!-- Mobile Menu -->
      <Transition name="mobile-menu">
        <div v-if="showMobileMenu" class="md:hidden mt-4 py-4 border-t border-gray-200">
          <nav class="flex flex-col space-y-3">
            <a 
              v-for="item in navigationItems" 
              :key="item.id"
              @click="handleMobileNavClick(item.id)"
              class="text-gray-600 hover:text-blue-600 font-medium cursor-pointer transition-colors duration-200 py-2"
            >
              {{ item.label }}
            </a>
          </nav>
        </div>
      </Transition>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { PersonalInfo } from '@/types'

// Props
interface Props {
  personalInfo: PersonalInfo
}

const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  'scroll-to': [sectionId: string]
}>()

// 响应式数据
const showMobileMenu = ref(false)

// 导航菜单项
const navigationItems = [
  { id: 'about', label: '关于我' },
  { id: 'experience', label: '工作经历' },
  { id: 'education', label: '教育背景' },
  { id: 'skills', label: '技能' },
  { id: 'contact', label: '联系方式' }
]

// 计算属性
const getInitials = (name: string): string => {
  return name
    .split(' ')
    .map(word => word.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

// 方法
const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const handleMobileNavClick = (sectionId: string) => {
  emit('scroll-to', sectionId)
  showMobileMenu.value = false
}
</script>

<style scoped>
/* Mobile menu transition */
.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: all 0.3s ease;
}

.mobile-menu-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
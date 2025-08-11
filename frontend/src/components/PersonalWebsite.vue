<template>
  <div class="personal-website min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
    <!-- 主要内容区域 -->
    <div class="relative">
      <!-- Header Section -->
      <Transition name="slide-down" appear>
        <HeaderSection 
          :personal-info="resumeData.personalInfo"
          @scroll-to="scrollToSection"
        />
      </Transition>
      
      <!-- Hero Section -->
      <Transition name="fade-up" appear>
        <HeroSection 
          :personal-info="resumeData.personalInfo"
        />
      </Transition>
      
      <!-- About Section -->
      <Transition name="fade-in" appear :delay="200">
        <AboutSection 
          :personal-info="resumeData.personalInfo"
          v-intersection="{ callback: onIntersection, options: { threshold: 0.3 } }"
        />
      </Transition>
      
      <!-- Experience Section -->
      <Transition name="slide-left" appear :delay="400">
        <ExperienceSection 
          :work-experience="resumeData.workExperience"
          v-intersection="{ callback: onIntersection, options: { threshold: 0.2 } }"
        />
      </Transition>
      
      <!-- Education Section -->
      <Transition name="slide-right" appear :delay="600">
        <EducationSection 
          :education="resumeData.education"
          v-intersection="{ callback: onIntersection, options: { threshold: 0.3 } }"
        />
      </Transition>
      
      <!-- Skills Section -->
      <Transition name="fade-up" appear :delay="800">
        <SkillsSection 
          :skills="resumeData.skills"
          v-intersection="{ callback: onIntersection, options: { threshold: 0.3 } }"
        />
      </Transition>
      
      <!-- Contact Section -->
      <Transition name="fade-in" appear :delay="1000">
        <ContactSection 
          :personal-info="resumeData.personalInfo"
          v-intersection="{ callback: onIntersection, options: { threshold: 0.3 } }"
        />
      </Transition>
    </div>
    
    <!-- 回到顶部按钮 -->
    <Transition name="scale">
      <button
        v-if="showBackToTop"
        @click="scrollToTop"
        class="fixed bottom-8 right-8 w-12 h-12 bg-blue-600 text-white rounded-full shadow-lg hover:bg-blue-700 hover:scale-110 transition-all duration-300 z-50 flex items-center justify-center"
        aria-label="回到顶部"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"></path>
        </svg>
      </button>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import type { ResumeData } from '@/types'
import HeaderSection from './website/HeaderSection.vue'
import HeroSection from './website/HeroSection.vue'
import AboutSection from './website/AboutSection.vue'
import ExperienceSection from './website/ExperienceSection.vue'
import EducationSection from './website/EducationSection.vue'
import SkillsSection from './website/SkillsSection.vue'
import ContactSection from './website/ContactSection.vue'

// Props
interface Props {
  resumeData: ResumeData
}

const props = defineProps<Props>()

// 响应式数据
const showBackToTop = ref(false)
const visibleSections = ref(new Set<string>())

// 滚动到指定区域的方法
const scrollToSection = (sectionId: string) => {
  const element = document.getElementById(sectionId)
  if (element) {
    element.scrollIntoView({ 
      behavior: 'smooth',
      block: 'start'
    })
  }
}

// 回到顶部
const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

// 处理滚动事件
const handleScroll = () => {
  showBackToTop.value = window.scrollY > 300
}

// 交叉观察器回调
const onIntersection = (entries: IntersectionObserverEntry[]) => {
  entries.forEach(entry => {
    const sectionId = entry.target.id
    if (entry.isIntersecting) {
      visibleSections.value.add(sectionId)
      // 添加动画类
      entry.target.classList.add('animate-in')
    } else {
      visibleSections.value.delete(sectionId)
    }
  })
}

// 自定义指令：交叉观察器
const vIntersection = {
  mounted(el: HTMLElement, binding: any) {
    const options = binding.value?.options || { threshold: 0.1 }
    const callback = binding.value?.callback || onIntersection
    
    const observer = new IntersectionObserver(callback, options)
    observer.observe(el)
    
    // 存储observer以便清理
    el._observer = observer
  },
  unmounted(el: HTMLElement) {
    if (el._observer) {
      el._observer.disconnect()
      delete el._observer
    }
  }
}

// 组件挂载时的初始化
onMounted(() => {
  // 添加平滑滚动样式
  document.documentElement.style.scrollBehavior = 'smooth'
  
  // 监听滚动事件
  window.addEventListener('scroll', handleScroll)
  
  // 初始检查滚动位置
  handleScroll()
})

// 组件卸载时清理
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.personal-website {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Vue Transition 动画 */
/* 滑动下降动画 */
.slide-down-enter-active {
  transition: all 0.6s ease-out;
}

.slide-down-enter-from {
  opacity: 0;
  transform: translateY(-50px);
}

/* 淡入上升动画 */
.fade-up-enter-active {
  transition: all 0.8s ease-out;
}

.fade-up-enter-from {
  opacity: 0;
  transform: translateY(50px);
}

/* 淡入动画 */
.fade-in-enter-active {
  transition: all 0.6s ease-out;
}

.fade-in-enter-from {
  opacity: 0;
}

/* 左滑动画 */
.slide-left-enter-active {
  transition: all 0.7s ease-out;
}

.slide-left-enter-from {
  opacity: 0;
  transform: translateX(-100px);
}

/* 右滑动画 */
.slide-right-enter-active {
  transition: all 0.7s ease-out;
}

.slide-right-enter-from {
  opacity: 0;
  transform: translateX(100px);
}

/* 缩放动画 */
.scale-enter-active,
.scale-leave-active {
  transition: all 0.3s ease;
}

.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

/* 滚动触发动画 */
.animate-in {
  animation: slideInUp 0.6s ease-out forwards;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 悬停效果增强 */
.hover\:scale-110:hover {
  transform: scale(1.1);
}

/* 自定义滚动条样式 */
:deep(*::-webkit-scrollbar) {
  width: 8px;
}

:deep(*::-webkit-scrollbar-track) {
  background: #f1f5f9;
}

:deep(*::-webkit-scrollbar-thumb) {
  background: #cbd5e1;
  border-radius: 4px;
}

:deep(*::-webkit-scrollbar-thumb:hover) {
  background: #94a3b8;
}

/* 响应式动画调整 */
@media (max-width: 768px) {
  .slide-left-enter-from,
  .slide-right-enter-from {
    transform: translateY(30px);
  }
}

/* 性能优化：减少重绘 */
* {
  will-change: auto;
}

.transition-all {
  will-change: transform, opacity;
}
</style>
<template>
  <div class="progress-container">
    <!-- 进度条标签 -->
    <div v-if="showLabel" class="flex justify-between items-center mb-2">
      <span class="text-sm font-medium text-gray-700">{{ label }}</span>
      <span class="text-sm text-gray-500">{{ progress }}%</span>
    </div>
    
    <!-- 进度条 -->
    <div class="progress-bar-bg" :class="sizeClass">
      <div 
        class="progress-bar-fill transition-all duration-300 ease-out"
        :class="[colorClass, sizeClass]"
        :style="{ width: `${progress}%` }"
      >
        <!-- 进度条动画效果 -->
        <div v-if="animated" class="progress-bar-animation"></div>
      </div>
    </div>
    
    <!-- 状态文本 -->
    <div v-if="statusText" class="mt-2">
      <p class="text-sm text-gray-600">{{ statusText }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  progress: number
  label?: string
  statusText?: string
  size?: 'sm' | 'md' | 'lg'
  color?: 'primary' | 'success' | 'warning' | 'error'
  animated?: boolean
  showLabel?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  progress: 0,
  size: 'md',
  color: 'primary',
  animated: false,
  showLabel: true
})

// 尺寸样式类
const sizeClass = computed(() => {
  const sizes = {
    sm: 'h-1',
    md: 'h-2',
    lg: 'h-3'
  }
  return sizes[props.size]
})

// 颜色样式类
const colorClass = computed(() => {
  const colors = {
    primary: 'bg-primary-600',
    success: 'bg-green-600',
    warning: 'bg-yellow-600',
    error: 'bg-red-600'
  }
  return colors[props.color]
})
</script>

<style scoped>
.progress-container {
  @apply w-full;
}

.progress-bar-bg {
  @apply w-full bg-gray-200 rounded-full overflow-hidden;
}

.progress-bar-fill {
  @apply rounded-full relative;
}

.progress-bar-animation {
  @apply absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-30;
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}
</style>
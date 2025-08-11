<template>
  <div class="loading-spinner" :class="sizeClass">
    <div class="spinner" :class="colorClass"></div>
    <span v-if="text" class="loading-text" :class="textSizeClass">{{ text }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  size?: 'sm' | 'md' | 'lg'
  color?: 'primary' | 'white' | 'gray'
  text?: string
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  color: 'primary'
})

// 尺寸样式类
const sizeClass = computed(() => {
  const sizes = {
    sm: 'gap-2',
    md: 'gap-3',
    lg: 'gap-4'
  }
  return sizes[props.size]
})

// 颜色样式类
const colorClass = computed(() => {
  const colors = {
    primary: 'border-primary-600 border-t-transparent',
    white: 'border-white border-t-transparent',
    gray: 'border-gray-600 border-t-transparent'
  }
  return colors[props.color]
})

// 文字尺寸样式类
const textSizeClass = computed(() => {
  const sizes = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg'
  }
  return sizes[props.size]
})
</script>

<style scoped>
.loading-spinner {
  @apply flex flex-col items-center justify-center;
}

.spinner {
  @apply border-4 border-solid rounded-full animate-spin;
}

.loading-spinner.gap-2 .spinner {
  @apply w-4 h-4;
}

.loading-spinner.gap-3 .spinner {
  @apply w-6 h-6;
}

.loading-spinner.gap-4 .spinner {
  @apply w-8 h-8;
}

.loading-text {
  @apply text-gray-600 font-medium;
}
</style>
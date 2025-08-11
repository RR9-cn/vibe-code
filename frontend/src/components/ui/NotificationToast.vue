<template>
  <Teleport to="body">
    <div class="toast-container">
      <Transition
        v-for="notification in notifications"
        :key="notification.id"
        name="toast"
        appear
      >
        <div
          class="toast"
          :class="getToastClass(notification.type)"
        >
          <!-- 图标 -->
          <div class="toast-icon">
            <component :is="getIcon(notification.type)" class="w-5 h-5" />
          </div>
          
          <!-- 内容 -->
          <div class="toast-content">
            <h4 v-if="notification.title" class="toast-title">
              {{ notification.title }}
            </h4>
            <p class="toast-message">{{ notification.message }}</p>
          </div>
          
          <!-- 关闭按钮 -->
          <button
            @click="removeNotification(notification.id)"
            class="toast-close"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </Transition>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 通知类型
export type NotificationType = 'success' | 'error' | 'warning' | 'info'

// 通知接口
export interface Notification {
  id: string
  type: NotificationType
  title?: string
  message: string
  duration?: number
}

// 通知列表
const notifications = ref<Notification[]>([])

// 添加通知
const addNotification = (notification: Omit<Notification, 'id'>) => {
  const id = Math.random().toString(36).substr(2, 9)
  const newNotification: Notification = {
    id,
    duration: 5000,
    ...notification
  }
  
  notifications.value.push(newNotification)
  
  // 自动移除通知
  if (newNotification.duration && newNotification.duration > 0) {
    setTimeout(() => {
      removeNotification(id)
    }, newNotification.duration)
  }
}

// 移除通知
const removeNotification = (id: string) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index > -1) {
    notifications.value.splice(index, 1)
  }
}

// 获取图标组件
const getIcon = (type: NotificationType) => {
  const icons = {
    success: 'CheckCircleIcon',
    error: 'XCircleIcon',
    warning: 'ExclamationTriangleIcon',
    info: 'InformationCircleIcon'
  }
  return icons[type]
}

// 获取Toast样式类
const getToastClass = (type: NotificationType) => {
  const classes = {
    success: 'toast-success',
    error: 'toast-error',
    warning: 'toast-warning',
    info: 'toast-info'
  }
  return classes[type]
}

// 图标组件
const CheckCircleIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
    </svg>
  `
}

const XCircleIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/>
    </svg>
  `
}

const ExclamationTriangleIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"/>
    </svg>
  `
}

const InformationCircleIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
    </svg>
  `
}

// 暴露方法供外部使用
defineExpose({
  addNotification,
  removeNotification
})
</script>

<style scoped>
.toast-container {
  @apply fixed top-4 right-4 z-50 space-y-2;
}

.toast {
  @apply flex items-start p-4 rounded-lg shadow-lg border max-w-sm bg-white;
}

.toast-icon {
  @apply flex-shrink-0 mr-3;
}

.toast-content {
  @apply flex-1 min-w-0;
}

.toast-title {
  @apply text-sm font-medium mb-1;
}

.toast-message {
  @apply text-sm;
}

.toast-close {
  @apply flex-shrink-0 ml-3 p-1 rounded-md hover:bg-gray-100 transition-colors;
}

.toast-success {
  @apply border-green-200 bg-green-50;
}

.toast-success .toast-icon {
  @apply text-green-600;
}

.toast-success .toast-title {
  @apply text-green-800;
}

.toast-success .toast-message {
  @apply text-green-700;
}

.toast-error {
  @apply border-red-200 bg-red-50;
}

.toast-error .toast-icon {
  @apply text-red-600;
}

.toast-error .toast-title {
  @apply text-red-800;
}

.toast-error .toast-message {
  @apply text-red-700;
}

.toast-warning {
  @apply border-yellow-200 bg-yellow-50;
}

.toast-warning .toast-icon {
  @apply text-yellow-600;
}

.toast-warning .toast-title {
  @apply text-yellow-800;
}

.toast-warning .toast-message {
  @apply text-yellow-700;
}

.toast-info {
  @apply border-blue-200 bg-blue-50;
}

.toast-info .toast-icon {
  @apply text-blue-600;
}

.toast-info .toast-title {
  @apply text-blue-800;
}

.toast-info .toast-message {
  @apply text-blue-700;
}

/* 过渡动画 */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>
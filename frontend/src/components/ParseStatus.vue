<template>
  <div class="parse-status-container">
    <!-- 状态卡片 -->
    <div class="status-card" :class="statusCardClass">
      <!-- 状态图标和标题 -->
      <div class="status-header">
        <div class="status-icon">
          <LoadingSpinner 
            v-if="parseStatus.status === 'parsing'" 
            size="md" 
            color="primary" 
          />
          <svg 
            v-else-if="parseStatus.status === 'success'" 
            class="w-8 h-8 text-green-600" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <svg 
            v-else-if="parseStatus.status === 'error'" 
            class="w-8 h-8 text-red-600" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <svg 
            v-else 
            class="w-8 h-8 text-gray-400" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
        </div>
        
        <div class="status-text">
          <h3 class="status-title">{{ statusTitle }}</h3>
          <p class="status-message">{{ parseStatus.message || defaultMessage }}</p>
        </div>
      </div>

      <!-- 进度条 -->
      <div v-if="showProgress" class="mt-4">
        <ProgressBar
          :progress="parseStatus.progress"
          :label="progressLabel"
          :animated="parseStatus.status === 'parsing'"
          :color="progressColor"
          size="md"
        />
      </div>

      <!-- 解析结果预览 -->
      <div v-if="parseStatus.status === 'success' && parseStatus.data" class="mt-6">
        <div class="result-preview">
          <h4 class="text-sm font-medium text-gray-700 mb-3">解析结果预览：</h4>
          <div class="preview-grid">
            <div class="preview-item">
              <span class="preview-label">姓名：</span>
              <span class="preview-value">{{ parseStatus.data.personalInfo.name || '未识别' }}</span>
            </div>
            <div class="preview-item">
              <span class="preview-label">邮箱：</span>
              <span class="preview-value">{{ parseStatus.data.personalInfo.email || '未识别' }}</span>
            </div>
            <div class="preview-item">
              <span class="preview-label">工作经历：</span>
              <span class="preview-value">{{ parseStatus.data.workExperience.length }} 项</span>
            </div>
            <div class="preview-item">
              <span class="preview-label">教育背景：</span>
              <span class="preview-value">{{ parseStatus.data.education.length }} 项</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="mt-6 flex flex-wrap gap-3">
        <!-- 重试按钮 -->
        <button
          v-if="parseStatus.status === 'error'"
          @click="handleRetry"
          :disabled="isRetrying"
          class="btn-primary"
        >
          <LoadingSpinner v-if="isRetrying" size="sm" color="white" />
          <span v-else>重试解析</span>
        </button>

        <!-- 生成网站按钮 -->
        <button
          v-if="parseStatus.status === 'success' && parseStatus.data"
          @click="handleGenerateWebsite"
          :disabled="isGenerating"
          class="btn-primary"
        >
          <LoadingSpinner v-if="isGenerating" size="sm" color="white" />
          <span v-else>生成个人网站</span>
        </button>

        <!-- 编辑数据按钮 -->
        <button
          v-if="parseStatus.status === 'success' && parseStatus.data"
          @click="handleEditData"
          class="btn-secondary"
        >
          编辑简历数据
        </button>

        <!-- 重新上传按钮 -->
        <button
          v-if="parseStatus.status === 'error'"
          @click="handleReupload"
          class="btn-secondary"
        >
          重新上传文件
        </button>
      </div>
    </div>

    <!-- 实时状态更新提示 -->
    <div v-if="isPolling" class="mt-4 text-center">
      <p class="text-sm text-gray-500">
        <LoadingSpinner size="sm" color="gray" />
        正在实时更新状态...
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useUploadStore } from '@/stores/upload'
import { useResumeStore } from '@/stores/resume'
import { useWebsiteStore } from '@/stores/website'
import { ApiService } from '@/services/api'
import { notify } from '@/services/notification'
import { handleError } from '@/utils'
import type { ParseStatus as ParseStatusType } from '@/types'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import ProgressBar from '@/components/ui/ProgressBar.vue'

interface Props {
  uploadId?: string
  autoRefresh?: boolean
  refreshInterval?: number
}

const props = withDefaults(defineProps<Props>(), {
  autoRefresh: true,
  refreshInterval: 2000
})

// 事件定义
const emit = defineEmits<{
  retry: []
  generateWebsite: []
  editData: []
  reupload: []
}>()

// 状态管理
const uploadStore = useUploadStore()
const resumeStore = useResumeStore()
const websiteStore = useWebsiteStore()

// 响应式状态
const isRetrying = ref(false)
const isGenerating = ref(false)
const isPolling = ref(false)
const pollTimer = ref<NodeJS.Timeout | null>(null)

// 计算属性
const parseStatus = computed(() => uploadStore.parseStatus)

const statusTitle = computed(() => {
  const titles = {
    idle: '等待解析',
    parsing: '正在解析',
    success: '解析完成',
    error: '解析失败'
  }
  return titles[parseStatus.value.status]
})

const defaultMessage = computed(() => {
  const messages = {
    idle: '准备开始解析简历内容',
    parsing: '正在使用AI技术解析您的简历...',
    success: '简历解析成功，可以生成个人网站了',
    error: '解析过程中出现错误，请重试'
  }
  return messages[parseStatus.value.status]
})

const statusCardClass = computed(() => {
  const classes = {
    idle: 'status-card-idle',
    parsing: 'status-card-parsing',
    success: 'status-card-success',
    error: 'status-card-error'
  }
  return classes[parseStatus.value.status]
})

const showProgress = computed(() => {
  return parseStatus.value.status === 'parsing' || parseStatus.value.progress > 0
})

const progressLabel = computed(() => {
  if (parseStatus.value.status === 'parsing') {
    return `解析进度: ${parseStatus.value.progress}%`
  }
  return ''
})

const progressColor = computed(() => {
  const colors = {
    idle: 'primary',
    parsing: 'primary',
    success: 'success',
    error: 'error'
  }
  return colors[parseStatus.value.status] as 'primary' | 'success' | 'error'
})

// 开始轮询状态
const startPolling = () => {
  if (!props.autoRefresh || !props.uploadId) return
  
  isPolling.value = true
  pollTimer.value = setInterval(async () => {
    try {
      const status = await ApiService.getParseStatus(props.uploadId!)
      uploadStore.setParseStatus(status)
      
      // 如果解析完成或失败，停止轮询
      if (status.status === 'success' || status.status === 'error') {
        stopPolling()
        
        // 如果解析成功，保存简历数据
        if (status.status === 'success' && status.data) {
          resumeStore.setCurrentResume(status.data)
        }
      }
    } catch (error) {
      console.error('获取解析状态失败:', error)
      // 继续轮询，不中断
    }
  }, props.refreshInterval)
}

// 停止轮询
const stopPolling = () => {
  if (pollTimer.value) {
    clearInterval(pollTimer.value)
    pollTimer.value = null
  }
  isPolling.value = false
}

// 处理重试
const handleRetry = async () => {
  if (!props.uploadId) return
  
  try {
    isRetrying.value = true
    
    // 重置状态
    uploadStore.setParseStatus({
      status: 'parsing',
      progress: 0,
      message: '正在重新解析...'
    })
    
    // 调用解析API
    await ApiService.parseResume(props.uploadId)
    
    // 重新开始轮询
    startPolling()
    
    notify.info('已重新开始解析，请稍候...')
    emit('retry')
    
  } catch (error) {
    const errorMessage = handleError(error)
    uploadStore.setParseStatus({
      status: 'error',
      progress: 0,
      message: errorMessage
    })
    notify.error(errorMessage, '重试失败')
  } finally {
    isRetrying.value = false
  }
}

// 处理生成网站
const handleGenerateWebsite = async () => {
  if (!parseStatus.value.data) return
  
  try {
    isGenerating.value = true
    websiteStore.setGenerating(true)
    
    const website = await ApiService.generateWebsite(parseStatus.value.data)
    websiteStore.setCurrentWebsite(website)
    websiteStore.setPreviewUrl(website.url)
    
    notify.success('个人网站生成成功！')
    emit('generateWebsite')
    
  } catch (error) {
    const errorMessage = handleError(error)
    websiteStore.setError(errorMessage)
    notify.error(errorMessage, '网站生成失败')
  } finally {
    isGenerating.value = false
    websiteStore.setGenerating(false)
  }
}

// 处理编辑数据
const handleEditData = () => {
  emit('editData')
}

// 处理重新上传
const handleReupload = () => {
  uploadStore.resetUpload()
  resumeStore.clearResume()
  emit('reupload')
}

// 监听uploadId变化
watch(() => props.uploadId, (newUploadId) => {
  if (newUploadId) {
    startPolling()
  } else {
    stopPolling()
  }
}, { immediate: true })

// 监听解析状态变化
watch(() => parseStatus.value.status, (newStatus) => {
  if (newStatus === 'success' || newStatus === 'error') {
    stopPolling()
  }
})

// 生命周期钩子
onMounted(() => {
  if (props.uploadId && parseStatus.value.status === 'parsing') {
    startPolling()
  }
})

onUnmounted(() => {
  stopPolling()
})
</script>

<style scoped>
.parse-status-container {
  @apply w-full;
}

.status-card {
  @apply bg-white rounded-lg border p-6 transition-all duration-200;
}

.status-card-idle {
  @apply border-gray-200;
}

.status-card-parsing {
  @apply border-blue-200 bg-blue-50;
}

.status-card-success {
  @apply border-green-200 bg-green-50;
}

.status-card-error {
  @apply border-red-200 bg-red-50;
}

.status-header {
  @apply flex items-start space-x-4;
}

.status-icon {
  @apply flex-shrink-0;
}

.status-text {
  @apply flex-1 min-w-0;
}

.status-title {
  @apply text-lg font-semibold text-gray-900 mb-1;
}

.status-message {
  @apply text-gray-600;
}

.result-preview {
  @apply bg-gray-50 rounded-lg p-4;
}

.preview-grid {
  @apply grid grid-cols-1 sm:grid-cols-2 gap-3;
}

.preview-item {
  @apply flex items-center space-x-2;
}

.preview-label {
  @apply text-sm font-medium text-gray-500 min-w-0 flex-shrink-0;
}

.preview-value {
  @apply text-sm text-gray-900 truncate;
}
</style>
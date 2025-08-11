<template>
  <div class="file-upload-container">
    <!-- 上传区域 -->
    <div
      ref="dropZone"
      class="upload-zone"
      :class="{
        'upload-zone-dragover': isDragOver,
        'upload-zone-disabled': isUploading
      }"
      @click="triggerFileInput"
      @drop="handleDrop"
      @dragover="handleDragOver"
      @dragenter="handleDragEnter"
      @dragleave="handleDragLeave"
    >
      <!-- 上传图标和文本 -->
      <div class="upload-content">
        <div class="upload-icon">
          <svg 
            v-if="!isUploading" 
            class="w-12 h-12 text-gray-400" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              stroke-linecap="round" 
              stroke-linejoin="round" 
              stroke-width="2" 
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" 
            />
          </svg>
          <LoadingSpinner v-else size="lg" color="primary" />
        </div>
        
        <div class="upload-text">
          <p class="upload-title">
            {{ isUploading ? '正在上传...' : '点击上传或拖拽文件到此处' }}
          </p>
          <p class="upload-subtitle">
            支持PDF格式，最大{{ maxSizeMB }}MB
          </p>
        </div>
      </div>
    </div>

    <!-- 隐藏的文件输入 -->
    <input
      ref="fileInput"
      type="file"
      accept=".pdf,application/pdf"
      class="hidden"
      @change="handleFileSelect"
      :disabled="isUploading"
    />

    <!-- 上传进度条 -->
    <div v-if="isUploading || uploadProgress > 0" class="mt-4">
      <ProgressBar
        :progress="uploadProgress"
        :label="uploadProgressLabel"
        :status-text="uploadStatusText"
        :animated="isUploading"
        color="primary"
      />
    </div>

    <!-- 错误信息 -->
    <div v-if="uploadError" class="mt-4">
      <div class="error-message">
        <div class="flex items-center">
          <svg class="w-5 h-5 text-red-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <span class="text-red-700 font-medium">上传失败</span>
        </div>
        <p class="text-red-600 text-sm mt-1">{{ uploadError }}</p>
        <button
          @click="retryUpload"
          class="btn-secondary mt-2 text-sm"
        >
          重试上传
        </button>
      </div>
    </div>

    <!-- 上传成功信息 -->
    <div v-if="uploadSuccess && !isUploading" class="mt-4">
      <div class="success-message">
        <div class="flex items-center">
          <svg class="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <span class="text-green-700 font-medium">上传成功</span>
        </div>
        <p class="text-green-600 text-sm mt-1">
          文件已成功上传，正在解析简历内容...
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useUploadStore } from '@/stores/upload'
import { ApiService } from '@/services/api'
import { notify } from '@/services/notification'
import { validateFileType, validateFileSize, formatFileSize, handleError } from '@/utils'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import ProgressBar from '@/components/ui/ProgressBar.vue'

interface Props {
  maxSizeMB?: number
  allowedTypes?: string[]
}

const props = withDefaults(defineProps<Props>(), {
  maxSizeMB: 10,
  allowedTypes: () => ['application/pdf']
})

// 事件定义
const emit = defineEmits<{
  uploadSuccess: [uploadId: string]
  uploadError: [error: string]
}>()

// 状态管理
const uploadStore = useUploadStore()

// 响应式引用
const dropZone = ref<HTMLElement>()
const fileInput = ref<HTMLInputElement>()
const isDragOver = ref(false)
const dragCounter = ref(0)
const selectedFile = ref<File | null>(null)

// 计算属性
const isUploading = computed(() => uploadStore.isUploading)
const uploadProgress = computed(() => uploadStore.uploadProgress)
const uploadError = computed(() => uploadStore.uploadError)
const uploadSuccess = computed(() => !!uploadStore.uploadId && !uploadStore.uploadError)

const uploadProgressLabel = computed(() => {
  if (uploadProgress.value === 100) {
    return '上传完成'
  }
  return `上传进度: ${uploadProgress.value}%`
})

const uploadStatusText = computed(() => {
  if (selectedFile.value) {
    return `正在上传: ${selectedFile.value.name} (${formatFileSize(selectedFile.value.size)})`
  }
  return ''
})

// 触发文件选择
const triggerFileInput = () => {
  if (!isUploading.value && fileInput.value) {
    fileInput.value.click()
  }
}

// 处理文件选择
const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  const files = target.files
  if (files && files.length > 0) {
    handleFile(files[0])
  }
}

// 处理拖拽相关事件
const handleDragOver = (event: DragEvent) => {
  event.preventDefault()
  event.stopPropagation()
}

const handleDragEnter = (event: DragEvent) => {
  event.preventDefault()
  event.stopPropagation()
  dragCounter.value++
  isDragOver.value = true
}

const handleDragLeave = (event: DragEvent) => {
  event.preventDefault()
  event.stopPropagation()
  dragCounter.value--
  if (dragCounter.value === 0) {
    isDragOver.value = false
  }
}

const handleDrop = (event: DragEvent) => {
  event.preventDefault()
  event.stopPropagation()
  
  isDragOver.value = false
  dragCounter.value = 0
  
  const files = event.dataTransfer?.files
  if (files && files.length > 0) {
    handleFile(files[0])
  }
}

// 处理文件
const handleFile = async (file: File) => {
  // 重置状态
  uploadStore.resetUpload()
  selectedFile.value = file

  // 验证文件类型
  if (!validateFileType(file, props.allowedTypes)) {
    const error = '不支持的文件格式，请选择PDF文件'
    uploadStore.setUploadError(error)
    notify.error(error)
    emit('uploadError', error)
    return
  }

  // 验证文件大小
  if (!validateFileSize(file, props.maxSizeMB)) {
    const error = `文件大小超过限制，最大支持${props.maxSizeMB}MB`
    uploadStore.setUploadError(error)
    notify.error(error)
    emit('uploadError', error)
    return
  }

  // 开始上传
  await uploadFile(file)
}

// 上传文件
const uploadFile = async (file: File) => {
  try {
    uploadStore.setUploading(true)
    uploadStore.setUploadProgress(0)

    const response = await ApiService.uploadFile(file, (progress) => {
      uploadStore.setUploadProgress(progress)
    })

    uploadStore.setUploadId(response.uploadId)
    notify.success('文件上传成功，开始解析简历内容')
    emit('uploadSuccess', response.uploadId)

  } catch (error) {
    const errorMessage = handleError(error)
    uploadStore.setUploadError(errorMessage)
    notify.error(errorMessage, '上传失败')
    emit('uploadError', errorMessage)
  } finally {
    uploadStore.setUploading(false)
  }
}

// 重试上传
const retryUpload = () => {
  if (selectedFile.value) {
    handleFile(selectedFile.value)
  }
}

// 防止页面默认拖拽行为
const preventDefaults = (event: DragEvent) => {
  event.preventDefault()
  event.stopPropagation()
}

// 生命周期钩子
onMounted(() => {
  // 防止整个页面的拖拽行为
  document.addEventListener('dragenter', preventDefaults)
  document.addEventListener('dragover', preventDefaults)
  document.addEventListener('dragleave', preventDefaults)
  document.addEventListener('drop', preventDefaults)
})

onUnmounted(() => {
  document.removeEventListener('dragenter', preventDefaults)
  document.removeEventListener('dragover', preventDefaults)
  document.removeEventListener('dragleave', preventDefaults)
  document.removeEventListener('drop', preventDefaults)
})
</script>

<style scoped>
.file-upload-container {
  @apply w-full;
}

.upload-zone {
  @apply border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer transition-all duration-200 hover:border-primary-400 hover:bg-primary-50;
}

.upload-zone-dragover {
  @apply border-primary-500 bg-primary-100;
}

.upload-zone-disabled {
  @apply cursor-not-allowed opacity-75 hover:border-gray-300 hover:bg-transparent;
}

.upload-content {
  @apply flex flex-col items-center space-y-4;
}

.upload-icon {
  @apply flex items-center justify-center;
}

.upload-text {
  @apply space-y-2;
}

.upload-title {
  @apply text-lg font-medium text-gray-700;
}

.upload-subtitle {
  @apply text-sm text-gray-500;
}

.error-message {
  @apply bg-red-50 border border-red-200 rounded-lg p-4;
}

.success-message {
  @apply bg-green-50 border border-green-200 rounded-lg p-4;
}
</style>
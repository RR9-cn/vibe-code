import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { UploadResponse, ParseStatus } from '@/types'

// 文件上传状态管理
export const useUploadStore = defineStore('upload', () => {
  // 状态
  const uploadId = ref<string>('')
  const uploadProgress = ref<number>(0)
  const isUploading = ref<boolean>(false)
  const uploadError = ref<string>('')
  
  const parseStatus = ref<ParseStatus>({
    status: 'idle',
    progress: 0,
    message: ''
  })

  // 动作
  const setUploadId = (id: string) => {
    uploadId.value = id
  }

  const setUploadProgress = (progress: number) => {
    uploadProgress.value = progress
  }

  const setUploading = (status: boolean) => {
    isUploading.value = status
  }

  const setUploadError = (error: string) => {
    uploadError.value = error
  }

  const setParseStatus = (status: ParseStatus) => {
    parseStatus.value = status
  }

  const resetUpload = () => {
    uploadId.value = ''
    uploadProgress.value = 0
    isUploading.value = false
    uploadError.value = ''
    parseStatus.value = {
      status: 'idle',
      progress: 0,
      message: ''
    }
  }

  return {
    // 状态
    uploadId,
    uploadProgress,
    isUploading,
    uploadError,
    parseStatus,
    
    // 动作
    setUploadId,
    setUploadProgress,
    setUploading,
    setUploadError,
    setParseStatus,
    resetUpload
  }
})
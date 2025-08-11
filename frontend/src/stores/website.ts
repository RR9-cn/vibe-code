import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { WebsiteConfig } from '@/types'

// 网站配置状态管理
export const useWebsiteStore = defineStore('website', () => {
  // 状态
  const currentWebsite = ref<WebsiteConfig | null>(null)
  const isGenerating = ref<boolean>(false)
  const generationProgress = ref<number>(0)
  const error = ref<string>('')
  const previewUrl = ref<string>('')

  // 动作
  const setCurrentWebsite = (website: WebsiteConfig) => {
    currentWebsite.value = website
  }

  const setGenerating = (status: boolean) => {
    isGenerating.value = status
  }

  const setGenerationProgress = (progress: number) => {
    generationProgress.value = progress
  }

  const setError = (errorMessage: string) => {
    error.value = errorMessage
  }

  const setPreviewUrl = (url: string) => {
    previewUrl.value = url
  }

  const clearWebsite = () => {
    currentWebsite.value = null
    error.value = ''
    previewUrl.value = ''
    generationProgress.value = 0
  }

  const updateColorScheme = (colorScheme: WebsiteConfig['colorScheme']) => {
    if (currentWebsite.value) {
      currentWebsite.value.colorScheme = colorScheme
    }
  }

  const updateTemplateId = (templateId: string) => {
    if (currentWebsite.value) {
      currentWebsite.value.templateId = templateId
    }
  }

  return {
    // 状态
    currentWebsite,
    isGenerating,
    generationProgress,
    error,
    previewUrl,
    
    // 动作
    setCurrentWebsite,
    setGenerating,
    setGenerationProgress,
    setError,
    setPreviewUrl,
    clearWebsite,
    updateColorScheme,
    updateTemplateId
  }
})
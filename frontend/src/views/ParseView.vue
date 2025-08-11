<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-4xl mx-auto">
      <!-- 页面标题 -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">简历解析</h1>
        <p class="text-gray-600">正在使用AI技术解析您的简历内容</p>
      </div>

      <!-- 解析状态组件 -->
      <ParseStatus
        :upload-id="uploadId"
        :auto-refresh="true"
        :refresh-interval="2000"
        @retry="handleRetry"
        @generate-website="handleGenerateWebsite"
        @edit-data="handleEditData"
        @reupload="handleReupload"
      />

      <!-- 返回上传页面链接 -->
      <div class="mt-8 text-center">
        <router-link 
          to="/upload" 
          class="text-primary-600 hover:text-primary-700 font-medium"
        >
          ← 返回上传页面
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUploadStore } from '@/stores/upload'
import { ApiService } from '@/services/api'
import { notify } from '@/services/notification'
import { handleError } from '@/utils'
import ParseStatus from '@/components/ParseStatus.vue'

const route = useRoute()
const router = useRouter()
const uploadStore = useUploadStore()

// 从路由参数获取uploadId
const uploadId = computed(() => route.params.uploadId as string)

// 处理重试
const handleRetry = () => {
  console.log('重试解析')
}

// 处理生成网站
const handleGenerateWebsite = () => {
  console.log('生成网站')
  // 可以导航到网站预览页面
  // router.push('/website/preview')
}

// 处理编辑数据
const handleEditData = () => {
  console.log('编辑数据')
  // 可以导航到数据编辑页面
  // router.push('/resume/edit')
}

// 处理重新上传
const handleReupload = () => {
  router.push('/upload')
}

// 初始化解析状态
const initializeParseStatus = async () => {
  if (!uploadId.value) {
    notify.error('缺少上传ID，请重新上传文件')
    router.push('/upload')
    return
  }

  try {
    // 获取当前解析状态
    const status = await ApiService.getParseStatus(uploadId.value)
    uploadStore.setParseStatus(status)
    
    // 如果状态是idle，开始解析
    if (status.status === 'idle') {
      await ApiService.parseResume(uploadId.value)
    }
    
  } catch (error) {
    const errorMessage = handleError(error)
    uploadStore.setParseStatus({
      status: 'error',
      progress: 0,
      message: errorMessage
    })
    notify.error(errorMessage, '获取解析状态失败')
  }
}

// 组件挂载时初始化
onMounted(() => {
  initializeParseStatus()
})
</script>
<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-2xl mx-auto">
      <h1 class="text-3xl font-bold text-center mb-8">上传您的简历</h1>
      
      <div class="card">
        <!-- 文件上传组件 -->
        <FileUpload
          :max-size-m-b="10"
          @upload-success="handleUploadSuccess"
          @upload-error="handleUploadError"
        />
        
        <!-- 上传说明 -->
        <div class="mt-6 p-4 bg-blue-50 rounded-lg">
          <h3 class="text-sm font-medium text-blue-800 mb-2">上传说明：</h3>
          <ul class="text-sm text-blue-700 space-y-1">
            <li>• 支持PDF格式的简历文件</li>
            <li>• 文件大小不超过10MB</li>
            <li>• 上传后将自动解析简历内容</li>
            <li>• 解析完成后可生成个人网站</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useUploadStore } from '@/stores/upload'
import { notify } from '@/services/notification'
import FileUpload from '@/components/FileUpload.vue'

const router = useRouter()
const uploadStore = useUploadStore()

// 处理上传成功
const handleUploadSuccess = (uploadId: string) => {
  console.log('上传成功，uploadId:', uploadId)
  
  // 导航到解析状态页面
  router.push(`/parse/${uploadId}`)
  
  notify.success('文件上传成功，正在解析简历内容...')
}

// 处理上传错误
const handleUploadError = (error: string) => {
  console.error('上传失败:', error)
  notify.error(error, '上传失败')
}
</script>
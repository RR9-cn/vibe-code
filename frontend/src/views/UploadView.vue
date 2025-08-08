<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-2xl mx-auto">
      <h1 class="text-3xl font-bold text-center mb-8">上传您的简历</h1>
      
      <div class="card">
        <div class="text-center">
          <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 hover:border-primary-500 transition-colors">
            <div class="text-gray-500">
              <svg class="mx-auto h-12 w-12 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <p class="text-lg mb-2">点击上传或拖拽文件到此处</p>
              <p class="text-sm text-gray-400">支持PDF格式，最大10MB</p>
            </div>
          </div>
          
          <button class="btn-primary mt-6">
            选择文件
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 上传页面组件逻辑
</script>
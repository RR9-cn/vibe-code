<template>
  <div id="app" class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <!-- 应用主容器 -->
    <RouterView />
  </div>
</template>

<script setup lang="ts">
// Vue 3 Composition API 设置
// 这里可以添加全局的应用逻辑
</script>

<style scoped>
/* 应用级别的样式 */
#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
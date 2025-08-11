<template>
  <div class="min-h-screen flex flex-col">
    <!-- 头部导航 -->
    <AppHeader />
    
    <!-- 主要内容区域 -->
    <main class="flex-1">
      <slot />
    </main>
    
    <!-- 页脚 -->
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import AppHeader from './AppHeader.vue'
import AppFooter from './AppFooter.vue'
</script>
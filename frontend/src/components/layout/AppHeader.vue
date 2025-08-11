<template>
  <header class="bg-white shadow-sm border-b border-gray-200">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Logo和标题 -->
        <div class="flex items-center space-x-4">
          <router-link to="/" class="flex items-center space-x-2">
            <div class="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <span class="text-xl font-bold text-gray-900">简历生成器</span>
          </router-link>
        </div>

        <!-- 导航菜单 -->
        <nav class="hidden md:flex items-center space-x-6">
          <router-link 
            to="/" 
            class="nav-link"
            :class="{ 'nav-link-active': $route.name === 'home' }"
          >
            首页
          </router-link>
          <router-link 
            to="/upload" 
            class="nav-link"
            :class="{ 'nav-link-active': $route.name === 'upload' }"
          >
            上传简历
          </router-link>
        </nav>

        <!-- 移动端菜单按钮 -->
        <button 
          @click="toggleMobileMenu"
          class="md:hidden p-2 rounded-lg hover:bg-gray-100"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
        </button>
      </div>

      <!-- 移动端菜单 -->
      <div v-show="showMobileMenu" class="md:hidden py-4 border-t border-gray-200">
        <nav class="flex flex-col space-y-2">
          <router-link 
            to="/" 
            class="mobile-nav-link"
            :class="{ 'mobile-nav-link-active': $route.name === 'home' }"
            @click="closeMobileMenu"
          >
            首页
          </router-link>
          <router-link 
            to="/upload" 
            class="mobile-nav-link"
            :class="{ 'mobile-nav-link-active': $route.name === 'upload' }"
            @click="closeMobileMenu"
          >
            上传简历
          </router-link>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 移动端菜单状态
const showMobileMenu = ref(false)

// 切换移动端菜单
const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

// 关闭移动端菜单
const closeMobileMenu = () => {
  showMobileMenu.value = false
}
</script>

<style scoped>
.nav-link {
  @apply text-gray-600 hover:text-primary-600 font-medium transition-colors duration-200;
}

.nav-link-active {
  @apply text-primary-600;
}

.mobile-nav-link {
  @apply block px-3 py-2 text-gray-600 hover:text-primary-600 hover:bg-gray-50 rounded-lg font-medium transition-colors duration-200;
}

.mobile-nav-link-active {
  @apply text-primary-600 bg-primary-50;
}
</style>
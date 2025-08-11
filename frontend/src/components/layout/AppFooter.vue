<template>
  <footer class="bg-gray-900 text-white">
    <div class="container mx-auto px-4 py-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- 产品信息 -->
        <div>
          <h3 class="text-lg font-semibold mb-4">个人简历网站生成器</h3>
          <p class="text-gray-400 text-sm leading-relaxed">
            快速将您的PDF简历转换为专业的个人网站，
            让您的职业形象更加出色。
          </p>
        </div>

        <!-- 快速链接 -->
        <div>
          <h3 class="text-lg font-semibold mb-4">快速链接</h3>
          <ul class="space-y-2">
            <li>
              <router-link to="/" class="footer-link">
                首页
              </router-link>
            </li>
            <li>
              <router-link to="/upload" class="footer-link">
                上传简历
              </router-link>
            </li>
          </ul>
        </div>

        <!-- 联系信息 -->
        <div>
          <h3 class="text-lg font-semibold mb-4">技术支持</h3>
          <div class="space-y-2 text-sm text-gray-400">
            <p>支持格式：PDF</p>
            <p>最大文件：10MB</p>
            <p>处理时间：1-3分钟</p>
          </div>
        </div>
      </div>

      <!-- 版权信息 -->
      <div class="border-t border-gray-800 mt-8 pt-6 text-center">
        <p class="text-gray-400 text-sm">
          © {{ currentYear }} 个人简历网站生成器. 保留所有权利.
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { computed } from 'vue'

// 当前年份
const currentYear = computed(() => new Date().getFullYear())
</script>

<style scoped>
.footer-link {
  @apply text-gray-400 hover:text-white transition-colors duration-200 text-sm;
}
</style>
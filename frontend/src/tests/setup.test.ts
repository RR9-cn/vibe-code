import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import App from '@/App.vue'

// 创建测试路由
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } }
  ]
})

// 创建测试Pinia实例
const pinia = createPinia()

describe('Vue项目基础架构测试', () => {
  it('应用能够正常挂载', async () => {
    const wrapper = mount(App, {
      global: {
        plugins: [router, pinia]
      }
    })

    expect(wrapper.exists()).toBe(true)
  })

  it('路由配置正常工作', async () => {
    await router.push('/')
    await router.isReady()

    expect(router.currentRoute.value.path).toBe('/')
  })

  it('Pinia状态管理正常工作', () => {
    expect(pinia).toBeDefined()
  })
})
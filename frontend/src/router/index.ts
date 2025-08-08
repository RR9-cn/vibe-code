import { createRouter, createWebHistory } from 'vue-router'

// 路由配置
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
      meta: {
        title: '首页 - 个人简历网站生成器'
      }
    },
    {
      path: '/upload',
      name: 'upload',
      component: () => import('@/views/UploadView.vue'),
      meta: {
        title: '上传简历 - 个人简历网站生成器'
      }
    }
  ]
})

// 路由守卫：设置页面标题
router.beforeEach((to) => {
  document.title = to.meta?.title as string || '个人简历网站生成器'
})

export default router
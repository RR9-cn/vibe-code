import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import NotificationToast from '@/components/ui/NotificationToast.vue'
import { NotificationService } from '@/services/notification'
import './style.css'

// 创建Vue应用实例
const app = createApp(App)

// 使用Pinia状态管理
app.use(createPinia())

// 使用Vue Router路由
app.use(router)

// 创建通知组件实例
const notificationApp = createApp(NotificationToast)
const notificationInstance = notificationApp.mount(document.createElement('div'))
NotificationService.setInstance(notificationInstance)

// 挂载应用到DOM
app.mount('#app')